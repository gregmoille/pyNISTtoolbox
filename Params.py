import numpy as np
import os
import ipdb
from copy import copy
import sys
import re
import inspect
import platform


NISTgeneratorPath = os.path.expanduser(r"~/AmunMount/NanoFab")
CNSTpath = os.path.expanduser(
    r"~/AmunMount/NanoFab/NIST/CNSTnanoToolboxV2019.05.01/cnst_script_files/"
)
GDSpath = r"/opt/gds_files_created/"
print("------")
print(platform.node())
print("------")
if platform.node() == "osiris":
    NISTgeneratorPath = r"/home/greg/AmunHome/NanoFab"
    CNSTpath = r"/home/greg/cnst_files/"
    GDSpath = r"/home/greg/gds_files_created/"
if platform.node() == "ra.local":
    NISTgeneratorPath = "/Users/greg/Gdrive/Work/NanoFab"
    CNSTpath = (
        r"/Users/greg/Gdrive/NanoFab/NIST/CNSTnanoToolboxV2019.05.01/cnst_script_files/"
    )
    GDSpath = r"/Users/greg/gds_files_created"
if (
    platform.node() == "horus"
    or platform.node() == "pegasus"
):
    # NISTgeneratorPath = '/Volumes/AmunDrive/Nanofab'
    NISTgeneratorPath = os.path.expanduser(r"~/AmunMount/NanoFab")
    CNSTpath = os.path.expanduser(
        r"~/AmunMount/NanoFab/NIST/CNSTnanoToolboxV2019.05.01/cnst_script_files/"
    )
    GDSpath = r"/opt/gds_files_created/"

if  platform.node() == "hephaistos.local":
    NISTgeneratorPath = os.path.expanduser(r"~/Documents/Nanofab")
    CNSTpath = os.path.expanduser(
        r"~/Documents/Nanofab/NIST/CNSTnanoToolboxV2019.05.01/cnst_script_files/"
    )
    GDSpath = r"/opt/gds_files_created/")

if not NISTgeneratorPath in sys.path:
    sys.path.insert(-1, NISTgeneratorPath)
import NISTgenerator as Gen


GlobalParams = dict(
    resist="positive",
    Wchip=2500,
    Hchip=10000,
    layer_ring=1,
    layer_waveguide=1,
    layer_stepper=3,
    layer_label=1,
    device_layer=1,
    box_layer=60,
    photomask_layer=1,
    layerField=30,
    layerLiftOff=20,
    Wbox=1000,
    ycalib=-8500,
)
Cells = dict(ncell=-1, cell_type=[], param=[], YSHIFT=[])
