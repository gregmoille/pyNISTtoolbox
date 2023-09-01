import numpy as np


def Bezier(t, p0, p1, p2, p3):
    return (
        (1 - t) ** 3 * np.array(p0)
        + 3 * (1 - t) ** 2 * t * np.array(p1)
        + 3 * (1 - t) * t**2 * np.array(p2)
        + t**3 * np.array(p3)
    )


def CreateThroughPort(fid, param, ncell, cnt_out):
    Name = param.get("name", None)
    layer = param.get("layer", None)
    layerWg = param.get("layerWg", layer)
    layerTapper = param.get("layerTapper", layer)

    RR = param.get("RR", None)
    RW = param.get("RW", None)
    G = param.get("G", None)
    x0 = param.get("x0", None)
    y0 = param.get("y0", None)
    x_shift= param.get("x_shift", None)
    Gdimer= param.get("Gdimer", None)

    angled_facets = param.get("angled_facets", None)
    resist = param.get("resist", "positive")
    Drop = param.get("Drop", False)
    y_drop = param.get("y_drop", 0)
    out_sep = param.get("out_sep", 5)
    # y_pos = param.get('y_pos', None)
    nr = param.get("nr", 1000)
    inp_WG_L = param.get("inp_WG_L", None)
    W = param.get("W", None)
    cap = param.get("cap", True)
    exp_w = param.get("exp_w", None)
    exp_w_tapper = param.get("exp_w_tapper", exp_w)
    in_tap_etch = param.get("in_tap_etch", 0)
    do_mixmatch = param.get("do_mixmatch", False)

    tot_length = param.get("tot_length", None)
    WG_through_port_y_pos = param.get("WG_through_port_y_pos", 0)
    font_size_pattern = param.get("font_size_pattern", 10)
    y_shift = param.get("y_shift", 0)
    input_inv_taper_length = param.get("input_inv_taper_length", None)
    input_st_length = param.get("input_st_length", None)
    input_inv_taper_st_length = param.get("input_inv_taper_st_length", 1)
    input_inv_taper_W = param.get("input_inv_taper_W", None)
    input_surplus_taper = param.get("input_surplus_taper", 50)

    output_st_length = param.get("output_st_length", input_st_length)
    output_inv_taper_st_length = param.get(
        "output_inv_taper_st_length", input_inv_taper_st_length
    )
    output_inv_taper_length = param.get(
        "output_inv_taper_length", input_inv_taper_length
    )
    output_inv_taper_W = param.get("output_inv_taper_W", input_inv_taper_W)
    output_surplus_taper = param.get("output_surplus_taper", input_surplus_taper)

    tapperLength = param.get("tapperLength", None)
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
    # -- ------------------------------ ------------------- -------^------- --------------------------------- ------------------------------- ---    y_thrgh
    #
    #    ^                             ^                   ^       x0      ^                                  ^                              ^
    # x1_in_lin                    x2_in_lin           x2_in_wg         x1_out_wg                       x1_out_lin                       x2_out_lin

    if input_st_length == None:
        input_st_length = tot_length / 2 - (inp_WG_L) - input_inv_taper_length
        output_st_length = input_st_length

    input_WG_length = (
        input_inv_taper_st_length + input_inv_taper_length + input_st_length
    )
    final_WG_length = (
        output_inv_taper_st_length + output_inv_taper_length + output_st_length
    )

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
    x1_out_wg_back = param.get("x1_out_wg_back", x1_out_wg)
    x2_out_lin = param.get("x2_out_lin", x2_out_lin)
    x1_out_lin = param.get("x1_out_lin", x1_out_lin)

    w3 = W / 2 - input_inv_taper_W / 2
    w4 = 0.350 / 2 - input_inv_taper_W / 2
    Ltap_ebeam = w4 * input_inv_taper_length / w3

    # ---------------------------------------------------------
    #             -- Create the Through port --
    # ---------------------------------------------------------

    if resist == "positive":
        #  -- Create the left cap- --
        wvg_type = "waveguideInv"
        # if input_surplus_taper > 0:
        #     fid.write('\t<{} {} '.format(x1_in_lin - input_surplus_taper, y_thrgh) +
        #               '{} {} '.format(x1_in_lin, y_thrgh) +
        #               '{} {} '.format(input_inv_taper_W, exp_w) +
        #               '0 0 0 {}>\n'.format(wvg_type))
        if cap:
            if do_mixmatch:
                fid.write(str(layerTapper) + " layer\n")
            else:
                fid.write(str(layerWg) + " layer\n")

            if tapperLength:
                x1_in_lin = x1_in_lin - tapperLength

            if input_surplus_taper > 0:
                x1_in_cap = x1_in_lin - input_inv_taper_st_length - input_surplus_taper
            else:
                x1_in_cap = x1_in_lin - input_inv_taper_st_length

            name_out.append(Name + "InCapSt" + "Cell" + str(ncell) + "_" + str(cnt_out))

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
                + "{} {} ".format(input_inv_taper_W, exp_w_tapper + in_tap_etch)
                + "0 1 0 {}>\n".format(wvg_type)
            )

            if do_mixmatch:
                fid.write(str(layerWg) + " layer\n")
        if tapperLength:
            name_out.append(Name + "Tl_" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "<"
                + Name
                + "Tl_"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            fid.write(
                "\t<{} {} ".format(x1_in_lin, y_thrgh)
                + "{} {} ".format(x1_in_lin + tapperLength, y_thrgh)
                + "{} {} ".format(input_inv_taper_W, exp_w_tapper)
                + "0 0 0 {}>\n".format(wvg_type)
            )
        #  -- Create the left linear tapper- --
        if tapperLength:
            x1_in_lin = x1_in_lin + tapperLength
        W1_in_lin = input_inv_taper_W + 2 * (exp_w_tapper + in_tap_etch)
        W2_in_lin = W + 2 * exp_w
        W2_in_lin_mid = 0.350 + 2 * exp_w
        Ws1_in_lin = input_inv_taper_W
        Ws2_in_lin = W

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
        if do_mixmatch:
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "\t<{} {} ".format(x1_in_lin, y_thrgh)
                + "{} {} ".format(x1_in_lin + Ltap_ebeam, y_thrgh)
                + "{} {} ".format(W1_in_lin, W2_in_lin_mid)
                + "{} {} ".format(Ws1_in_lin, 0.350)
                + "0 linearTaperSlot>\n"
            )
            fid.write(
                "\t<{} {} ".format(x1_in_lin + Ltap_ebeam, y_thrgh)
                + "{} {} ".format(x1_in_lin + Ltap_ebeam, y_thrgh)
                + "{} {} ".format(0.350, exp_w)
                + "0 0 1 {}>\n".format(wvg_type)
            )

            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "\t<{} {} ".format(x1_in_lin + Ltap_ebeam, y_thrgh)
                + "{} {} ".format(x2_in_lin, y_thrgh)
                + "{} {} ".format(W2_in_lin_mid, W2_in_lin)
                + "{} {} ".format(0.35, Ws2_in_lin)
                + "0 linearTaperSlot>\n"
            )

            # fid.write(str(layerWg) + ' layer\n')
        else:

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
            + "0 0 1 {}>\n".format(wvg_type)
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
            + "0 1 0 {}>\n".format(wvg_type)
        )

        # -- Create the output linear tapper --
        W1_in_lin = output_inv_taper_W + 2 * (exp_w_tapper + in_tap_etch)
        W2_in_lin = W + 2 * exp_w
        W1_in_lin_mid = 0.350 + 2 * exp_w
        Ws1_in_lin = output_inv_taper_W
        Ws2_in_lin = W
        name_out.append(Name + "OL" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerTapper) + " layer\n")
        fid.write(
            "<" + Name + "OL" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
        )

        if do_mixmatch:
            fid.write(str(layerWg) + " layer\n")

            fid.write(
                "<{} {} ".format(x1_out_lin, y_thrgh)
                + "{} {} ".format(x2_out_lin - Ltap_ebeam, y_thrgh)
                + "{} {} ".format(W2_in_lin, W1_in_lin_mid)
                + "{} {} ".format(Ws2_in_lin, 0.35)
                + "0 linearTaperSlot>\n"
            )

            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "\t<{} {} ".format(x2_out_lin - Ltap_ebeam, y_thrgh)
                + "{} {} ".format(x2_out_lin - Ltap_ebeam, y_thrgh)
                + "{} {} ".format(0.350, exp_w)
                + "0 1 0 {}>\n".format(wvg_type)
            )
            fid.write(
                "<{} {} ".format(x2_out_lin - Ltap_ebeam, y_thrgh)
                + "{} {} ".format(x2_out_lin, y_thrgh)
                + "{} {} ".format(W1_in_lin_mid, W1_in_lin)
                + "{} {} ".format(0.35, Ws1_in_lin)
                + "0 linearTaperSlot>\n"
            )
            fid.write(str(layerWg) + " layer\n")

        else:
            fid.write(
                "<{} {} ".format(x1_out_lin, y_thrgh)
                + "{} {} ".format(x2_out_lin, y_thrgh)
                + "{} {} ".format(W2_in_lin, W1_in_lin)
                + "{} {} ".format(Ws2_in_lin, Ws1_in_lin)
                + "0 linearTaperSlot>\n"
            )

        if tapperLength:
            name_out.append(Name + "Tr_" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "<"
                + Name
                + "Tr_"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            fid.write(
                "\t<{} {} ".format(x2_out_lin, y_thrgh)
                + "{} {} ".format(x2_out_lin + tapperLength, y_thrgh)
                + "{} {} ".format(input_inv_taper_W, exp_w_tapper + in_tap_etch)
                + "0 0 0 {}>\n".format(wvg_type)
            )
        # #  -- Create end cap --
        if do_mixmatch:
            fid.write(str(layerTapper) + " layer\n")
        if tapperLength:
            x2_out_lin = x2_out_lin + tapperLength

        # if output_surplus_taper > 0:
        #     fid.write('\t<{} {} '.format(x2_out_lin , y_thrgh) +
        #               '{} {} '.format(x2_out_lin + output_surplus_taper, y_thrgh) +
        #               '{} {} '.format(output_inv_taper_W, exp_w) +
        #               '0 0 0 {}>\n'.format(wvg_type))
        if output_surplus_taper > 0:
            x2_out_cap = x2_out_lin + output_inv_taper_st_length + output_surplus_taper
        else:
            x2_out_cap = x2_out_lin + output_inv_taper_st_length
        W_out_tap = output_inv_taper_W
        We_out_tap = (W1_in_lin - W_out_tap) / 2

        name_out.append(Name + "OC" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerTapper) + " layer\n")
        fid.write(
            "<" + Name + "OC" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
        )
        fid.write(
            "<{} {} ".format(x2_out_lin, y_thrgh)
            + "{} {} ".format(x2_out_cap, y_thrgh)
            + "{} {} ".format(output_inv_taper_W, We_out_tap)
            + "0 0 1 {}>\n".format(wvg_type)
        )

        if do_mixmatch:
            fid.write(str(layerWg) + " layer\n")

    else:
        wvg_type = "waveguide"
        #  -- Create the left cap- --
        if cap:
            x1_in_cap = x1_in_lin - input_inv_taper_st_length
            name_out.append(Name + "IC" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "<"
                + Name
                + "IC"
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
        name_out.append(Name + "InL" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(
            "<" + Name + "InL" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
        )
        fid.write(str(layerTapper) + " layer\n")
        if angled_facets is None:

            #  -- small surplus for cuting --
            if input_surplus_taper > 0:
                fid.write(
                    "\t<{} {} ".format(x1_in_lin - input_surplus_taper, y_thrgh)
                    + "{} {} ".format(x1_in_lin, y_thrgh)
                    + "{} ".format(input_inv_taper_W)
                    + "0 0 0 {}>\n".format(wvg_type)
                )
            #  -- Create the left linear tapper- --
            # W1_in_lin = input_inv_taper_W+2*exp_w
            # W2_in_lin = W+2*exp_w
            Ws1_in_lin = input_inv_taper_W
            Ws2_in_lin = W

            if do_mixmatch:
                fid.write(
                    "\t<{} {} ".format(
                        x1_in_lin - 5 + 3.5 / 2 - input_inv_taper_W / 2, y_thrgh
                    )
                    + "{} {} ".format(x1_in_lin + Ltap_ebeam - 3.5 / 2, y_thrgh)
                    + "{} ".format(3.5)
                    + "0 1 1 {}>\n".format(wvg_type)
                )

            fid.write(
                "\t<{} {} ".format(x1_in_lin, y_thrgh)
                + "{} {} ".format(x2_in_lin, y_thrgh)
                + "{} {} ".format(Ws1_in_lin, Ws2_in_lin)
                + "0 linearTaper>\n"
            )

            # -- Create Left waveguide --
            W_in_wg = W
            # We_in_wg = exp_w

            name_out.append(Name + "IW1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "<"
                + Name
                + "IW1_"
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

        else:
            Ws1_in_lin = input_inv_taper_W
            Ws2_in_lin = W
            Ltaper = x2_in_lin - x1_in_lin
            angle_deg = angled_facets
            angle = angle_deg * np.pi / 180
            tap_short = 25 * np.cos(angle) * 2 / (np.sqrt(2))

            y_in_angle = y_thrgh - Ltaper * np.sin(angle)
            y_out_angle = y_in_angle + (Ltaper - tap_short) * np.sin(angle)
            x_out_angle = x1_in_lin + (Ltaper - tap_short) * np.cos(angle)

            x3 = x_out_angle - Ws2_in_lin / 2 * np.sin(angle)
            y3 = y_out_angle + Ws2_in_lin / 2
            x4 = x_out_angle + Ws2_in_lin / 2 * np.sin(angle)
            y4 = y_out_angle - Ws2_in_lin / 2

            fid.write(
                f"\t{x1_in_lin:.3f} {y_in_angle + Ws1_in_lin/2:.3f} "
                + f"{x3:.3f} {y3:.3f} "
                + f"{x4:.3f} {y4:.3f} "
                + f"{x1_in_lin:.3f} {y_in_angle - Ws1_in_lin/2:.3f} "
                + "points2shape\n"
            )

            W_in_wg = W
            # We_in_wg = exp_w

            name_out.append(Name + "IW1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "<"
                + Name
                + "IW1_"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )
            dy = y_thrgh - Ws2_in_lin / 2 - y4
            p0 = [x4, y4]
            p1 = [x4 + dy / np.tan(angle), y_thrgh - Ws2_in_lin / 2]
            p2 = [x2_in_lin, y_thrgh - Ws2_in_lin / 2]
            p3 = [x2_in_lin + 5, y_thrgh - Ws2_in_lin / 2]
            xyBzst_down = np.array(
                [Bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 40)]
            )
            dy = y_thrgh + Ws2_in_lin / 2 - y3
            p0 = [x3, y3]
            p1 = [x3 + dy / np.tan(angle), y_thrgh + Ws2_in_lin / 2]
            p2 = [x2_in_lin, y_thrgh + Ws2_in_lin / 2]
            p3 = [x2_in_lin + 5, y_thrgh + Ws2_in_lin / 2]
            xyBzst_up = np.array(
                [Bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 40)]
            )
            xyBzt = np.vstack([xyBzst_up, xyBzst_down[::-1]])
            for xx, yy in xyBzt:
                fid.write(f"{xx:.3f} {yy:.3f} ")
            fid.write("points2shape\n ")

            fid.write(
                "\t<{} {} ".format(x2_in_lin + 5, y_thrgh)
                + "{} {} ".format(x2_in_wg, y_thrgh)
                + "{} ".format(W)
                + "0 0 0 {}>\n".format(wvg_type)
            )

        # -- Create Right waveguide --
        W_in_wg = W
        # We_in_wg = exp_w

        name_out.append(Name + "IW1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(str(layerWg) + " layer\n")
        fid.write(
            "<"
            + Name
            + "IW1_"
            + "Cell"
            + str(ncell)
            + "_"
            + str(cnt_out)
            + " struct>\n"
        )
        if angled_facets is None:
            shift = 0
        else:
            shift = -10
        fid.write(
            "\t<{} {} ".format(x1_out_wg, y_thrgh)
            + "{} {} ".format(x1_out_lin + shift, y_thrgh)
            + "{} ".format(W)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        if angled_facets is None:
            # -- Create the output linear tapper --
            W1_in_lin = output_inv_taper_W + 2 * exp_w_tapper
            # W2_in_lin = W+2*exp_w
            # Ws1_in_lin = output_inv_taper_W
            # Ws2_in_lin = W
            name_out.append(Name + "OL" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerTapper) + " layer\n")
            fid.write(
                "<"
                + Name
                + "OL"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )

            if do_mixmatch:
                fid.write(
                    "\t<{} {} ".format(x2_out_lin - Ltap_ebeam + 3.5 / 2, y_thrgh)
                    + "{} {} ".format(
                        x2_out_lin + 5 - 3.5 / 2 + output_inv_taper_W / 2, y_thrgh
                    )
                    + "{} ".format(3.5)
                    + "0 1 1 {}>\n".format(wvg_type)
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

                name_out.append(Name + "" + "Cl" + str(ncell) + "_" + str(cnt_out))
                fid.write(str(layerTapper) + " layer\n")
                fid.write(
                    "<" + Name + "Cl" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
                )
                fid.write(
                    "<{} {} ".format(x2_out_lin, y_thrgh)
                    + "{} {} ".format(x2_out_cap, y_thrgh)
                    + "{} ".format(output_inv_taper_W)
                    + "0 0 1 {}>\n".format(wvg_type)
                )

            #  -- small surplus for cuting --
            if output_surplus_taper > 0:
                fid.write(
                    "\t<{} {} ".format(x2_out_lin, y_thrgh)
                    + "{} {} ".format(x2_out_lin + output_surplus_taper, y_thrgh)
                    + "{} ".format(output_inv_taper_W)
                    + "0 0 0 {}>\n".format(wvg_type)
                )
        else:
            y_out_angle = y_thrgh + Ltaper * np.sin(angle)
            y_in_angle = y_out_angle - (Ltaper - tap_short) * np.sin(angle)
            x_in_angle = x2_out_lin - (Ltaper - tap_short) * np.cos(angle)

            x3 = x_in_angle - Ws2_in_lin / 2 * np.sin(angle)
            y3 = y_in_angle + Ws2_in_lin / 2
            x4 = x_in_angle + Ws2_in_lin / 2 * np.sin(angle)
            y4 = y_in_angle - Ws2_in_lin / 2

            fid.write(
                f"\t{x2_out_lin:.3f} {y_out_angle + Ws1_in_lin/2:.3f} "
                + f"{x3:.3f} {y3:.3f} "
                + f"{x4:.3f} {y4:.3f} "
                + f"{x2_out_lin:.3f} {y_out_angle - Ws1_in_lin/2:.3f} "
                + "points2shape\n"
            )

            name_out.append(Name + "IW1_" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "<"
                + Name
                + "IW1_"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )

            dy = y_thrgh - Ws2_in_lin / 2 - y4
            p0 = [x4, y4]
            p1 = [x4 + dy / np.tan(angle), y_thrgh - Ws2_in_lin / 2]
            p2 = [x1_out_lin, y_thrgh - Ws2_in_lin / 2]
            p3 = [x1_out_lin + shift, y_thrgh - Ws2_in_lin / 2]
            xyBzst_down = np.array(
                [Bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 40)]
            )
            p0 = [x3, y3]
            dy = y_thrgh - Ws2_in_lin / 2 - y3
            p1 = [x3 + dy / np.tan(angle), y_thrgh + Ws2_in_lin / 2]
            p2 = [x1_out_lin, y_thrgh + Ws2_in_lin / 2]
            p3 = [x1_out_lin + shift, y_thrgh + Ws2_in_lin / 2]
            xyBzst_up = np.array(
                [Bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 40)]
            )
            xyBzt = np.vstack([xyBzst_up, xyBzst_down[::-1]])
            for xx, yy in xyBzt:
                fid.write(f"{xx:.3f} {yy:.3f} ")
            fid.write("points2shape\n ")
        if Drop:
            name_out.append(Name + "Drop_" + "Cell" + str(ncell) + "_" + str(cnt_out))
            fid.write(str(layerWg) + " layer\n")
            fid.write(
                "<"
                + Name
                + "Drop_"
                + "Cell"
                + str(ncell)
                + "_"
                + str(cnt_out)
                + " struct>\n"
            )

            fid.write(
                f"<{x1_out_wg + 10:.3f} {y_drop:.3f} "
                + f"{x1_out_wg - 12:.3f} {y_drop:.3f} "
                + f"{Ws2_in_lin:.3f} "
                + f"0 0 1 {wvg_type}>\n"
            )

            R90 = 23 + 4
            if Gdimer is None:
                fid.write(
                    f"\t<{x1_out_wg - RR/2 - 2:.3f} {y_drop:.3f} "
                    + f"{x1_out_wg - RR/2 - 23:.3f} {y_drop + 23:.3f} "
                    + f"{W:.3f} {0} "
                    + "sBend>\n"
                )
                
                fid.write(
                    f"\t<{x1_out_wg - RR/2 - 23:.3f} {y_drop + 23:3f} "
                    + f"{-R90/2:.3f} {-R90/2:3f} "
                    + f"{W:.3f} "
                    + "0 90degreeBendLH>\n"
                )
                fid.write(
                    f"\t<{x1_out_wg - RR/2 - 23 - R90/2:.3f} {y_drop + 23 - R90/2:3f} "
                    + f"{R90/2:.3f} {R90/2:3f} "
                    + f"{W:.3f} "
                    + "-90 90degreeBendLH>\n"
                )

                fid.write(
                    f"<{x1_out_wg - RR/2 - 23:.3f} {y_drop + 23 - R90:.3f} "
                    + f"{x1_out_wg_back:.3f} {y_drop + 23 - R90:.3f} "
                    + f"{Ws2_in_lin:.3f} "
                    + f"0 0 0 {wvg_type}>\n"
                )
                Hdrop = (y_thrgh - out_sep) - (y_drop + 23 - R90)

                fid.write(
                    f"\t<{x1_out_wg_back :.3f} {y_drop + 23 - R90:3f} "
                    + f"{x_shift - 2*RR:.3f} {Hdrop:.3f} "
                    + f"{W:.3f} {0} "
                    + "sBendLH>\n"
                )
            else: 
                fid.write(
                    f"<{x1_out_wg + 10:.3f} {y_drop:.3f} "
                    + f"{x1_out_wg_back:.3f} {y_drop:.3f} "
                    + f"{Ws2_in_lin:.3f} "
                    + f"0 0 0 {wvg_type}>\n"
                )
                Hdrop = (y_thrgh - out_sep) - (y_drop)

                fid.write(
                    f"\t<{x1_out_wg_back :.3f} {y_drop:3f} "
                    + f"{x_shift - 2*RR:.3f} {Hdrop:.3f} "
                    + f"{W:.3f} {0} "
                    + "sBendLH>\n"
                )
                
            

            fid.write(
                f"<{x1_out_wg_back  +(x_shift - 2*RR):.3f} {y_thrgh - out_sep:.3f} "
                + f"{x1_out_lin:.3f} {y_thrgh - out_sep:.3f} "
                + f"{Ws2_in_lin:.3f} "
                + f"0 0 0 {wvg_type}>\n"
            )

            fid.write(
                "<{:.3f} {:.3f} ".format(x1_out_lin, y_thrgh - out_sep)
                + "{:.3f} {:.3f} ".format(x2_out_lin, y_thrgh - out_sep)
                + "{:.3f} {:.3f} ".format(Ws2_in_lin, Ws1_in_lin)
                + "0 linearTaper>\n"
            )

        #  -- Create the left linear tapper- --
    # ---------------------------------------------------------
    #        -- Merge everything in 1 structure --
    # ---------------------------------------------------------
    fid.write("\n")
    fid.write("<" + Name + "Tport" + str(ncell) + "_" + str(cnt_out) + " struct>\n")
    for n in name_out:
        fid.write("\t<" + n + " 0 0 0 1 0 instance>\n")

    return [Name + "Tport" + str(ncell) + "_" + str(cnt_out)]
