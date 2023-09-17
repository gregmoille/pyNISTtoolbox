import numpy as np
from copy import copy


def RingPulleyWgShifted(Cells, param, Bloc, design_number=False):

    y0 = 0
    # -- Loop through parameter space--
    # -------------------------------------------------------
    yTop = [-125 - Bloc[0].get("top_shift", 0)]
    for ib in np.arange(1, len(Bloc)):
        Ndevices = 1
        for k, itm in Bloc[ib - 1].items():
            if type(itm) == list or type(itm) == np.array:
                Ndevices *= len(itm)
        Hblock = Bloc[ib - 1]["ypitch"] * Ndevices

        yTop += [yTop[-1] - Hblock - 80 - Bloc[ib].get("top_shift", 0)]

    ii_ring = 0

    if design_number:
        AddedName = f"D{design_number}"
    else:
        AddedName = ""

    if param["foundry"].lower() == "aim":
        font = "Source Code Pro"
    else:
        font = "Square Dot Digital-7"

    for BB, yt in zip(Bloc, yTop):
        # y0 = -400
        y0 = yt
        RingParams = {
            "name": f"{AddedName}B{ii_ring}_",
            "datatype": BB.get("datatype", 0),
            "layer": BB.get("layer", 2),
            "layerWg": BB.get("layer", 2),
            "layerTapper": BB.get("layer", 2),
            "layerLabel": BB.get("layer", 2),
            "RR": BB.get("RR", 23),
            "RW": BB.get("RW", 1000),
            "G": BB.get("G", 0.1),
            "Gdimer": BB.get("Gdimer", None),
            "Drop": BB.get("Drop", False),
            "Lc": BB.get("Lc", 0),
            "Lrace": BB.get("Lrace", 0),
            "trck_type": BB.get("trck_type", "Euler"),
            "RW_optim": BB.get("RW_optim", True),
            "box": False,
            "alpha_connect": np.pi / 3,
            "x0": 0,
            "resist": BB.get("resist", "negative"),
            "circle_coupling": BB.get("circle_coupling", False),
            "xdec": BB.get("xdec", 140),
            "W": BB.get("W", 0.5),
            "CosAmp": BB.get("CosAmp", None),
            "Nmodulation": BB.get("Nmodulation", 0.5),
            "CosPhase": BB.get("CosPhase", None),
            "y0": BB.get("y0", 0),
            "font": font,
            "fontsize": BB.get("fontsize", 7),
            "exp_w": BB.get("exp_w", 2),
            "tot_length": param["Wchip"],
            "y_shift": -1 * BB.get("ypitch", 10),
            "carriage_shift": BB.get("carriage_shift", 0),
            "S_in_shift": BB.get("S_in_shift", 0),
            "S_shrink": BB.get("S_shrink", 0),
            "yrace_shift": BB.get("yrace_shift", 0),
            "x_shift": BB.get("xpitch", 140),
            "y_pos_text": BB.get("y_pos_text", -7.5),
            "x_pos_text": BB.get("x_pos_text", -(param["Wchip"] / 2 - 40)),
            "input_inv_taper_st_length": BB.get("input_inv_taper_st_length", 10),
            "input_inv_taper_length": BB.get("input_inv_taper_length", 220),
            "input_st_length": BB.get("input_st_length", 750),
            "input_inv_taper_W": BB.get("Wtapper", 0.200),
            "output_st_length": BB.get("output_st_length", 2250),
            "output_inv_taper_st_length": BB.get("output_inv_taper_st_length", 10),
            "output_inv_taper_length": BB.get("output_inv_taper_length", 220),
            "output_inv_taper_W": BB.get("Wtapper", 0.200),
            "inp_WG_L": 00,
            "input_surplus_taper": BB.get("surplus_taper", 0),
            "st_WG_Lc": 100,
            "left_label": True,
            "x_text_left": BB.get("x_text_left", param["Wchip"] / 2 - 40),
            "heater": BB.get("heater", False),
            "Wopen": BB.get("Wopen", 35),
            "angled_facets": BB.get("angled_facets", None),
        }

        if True:
            if BB.get("racetrack", False):
                Cells["cell_type"].append("Gen.Ring.CreateRaceTrackThroughShifted")
                Cells["YSHIFT"].append(y0 + 25)
            else:
                Cells["cell_type"].append("Gen.Ring.CreateWGRingPulleyWgShifted")
                Cells["YSHIFT"].append(y0)

            Cells["param"].append(RingParams)

        #  -- Cells: Bonding Box --
        # -------------------------------------------------------

        W = param["Wchip"]
        H = param["Hchip"]
        x0_bdg = -W / 2
        # cell_type.append('Gen.Misc.CreateBumpStruct')
        if param["foundry"].lower() == "aim":
            BoundingParam = {
                "name": f"{AddedName}BDG_Box",
                "layer": 11,
                "datatype": 100,
                "y0": +25,
                "H": H + 100,
                "W": W + 100,
                "Wwg": 100,
                "Xspace": 0,
            }
            Cells["cell_type"].append("Gen.Misc.WgBoundingChip")
            Cells["param"].append(BoundingParam)
            Cells["YSHIFT"].append(0)

        else:
            BoundingParam = {
                "name": f"{AddedName}BDG_Box",
                "layer": 100,
                "datatype": 2,
                "corner": (-W / 2, -H),
                "w_h": (W, H),
                "Yspace": 0,
                "Xspace": 0,
            }
            Cells["cell_type"].append("Gen.Misc.CreateBumpStruct")
            Cells["param"].append(BoundingParam)
            Cells["YSHIFT"].append(0)
            #  -- Cells: Bonding Box --
            # -------------------------------------------------------
            # cell_type.append('Gen.Misc.CreateBumpStruct')
            BoundingParam = {
                "name": f"{AddedName}BDG_Shift",
                "layer": 100,
                "datatype": 0,
                "corner": (-W / 2 + 10, -H),
                "w_h": (W - 20, H),
                "Yspace": 0,
                "Xspace": 0,
            }
            Cells["cell_type"].append("Gen.Misc.CreateBumpStruct")
            Cells["param"].append(BoundingParam)
            Cells["YSHIFT"].append(0)
        ii_ring += 1
