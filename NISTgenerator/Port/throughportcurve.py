import numpy as np


def CreateThroughPortCurve(fid, param, ncell, cnt_out):
    Name = param.get("name", None)
    layer = param.get("layer", None)
    layerWg = param.get("layerWg", layer)
    layerTapper = param.get("layerTapper", layer)
    angled_facets = param.get("angled_facets", False)
    RR = param.get("RR", None)
    RW = param.get("RW", None)
    G = param.get("G", None)
    x0 = param.get("x0", None)
    y0 = param.get("y0", None)
    resist = param.get("resist", "positive")
    # y_pos = param.get('y_pos', None)
    nr = param.get("nr", 1000)
    inp_WG_L = param.get("inp_WG_L", None)
    W = param.get("W", None)
    cap = param.get("cap", True)
    exp_w = param.get("exp_w", None)
    tot_length = param.get("tot_length", None)
    WG_through_port_y_pos = param.get(
        "WG_through_port_y_pos",
    )
    font_size_pattern = param.get("font_size_pattern", 10)
    y_shift = param.get("y_shift", 0)
    input_inv_taper_length = param.get("input_inv_taper_length", None)
    input_st_length = param.get("input_st_length", None)
    input_inv_taper_st_length = param.get("input_inv_taper_st_length", None)
    input_inv_taper_W = param.get("input_inv_taper_W", None)
    output_st_length = param.get("output_st_length", None)
    output_inv_taper_st_length = param.get("output_inv_taper_st_length", None)
    output_inv_taper_length = param.get("output_inv_taper_length", None)
    output_inv_taper_W = param.get("output_inv_taper_W", None)

    input_WG_length = (
        input_inv_taper_st_length + input_inv_taper_length + input_st_length
    )
    final_WG_length = (
        output_inv_taper_st_length + output_inv_taper_length + output_st_length
    )

    name_out = []

    # ---------------------------------------------------------
    #     -- Compute coordinate for the through port --
    # ---------------------------------------------------------
    # Through port
    #    <--------------------------------------------------- total length ----------------------------------------------------------------->
    #    <- input_inv_taper_length  ->                                                                      <-  output_inv_taper_length ->
    #                                   <-input_st_length->
    #                                                       <  2*inp_WG_L >
    #                                                                       <----------   automatic --------->
    # -- ------------------------------ -------              --------^------- --------------------------------- ------------------------------- ---    y_thrgh
    #                                          _____________
    #    ^                             ^      ^            ^       x0      ^                                  ^                              ^
    # x1_in_lin                    x2_in_lin   xin_c     x2_in_wg         x1_out_wg                       x1_out_lin                       x2_out_lin

    x1_in_lin = x0 - inp_WG_L - input_st_length - input_inv_taper_length
    x2_in_lin = x0 - inp_WG_L - input_st_length
    x2_in_wg = x0 - inp_WG_L
    x1_out_wg = x0 + inp_WG_L
    x2_out_lin = tot_length + x1_in_lin
    x1_out_lin = x2_out_lin - output_inv_taper_length

    y_thrgh = WG_through_port_y_pos

    x1_in_lin = param.get("x1_in_lin", x1_in_lin)
    x2_in_lin = param.get("x2_in_lin", x2_in_lin)
    x2_in_wg = param.get("x2_in_wg", x2_in_wg)
    x1_out_wg = param.get("x1_out_wg", x1_out_wg)
    x2_out_lin = param.get("x2_out_lin", x2_out_lin)
    x1_out_lin = param.get("x1_out_lin", x1_out_lin)
    xin_c = param.get("xin_c", None)
    yin_c = param.get("yin_c", None)

    x_sleft_out = param.get("x_sleft_out", 0)
    cx1 = param.get("cx1", None)
    cy1 = param.get("cy1", None)
    cx2 = param.get("cx2", None)
    cy2 = param.get("cy2", None)

    # ---------------------------------------------------------
    #             -- Create the Through port --
    # ---------------------------------------------------------

    if resist == "positive":
        #  -- Create the left cap- --
        if cap:
            wvg_type = "waveguideInv"
            x1_in_cap = x1_in_lin - input_inv_taper_st_length
            name_out.append(Name + "InCapSt" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "<"
                + Name
                + "InCapSt"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            fid.write(
                "\t<{} {} ".format(x1_in_cap, y_thrgh)
                + "{} {} ".format(x1_in_lin, y_thrgh)
                + "{} {} ".format(input_inv_taper_W, exp_w)
                + "0 1 0 {}>\n".format(wvg_type)
            )

        #  -- Create the left linear tapper- --
        W1_in_lin = input_inv_taper_W + 2 * exp_w
        W2_in_lin = W + 2 * exp_w
        Ws1_in_lin = input_inv_taper_W
        Ws2_in_lin = W

        fid.write(str(layerTapper) + " layer\n")
        name_out.append(Name + "InLin" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(
            "<"
            + Name
            + "InLin"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(x1_in_lin, y_thrgh)
            + "{} {} ".format(x2_in_lin, y_thrgh)
            + "{} {} ".format(W1_in_lin, W2_in_lin)
            + "{} {} ".format(Ws1_in_lin, Ws2_in_lin)
            + "0 linearTaperSlot>\n"
        )

        # -- Create Left waveguide --
        W_in_wg = W
        We_in_wg = exp_w

        name_out.append(Name + "InWg1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerWg) + " layer\n")
        fid.write(
            "<"
            + Name
            + "InWg1_"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(x2_in_lin, y_thrgh)
            + "{} {} ".format(x2_in_wg, y_thrgh)
            + "{} {} ".format(W, We_in_wg)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        # -- Create Right waveguide --
        W_in_wg = W
        We_in_wg = exp_w

        name_out.append(Name + "InWg1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerWg) + " layer\n")
        fid.write(
            "<"
            + Name
            + "InWg1_"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(x1_out_wg, y_thrgh)
            + "{} {} ".format(x1_out_lin, y_thrgh)
            + "{} {} ".format(W, We_in_wg)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        # -- Create the output linear tapper --
        W1_in_lin = output_inv_taper_W + 2 * exp_w
        W2_in_lin = W + 2 * exp_w
        Ws1_in_lin = output_inv_taper_W
        Ws2_in_lin = W
        name_out.append(Name + "OutLin" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerTapper) + " layer\n")
        fid.write(
            "<"
            + Name
            + "OutLin"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "<{} {} ".format(x1_out_lin, y_thrgh)
            + "{} {} ".format(x2_out_lin, y_thrgh)
            + "{} {} ".format(W2_in_lin, W1_in_lin)
            + "{} {} ".format(Ws2_in_lin, Ws1_in_lin)
            + "0 linearTaperSlot>\n"
        )

        # #  -- Create end cap --
        x2_out_cap = x2_out_lin + output_inv_taper_st_length
        W_out_tap = output_inv_taper_W
        We_out_tap = (W1_in_lin - W_out_tap) / 2

        name_out.append(Name + "OutCapSt" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerTapper) + " layer\n")
        fid.write(
            "<"
            + Name
            + "OutCapSt"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "<{} {} ".format(x2_out_lin, y_thrgh)
            + "{} {} ".format(x2_out_cap, y_thrgh)
            + "{} {} ".format(output_inv_taper_W, We_out_tap)
            + "0 0 1 {}>\n".format(wvg_type)
        )
    else:
        wvg_type = "waveguide"
        #  -- Create the left cap- --
        if cap:
            x1_in_cap = x1_in_lin - input_inv_taper_st_length
            name_out.append(Name + "InCapSt" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "<"
                + Name
                + "InCapSt"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            fid.write(
                "\t<{} {} ".format(x1_in_cap, y_thrgh)
                + "{} {} ".format(x1_in_lin, y_thrgh)
                + "{} ".format(input_inv_taper_W)
                + "0 1 0 {}>\n".format(wvg_type)
            )
        if not angled_facets:
            #  -- Create the left linear tapper- --
            W1_in_lin = input_inv_taper_W + 2 * exp_w
            W2_in_lin = W + 2 * exp_w
            Ws1_in_lin = input_inv_taper_W
            Ws2_in_lin = W

            name_out.append(Name + "InLin" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "<"
                + Name
                + "InLin"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            fid.write(
                "\t<{} {} ".format(x1_in_lin, y_thrgh)
                + "{} {} ".format(x2_in_lin, y_thrgh)
                + "{} {} ".format(Ws1_in_lin, Ws2_in_lin)
                + "0 linearTaper>\n"
            )
        else:
            W1_in_lin = input_inv_taper_W + 2 * exp_w
            W2_in_lin = W + 2 * exp_w
            Ws1_in_lin = input_inv_taper_W
            Ws2_in_lin = W

        # -- Create Left waveguide --
        W_in_wg = W
        We_in_wg = exp_w

        name_out.append(Name + "InWg1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerWg) + " layer\n")
        fid.write(
            "<"
            + Name
            + "InWg1_"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(x2_in_lin, y_thrgh)
            + "{} {} ".format(x2_in_wg, y_thrgh)
            + "{} ".format(W)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        fid.write(str(layer) + " layer\n")
        name_out.append(Name + "InSin" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(
            "<"
            + Name
            + "InSin"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(x2_in_wg, y_thrgh)
            + "{} {} ".format(xin_c, yin_c)
            + "{} {} ".format(W, 0)
            + "sBend>\n"
        )

        name_out.append(Name + "InWgC1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerWg) + " layer\n")
        fid.write(
            "<"
            + Name
            + "InWgC1_"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(xin_c, yin_c)
            + "{} {} ".format(x_sleft_out, yin_c)
            + "{} ".format(W)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        # -- Create Right waveguide --
        W_in_wg = W
        We_in_wg = exp_w

        name_out.append(Name + "InWg1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerWg) + " layer\n")
        fid.write(
            "<"
            + Name
            + "InWg1_"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "\t<{} {} ".format(x1_out_wg, y_thrgh)
            + "{} {} ".format(x1_out_lin, y_thrgh)
            + "{} ".format(W)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        # -- Create the output linear tapper --
        W1_in_lin = output_inv_taper_W + 2 * exp_w
        W2_in_lin = W + 2 * exp_w
        Ws1_in_lin = output_inv_taper_W
        Ws2_in_lin = W
        name_out.append(Name + "OutLin" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerTapper) + " layer\n")
        fid.write(
            "<"
            + Name
            + "OutLin"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        fid.write(
            "<{} {} ".format(x1_out_lin, y_thrgh)
            + "{} {} ".format(x2_out_lin, y_thrgh)
            + "{} {} ".format(Ws2_in_lin, Ws1_in_lin)
            + "0 linearTaper>\n"
        )

        # #  -- Create end cap --
        if cap:
            x2_out_cap = x2_out_lin + output_inv_taper_st_length
            W_out_tap = output_inv_taper_W
            We_out_tap = (W1_in_lin - W_out_tap) / 2

            name_out.append(
                Name + "OutCapSt" + "Cell" + str(ncell) + "_" + str(cnt_out)
            )
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "<"
                + Name
                + "OutCapSt"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            fid.write(
                "<{} {} ".format(x2_out_lin, y_thrgh)
                + "{} {} ".format(x2_out_cap, y_thrgh)
                + "{} ".format(output_inv_taper_W)
                + "0 0 1 {}>\n".format(wvg_type)
            )
    # ---------------------------------------------------------
    #        -- Merge everything in 1 structure --
    # ---------------------------------------------------------
    fid.write("\n")
    fid.write(
        "<" + Name + "_ThroughPort" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
    )
    for n in name_out:
        fid.write("\t<" + n + " 0 0 0 1 0 instance>\n")

    return [Name + "_ThroughPort" + str(ncell) + "_" + str(cnt_out)]
