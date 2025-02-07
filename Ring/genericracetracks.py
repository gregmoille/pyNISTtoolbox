import numpy as np
from copy import copy


def GenericRaceTracks(Cells, param, Bloc):
    # ------------------------------------------
    yTop = [150 + 70 - Bloc[0].get("top_shift", 0)]
    for ib in np.arange(1, len(Bloc)):
        N = 1
        for k, itm in Bloc[ib - 1].items():
            if type(itm) == list or type(itm) == np.array:
                N *= len(itm)
        Ndevices = N + 0.5
        Hblock = Bloc[ib - 1]["ypitch"] * Ndevices

        yTop += [yTop[-1] - Hblock - 20 - Bloc[ib].get("top_shift", 0)]

    ii_ring = 0

    layerField = 30
    for BB, yt in zip(Bloc, yTop):
        y0 = yt
        RR = {
            "name": f"R{ii_ring:02d}_",
            "x0": 0,
            "y0": 0,
            "tot_length": param["Wchip"],
            "exp_w": BB.get("exp_w", 2),
            "exp_w_ring": BB.get("exp_w_ring", 2),
            "layer": [
                param["layer_ring"],
                0,
                param["layer_waveguide"],
                param["layer_stepper"],
            ],
            "RR": BB.get("R", None),
            "RW": BB.get("RW", None),
            "Lc": BB.get("Lc", None),
            "Lrace": BB.get("Lrace", None),
            "RWtaper": BB.get("RWtaper", False),
            "trck_type": BB.get("trck_type", "Euler"),
            "Lcpl": BB.get("Lcpl", 0),
            "LcDrop": BB.get("LcDrop", None),
            "G": BB.get("G", None),
            "W": BB.get("W", None),
            "Wbend": BB.get("Wdrop", 0) + 0.35,
            "Gdrop": BB.get("Gdrop", None),
            "Wdrop": BB.get("Wdrop", 0),
            "Nmodulation": BB.get("Nmodulation", None),
            "Amodulation": BB.get("Amodulation", None),
            "y_shift": -1 * BB.get("ypitch", None),
            "y_pos_text": BB.get("y_pos_text", 0),
            "x_pos_text": -param["Wchip"] / 2 + 400,
            "label_out": BB.get("label_out", True),
            "x_pos_text_out": param["Wchip"] / 2 - 400,
            "input_inv_taper_st_length": BB.get("input_inv_taper_st_length", 5),
            "input_inv_taper_length": BB.get("input_inv_taper_length", 800),
            "input_inv_taper_W": BB.get("Wtapper", 0.15),
            "inp_WG_L": BB.get("inp_WG_L", 50),
            "polarity": param["resist"],
            "Wbdg": None,
            "Hbdg": None,
            "Bdg_layer": 98,
            "y_blockline_dec": 6,
            "through_drop": BB.get("through_drop", False),
            "Nmod_pts": BB.get("Nmod_pts", 2000),
            "output_inv_taper_W_drop": BB.get("WtapperDrop", 0.15),
        }

        Cells["cell_type"].append("Gen.Ring.CreateRaceTrackCpldBend")
        Cells["param"].append(RR)
        Cells["YSHIFT"].append(copy(y0))

        # -- get the number of device to increment the field layer
        Ntot = (
            len(BB.get("G", [0]))
            * len(BB.get("RW", [0]))
            * len(BB.get("Lc", [0]))
            * len(BB.get("Amodulation", [0]))
            * len(BB.get("Sigmamodulation", [0]))
            * len(BB.get("Gdrop", [0]))
            * len(BB.get("LcDrop", [0]))
        )

        if "Hbox" in param.keys():
            Hbox = param["Hbox"]
        else:
            Hbox = BB.get("ypitch", None)

            if param["Wbox"] < Hbox:
                Hbox = param["Wbox"]

        increment = param.get("IncrementLayerField", True)
        Fbox = {
            "Name": f"R{ii_ring:02d}_Fld",
            "Hbox": Hbox,
            "Nx": 1,
            "ypitch": BB.get("ypitch", Hbox),
            "increment": increment,
            "Wbox": param["Wbox"],
            "y0": -2 - 19,
            "layer": param["layerField"],
            "yshift0": 4.9,  # -Bloc[0]['ypitch']/2,
            "N": Ntot,
            "Wchip": param["Wchip"],
        }

        Cells["cell_type"].append("Gen.Misc.FieldBox")
        Cells["param"].append(Fbox)
        Cells["YSHIFT"].append(copy(y0))

        if increment:
            param["layerField"] += Ntot

        GdropLabell = {
            "name": f"R{ii_ring:02d}_Lbl",
            "layer": param["layer_label"],
            "box": True,
            "font": "Source Code Pro",
            "font_size_pattern": 20,
            "txt": BB["Label"],
            "x_pos_text": -850,
            "y_pos_text": +28,
        }
        Cells["cell_type"].append("Gen.Misc.CreateLabel")
        Cells["param"].append(GdropLabell)
        Cells["YSHIFT"].append(copy(y0))
        ii_ring += 1
