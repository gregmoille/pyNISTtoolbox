import numpy as np
from copy import copy
import re
import pandas as pd
from NISTgenerator.Port import (
    CreateThroughPort,
    CreateThroughPortTilted,
    CreateThroughPortCurveS,
)
from NISTgenerator.Misc.label import CreateLabel
from NISTgenerator.Misc.heater import LigentecHeater


def CreateWGRingPulleyWgShifted(fid, param, ncell):
    Name = param.get("name", None)
    layer = param.get("layer", None)
    datatype = param.get("datatype", 0)
    layerWg = param.get("layerWg", layer)
    layerTapper = param.get("layerTapper", layer)
    layerLabel = param.get("layerLabel", layer)
    RR = param.get("RR", None)
    RW = param.get("RW", None)
    G = param.get("G", None)
    Drop = param.get("Drop", None)
    Gdimer = param.get("Gdimer", None)

    box = param.get("box", False)
    font = param.get("font", "Source Code Pro")
    fontsize = param.get("fontsize", 8)
    LC = param.get("Lc", 0)
    x0 = param.get("x0", None)
    y0 = param.get("y0", None)
    W = param.get("W", None)
    tot_length = param.get("tot_length", 2000)
    αc0 = param.get("alpha_connect", np.pi / 3)

    x_pos_text = param.get("x_pos_text", -1000)
    y_pos_text = param.get("y_pos_text", -15)
    nr = param.get("nr", 1000)
    inp_WG_L = param.get("inp_WG_L", None)
    exp_w = param.get("exp_w", None)
    font_size_pattern = param.get("font_size_pattern", 10)
    y_shift = param.get("y_shift", 0)
    x_shift = param.get("x_shift", 0)
    xdec = param.get("xdec", 0)
    S_in_shift = param.get("S_in_shift", 0)
    S_shrink = param.get("S_shrink", 0)
    input_inv_taper_length = param.get("input_inv_taper_length", None)
    input_st_length = param.get("input_st_length", None)
    input_inv_taper_st_length = param.get("input_inv_taper_st_length", None)
    input_inv_taper_W = param.get("input_inv_taper_W", None)
    input_surplus_taper = param.get("input_surplus_taper", None)
    output_st_length = param.get("output_st_length", None)
    output_inv_taper_st_length = param.get("output_inv_taper_st_length", None)
    output_inv_taper_length = param.get("output_inv_taper_length", None)
    output_inv_taper_W = param.get("output_inv_taper_W", None)

    heater = param.get("heater", False)
    Wopen = param.get("Wopen", 35)
    left_label = param.get("left_label", False)
    x_text_left = param.get("x_text_left", 0)
    cap = param.get("cap", False)
    resist = param.get("resist", "negative")
    do_field = param.get("doField", False)

    carriage_shift = param.get("carriage_shift", 0)
    CosAmp = param.get("CosAmp", None)
    CosPhase = param.get("CosPhase", None)
    Nmodulation = param.get("Nmodulation", 0.5)
    params_port = copy(param)
    angled_facets = param.get("angled_facets", None)

    if not type(G) == list:
        G = [G]
    if not type(RR) == list:
        RR = [RR]
    if not type(RW) == list:
        RW = [RW]
    if not type(LC) == list:
        LC = [LC]
    if not type(W) == list:
        W = [W]
    if not type(CosAmp) == list:
        CosAmp = [CosAmp]
    if not type(CosPhase) == list:
        CosPhase = [CosPhase]
    if not type(Gdimer) == list:
        Gdimer = [Gdimer]

    name_out = []

    cnt = 0
    cnt_shift = 0
    name_out = []
    name_loop = []
    y_pos = y0 - y_shift
    RRmax = np.max(RR)
    field_box = 30
    prev_txt_RR = ""
    prev_txt_RW = ""
    prev_txt_G = ""
    prev_txt_Gdimer = ""
    prev_txt_W = ""
    prev_txt_LC = ""
    prev_txt_CosAmp = ""
    prev_txt_CosPhase = ""

    txt_dev = pd.DataFrame(
        dict(
            RW=[0, 1e3, prev_txt_RW, prev_txt_RW, len(RW)],
            G=[0, 1e3, prev_txt_G, prev_txt_G, len(G)],
            Gdim=[0, 1e3, prev_txt_Gdimer, prev_txt_Gdimer, len(Gdimer)],
            Lc=[0, 1, prev_txt_LC, prev_txt_LC, len(LC)],
            W=[0, 1e3, prev_txt_W, prev_txt_W, len(W)],
            RR=[0, 1, prev_txt_RR, prev_txt_RR, len(RR)],
            A=[0, 1e3, prev_txt_CosAmp, prev_txt_CosAmp, len(CosAmp)],
            phi=[0, 180 / np.pi, prev_txt_CosPhase, prev_txt_CosPhase, len(CosPhase)],
        )
    )
    txt_dev = txt_dev.T
    txt_dev.columns = ["val", "scale", "prev", "current", "len"]

    for lc in LC:
        for g in G:
            for gdimer in Gdimer:
                for rw in RW:
                    for rrOut in RR:
                        for w in W:
                            for cos_amp in CosAmp:
                                for cos_phase in CosPhase:
                                    rr = rrOut - rw
                                    r1 = rr + g + w / 2
                                    θ = r1 * np.cos(lc / (2 * r1))
                                    Δ = r1 - (rr + g + w / 2)

                                    name_out = []

                                    # Create the First Through port
                                    # αc = αc0
                                    Ls = inp_WG_L
                                    Ls = 10
                                    xstart = tot_length / 2
                                    input_st_length = (
                                        xstart - input_inv_taper_length - Ls
                                    )
                                    y_pos = y_shift + y_pos
                                    rext = rr + rw + g + w / 2

                                    WG_through_port_y_pos = y_pos
                                    Rdec = (
                                        +rr
                                        + rw
                                        + g
                                        + w / 2
                                        - 2 * rext * (1 - np.cos(lc / (rext * 2)))
                                    )  # - 2

                                    x_pos0 = xdec - Ls - input_st_length
                                    if cnt_shift > 0:
                                        x_pos = x_shift * cnt_shift + x_pos0
                                        x_sleft = x_pos0
                                        xrconnect = (
                                            x_pos + 2 * np.sin(lc / (rext) / 2) * rext
                                        )

                                        x_left = x0 - inp_WG_L - input_st_length
                                        x_sleft_out = x_pos - x_shift
                                        y_sleft = y_pos - 2 * RRmax + (rr - Rdec) - rw

                                        if (
                                            xrconnect
                                            > tot_length / 2 - input_inv_taper_length
                                        ):
                                            y_pos = y_sleft - carriage_shift
                                            WG_through_port_y_pos = (
                                                y_pos  # WG_through_port_y_pos - 2*RRmax
                                            )
                                            cnt_shift = 0
                                            x_pos = x_pos0
                                            x_left = (
                                                x_pos
                                                - 2 * np.sin(lc / (rext) / 2) * rext
                                            )
                                            x_sleft = 0
                                            # x_right = x_pos + 2 * np.sin(lc / (rext) / 2) * rext
                                            y_sleft = 0
                                            x_sleft_out = 0
                                            xrconnect = (
                                                x_pos
                                                + 2 * np.sin(lc / (rext) / 2) * rext
                                            )

                                    else:
                                        x_pos = x_pos0
                                        x_left = (
                                            x_pos - 2 * np.sin(lc / (rext) / 2) * rext
                                        )
                                        x_sleft = 0
                                        # x_right = x_pos - (cx1 - 2 * rr)
                                        y_sleft = 0
                                        x_sleft_out = 0
                                        xrconnect = (
                                            x_pos + 2 * np.sin(lc / (rext) / 2) * rext
                                        )

                                    fid.write(str(layer) + " layer\n")
                                    fid.write(str(datatype) + " dataType\n")

                                    # name_out.append(Name + "C" + str(ncell) + "_" + str(cnt))

                                    dec = (
                                        rr
                                        - r1 * (1 - np.cos(lc / (r1) / 2)) * (r1)
                                        + 1.52888
                                    )

                                    if resist == "negative":
                                        if cos_amp is not None:
                                            Des = re.findall("(D\d+).*", Name)
                                            if len(Des) > 0:
                                                DesName = Des[0] + f"C{ncell}"
                                            else:
                                                DesName = ""

                                            fid.write(
                                                f"<{DesName}Toremove{cnt} struct>\n"
                                            )
                                            fid.write(str(3) + " layer\n")
                                            fid.write(
                                                "\t<{:.3f} {:.3f} ".format(
                                                    x_pos, y_pos - Rdec
                                                )
                                                + "{} {} ".format(0, rr + rw)
                                                + "{} {} ".format(g, lc)
                                                + "{} ".format(w)
                                                + "{} ".format(0)
                                                + "0 ringPulleyLCAV>\n"
                                            )

                                            fid.write(str(4) + " layer\n\t")
                                            if Nmodulation < 1:
                                                Npts = 600
                                            else:
                                                Npts = 10000
                                            fid.write(
                                                "\t{} {} ".format(x_pos, y_pos - Rdec)
                                                + "{} {} ".format(
                                                    0,
                                                    rr,
                                                )
                                                + f"{2 * Nmodulation:.0f} "
                                                + f"{cos_amp} "
                                                + f"{Npts} {cos_phase*180/np.pi:.3f} torusWaveIn\n"
                                            )

                                            fid.write(
                                                f"<{DesName}innerRing {DesName}Toremove{cnt} {4} genArea>\n"
                                            )
                                            fid.write(
                                                f"<{DesName}outerRing {DesName}Toremove{cnt} {3} genArea>\n"
                                            )
                                            name_out += [f"{Name}C{ncell}_ring{cnt}"]
                                            fid.write(
                                                f"<{Name}C{ncell}_ring{cnt} struct>\n"
                                            )
                                            fid.write(
                                                f"<{DesName}outerRing {DesName}innerRing {layer} XOR>\n"
                                            )

                                            fid.write(str(layer) + " layer\n")

                                        else:
                                            name_out += [f"{Name}C{ncell}_{cnt}"]
                                            fid.write(
                                                f"<{Name}C{ncell}_{cnt} struct>\n"
                                            )
                                            fid.write(
                                                f"<{x_pos:.3f} {y_pos - Rdec:.3f} "
                                                + f"{rr} {rw} {g} {lc} {w} 0 "
                                                + "0 ringPulleyLCAV>\n"
                                            )
                                            if gdimer is not None:
                                                ydim_shift = -5
                                                xdim = np.sqrt(
                                                    (2 * (rr + rw) + gdimer) ** 2
                                                    - ydim_shift**2
                                                )

                                                fid.write(
                                                    f"<{x_pos - xdim:.3f} {y_pos - Rdec + ydim_shift:.3f} "
                                                    + f"{rr} {rw} 0 0 0 0 "
                                                    + "0 ringPulleyLCAV>\n"
                                                )

                                        if heater:
                                            params_heater = copy(param)
                                            if gdimer is not None:
                                                params_heater["theta_heat_deg"] = 120
                                                params_heater["rot"] = 120
                                                params_heater["pad_loc"] = "top"
                                            if rr > 200:
                                                params_heater["pad_loc"] = "left"
                                            params_heater["name"] = Name + str(cnt)
                                            params_heater["Wopen"] = Wopen
                                            params_heater["x_pos"] = x_pos
                                            params_heater["y_pos"] = y_pos - Rdec
                                            params_heater["rw"] = rw
                                            params_heater["rr"] = rr
                                            name_out += LigentecHeater(
                                                fid, params_heater, ncell, cnt
                                            )
                                            fid.write(str(layer) + " layer\n")
                                            fid.write(str(datatype) + " dataType\n")

                                            if gdimer is not None:
                                                params_heater2 = copy(params_heater)
                                                params_heater2["rot"] = -60
                                                params_heater2["name"] = (
                                                    Name + str(cnt) + "dim"
                                                )
                                                params_heater2["x_pos"] = x_pos - xdim
                                                params_heater2["y_pos"] = (
                                                    y_pos - Rdec + ydim_shift
                                                )
                                                name_out += LigentecHeater(
                                                    fid, params_heater2, ncell, cnt
                                                )
                                                fid.write(str(layer) + " layer\n")
                                                fid.write(str(datatype) + " dataType\n")

                                    else:
                                        if cos_amp is not None:
                                            pass
                                        else:
                                            fid.write(
                                                "<{} {} ".format(x_pos, y_pos - Rdec)
                                                + "{} {} {} ".format(rr + rw, rw, exp_w)
                                                + "{} {} ".format(g, lc)
                                                + "{} {} ".format(w, exp_w)
                                                + "{} ".format(0)
                                                + "0 ringPulleyInvPosLCAV>\n"
                                            )

                                    if do_field:
                                        fid.write(str(field_box + cnt) + " layer\n")
                                        fid.write(
                                            f"{x_pos-1.25*rr} {y_pos-Rdec-1.25*rr} "
                                            + f"{2.5*rr} {2.5*rr} "
                                            + "0 0 "
                                            + "0 roundrect\n"
                                        )
                                        fid.write(str(layer) + " layer\n")

                                    # -- Port
                                    yc = y_pos - (r1 - rr - g - w)
                                    y_txt = WG_through_port_y_pos + y_pos_text
                                    params_port["name"] = Name + str(cnt)
                                    params_port["cnt_shift"] = cnt_shift
                                    params_port["Drop"] = Drop
                                    params_port["Gdimer"] = gdimer
                                    if Drop:
                                        params_port["out_sep"] = 3.5
                                    params_port["y_drop"] = (
                                        y_pos - Rdec - (rr) - rw - w / 2 - g
                                    )
                                    if gdimer is not None:
                                        params_port["y_drop"] += ydim_shift
                                    params_port["RR"] = rr
                                    params_port["G"] = g
                                    if gdimer is not None:
                                        params_port["G"] += ydim_shift
                                    params_port["RW"] = rw
                                    params_port["W"] = w
                                    params_port["inp_WG_L"] = Ls
                                    params_port["input_st_length"] = input_st_length
                                    params_port["resist"] = resist
                                    params_port[
                                        "input_surplus_taper"
                                    ] = input_surplus_taper
                                    params_port[
                                        "output_surplus_taper"
                                    ] = input_surplus_taper
                                    params_port["cap"] = cap
                                    params_port["layerWg"] = layerWg
                                    params_port["do_field"] = do_field
                                    params_port["layer_field"] = field_box + cnt
                                    params_port["layerTapper"] = layerTapper
                                    params_port["x2_in_wg"] = x_left
                                    params_port["x1_out_wg"] = xrconnect
                                    if gdimer is not None:
                                        params_port["x1_out_wg"] -= xdim
                                        params_port["x1_out_wg_back"] = xrconnect
                                    params_port["xin_c"] = x_sleft
                                    if gdimer is not None:
                                        params_port["xin_c"] -= xdim
                                    params_port["yin_c"] = y_sleft
                                    params_port["S_in_shift"] = S_in_shift
                                    params_port["x_sleft_out"] = x_sleft_out
                                    params_port["x_shift"] = x_shift
                                    # params_port["Slength"] = Slenght
                                    params_port["xR"] = x_pos - np.sin(
                                        lc / (rr + g + w / 2) / 2
                                    ) * (rr + g + w / 2)
                                    params_port[
                                        "WG_through_port_y_pos"
                                    ] = WG_through_port_y_pos

                                    if cnt_shift > 0:
                                        name_out += CreateThroughPortCurveS(
                                            fid, params_port, ncell, cnt
                                        )
                                    else:

                                        name_out += CreateThroughPort(
                                            fid, params_port, ncell, cnt
                                        )

                                    # # conenct left
                                    αc = αc0
                                    x1 = x_pos - 2 * np.sin(lc / (rext) / 2) * rext
                                    Sdimshift = 0
                                    if gdimer is not None:
                                        Sdimshift = -xdim
                                        # fid.write(str(layer) + " layer\n")
                                        # fid.write(
                                        #         f"\t<{x1:.3f} {WG_through_port_y_pos:.3f} "
                                        #         + f"{x1 + 2*rr+5:.3f} {WG_through_port_y_pos:.3f} "
                                        #         + f"{w:.3f} 0 0 0 waveguide>\n"
                                        #     )
                                    if cnt_shift > 0:
                                        αc = 2 * αc

                                        y1 = yc + (r1 - w / 2) * np.cos(0.5 * lc / r1)
                                        cx1 = (
                                            x_pos - 2 * rr
                                        )  # - r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                        cy1 = yc + r1 * np.sin(
                                            np.pi / 2 - 0.5 * lc / r1 - αc / 2
                                        ) / np.cos(αc / 2)
                                        cx2 = x_pos - x_shift + rr
                                        cy2 = y_sleft
                                        x2 = x_pos - x_shift
                                        y2 = cy2
                                        fid.write(str(layer) + " layer\n")
                                        if resist == "negative":
                                            # pass\
                                            fid.write(
                                                f"\t<{x2-S_shrink:.3f} {y2:.3f} "
                                                + f"{x1 + Sdimshift+S_shrink:.3f} {WG_through_port_y_pos:.3f} "
                                                + f"{w:.3f} {0} "
                                                + "sBend>\n"
                                            )
                                            if np.abs(S_shrink) > 0:
                                                fid.write(
                                                    f"\t<{x2-S_shrink:.3f} {y2:.3f} "
                                                    + f"{x2:.3f} {y2:.3f} "
                                                    + f"{w:.3f} 0 0 0 waveguide>\n"
                                                )
                                                fid.write(
                                                    f"\t<{x1 + Sdimshift+S_shrink:.3f} {WG_through_port_y_pos:.3f} "
                                                    + f"{x1 + Sdimshift:.3f} {WG_through_port_y_pos:.3f} "
                                                    + f"{w:.3f} 0 0 0 waveguide>\n"
                                                )
                                        else:
                                            fid.write(
                                                "\t<{} {} ".format(x2, y2)
                                                + "{} {} ".format(
                                                    x1 - x2 - Ls,
                                                    WG_through_port_y_pos - y2,
                                                )
                                                + "{} {} {} ".format(w, exp_w, 0)
                                                + "sBendInv>\n"
                                            )

                                        if do_field:
                                            fid.write(str(field_box + cnt) + " layer\n")
                                            Lsbend = (x1 - x2) - 1.25 * rr
                                            # xc = x_pos-1.5*rr - Lsbend
                                            fid.write(
                                                f"{x2} {y_pos-Rdec-1.25*rr} "
                                                + f"{Lsbend} {2.5*rr} "
                                                + "0 0 "
                                                + "0 roundrect\n"
                                            )
                                            fid.write(
                                                "\t<{} {} ".format(x2, y2)
                                                + "{} {} ".format(
                                                    x1 - Ls, WG_through_port_y_pos
                                                )
                                                + "{} {} ".format(30, 0)
                                                + "sBend>\n"
                                            )
                                            fid.write(str(layer) + " layer\n")
                                    else:
                                        # Slenght = x1 - x2
                                        fid.write(str(layerWg) + " layer\n")
                                        if do_field:
                                            Lright = np.abs(-tot_length / 2 + (x1 - Ls))
                                            # print(Lright)
                                            Nbox = int(np.floor(Lright / 500))
                                            # print(Nbox)
                                            fid.write(str(field_box + cnt) + " layer\n")
                                            for nf in range(Nbox - 1):
                                                xc = x_pos - 1.25 * rr
                                                fid.write(
                                                    f"{xc - (nf+1)*500} {WG_through_port_y_pos-15  } "
                                                    + f"{500} {30} "
                                                    + "0 0 "
                                                    + "0 roundrect\n"
                                                )
                                            fid.write(str(layer) + " layer\n")

                                    if do_field:
                                        Lright = tot_length / 2 - (x1r + Ls)
                                        # print(Lright)
                                        Nbox = int(np.ceil(Lright / 500))
                                        # print(Nbox)
                                        fid.write(str(field_box + cnt) + " layer\n")
                                        for nf in range(Nbox):
                                            xc = x_pos + 1.25 * rr
                                            fid.write(
                                                f"{xc + nf*500} {WG_through_port_y_pos-15  } "
                                                + f"{500} {30} "
                                                + "0 0 "
                                                + "0 roundrect\n"
                                            )
                                        fid.write(str(layer) + " layer\n")

                                    # --- Labels
                                    txt_dev["val"].loc["RR"] = rrOut
                                    txt_dev["val"].loc["RW"] = rw
                                    txt_dev["val"].loc["G"] = g
                                    txt_dev["val"].loc["Gdim"] = gdimer
                                    txt_dev["val"].loc["W"] = w
                                    txt_dev["val"].loc["Lc"] = lc
                                    txt_dev["val"].loc["A"] = cos_amp
                                    txt_dev["val"].loc["phi"] = cos_phase
                                    txt_dev.current = [
                                        f"{nn}={xx*ss:g}" if xx is not None else ""
                                        for nn, xx, ss in zip(
                                            txt_dev.index, txt_dev.val, txt_dev.scale
                                        )
                                    ]
                                    if angled_facets is not None:
                                        mask = ~(txt_dev.current == txt_dev.prev)
                                        txt_dev.prev[mask] = txt_dev[mask].current
                                        txt = " ".join(txt_dev[mask].current.values)
                                    else:
                                        mask = txt_dev.len > 1
                                        txt = " ".join(txt_dev[mask].current.values)

                                    par_lab = {
                                        "x_pos_text": x_pos_text,
                                        "y_pos_text": y_txt,
                                        "x_pos_left": x_text_left,
                                        "txt": txt,
                                        "name": Name + "_" + str(cnt),
                                    }
                                    # if param["angled_facets"]:
                                    if par_lab["x_pos_left"]:
                                        par_lab["x_pos_left"] = par_lab[
                                            "x_pos_left"
                                        ] - 6 * len(txt)

                                    par_lab["layer"] = layerLabel
                                    par_lab["datatype"] = datatype
                                    par_lab["box"] = box
                                    par_lab["font"] = font
                                    par_lab["font_size_pattern"] = fontsize

                                    name_out += CreateLabel(fid, par_lab, ncell)

                                    cnt_shift += 1
                                    cnt += 1
                                    subcell = "{}Rg{}".format(Name, cnt)
                                    # subcell = subcell.replace('.', 'p')
                                    fid.write("<" + subcell + " struct>\n")
                                    for n in name_out:
                                        fid.write("<" + n + " 0 0 0 1 0 instance>\n")
                                    fid.write("\n")
                                    name_loop.append(subcell)

    fid.write("<" + Name + str(ncell) + " struct>\n")
    for n in name_loop:
        fid.write("<" + n + " 0 0 0 1 0 instance>\n")

    fid.write("\n")

    return [Name + str(ncell)]
