import numpy as np


def Bezier(t, p0, p1, p2, p3):
    return (
        (1 - t) ** 3 * np.array(p0)
        + 3 * (1 - t) ** 2 * t * np.array(p1)
        + 3 * (1 - t) * t**2 * np.array(p2)
        + t**3 * np.array(p3)
    )


def CreateThroughPortCurveS(fid, param, ncell, cnt_out):
    Name = param.get("name", None)
    layer = param.get("layer", None)
    layerWg = param.get("layerWg", layer)
    layerTapper = param.get("layerTapper", layer)
    racetrack = param.get("racetrack", False)
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
    xR = param.get("xR", 0)
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
    input_surplus_taper = param.get("input_surplus_taper", 0)

    output_st_length = param.get("output_st_length", input_st_length)
    output_inv_taper_st_length = param.get(
        "output_inv_taper_st_length", input_inv_taper_st_length
    )
    output_inv_taper_length = param.get(
        "output_inv_taper_length", input_inv_taper_length
    )
    output_inv_taper_W = param.get("output_inv_taper_W", input_inv_taper_W)
    output_surplus_taper = param.get("output_surplus_taper", 0)

    do_field = param.get("do_field", False)
    layer_field = param.get("layer_field", None)

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
        wvg_type = "waveguideInv"
        if input_surplus_taper > 0:
            fid.write(
                "\t<{} {} ".format(x1_in_lin - input_surplus_taper, y_thrgh)
                + "{} {} ".format(x1_in_lin, y_thrgh)
                + "{} {} ".format(input_inv_taper_W, exp_w)
                + "0 0 0 {}>\n".format(wvg_type)
            )
        if cap:
            if input_surplus_taper > 0:
                x1_in_cap = x1_in_lin - input_inv_taper_st_length - input_surplus_taper
            else:
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

        if do_field:
            fid.write(str(layer_field) + " layer\n")
            Lbox = np.abs(x1_in_lin - input_surplus_taper - (x2_in_lin)) + 5
            # xc = x_pos-1.5*rr - Lsbend
            # L
            fid.write(
                f"{x1_in_lin - input_surplus_taper - 5} {y_thrgh-15} "
                + f"{Lbox} {30} "
                + "0 0 "
                + "0 roundrect\n"
            )
            fid.write(str(layerTapper) + " layer\n")

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

        fid.write(
            "\t<{} {} ".format(x2_in_wg, y_thrgh)
            + "{} {} ".format(xin_c - x2_in_wg, yin_c - y_thrgh)
            + "{} {} {} ".format(W, exp_w, 0)
            + "sBendInv>\n"
        )
        if do_field:
            fid.write(str(layer_field) + " layer\n")
            Lbox = np.abs(xin_c - x2_in_wg)
            H = np.abs(yin_c - y_thrgh) + 30
            y0 = y_thrgh + 15
            fid.write(f"{x2_in_wg} {y0-H} " + f"{Lbox} {H} " + "0 0 " + "0 roundrect\n")
            fid.write(str(layerTapper) + " layer\n")

        fid.write(
            "\t<{} {} ".format(xin_c, yin_c)
            + "{} {} ".format(x_sleft_out, yin_c)
            + "{} {} ".format(W, exp_w)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        if do_field:
            fid.write(str(layer_field) + " layer\n")
            Lbox = np.abs(x_sleft_out - xin_c)
            H = 30
            y0 = yin_c
            if Lbox > 500:
                Nbox = int(Lbox / 500)
                for nb in range(Nbox):
                    fid.write(
                        f"{xin_c + 500*nb} {y0-H/2} "
                        + f"{Lbox} {H} "
                        + "0 0 "
                        + "0 roundrect\n"
                    )

                Wleftover = Lbox - Nbox * 500
                fid.write(
                    f"{xin_c + 500*Nbox} {y0-H/2} "
                    + f"{Wleftover} {H} "
                    + "0 0 "
                    + "0 roundrect\n"
                )
                fid.write(str(layerTapper) + " layer\n")

            else:
                fid.write(
                    f"{xin_c} {y0-H/2} " + f"{Lbox} {H} " + "0 0 " + "0 roundrect\n"
                )
            fid.write(str(layerTapper) + " layer\n")

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
        if output_surplus_taper > 0:
            fid.write(
                "\t<{} {} ".format(x2_out_lin, y_thrgh)
                + "{} {} ".format(x2_out_lin + output_surplus_taper, y_thrgh)
                + "{} {} ".format(output_inv_taper_W, exp_w)
                + "0 0 0 {}>\n".format(wvg_type)
            )
        if cap:
            if output_surplus_taper > 0:
                x2_out_cap = (
                    x2_out_lin + output_inv_taper_st_length + output_surplus_taper
                )
            else:
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
        Ws1_in_lin = input_inv_taper_W
        Ws2_in_lin = W
        name_out.append(Name + "InL" + "Cell" + str(ncell) + "_" + str(cnt_out))
        fid.write(
            "<" + Name + "InL" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
        )
        fid.write(str(layerTapper) + " layer\n")

        if not angled_facets:
            #  -- small surplus for cuting --
            if input_surplus_taper > 0:
                fid.write(
                    "\t<{} {} ".format(x1_in_lin - input_surplus_taper, y_thrgh)
                    + "{} {} ".format(x1_in_lin, y_thrgh)
                    + "{} ".format(input_inv_taper_W)
                    + "0 0 0 {}>\n".format(wvg_type)
                )

            fid.write(
                "\t<{:.3f} {:.3f} ".format(x1_in_lin, y_thrgh)
                + "{:.3f} {:.3f} ".format(x2_in_lin, y_thrgh)
                + "{:.3f} {:.3f} ".format(Ws1_in_lin, Ws2_in_lin)
                + "0 linearTaper>\n"
            )
        else:
            Ws1_in_lin = input_inv_taper_W
            Ws2_in_lin = W
            Ltaper = x2_in_lin - x1_in_lin
            angle_deg = 7
            tap_short = 15
            angle = angle_deg * np.pi / 180
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
            p0 = [x4, y4]
            p1 = [x2_in_lin, y_thrgh - Ws2_in_lin / 2]
            p3 = [x2_in_lin + 5, y_thrgh - Ws2_in_lin / 2]
            xyBzst_down = np.array(
                [Bezier(t, p0, p1, p1, p3) for t in np.linspace(0, 1, 40)]
            )
            p0 = [x3, y3]
            p1 = [x2_in_lin, y_thrgh + Ws2_in_lin / 2]
            p3 = [x2_in_lin + 5, y_thrgh + Ws2_in_lin / 2]
            xyBzst_up = np.array(
                [Bezier(t, p0, p1, p1, p3) for t in np.linspace(0, 1, 40)]
            )
            xyBzt = np.vstack([xyBzst_up, xyBzst_down[::-1]])
            for xx, yy in xyBzt:
                fid.write(f"{xx:.3f} {yy:.3f} ")
            fid.write("points2shape\n ")

        # -- Create Left waveguide --
        W_in_wg = W
        # We_in_wg = exp_w

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

        if not angled_facets:
            shiftS = 0
        else:
            shiftS = 5

        fid.write(
            "\t<{:.3f} {:.3f} ".format(x2_in_lin + shiftS, y_thrgh)
            + "{:.3f} {:.3f} ".format(x2_in_wg, y_thrgh)
            + "{:.3f} ".format(W)
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
            "\t<{:.3f} {:.3f} ".format(x2_in_wg, y_thrgh)
            + "{:.3f} {:.3f} ".format(xin_c, yin_c)
            + "{:.3f} {} ".format(W, 0)
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
            "\t<{:.3f} {:.3f} ".format(xin_c, yin_c)
            + "{:.3f} {:.3f} ".format(x_sleft_out, yin_c)
            + "{:.3f} ".format(W)
            + "0 0 0 {}>\n".format(wvg_type)
        )

        # -- Create Right waveguide --
        W_in_wg = W
        # We_in_wg = exp_w

        if x1_out_wg is None:
            if racetrack:
                xcpl = param.get("xcpl", None)
                fid.write(
                    f"\t<{xcpl:.3f} {WG_through_port_y_pos-5:.3f} "
                    + f"{xcpl:.3f} {WG_through_port_y_pos+ RR - 15:3f} "
                    + f"{W:.3f} "
                    + "0 0 0 waveguide>\n"
                )

                fid.write(
                    f"\t<{x_sleft_out:.3f} {yin_c:.3f} "
                    + f"{xcpl:.3f} {WG_through_port_y_pos-5:3f} "
                    + f"{W:.3f} "
                    + "0 90degreeBend>\n"
                )

                fid.write(
                    f"\t<{xcpl:.3f} {WG_through_port_y_pos +  RR - 15:3f} "
                    + f"{-20:.3f} {20:3f} "
                    + f"{W:.3f} "
                    + "-90 90degreeBendLH>\n"
                )

                fid.write(
                    f"\t<{xcpl + 20:.3f} {WG_through_port_y_pos+ RR +5:.3f} "
                    + f"{tot_length/2 - input_inv_taper_length - 60:.3f} {WG_through_port_y_pos+ RR +5:3f} "
                    + f"{W:.3f} "
                    + "0 0 0 waveguide>\n"
                )

                fid.write(
                    f"\t<{xcpl + 20:.3f} {WG_through_port_y_pos+ RR +5:.3f} "
                    + f"{tot_length/2 - input_inv_taper_length - 60:.3f} {WG_through_port_y_pos+ RR +5:3f} "
                    + f"{W:.3f} "
                    + "0 0 0 waveguide>\n"
                )

                fid.write(
                    f"\t<{tot_length/2 - input_inv_taper_length - 60:.3f} {WG_through_port_y_pos+ RR +5:3f} "
                    + f"{tot_length/2 - input_inv_taper_length} {WG_through_port_y_pos} "
                    + "{:.3f} {} ".format(W, 0)
                    + "sBend>\n"
                )

        else:
            if not angled_facets:
                shift = 0
            else:
                shift = -10
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
                "\t<{:.3f} {:.3f} ".format(x1_out_wg, y_thrgh)
                + "{:.3f} {:.3f} ".format(x1_out_lin + shift, y_thrgh)
                + "{:.3f} ".format(W)
                + "0 0 0 {}>\n".format(wvg_type)
            )
        if not angled_facets:
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
                "<{:.3f} {:.3f} ".format(x1_out_lin, y_thrgh)
                + "{:.3f} {:.3f} ".format(x2_out_lin, y_thrgh)
                + "{:.3f} {:.3f} ".format(Ws2_in_lin, Ws1_in_lin)
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
                    "<{:.3f} {:.3f} ".format(x2_out_lin, y_thrgh)
                    + "{:.3f} {:.3f} ".format(x2_out_cap, y_thrgh)
                    + "{:.3f} ".format(output_inv_taper_W)
                    + "0 0 1 {}>\n".format(wvg_type)
                )

            #  -- small surplus for cuting --
            if output_surplus_taper > 0:
                fid.write(
                    "\t<{:.3f} {:.3f} ".format(x2_out_lin, y_thrgh)
                    + "{:.3f} {:.3f} ".format(
                        x2_out_lin + output_surplus_taper, y_thrgh
                    )
                    + "{:.3f} ".format(output_inv_taper_W)
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

            p0 = [x4, y4]
            p1 = [x1_out_lin, y_thrgh - Ws2_in_lin / 2]
            p3 = [x1_out_lin + shift, y_thrgh - Ws2_in_lin / 2]
            xyBzst_down = np.array(
                [Bezier(t, p0, p1, p1, p3) for t in np.linspace(0, 1, 40)]
            )
            p0 = [x3, y3]
            p1 = [x1_out_lin, y_thrgh + Ws2_in_lin / 2]
            p3 = [x1_out_lin + shift, y_thrgh + Ws2_in_lin / 2]
            xyBzst_up = np.array(
                [Bezier(t, p0, p1, p1, p3) for t in np.linspace(0, 1, 40)]
            )
            xyBzt = np.vstack([xyBzst_up, xyBzst_down[::-1]])
            for xx, yy in xyBzt:
                fid.write(f"{xx:.3f} {yy:.3f} ")
            fid.write("points2shape\n ")
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