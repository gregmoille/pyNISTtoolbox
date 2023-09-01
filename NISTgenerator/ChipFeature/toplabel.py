from copy import copy
import numpy as np


def TopLabel(Cells, param, Bloc, data=None, design_number=None):
    ylbl = 340
    ydec = 30
    y0 = 0
    L = 60
    logo = param.get("logo", None)
    logo_shift = param.get("logo_shift", -300)
    if not data:
        label = [f"{param['filename']}".replace(".cnst", "")]
        font = "Source Code Pro"
        font_size_pattern = 26
        x_pos_text = -460
        layer = 2
    else:
        label = [data.get("label", "Stuff")]
        font = data.get("font", "Square Dot Digital-7")
        font_size_pattern = data.get("font_size_pattern", 30)
        layer = data.get("layer", 2)
        datatype = data.get("datatype", 0)
        x_pos_text = -(param["Wchip"] / 2 - 290)  # -660
    # mrk = '•'*((L-2-len(label[0]))//2)
    # add = '•'* ((L-2-len(label[0]))%2)
    # label[0] = mrk+ ' ' +label[0]+ ' ' +mrk+ add
    if design_number:
        AddedName = f"D{design_number}"
    else:
        AddedName = ""

    MainLabel = {
        "name": f"{AddedName}MainLabel_txt",
        "layer": layer,
        "datatype": datatype,
        "box": False,
        "font": font,
        "font_size_pattern": font_size_pattern,
        "x_pos_text": x_pos_text,
        "nist_log": True,
        "xnist": param["Wchip"] / 2 - 400,
    }

    if not data:
        ylbl = 340
        ydec = 30
    else:
        ylbl = -45
        ydec = 0
    for lbl in label:
        mainlbl = copy(MainLabel)
        mainlbl["txt"] = lbl
        mainlbl["y_pos_text"] = ylbl
        mainlbl["ynist"] = ylbl
        mainlbl["logo"] = logo
        mainlbl["logo_shift"] = logo_shift
    Cells["cell_type"].append("Gen.Misc.CreateLabel")
    Cells["param"].append(mainlbl)
    Cells["YSHIFT"].append(0)
    ylbl -= ydec

    if not data:
        BoundingLabel = {
            "name": f"{AddedName}MainLabel_Bdg",
            "layer": param["layer_label"],
            "x0": 0,
            "y0": ylbl,
            "W": 950,
            "H": ydec * len(label),
            "Yspace": 30,
            "Xspace": 30,
        }

        Cells["cell_type"].append("Gen.Misc.WgBoundingChip")
        Cells["param"].append(BoundingLabel)
        Cells["YSHIFT"].append(0)
