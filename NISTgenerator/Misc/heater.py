import numpy as np


def CreateHeater(fid, param, ncell):
    Name = param.get("name", None)
    layer = param.get("layer_heater", 5)
    x0 = param.get("x0", 0)
    y0 = param.get("y0", 0)

    RR = param.get("RR", None)

    RWetch = param.get("RWetch", None)
    RWin = param.get("RWin", None)
    WetchAdd = param.get("WetchAdd", None)

    W = param.get("W", None)
    G = param.get("G", None)
    Lc = param.get("Lc", None)
    LcDrop = param.get("LcDrop", None)
    Gdrop = param.get("Gdrop", None)
    Nmodulation = param.get("Nmodulation", None)
    Amodulation_list = param.get("Amodulation", None)
    Sigmamodulation_list = param.get("Sigmamodulation", None)

    angle = param.get("Heaterangle", np.pi)
    Wheater = param.get("Wheater", 3)
    Wpad = param.get("Wpad", 30)
    ydecpad = param.get("ydecpad", 300)
    ytoppad = param.get("ytoppad", 200)
    signpad = param.get("signpad", 1)
    y_shift = param.get("y_shift", 100)
    xmir = param.get("xmiror", 1)
    if not type(G) == list:
        G = [G]
    if not type(Gdrop) == list:
        if Gdrop == None:
            Gdrop = [None]
        else:
            Gdrop = [Gdrop]
        countGdrop = 0
    else:
        if Gdrop == G:
            countGdrop = 0
        else:
            countGdrop = 1
    if not type(RR) == list:
        RR = [RR]
    if not type(RWetch) == list:
        RWetch = [RWetch]
    if not type(RWin) == list:
        RWin = [RWin]
    if not type(Lc) == list:
        if Lc == None:
            Lc = [None]
        else:
            Lc = [Lc]
    if not type(LcDrop) == list:
        if LcDrop == None:
            LcDrop = [None]
        else:
            LcDrop = [LcDrop]
    if not type(Amodulation_list) == list:
        Amodulation_list = [Amodulation_list]
    if not type(Sigmamodulation_list) == list:
        Sigmamodulation_list = [Sigmamodulation_list]

    N = (
        len(G)
        * len(Gdrop)
        * len(RR)
        * len(RWin)
        * len(Lc)
        * len(LcDrop)
        * len(Amodulation_list)
        * len(Sigmamodulation_list)
    )

    x = {}
    y = {}

    name_loop = []
    print("------------------------------------")
    θ = -np.linspace(-angle / 2 + np.pi / 2, angle / 2 + np.pi / 2, 1000)
    if signpad == -1:
        iix = N - 1
        iiy = 0
    else:
        iix = 0
        iiy = 0
    print(iix)
    for g in G:
        for gdrop in Gdrop:
            for rr in RR:
                for rwIn in RWin:
                    for rwetch in RWetch:
                        for lc in Lc:
                            for lcd in LcDrop:
                                for Amodulation in Amodulation_list:
                                    for Sigmamodulation in Sigmamodulation_list:

                                        # heater rings
                                        fid.write(str(layer) + " layer\n")
                                        x1 = (rr - rwIn / 2 + Wheater / 2) * np.cos(θ)
                                        y1 = (rr - rwIn / 2 + Wheater / 2) * np.sin(θ)
                                        x2 = (rr - rwIn / 2 - Wheater / 2) * np.cos(θ)
                                        y2 = (rr - rwIn / 2 - Wheater / 2) * np.sin(θ)
                                        x = np.concatenate([x1, x2[::-1]])
                                        y = np.concatenate([y1, y2[::-1]])
                                        fid.write(
                                            "<Htr_"
                                            + Name
                                            + str(ncell)
                                            + "_"
                                            + str(iix)
                                            + " struct>\n"
                                        )
                                        name_loop.append(
                                            "Htr_" + Name + str(ncell) + "_" + str(iix)
                                        )

                                        for xx, yy in zip(x, y):
                                            fid.write(
                                                f"{xx} {yy + iiy *y_shift - (rr + g+ W/2)} "
                                            )
                                        fid.write("points2shape\n")

                                        # pads
                                        fid.write(
                                            "<pads_"
                                            + Name
                                            + str(ncell)
                                            + "_"
                                            + str(iix)
                                            + " struct>\n"
                                        )
                                        name_loop.append(
                                            "pads_" + Name + str(ncell) + "_" + str(iix)
                                        )

                                        ytop = ytoppad

                                        for ilayr in [0, 1]:
                                            scale = 0.25
                                            fid.write(f"{layer+ilayr} layer\n")
                                            for isgn in [-1, 1]:
                                                xp = [
                                                    isgn
                                                    * (
                                                        Wpad
                                                        + ydecpad
                                                        + ilayr * scale * Wpad
                                                    ),
                                                    isgn
                                                    * (ydecpad - ilayr * Wpad * scale),
                                                    isgn
                                                    * (ydecpad - ilayr * Wpad * scale),
                                                    isgn
                                                    * (
                                                        Wpad
                                                        + ydecpad
                                                        + ilayr * scale * Wpad
                                                    ),
                                                ]
                                                yp = [
                                                    -Wpad / 2 + ytop - scale * Wpad,
                                                    -Wpad / 2 + ytop - scale * Wpad,
                                                    Wpad / 2 + ytop + scale * Wpad,
                                                    Wpad / 2 + ytop + scale * Wpad,
                                                ]
                                                for xx, yy in zip(xp, yp):
                                                    # fid.write(f'{xx} {yy + ii *y_shift - (rr + g+ W/2)} ')
                                                    fid.write(
                                                        f"{xx + isgn * iix * 2.5 * Wpad} {yy} "
                                                    )
                                                fid.write("points2shape\n")

                                        fid.write(f"{layer} layer\n")
                                        for isgn in [-1, 1]:
                                            xp = [
                                                isgn * (Wpad + ydecpad),
                                                isgn * ydecpad,
                                                isgn * ydecpad,
                                                isgn * (Wpad + ydecpad),
                                            ]
                                            yp = [
                                                -Wpad / 2 + ytop,
                                                -Wpad / 2 + ytop,
                                                Wpad / 2
                                                + iiy * y_shift
                                                - (rr + g + W / 2),
                                                Wpad / 2
                                                + iiy * y_shift
                                                - (rr + g + W / 2),
                                            ]
                                            for xx, yy in zip(xp, yp):
                                                # fid.write(f'{xx} {yy + ii *y_shift - (rr + g+ W/2)} ')
                                                fid.write(
                                                    f"{xx + isgn * iix * 2.5 * Wpad} {yy} "
                                                )
                                            fid.write("points2shape\n")

                                        for isgn in [-1, 1]:
                                            xp = [
                                                isgn * (Wpad + ydecpad) - isgn * Wpad,
                                                isgn * ydecpad
                                                + isgn * iix * 2.5 * Wpad
                                                + isgn * Wpad,
                                                isgn * ydecpad
                                                + isgn * iix * 2.5 * Wpad
                                                + isgn * Wpad,
                                                isgn * (Wpad + ydecpad) - isgn * Wpad,
                                            ]
                                            yp = [
                                                -Wpad / 2
                                                + iiy * y_shift
                                                - (rr + g + W / 2),
                                                -Wpad / 2
                                                + iiy * y_shift
                                                - (rr + g + W / 2),
                                                Wpad / 2
                                                + iiy * y_shift
                                                - (rr + g + W / 2),
                                                Wpad / 2
                                                + iiy * y_shift
                                                - (rr + g + W / 2),
                                            ]
                                            for xx, yy in zip(xp, yp):
                                                # fid.write(f'{xx} {yy + ii *y_shift - (rr + g+ W/2)} ')
                                                fid.write(f"{xx} {yy} ")
                                            fid.write("points2shape\n")

                                        # connectors
                                        fid.write(
                                            "<cnct_"
                                            + Name
                                            + str(ncell)
                                            + "_"
                                            + str(iix)
                                            + " struct>\n"
                                        )
                                        name_loop.append(
                                            "cnct_" + Name + str(ncell) + "_" + str(iix)
                                        )
                                        for isgn, ind in zip([-1, 1], [-1, 0]):
                                            if y1[ind] > y2[ind]:
                                                xtop = x1[ind]
                                                ytop = y1[ind]
                                                xbot = x2[ind]
                                                ybot = y2[ind]
                                            else:
                                                xbot = x1[ind]
                                                ybot = y1[ind]
                                                xtop = x2[ind]
                                                ytop = y2[ind]

                                            xc = [
                                                isgn * (ydecpad),
                                                xbot,
                                                xtop,
                                                isgn * ydecpad,
                                            ]
                                            yc = [-Wpad / 2, ybot, ytop, Wpad / 2]

                                            for xx, yy in zip(xc, yc):
                                                fid.write(
                                                    f"{xx} {yy + iiy *y_shift - (rr + g+ W/2)} "
                                                )
                                            fid.write("points2shape\n")

                                        iix += signpad
                                        iiy += 1

    fid.write("<" + Name + "htr" + str(ncell) + " struct>\n")
    for nme in name_loop:
        fid.write("\t<" + nme + " 0 0 0 1 0 instance>\n")

    fid.write("# ******************************\n")
    return [Name + "htr" + str(ncell)]


