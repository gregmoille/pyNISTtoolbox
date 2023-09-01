import os, sys
from copy import copy
import shutil

parFile = os.path.expanduser(r"/Users/greg/Documents/Nanofab/PatternDesign/")
if not parFile in sys.path:
    sys.path.insert(-1, parFile)
from Params import *
from ParametersDesign import *


# █▀▀ █▀▀ █▄░█ █▀▀ █▀█ ▄▀█ █░░   █▀█ ▄▀█ █▀█ ▄▀█ █▀▄▀█
# █▄█ ██▄ █░▀█ ██▄ █▀▄ █▀█ █▄▄   █▀▀ █▀█ █▀▄ █▀█ █░▀░█
GlobalParams[
    "filefun"
] = lambda design: f"{os.path.dirname(__file__)}/SpaceForceRun1_Design{design}"
GlobalParams["Wchip"] = 1900
GlobalParams["Hchip"] = 5380
GlobalParams["LogPath"] = "logs"
GlobalParams["foundry"] = "Ligentec"
Blocks = {}

# █▀▀ █░█ █ █▀█   █▀█ ▄▀█ █▀█ ▄▀█ █▀▄▀█
# █▄▄ █▀█ █ █▀▀   █▀▀ █▀█ █▀▄ █▀█ █░▀░█
Blocks = {**Blocks, **DesignTHz()}
Blocks = {**Blocks, **Design750()}
Blocks = {**Blocks, **Design500()}
Blocks = {**Blocks, **Design200()}
Blocks = {**Blocks, **DesignVeryLow()}
Blocks = {**Blocks, **DesignRaceTrack()}
Blocks = {**Blocks, **DesignDimer()}


# █▄▄ █░█ █ █░░ █▀▄ █▀▀ █▀█
# █▄█ █▄█ █ █▄▄ █▄▀ ██▄ █▀▄
to_do = np.arange(11, 11.1).astype(int)
for index in to_do:
    block = Blocks[index]
    if index > 42:
        GlobalParams["Hchip"] = 5380 - 1490 - 120
    Cells = dict(ncell=-1, cell_type=[], param=[], YSHIFT=[])
    for bb in block:
        if not "Wtapper" in bb.keys():
            bb["Wtapper"] = 0.200
        bb.update(heater=True, fontsize=10)
    Params = copy(GlobalParams)
    Params["filename"] = f"SpaceForceRun2_Design{index}.cnst"
    Params["pyfile"] = Params["filefun"](index) + ".py"
    Params["logo"] = "SpaceForce_logo"
    Params["logo_shift"] = -125
    # --------------------------------------------------------
    # █▄▄ █░█ █ █░░ █▀▄ █ █▄░█ █▀▀   █▄▄ █░░ █▀█ █▀▀ █▄▀ █▀
    # █▄█ █▄█ █ █▄▄ █▄▀ █ █░▀█ █▄█   █▄█ █▄▄ █▄█ █▄▄ █░█ ▄█
    # --------------------------------------------------------
    Gen.Utils.LogFile(Params, block, Cells, design_number=index)
    Gen.Ring.RingPulleyWgShifted(Cells, Params, block, design_number=index)
    label = dict(label=f'Chip {index} • {block[0]["Label"]}')
    Gen.ChipFeature.TopLabel(Cells, Params, block, data=label, design_number=index)
    # # --------------------------------------------------------
    # # █▀▀ █▀▀ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ █▀█ █▀█
    # # █▄█ ██▄ █░▀█ ██▄ █▀▄ █▀█ ░█░ █▄█ █▀▄
    # # --------------------------------------------------------
    Gen.Builder.CreateCNST(
        Cells["cell_type"],
        Cells["param"],
        Params["filename"],
        yshift=Cells["YSHIFT"],
        CNSTpath=CNSTpath,
        top_cell_name=f"D{index}TOP",
        xdec=GlobalParams["Wchip"] / 2,
        ydec=GlobalParams["Hchip"],
        res=0.005,
    )

    Gen.Builder.CreateGDS(
        Params["filename"],
        CNSTpath=CNSTpath,
        GDSpath=GDSpath,
        ToolBoxPath=CNSTpath.split("cnst_")[0],
        javaVers="CNSTspecialScriptsV2019.05.01.jar",
        removeRobCell=True,
        dogds=True,
        dcty=os.path.dirname(__file__),
    )
