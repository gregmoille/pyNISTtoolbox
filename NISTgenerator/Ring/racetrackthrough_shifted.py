from copy import copy
import ipdb
import numpy as np
import scipy.constants as cts
import scipy.signal as signal
from scipy.fft import fft, ifft, ifftshift
from NISTgenerator.Port import (
    CreateThroughDropPortSeparated,
    CreateThroughPort,
    CreateThroughPortTilted,
    CreateThroughPortCurveS,
)
from NISTgenerator.Misc import CreateLabel, CreateBumpStruct

from .racetrack import GenerateRaceTrack
from .racetrackChristy import GenerateRaceTrackChristy
from NISTgenerator.Misc.heater import LigentecHeaterRaceTrack


def CreateRaceTrackThroughShifted(fid, param, ncell):

    resist = param.get("resist", "negative")
    # -- General Parameters --
    Name = param.get("name", None)
    layer = param.get("layer", None)
    if resist == "positive":
        layer_stepper = layer
        layer_waveguide = layer
        layer = layer

    RR = param.get("RR", None)
    x0 = param.get("x0", None)
    y0 = param.get("y0", None)
    y_shift = param.get("y_shift", 0)
    x_shift = param.get("x_shift", 50)
    xdec = param.get("xdec", x_shift)

    # -- Racetrack Parameters --
    W = param.get("W", None)
    G = param.get("G", None)
    Lrace = param.get("Lrace", None)
    Lc = param.get("Lc", None)
    RR = param.get("RR", None)
    RW = param.get("RW", None)
    p = param.get("p", 0.3553535)
    circle_coupling = param.get("circle_coupling", False)
    αc0 = param.get("alpha_connect", np.pi / 3)
    datatype = param.get("datatype", 0)
    # -- Bus parameters --s
    inp_WG_L = param.get("inp_WG_L", None)
    exp_w = param.get("exp_w", None)
    exp_w_tapper = param.get("exp_w_tapper", exp_w)
    tot_length = param.get("tot_length", 1850)
    in_tap_etch = param.get("in_tap_etch", 0)
    tapperLength = param.get("tapperLength", None)
    input_inv_taper_length = param.get("input_inv_taper_length", None)
    ouput_inv_taper_length = param.get("ouput_inv_taper_length", input_inv_taper_length)
    input_inv_taper_st_length = param.get("input_inv_taper_st_length", None)
    output_inv_taper_st_length = param.get(
        "output_inv_taper_st_length", input_inv_taper_st_length
    )
    input_inv_taper_W = param.get("input_inv_taper_W", None)
    output_inv_taper_W = param.get("output_inv_taper_W", input_inv_taper_W)

    heater = param.get("heater", False)
    # -- Modulation Parameters --
    Nmodulation = param.get("Nmodulation", None)
    Amodulation = param.get("Amodulation", None)
    Sigmamodulation = param.get("Sigmamodulation", None)
    Gaussmodulation_spread = param.get("Gaussmodulation_spread", None)
    Nmod_pts = param.get("Nmod_pts", 2000)

    # -- Block Between Devices Parameters --
    blockline = param.get("blockline", False)
    y_blockline_dec = param.get("y_blockline_dec", 10)
    x_dec_block = param.get("x_dec_block", 0)
    yrace_shift = param.get("yrace_shift", 0)
    carriage_shift = param.get("carriage_shift", 0)

    # -- Label Parameters
    x_pos_text = param.get("x_pos_text", -1000)
    y_pos_text = param.get("y_pos_text", -20)
    x_pos_text_out = param.get("x_pos_text_out", -x_pos_text)
    label_out = param.get("label_out", True)
    font_size_pattern = param.get("font_size_pattern", 10)
    font = param.get("font", "Source Code Pro")

    polarity = param.get("polarity", "positive")
    params_port = copy(param)
    params_track = copy(param)

    if not type(G) == list:
        G = [G]
    if not type(RW) == list:
        RW = [RW]
    if not type(Lc) == list:
        Lc = [Lc]

    cnt = 0

    if resist == "positive":
        fid.write("{} layer\n".format(layer))
    else:
        fid.write("{} layer\n".format(layer))
    name_loop = []

    y0original = copy(y0)
    # y0 =

    cnt_shift = 0
    y_pos = y0 - y_shift

    for g in G:
        for rw in RW:
            for lc in Lc:
                name_out = []

                Lmid_str = (Lrace - 2 * np.pi * RR) / 3

                y_pos += y_shift  # * cnt + y0
                x_xtx = x0 + x_pos_text
                y_txt = y_pos + y_pos_text

                r1 = RR + g + W / 2
                x_xtx = x0 + x_pos_text

                name_out = []

                # Create the First Through port
                αc = αc0
                Ls = inp_WG_L  #
                xstart = tot_length / 2
                input_st_length = xstart - input_inv_taper_length - Ls
                rext = RR + rw + g + W / 2

                WG_through_port_y_pos = y_pos
                Rdec = rext

                x_pos0 = xdec - Ls - input_st_length
                cx1 = 0

                x_pos0 = xdec - Ls - input_st_length
                cx1 = 0

                x_pos = x_shift * cnt_shift + x_pos0  # - (cx1 - 3*RR)
                xpos1 = x_shift + x_pos0 - (cx1 - 3 * RR)

                x_left = x0 - inp_WG_L - input_st_length
                x_sleft_out = x_pos - x_shift + (Lrace - 2 * np.pi * RR) / 3
                x_right = x_pos + (Lrace - 2 * np.pi * RR) / 4 + 5

                if x_right > tot_length / 2 - input_inv_taper_length:
                    cx1 = 0
                    y_pos = y_pos - 2 * RR - carriage_shift
                    WG_through_port_y_pos = y_pos
                    cnt_shift = 0
                    x_pos = x_shift * cnt_shift + x_pos0
                    xpos1 = x_shift + x_pos0 - (cx1 - 3 * RR)
                    x_left = x0 - inp_WG_L - input_st_length
                    x_sleft_out = x_pos - x_shift + (Lrace - 2 * np.pi * RR) / 3
                    x_right = x_pos + lc / 2 + 25

                # -- Create the Racetrack
                params_track["G"] = g
                params_track["Lc"] = lc
                params_track["RW"] = rw
                params_track["Ljoin"] = inp_WG_L
                params_track["layer"] = layer
                params_track["y0"] = y_pos
                params_track["x0"] = x_pos
                params_track["circle_coupling"] = circle_coupling
                params_track["R0"] = RR

                name, xy_met, xy_tot = GenerateRaceTrackChristy(
                    fid, params_track, ncell, cnt
                )
                if heater:
                    params_heater = copy(param)
                    params_heater["name"] = Name + str(cnt)
                    params_heater["x_pos"] = x_pos
                    params_heater["y_pos"] = y_pos
                    params_heater["rw"] = rw
                    params_heater["xyP1p"] = xy_met
                    name_out += LigentecHeaterRaceTrack(fid, params_heater, ncell, cnt)
                    fid.write(str(layer) + " layer\n")
                    fid.write(str(datatype) + " dataType\n")

                xtrack, ytrack = xy_tot[:, 0], xy_tot[:, 1]

                name_out += name
                if cnt == 0:
                    x_sleft = x_pos + xtrack.min() - 30
                y_txt = WG_through_port_y_pos + y_pos_text
                params_port["name"] = Name + "_" + str(cnt)
                params_port["RR"] = RR
                params_port["G"] = g
                params_port["RW"] = rw
                params_port["W"] = W
                params_port["inp_WG_L"] = Ls
                params_port["input_st_length"] = input_st_length
                params_port["input_inv_taper_W"] = input_inv_taper_W
                if output_inv_taper_W == input_inv_taper_W:
                    params_port["output_inv_taper_W"] = output_inv_taper_W
                else:
                    params_port["output_inv_taper_W"] = output_inv_taper_W
                params_port["resist"] = "negative"
                params_port["cap"] = False
                params_port["layerWg"] = layer
                params_port["layerTapper"] = layer
                params_port["x2_in_wg"] = x_left
                params_port["x1_out_wg"] = None
                params_port["xin_c"] = x_left + 60
                params_port["yin_c"] = y_pos - RR - 4
                params_port["x_sleft_out"] = x_pos + xtrack.min() - 30
                params_port["xR"] = x_pos
                params_port["WG_through_port_y_pos"] = y_pos
                params_port["racetrack"] = True
                params_port["xcpl"] = x_pos + xtrack.min() - W / 2 - g
                name_out += CreateThroughPortCurveS(fid, params_port, ncell, cnt)

                if len(G) > 1:
                    txt_G = " G={:.0f}".format(g * 1e3)
                else:
                    txt_G = ""
                if len(RW) > 1:
                    txt_RW = " RW={:.0f}".format(rw * 1e3)
                else:
                    txt_RW = ""
                if len(Lc) > 1:
                    txt_Lc = " Lc={:.0f}".format(lc)
                else:
                    txt_Lc = ""

                txt = txt_RW + txt_G + txt_Lc

                if not txt == "":
                    if resist == "positive":
                        layer_loop = [layer_stepper, layer_waveguide]
                        box = True
                    else:
                        layer_loop = [layer]
                        box = False

                    for llyr in layer_loop:
                        par_lab = {
                            "x_pos_text": x_pos_text,
                            "y_pos_text": y_txt,
                            "txt": txt,
                            "font": font,
                            "layer": llyr,
                            "box": box,
                            "name": "Lbl"
                            + Name.replace("_", "")
                            + "Cell"
                            + str(ncell)
                            + "_"
                            + str(cnt),
                        }
                        name_out += CreateLabel(fid, par_lab, ncell)

                        if label_out:
                            par_lab = {
                                "x_pos_text": x_pos_text_out - 6 * len(txt),
                                "y_pos_text": y_txt,
                                "txt": txt,
                                "font": font,
                                "box": box,
                                "layer": llyr,
                                "name": "Lbl"
                                + Name.replace("_", "")
                                + "Cell"
                                + str(ncell)
                                + "_"
                                + str(cnt),
                            }
                            name_out += CreateLabel(fid, par_lab, ncell)

                # Create Bottom block waveguide

                subcell = "{}Rct{}".format(Name, cnt)

                fid.write(
                    "<" + subcell + "_" + str(ncell) + "_" + str(cnt) + " struct>\n"
                )
                for n in name_out:
                    fid.write("\t<" + n + " 0 0 0 1 0 instance>\n")

                fid.write("\n")
                name_loop.append(subcell + "_" + str(ncell) + "_" + str(cnt))

                cnt += 1
                cnt_shift += 1

    fid.write("<" + Name + str(ncell) + " struct>\n")
    for n in name_loop:
        fid.write("\t<" + n + " 0 {:.3f} 0 1 0 instance>\n".format(-RR - G[0] - W / 2))

    fid.write("\n")
    fid.write("# ******************************\n")

    return [Name + str(ncell)]