def LigentecHeater(fid, param, ncell, cnt_out):
    Name = param.get("name", None)
    x_pos = param.get("x_pos", 0)
    x_shift = param.get("x_shift", 0)
    y_shift = param.get("y_shift", 0)
    y_pos = param.get("y_pos", 0)
    Wopen = param.get("Wopen", 35)  # P1PAD
    Wpad = param.get("Wpad", Wopen + 10)  # P1R
    Wvia = param.get("Wvia", 0.36)
    WviaBlock = param.get("WviaBlock", 0.36 + 6)
    wmet_tap = 6
    pad_loc = param.get("pad_loc", "right")
    rw = param.get("rw", 1)
    rr = param.get("rr", 23)
    theta_heat_0deg = param.get("theta_heat_0deg", 60)
    theta_heat_deg = param.get("theta_heat_deg", None)
    rot = param.get("rot", None)
    do_half = False
    if rot is None:
        rot = 0
        do_half = True
    theta_heat_0 = theta_heat_0deg * np.pi / 180
    Lalone_0 = theta_heat_0 * 23
    if theta_heat_deg is None:
        theta_heat = Lalone_0 / rr  # + rot * np.pi / 180
        if do_half:
            rot = (-theta_heat / 2) * 180 / np.pi
            theta_heat += rot * np.pi / 180
        theta_heat_deg = 180 * theta_heat / (np.pi)

    else:

        theta_heat_deg += rot
        theta_heat = theta_heat_deg * np.pi / 180

    # -- above ring
    Wheat = rw + 2 * 0.300

    name_out = []
    name_out.append(Name + "p1p" + "Cell" + str(ncell) + "_" + str(cnt_out))
    fid.write(
        "<" + Name + "p1p" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
    )
    # === Heater P1p
    # ==============================
    fid.write(str(30) + " layer\n")
    fid.write(str(0) + " dataType\n")
    fid.write(
        f"{x_pos:.3f} {y_pos:.3f} "
        + f"{rr-0.300} {rr+rw+0.300} "
        + f"{theta_heat_deg} {360 +rot} "
        + f"{300} torus\n"
    )
    ## --------------
    ## ---- TOP -----
    ## --------------
    name_out.append(Name + "p1pr" + "Cell" + str(ncell) + "_" + str(cnt_out))
    fid.write(
        "<" + Name + "p1pr" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
    )
    # === Metal around via P1P
    # ==============================
    for sign, th in zip([+1, -1], [theta_heat, rot * np.pi / 180]):
        rot_sign = np.sign(rot)
        if rot_sign == 0:
            rot_sign = -1
        for ll in [30, 32]:
            fid.write(str(ll) + " layer\n")
            fid.write(str(0) + " dataType\n")
            rmet1 = rr + rw / 2 + WviaBlock / 2
            rmet0 = rr + rw / 2 - WviaBlock / 2

            x1_p1p = x_pos + rmet1 * np.cos(th)
            y1_p1p = y_pos - rot_sign * rmet1 * np.sin(th)
            x2_p1p = x_pos + np.sqrt(rmet1**2 + WviaBlock**2) * np.cos(
                th - sign * np.arctan(WviaBlock / rmet1)
            )
            y2_p1p = y_pos - rot_sign * np.sqrt(rmet1**2 + WviaBlock**2) * np.sin(
                th - sign * np.arctan(WviaBlock / rmet1)
            )
            x3_p1p = x_pos + np.sqrt(rmet0**2 + WviaBlock**2) * np.cos(
                th - sign * np.arctan(WviaBlock / rmet0)
            )
            y3_p1p = y_pos - rot_sign * np.sqrt(rmet0**2 + WviaBlock**2) * np.sin(
                th - sign * np.arctan(WviaBlock / rmet0)
            )
            x4_p1p = x_pos + rmet0 * np.cos(th)
            y4_p1p = y_pos - rot_sign * rmet0 * np.sin(th)
            fid.write(
                f"{x1_p1p:.3f} {y1_p1p:.3f} "
                + f"{x2_p1p:.3f} {y2_p1p:.3f} "
                + f"{x3_p1p:.3f} {y3_p1p:.3f} "
                + f"{x4_p1p:.3f} {y4_p1p:.3f} "
                + f"points2shape\n"
            )

            fid.write(str(31) + " layer\n")
            fid.write(str(0) + " dataType\n")
            # -- top
            via_shift = WviaBlock / 2 - Wvia / 2
            r_rwc = rr + rw / 2
            rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + via_shift**2)
            th1 = th - sign * np.arctan(via_shift / (r_rwc + Wvia / 2))
            x1 = x_pos + rmet1 * np.cos(th1)
            y1 = y_pos + rmet1 * np.sin(th1)

            rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + (via_shift + Wvia) ** 2)
            th1 = th - sign * np.arctan((via_shift + Wvia) / (r_rwc + Wvia / 2))
            x2 = x_pos + rmet1 * np.cos(th1)
            y2 = y_pos + rmet1 * np.sin(th1)

            rmet1 = np.sqrt((r_rwc - Wvia / 2) ** 2 + (via_shift + Wvia) ** 2)
            th1 = th - sign * np.arctan((via_shift + Wvia) / (r_rwc - Wvia / 2))
            x3 = x_pos + rmet1 * np.cos(th1)
            y3 = y_pos + rmet1 * np.sin(th1)

            rmet1 = np.sqrt((r_rwc - Wvia / 2) ** 2 + (via_shift) ** 2)
            th1 = th - sign * np.arctan((via_shift) / (r_rwc - Wvia / 2))
            x4 = x_pos + rmet1 * np.cos(th1)
            y4 = y_pos + rmet1 * np.sin(th1)
            fid.write(
                f"{x1:.3f} {y1:.3f} "
                + f"{x2:.3f} {y2:.3f} "
                + f"{x3:.3f} {y3:.3f} "
                + f"{x4:.3f} {y4:.3f} "
                + f"points2shape\n"
            )

        if pad_loc == "right":
            fid.write(str(33) + " layer\n")
            fid.write(str(0) + " dataType\n")
            rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + via_shift**2)
            th1 = theta_heat - np.arctan(via_shift / (r_rwc + Wvia / 2))
            y_pad = y_pos + sign * (Wpad / 2 + 35)
            r_met_diff = rr + rw + 10
            theta_corner = np.arccos((y_pad - y_pos - sign * (Wpad / 2)) / r_met_diff)
            if ~np.isnan(theta_corner):
                y_pad = y_pos + sign * (Wpad / 2 + 35)
                x_pad = x_pos + r_met_diff * np.sin(theta_corner) + Wpad / 2

                if x_pad < x_pos + rr + rw + 12.5:
                    x_pad = x_pos + rr + rw + 12.5
            else:
                x_pad = x_pos + rr + rw + 12.5
            fid.write(
                f"{x_pad +  - Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
                + f"{x_pad - Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
                + f"{x_pad + Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
                + f"{x_pad + Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
                + "points2shape\n"
            )
            fid.write(str(32) + " layer\n")
            fid.write(str(0) + " dataType\n")

            fid.write(
                f"{x_pad  - Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
                + f"{x_pad - Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
                + f"{x_pad + Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
                + f"{x_pad + Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
                + "points2shape\n"
            )

            pad_dist = x_pad - x2_p1p
            Wmet_rout = np.abs(y2_p1p - y1_p1p)

            fid.write(
                f"{x_pad + Wpad/2:.3f} {y_pad - sign * Wpad/2:.3f} "
                + f"{x_pad + Wmet_rout/2:.3f} {y1_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y1_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wpad/2:.3f} {y_pad - sign* Wpad/2:.3f} "
                + "points2shape\n"
            )

            fid.write(
                f"{x_pad + Wmet_rout/2:.3f} {y1_p1p + sign*Wmet_rout/2:.3f} "
                + f"{x_pad + Wmet_rout/2:.3f} {y1_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y1_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y1_p1p + sign*Wmet_rout/2:.3f} "
                + "points2shape\n"
            )

            fid.write(
                f"{x_pad - Wmet_rout:.3f} {y2_p1p:.3f} "
                + f"{x_pad + Wmet_rout/2:.3f} {y1_p1p + sign*Wmet_rout/2:.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y1_p1p + sign*Wmet_rout/2:.3f} "
                + f"{x_pad - Wmet_rout:.3f} {y1_p1p:.3f} "
                + "points2shape\n"
            )

            fid.write(
                f"{x2_p1p:.3f} {y2_p1p:.3f} "
                + f"{x_pad - Wmet_rout:.3f} {y2_p1p:.3f} "
                + f"{x_pad - Wmet_rout:.3f} {y1_p1p:.3f} "
                + f"{x1_p1p:.3f} {y1_p1p:.3f} "
                + "points2shape\n"
            )

        if pad_loc == "left":
            fid.write(str(33) + " layer\n")
            fid.write(str(0) + " dataType\n")
            rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + via_shift**2)
            th1 = theta_heat - np.arctan(via_shift / (r_rwc + Wvia / 2))
            y_pad = y_pos + sign * (Wpad / 2 + 35)
            r_met_diff = rr - 20
            theta_corner = np.arccos((y_pad - y_pos + sign * (Wpad / 2)) / r_met_diff)
            if ~np.isnan(theta_corner):

                y_pad = y_pos + sign * (Wpad / 2 + 35)
                x_pad = x_pos + r_met_diff * np.sin(theta_corner) - Wpad / 2

                if x_pad + Wpad / 2 > x_pos + rr - 20:
                    print(x_pad)
                    x_pad = x_pos + rr - 15 - Wpad / 2
            else:
                x_pad = x_pos + rr - 12.5
            fid.write(
                f"{x_pad +  - Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
                + f"{x_pad - Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
                + f"{x_pad + Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
                + f"{x_pad + Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
                + "points2shape\n"
            )
            fid.write(str(32) + " layer\n")
            fid.write(str(0) + " dataType\n")

            fid.write(
                f"{x_pad  - Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
                + f"{x_pad - Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
                + f"{x_pad + Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
                + f"{x_pad + Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
                + "points2shape\n"
            )

            pad_dist = -(x_pad - x3_p1p)
            Wmet_rout = np.abs(y3_p1p - y4_p1p)

            fid.write(
                f"{x_pad + Wpad/2:.3f} {y_pad - sign * Wpad/2:.3f} "
                + f"{x_pad + Wmet_rout/2:.3f} {y4_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y4_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wpad/2:.3f} {y_pad - sign* Wpad/2:.3f} "
                + "points2shape\n"
            )

            fid.write(
                f"{x_pad + Wmet_rout/2:.3f} {y4_p1p + sign*Wmet_rout/2:.3f} "
                + f"{x_pad + Wmet_rout/2:.3f} {y4_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y4_p1p + sign*(Wmet_rout/2 + 5):.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y4_p1p + sign*Wmet_rout/2:.3f} "
                + "points2shape\n"
            )

            fid.write(
                f"{x_pad + Wmet_rout:.3f} {y3_p1p:.3f} "
                + f"{x_pad - Wmet_rout/2:.3f} {y4_p1p + sign*Wmet_rout/2:.3f} "
                + f"{x_pad + Wmet_rout/2:.3f} {y4_p1p + sign*Wmet_rout/2:.3f} "
                + f"{x_pad + Wmet_rout:.3f} {y4_p1p:.3f} "
                + "points2shape\n"
            )

            fid.write(
                f"{x3_p1p:.3f} {y3_p1p:.3f} "
                + f"{x_pad + Wmet_rout:.3f} {y3_p1p:.3f} "
                + f"{x_pad + Wmet_rout:.3f} {y4_p1p:.3f} "
                + f"{x4_p1p:.3f} {y4_p1p:.3f} "
                + "points2shape\n"
            )

        elif pad_loc == "top":
            # for sign, th in zip([+1, -1], [theta_heat, rot * np.pi / 180]):
            fid.write(str(33) + " layer\n")
            fid.write(str(0) + " dataType\n")
            rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + via_shift**2)
            th1 = theta_heat - np.arctan(via_shift / (r_rwc + Wvia / 2))
            x_pad = x_pos  # + rr + rw + 1 + Wpad / 2
            y_pad = y_pos + sign * (rr + Wpad / 2 + 15)  # + rw + rmet1 * np.sin(th1)
            fid.write(
                f"{x_pad +  - Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
                + f"{x_pad - Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
                + f"{x_pad + Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
                + f"{x_pad + Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
                + "points2shape\n"
            )
            fid.write(str(32) + " layer\n")
            fid.write(str(0) + " dataType\n")
            fid.write(
                f"{x_pad  - Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
                + f"{x_pad - Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
                + f"{x_pad + Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
                + f"{x_pad + Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
                + "points2shape\n"
            )

            xtap = (x_pad - rot_sign * Wpad / 2 + x4_p1p) / 2
            Wmet_route = np.abs(x1_p1p - x2_p1p)
            ymet_shift = y_pad - sign * 3 * wmet_tap / 4

            if rot_sign == 1:
                fid.write(
                    f"{x_pad  - Wpad/2:.3f} {y_pad - sign * Wpad/2:.3f} "
                    + f"{x2_p1p:.3f} {y1_p1p + sign*3:.3f} "
                    + f"{x1_p1p:.3f} {y1_p1p+ sign*3:.3f} "
                    + f"{x_pad  + Wpad/2:.3f} {y_pad - sign * Wpad/2:.3f} "
                    + "points2shape\n"
                )
            else:
                fid.write(
                    f"{x_pad  - Wpad/2:.3f} {y_pad - sign * Wpad/2:.3f} "
                    + f"{x1_p1p:.3f} {y1_p1p + sign*3:.3f} "
                    + f"{x2_p1p:.3f} {y1_p1p+ sign*3:.3f} "
                    + f"{x_pad  + Wpad/2:.3f} {y_pad - sign * Wpad/2:.3f} "
                    + "points2shape\n"
                )

            fid.write(
                f"{x1_p1p:.3f} {y1_p1p + sign*3:.3f} "
                + f"{x1_p1p:.3f} {y1_p1p:.3f} "
                + f"{x2_p1p:.3f} {y2_p1p:.3f} "
                + f"{x2_p1p:.3f} {y1_p1p+ sign* 3:.3f} "
                + "points2shape\n"
            )

    # # === PADS opening P1PAD
    # # ==============================
    # fid.write(str(33) + " layer\n")
    # fid.write(str(0) + " dataType\n")
    # rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + via_shift**2)
    # th1 = theta_heat - np.arctan(via_shift / (r_rwc + Wvia / 2))
    # x_pad = x_pos + rr + rw + 1 + Wpad / 2
    # y_pad = y_pos + 35 + rw + rmet1 * np.sin(th1)
    # fid.write(
    #     f"{x_pad +  - Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
    #     + f"{x_pad - Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
    #     + f"{x_pad + Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
    #     + f"{x_pad + Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
    #     + "points2shape\n"
    # )
    # # === Connection P1R
    # # ==============================
    # # <x1 y1 cx1 cy1 cx2 cy2 x2 y2 W θ(x1 ,y1 ) bezierCurve>
    # fid.write(str(32) + " layer\n")
    # fid.write(str(0) + " dataType\n")
    # fid.write(
    #     f"{x_pad + Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
    #     + f"{x_pad + Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
    #     + f"{x_pad - Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
    #     + f"{x_pad - Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
    #     + "points2shape\n"
    # )
    # met_dist = np.abs(y4 - (y_pad - Wpad / 2))
    # ymet1 = y_pad - Wpad / 2
    # ymet2 = ymet1 - 3 * met_dist / 8
    # ymet3 = ymet1 - 6 * met_dist / 8
    # ymet4 = ymet1 - met_dist
    # wmet_tap = 3
    # fid.write(
    #     f"{x_pad + Wpad/2:.3f} {ymet1:.3f} "
    #     + f"{x_pad + wmet_tap/2:.3f} {ymet2:.3f} "
    #     + f"{x_pad - wmet_tap/2:.3f} {ymet2:.3f} "
    #     + f"{x_pad - Wpad/2:.3f} {ymet1:.3f} "
    #     + "points2shape\n"
    # )

    # fid.write(
    #     f"{x_pad + wmet_tap/2:.3f} {ymet2:.3f} "
    #     + f"{x_pad + wmet_tap/2:.3f} {ymet3:.3f} "
    #     + f"{x_pad - wmet_tap/2:.3f} {ymet3:.3f} "
    #     f"{x_pad - wmet_tap/2:.3f} {ymet2:.3f} " + "points2shape\n"
    # )

    # xmet3 = x_pad - 3 * met_dist / 8 * np.cos(np.pi / 4)
    # fid.write(
    #     f"{x_pad + wmet_tap/2:.3f} {ymet3:.3f} "
    #     + f"{xmet3:.3f} {ymet4 - wmet_tap/2:.3f} "
    #     + f"{xmet3:.3f} {ymet4 + wmet_tap/2:.3f} "
    #     + f"{x_pad - wmet_tap/2:.3f} {ymet3:.3f} "
    #     + "points2shape\n"
    # )
    # x_end = (x_pad - Wpad / 2 + x2_p1p) / 2
    # if y2_p1p > ymet4 - wmet_tap / 2:
    #     fid.write(
    #         f"{xmet3:.3f} {ymet4 + wmet_tap/2:.3f} "
    #         + f"{x_end:.3f} {ymet4 + wmet_tap/2:.3f} "
    #         + f"{x1_p1p:.3f} {y1_p1p:.3f} "
    #         + f"{x2_p1p:.3f} {y2_p1p:.3f} "
    #         + f"{x3_p1p:.3f} {y3_p1p:.3f} "
    #         + f"{x_end:.3f} {ymet4 - wmet_tap/2:.3f} "
    #         + f"{xmet3:.3f} {ymet4 - wmet_tap/2:.3f} "
    #         + "points2shape\n"
    #     )
    # else:
    #     fid.write(
    #         f"{xmet3:.3f} {ymet4 + wmet_tap/2:.3f} "
    #         + f"{x_end:.3f} {ymet4 + wmet_tap/2:.3f} "
    #         + f"{x1_p1p:.3f} {y1_p1p:.3f} "
    #         + f"{x2_p1p:.3f} {y2_p1p:.3f} "
    #         + f"{x_end:.3f} {ymet4 - wmet_tap/2:.3f} "
    #         + f"{xmet3:.3f} {ymet4 - wmet_tap/2:.3f} "
    #         + "points2shape\n"
    #     )

    ## -----------------
    ## ---- BOTTOM -----
    ## -----------------
    # # === Metal around via P1P
    # # ==============================
    # for ll in [30, 32]:
    #     fid.write(str(ll) + " layer\n")
    #     fid.write(str(0) + " dataType\n")
    #     theta_heat_bot = rot * np.pi / 180
    #     rmet1 = rr + rw / 2 + WviaBlock / 2
    #     rmet0 = rr + rw / 2 - WviaBlock / 2
    #     x1_p1p = x_pos + rmet1 * np.cos(theta_heat_bot)
    #     y1_p1p = y_pos + rmet1 * np.sin(theta_heat_bot)
    #     x2_p1p = x_pos + np.sqrt(rmet1**2 + WviaBlock**2) * np.cos(
    #         theta_heat_bot + np.arctan(WviaBlock / rmet1)
    #     )
    #     y2_p1p = y_pos + np.sqrt(rmet1**2 + WviaBlock**2) * np.sin(
    #         theta_heat_bot + np.arctan(WviaBlock / rmet1)
    #     )
    #     x3_p1p = x_pos + np.sqrt(rmet0**2 + WviaBlock**2) * np.cos(
    #         theta_heat_bot + np.arctan(WviaBlock / rmet0)
    #     )
    #     y3_p1p = y_pos + np.sqrt(rmet0**2 + WviaBlock**2) * np.sin(
    #         theta_heat_bot + np.arctan(WviaBlock / rmet0)
    #     )
    #     x4_p1p = x_pos + rmet0 * np.cos(theta_heat_bot)
    #     y4_p1p = y_pos + rmet0 * np.sin(theta_heat_bot)
    #     fid.write(
    #         f"{x1_p1p:.3f} {y1_p1p:.3f} "
    #         + f"{x2_p1p:.3f} {y2_p1p:.3f} "
    #         + f"{x3_p1p:.3f} {y3_p1p:.3f} "
    #         + f"{x4_p1p:.3f} {y4_p1p:.3f} "
    #         + f"points2shape\n"
    #     )

    # # === Via opening P1VIA
    # # ==============================
    # fid.write(str(31) + " layer\n")
    # fid.write(str(0) + " dataType\n")
    # # -- top
    # via_shift = WviaBlock / 2 - Wvia / 2
    # r_rwc = rr + rw / 2
    # rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + via_shift**2)
    # th1 = theta_heat_bot + np.arctan(via_shift / (r_rwc + Wvia / 2))
    # x1 = x_pos + rmet1 * np.cos(th1)
    # y1 = y_pos + rmet1 * np.sin(th1)

    # rmet1 = np.sqrt((r_rwc + Wvia / 2) ** 2 + (via_shift + Wvia) ** 2)
    # th1 = theta_heat_bot + np.arctan((via_shift + Wvia) / (r_rwc + Wvia / 2))
    # x2 = x_pos + rmet1 * np.cos(th1)
    # y2 = y_pos + rmet1 * np.sin(th1)

    # rmet1 = np.sqrt((r_rwc - Wvia / 2) ** 2 + (via_shift + Wvia) ** 2)
    # th1 = theta_heat_bot + np.arctan((via_shift + Wvia) / (r_rwc - Wvia / 2))
    # x3 = x_pos + rmet1 * np.cos(th1)
    # y3 = y_pos + rmet1 * np.sin(th1)

    # rmet1 = np.sqrt((r_rwc - Wvia / 2) ** 2 + (via_shift) ** 2)
    # th1 = theta_heat_bot + np.arctan((via_shift) / (r_rwc - Wvia / 2))
    # x4 = x_pos + rmet1 * np.cos(th1)
    # y4 = y_pos + rmet1 * np.sin(th1)
    # fid.write(
    #     f"{x1:.3f} {y1:.3f} "
    #     + f"{x2:.3f} {y2:.3f} "
    #     + f"{x3:.3f} {y3:.3f} "
    #     + f"{x4:.3f} {y4:.3f} "
    #     + f"points2shape\n"
    # )

    # # === PADS opening P1PAD
    # # ==============================
    # fid.write(str(33) + " layer\n")
    # fid.write(str(0) + " dataType\n")
    # x_pad = x_pos + rr + rw + 1 + Wpad / 2
    # y_pad = y_pos - 35 - rw
    # fid.write(
    #     f"{x_pad +  - Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
    #     + f"{x_pad - Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
    #     + f"{x_pad + Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
    #     + f"{x_pad + Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
    #     + "points2shape\n"
    # )

    # # === Connection P1R
    # # ==============================
    # # <x1 y1 cx1 cy1 cx2 cy2 x2 y2 W θ(x1 ,y1 ) bezierCurve>
    # fid.write(str(32) + " layer\n")
    # fid.write(str(0) + " dataType\n")
    # fid.write(
    #     f"{x_pad + Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
    #     + f"{x_pad + Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
    #     + f"{x_pad - Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
    #     + f"{x_pad - Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
    #     + "points2shape\n"
    # )
    # met_dist = (y_pos + WviaBlock / 2) - (y_pad + Wpad / 2)
    # ymet1 = y_pad + Wpad / 2
    # ymet2 = ymet1 + 3 * met_dist / 8
    # ymet3 = ymet1 + 6 * met_dist / 8
    # ymet4 = ymet1 + met_dist
    # wmet_tap = 3
    # fid.write(
    #     f"{x_pad + Wpad/2:.3f} {ymet1:.3f} "
    #     + f"{x_pad + wmet_tap/2:.3f} {ymet2:.3f} "
    #     + f"{x_pad - wmet_tap/2:.3f} {ymet2:.3f} "
    #     + f"{x_pad - Wpad/2:.3f} {ymet1:.3f} "
    #     + "points2shape\n"
    # )

    # fid.write(
    #     f"{x_pad + wmet_tap/2:.3f} {ymet2:.3f} "
    #     + f"{x_pad + wmet_tap/2:.3f} {ymet3:.3f} "
    #     + f"{x_pad - wmet_tap/2:.3f} {ymet3:.3f} "
    #     f"{x_pad - wmet_tap/2:.3f} {ymet2:.3f} " + "points2shape\n"
    # )

    # xmet3 = x_pad - 3 * met_dist / 8 * np.cos(np.pi / 4)
    # fid.write(
    #     f"{x_pad + wmet_tap/2:.3f} {ymet3:.3f} "
    #     + f"{xmet3:.3f} {ymet4 + wmet_tap/2:.3f} "
    #     + f"{xmet3:.3f} {ymet4 - wmet_tap/2:.3f} "
    #     + f"{x_pad - wmet_tap/2:.3f} {ymet3:.3f} "
    #     + "points2shape\n"
    # )

    # fid.write(
    #     f"{xmet3:.3f} {ymet4 + wmet_tap/2:.3f} "
    #     + f"{x_pos + rr+rw/2 + WviaBlock:.3f} {ymet4 + wmet_tap/2:.3f} "
    #     + f"{x_pos + rr+rw/2 + WviaBlock/2:.3f} {ymet4 +WviaBlock/2:.3f} "
    #     + f"{x_pos + rr+rw/2 + WviaBlock/2:.3f} {ymet4  -WviaBlock/2:.3f} "
    #     + f"{x_pos + rr+rw/2 + WviaBlock:.3f} {ymet4 - wmet_tap/2:.3f} "
    #     + f"{xmet3:.3f} {ymet4 - wmet_tap/2:.3f} "
    #     + "points2shape\n"
    # )

    # -- Wrap up the cell
    fid.write("\n")
    fid.write("<" + Name + "_Heater" + str(ncell) + "_" + str(cnt_out) + " struct>\n")
    for n in name_out:
        fid.write("\t<" + n + " 0 0 0 1 0 instance>\n")

    return [Name + "_Heater" + str(ncell) + "_" + str(cnt_out)]


def LigentecHeaterRaceTrack(fid, param, ncell, cnt_out):
    Name = param.get("name", None)
    x_pos = param.get("x_pos", 0)
    x_shift = param.get("x_shift", 0)
    y_shift = param.get("y_shift", 0)
    y_pos = param.get("y_pos", 0)
    xyP1p = param.get("xyP1p", None)  # P1p
    Wopen = param.get("Wopen", 20)  # P1PAD
    Wpad = param.get("Wpad", Wopen + 10)  # P1R
    Wvia = param.get("Wvia", 0.32)
    WviaBlock = param.get("WviaBlock", 0.32 + 6)

    # === Heater P1p
    # ==============================
    name_out = []
    name_out.append(Name + "p1p" + "Cell" + str(ncell) + "_" + str(cnt_out))
    fid.write(
        "<" + Name + "p1p" + "Cell" + str(ncell) + "_" + str(cnt_out) + " struct>\n"
    )
    fid.write(str(30) + " layer\n")
    fid.write(str(0) + " dataType\n")
    for x, y in xyP1p:
        fid.write(f"{x+x_pos:.6f} {y+y_pos:.6f} ")
    fid.write(f"points2shape\n")

    ## --------------
    ## ---- Left -----
    ## --------------
    for ii in [1, -1]:
        # === Metal around via P1P
        # ==============================

        if ii == 1:
            ind0 = 0
        else:
            ind0 = -1
        xp1p, yp1p = xyP1p.T
        xvia = x_pos + ii * (xp1p[ind0] + WviaBlock / 2)
        y0 = y_pos + (yp1p[0] + yp1p[-1]) / 2
        for ll in [30, 32]:
            fid.write(str(ll) + " layer\n")
            fid.write(str(0) + " dataType\n")
            fid.write(
                f"{xvia - WviaBlock/2:.3f} {y0 -WviaBlock/2 :.3f} "
                + f"{xvia - WviaBlock/2:.3f} {y0 +WviaBlock/2 :.3f} "
                + f"{xvia + WviaBlock/2:.3f} {y0 +WviaBlock/2 :.3f} "
                + f"{xvia + WviaBlock/2:.3f} {y0 -WviaBlock/2 :.3f} "
                + f"points2shape\n"
            )

        # === Via opening P1VIA
        # ==============================
        fid.write(str(31) + " layer\n")
        fid.write(str(0) + " dataType\n")
        fid.write(
            f"{xvia - Wvia/2:.3f} {y0 -Wvia/2 :.3f} "
            + f"{xvia - Wvia/2:.3f} {y0 +Wvia/2 :.3f} "
            + f"{xvia + Wvia/2:.3f} {y0 +Wvia/2 :.3f} "
            + f"{xvia + Wvia/2:.3f} {y0 -Wvia/2 :.3f} "
            + f"points2shape\n"
        )

        # === PADS opening P1PAD
        # ==============================
        fid.write(str(33) + " layer\n")
        fid.write(str(0) + " dataType\n")
        xpad = xvia - ii * 45
        y_pad = y0 + Wpad / 2 + 15
        fid.write(
            f"{xpad - Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
            + f"{xpad - Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
            + f"{xpad + Wopen/2:.3f} {y_pad + Wopen/2:.3f} "
            + f"{xpad + Wopen/2:.3f} {y_pad - Wopen/2:.3f} "
            + "points2shape\n"
        )
        # === Connection P1R
        # ==============================
        fid.write(str(32) + " layer\n")
        fid.write(str(0) + " dataType\n")
        fid.write(
            f"{xpad + Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
            + f"{xpad + Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
            + f"{xpad - Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
            + f"{xpad - Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
            + "points2shape\n"
        )
        wmet_tap = 3
        xtapmet = (xpad + ii * Wpad / 2) + (xvia - (xpad + ii * Wpad / 2)) / 2
        fid.write(
            f"{xpad + ii*Wpad/2:.3f} {y_pad - Wpad/2:.3f} "
            + f"{xtapmet:.3f} {y_pad - wmet_tap/2:.3f} "
            + f"{xtapmet:.3f} {y_pad + wmet_tap/2:.3f} "
            + f"{xpad + ii*Wpad/2:.3f} {y_pad + Wpad/2:.3f} "
            + "points2shape\n"
        )
        xangle = xvia - ii * 5
        fid.write(
            f"{xtapmet:.3f} {y_pad - wmet_tap/2:.3f} "
            f"{xangle:.3f} {y_pad - wmet_tap/2:.3f} "
            f"{xangle:.3f} {y_pad + wmet_tap/2:.3f} "
            + f"{xtapmet:.3f} {y_pad + wmet_tap/2:.3f} "
            + "points2shape\n"
        )
        fid.write(
            f"{xangle:.3f} {y_pad - wmet_tap/2:.3f} "
            + f"{xvia-ii*wmet_tap/2:.3f} {y_pad - 5:.3f} "
            + f"{xvia+ii*wmet_tap/2:.3f} {y_pad - 5:.3f} "
            + f"{xangle:.3f} {y_pad + wmet_tap/2:.3f} "
            + "points2shape\n"
        )
        fid.write(
            f"{xvia-wmet_tap/2:.3f} {y_pad - 5:.3f} "
            + f"{xvia-wmet_tap/2:.3f} {y0 +WviaBlock/2 + 3:.3f} "
            + f"{xvia+wmet_tap/2:.3f} {y0 +WviaBlock/2 + 3:.3f} "
            + f"{xvia+wmet_tap/2:.3f} {y_pad - 5:.3f} "
            + "points2shape\n"
        )
        fid.write(
            f"{xvia-wmet_tap/2:.3f} {y0 +WviaBlock/2 + 3:.3f} "
            + f"{xvia - WviaBlock/2:.3f} {y0 +WviaBlock/2 :.3f} "
            + f"{xvia + WviaBlock/2:.3f} {y0 +WviaBlock/2 :.3f} "
            + f"{xvia+wmet_tap/2:.3f} {y0 +WviaBlock/2 + 3:.3f} "
            + "points2shape\n"
        )

    fid.write("\n")
    fid.write("<" + Name + "_Heater" + str(ncell) + "_" + str(cnt_out) + " struct>\n")
    for n in name_out:
        fid.write("\t<" + n + " 0 0 0 1 0 instance>\n")

    return [Name + "_Heater" + str(ncell) + "_" + str(cnt_out)]
