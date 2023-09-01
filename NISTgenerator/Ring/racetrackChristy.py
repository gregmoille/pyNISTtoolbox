from copy import copy
from pickle import FALSE

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as itg
from scipy import constants as cts
from scipy.interpolate import UnivariateSpline
from scipy.special import fresnel
from shapely.geometry import Polygon


def getEuler(R0=10, num_points=10000, theta=np.pi / 2):
    # compute the path length
    Radjust = 2 * R0  # adjust the scaling due to the fresnel definition in scipy
    L = Radjust * theta  # HALF of total length
    s = np.linspace(0, L, num_points)
    f = np.sqrt(np.pi * Radjust * L / 2) + 1e-18
    y, x = fresnel(s / f)
    y, x = f * y, f * x
    return x, y, s


def getCircle(R0=20, num_points=10000):
    angle = np.linspace(3 * np.pi / 2, 2 * np.pi, int(num_points / 2))
    x2 = R0 * np.cos(angle) + R0
    y2 = R0 * np.sin(angle)
    return x2, y2


def getBezier(
    R0=20,
    p0=np.array([0, 0]),
    p1=np.array([45, 0]),
    p2=np.array([50, 16]),
    p3=np.array([50, 25]),
    num_points=10000,
):
    p0 = p0 * R0 / 20
    p1 = p1 * R0 / 20
    p2 = p2 * R0 / 20
    p3 = p3 * R0 / 20
    ts = np.linspace(0, 1, num_points)
    bx = np.zeros(ts.size)
    by = np.zeros(ts.size)
    for i in range(ts.size):
        bx[i] = (
            ((1 - ts[i]) ** 3) * p0[0]
            + 3 * ((1 - ts[i]) ** 2) * ts[i] * p1[0]
            + 3 * (1 - ts[i]) * (ts[i] ** 2) * p2[0]
            + (ts[i] ** 3) * p3[0]
        )
        by[i] = (
            ((1 - ts[i]) ** 3) * p0[1]
            + 3 * ((1 - ts[i]) ** 2) * ts[i] * p1[1]
            + 3 * (1 - ts[i]) * (ts[i] ** 2) * p2[1]
            + (ts[i] ** 3) * p3[1]
        )
    return bx, by


def getPathLength(x, y):
    prevx = x[0]
    prevy = y[0]
    length = 0
    for xx, yy in zip(x[1::], y[1::]):
        Δx = xx - prevx
        Δy = yy - prevy
        Δs = np.sqrt(Δx**2 + Δy**2)
        length += Δs

        prevx, prevy = xx, yy
    return length


def slicePath(x, y, steps):
    L = getPathLength(x, y)
    ind = [0]
    prevx = x[0]
    prevy = y[0]
    length = 0
    length_portion = []
    for ii, (xx, yy) in enumerate(zip(x[1::], y[1::])):
        Δx = xx - prevx
        Δy = yy - prevy
        Δs = np.sqrt(Δx**2 + Δy**2)
        length += Δs
        prevx, prevy = xx, yy
        if length >= L / steps:
            length_portion += [length]
            length = 0
            ind += [ii]
    length_portion = np.array(length_portion)
    Δs = np.mean(length_portion)
    return ind, Δs


def normalizeVec(x, y):
    distance = np.sqrt(x * x + y * y)
    return x / distance, y / distance


def makeOffsetPoly(oldX, oldY, offset, outer_ccw=1):
    Npts = oldX.size
    newX = np.zeros(Npts)
    newY = np.zeros(Npts)
    if not type(offset) == np.array:
        offset = np.ones(Npts) * offset
    for ii, (xx, yy) in enumerate(zip(oldX, oldY)):
        prev = (ii + Npts - 1) % Npts
        next = (ii + 1) % Npts

        vnX = oldX[next] - xx
        vnY = oldY[next] - yy
        vnnX, vnnY = normalizeVec(vnX, vnY)
        nnnX = vnnY
        nnnY = -vnnX

        vpX = xx - oldX[prev]
        vpY = yy - oldY[prev]
        vpnX, vpnY = normalizeVec(vpX, vpY)
        npnX = vpnY * outer_ccw
        npnY = -vpnX * outer_ccw

        bisX = (nnnX + npnX) * outer_ccw
        bisY = (nnnY + npnY) * outer_ccw

        bisnX, bisnY = normalizeVec(bisX, bisY)
        bislen = offset[ii] / np.sqrt((1 + nnnX * npnX + nnnY * npnY) / 2)

        newX[ii] = xx + bislen * bisnX
        newY[ii] = yy + bislen * bisnY

    return newX, newY


def getPoints(length, width, func, **kwargs):
    RW = kwargs.get("RW", 1.4)
    R0 = kwargs.get("R0", 20)
    pts = kwargs.get("num_points", 100000)
    tap = kwargs.get("tapering", False)
    Wmet = kwargs.get("Wmet", 2)

    # steps = int(pt0)

    if func == "Euler":
        x, y, s = getEuler(R0=R0, num_points=pts)
        y = y - y[-1]
    elif func == "Partial Euler":
        pass
        y = y - y[-1]
    elif func == "Half circle":
        x, y = getCircle(R0=R0, num_points=pts)
    elif func == "Bezier":
        x, y = getBezier(R0=R0, num_points=pts)  # only coded for R0 = 20
        y = y - y[-1]
    elif func == "Optimal":
        pass

    scale = width / 2 / (-y[0])  # scale width of racetrack to fit in boxx
    x = scale * x
    y = scale * y

    if tap:
        if func == "Optimal":
            pass
        else:
            ind, Δs = slicePath(x, y, x.size)
            dydx = np.gradient(y) / np.gradient(x)
            d2ydx2 = np.gradient(dydx) / np.gradient(x)
            R = ((1 + dydx**2) ** (3 / 2)) / (d2ydx2)
            ind_avg = np.vstack([ind[:-1], ind[1::]]).T
            Ravg = np.array([R[ii[0] : ii[-1] + 1].mean() for ii in ind_avg])

            xfit = np.arange(Ravg.size)
            tofit = np.poly1d(np.polyfit(xfit, 1 / Ravg, 6))
            Ravg = 1 / tofit(xfit)
            RW_v = -RW * np.ones(Ravg.size)
            newRW = Ravg * (1 - np.exp(RW_v / Ravg))
            newRW = np.concatenate([[RW], newRW])
    else:
        newRW = RW * np.ones(x.size)

    # -- Connect path --
    x = x - x.min()
    Lcurve = 4 * getPathLength(x, y)

    straight = (length - Lcurve) / 2
    x = np.concatenate(
        [
            x + straight / 2,
            np.flip(x) + straight / 2,
            -x - straight / 2,
            np.flip(-x) - straight / 2,
            [x[0] + straight / 2],
        ]
    )
    y = np.concatenate([y, np.flip(-y), -y, np.flip(y), [y[0]]])
    newRW = np.concatenate([newRW, np.flip(newRW), newRW, np.flip(newRW), [RW]])

    xin, yin = makeOffsetPoly(x, y, -newRW / 2)
    xout, yout = makeOffsetPoly(x, y, newRW / 2)
    ind = np.unique(
        np.concatenate([np.where(~np.isnan(xin)), np.where(~np.isnan(yin))])
    )

    xmetin, ymetin = makeOffsetPoly(x, y, -Wmet / 2)
    ymetin = ymetin[~np.isnan(xmetin)]
    xmetin = xmetin[~np.isnan(xmetin)]
    xmetin = xmetin[~np.isnan(ymetin)]
    ymetin = ymetin[~np.isnan(ymetin)]

    xmetout, ymetout = makeOffsetPoly(x, y, +Wmet / 2)
    ymetout = ymetout[~np.isnan(xmetout)]
    xmetout = xmetout[~np.isnan(xmetout)]
    xmetout = xmetout[~np.isnan(ymetout)]
    ymetout = ymetout[~np.isnan(ymetout)]

    ymetin = -ymetin
    ymetout = -ymetout
    xmetin = np.insert(xmetin, 0, 20)
    xmetin = np.insert(xmetin, xmetin.size, -20)
    ymetin = np.insert(ymetin, 0, ymetin[0])
    ymetin = np.insert(ymetin, ymetin.size, ymetin[0])

    xmetout = np.insert(xmetout, 0, 20)
    xmetout = np.insert(xmetout, xmetout.size, -20)
    ymetout = np.insert(ymetout, 0, ymetout[0])
    ymetout = np.insert(ymetout, ymetout.size, ymetout[0])

    xmet = np.concatenate([xmetin[::-1], xmetout])
    ymet = np.concatenate([ymetin[::-1], ymetout])
    xymet = np.vstack([xmet, ymet]).T
    xin, yin, xout, yout = xin[ind], yin[ind], xout[ind], yout[ind]
    xin = np.concatenate([xin, [xin[0]]])
    yin = np.concatenate([yin, [yin[0]]])

    xy = np.vstack([x, y]).T
    xyin = np.vstack([xin[::-1], yin]).T
    xyout = np.vstack([xout[::-1], yout]).T
    xlayout = np.concatenate([xin[::-1], xout])
    ylayout = np.concatenate([yin[::-1], yout])

    xlayout = np.concatenate([xlayout, [xout[0] - 0.0001]])
    ylayout = np.concatenate([ylayout, [yout[0] - 0.0001]])

    xylayout = np.vstack([xlayout, ylayout]).T
    return xy, xylayout, xymet, xyin, xyout, newRW


def GenerateRaceTrackChristy(fid, param, ncell, cnt_out):
    circle_coupling = param.get("circle_coupling", False)
    resist = param.get("resist", "positive")
    Name = param.get("name")
    R0 = param.get("RR")
    trck_type = param.get("trck_type", "Euler")
    Ltot = param.get("Lrace")
    RWtaper = param.get("RWtaper")
    y0 = param.get("y0")
    x0 = param.get("x0")

    left_coupling = param.get("left_coupling", False)

    # print(x0)
    layer = param.get("layer")
    layer_mixmatch = param.get("layer_mixmatch", None)

    W = param.get("RW")
    sleeve = param.get("exp_w")
    G = param.get("G")
    Wwg = param.get("W")
    Lcpl = param.get("Lc")
    Ljoin = param.get("Ljoin")
    yshift = param.get("yshift", 0)

    xy_center, xytot, xymet, _, _, _ = getPoints(
        Ltot, 2 * R0, trck_type, RW=W, R0=R0, num_points=200, tapering=RWtaper
    )

    xtot = xytot[:, 0]
    ytot = xytot[:, 1]

    Wtot = np.max(xtot) - np.min(xtot)

    # yshift += np.max(xytot[:, 1]) - W / 2

    if resist == "positive":
        _, xysleeve, _, _, _ = getPoints(
            Ltot,
            2 * R0,
            trck_type,
            RW=W + 2 * sleeve,
            R0=R0,
            num_points=200,
            tapering=False,
        )
        wg_struct = f"{Name}Wg{ncell}_{cnt_out}"
        sleev_struct = f"{Name}Slv{ncell}_{cnt_out}"

        fid.write(f"{layer} layer\n")
        fid.write(f"<{wg_struct} struct>\n")
        for x, y in zip(xtot + x0, ytot - yshift + y0):
            fid.write(f"{x:.6f} {y:.6f} ")
        fid.write(f"points2shape\n")

        fid.write(f"{layer} layer\n")
        # xsleeve =  xtot[::10]
        # ysleeve = ytot[::10]

        if left_coupling:
            Lr = np.max(xtot) - np.min(xtot)
            x1cpl = np.min(xtot) - G - Wwg / 2
            y1cpl = -yshift + 2
            x0cpl = np.min(xtot) - W / 2 - G - W / 2 - yshift + 2
            Lstart_left = Ljoin + x0cpl
            y0cpl = 0

            fid.write(
                f"\t<{x0cpl-Lstart_left} {y0cpl+ y0} {x0cpl} {y0cpl+ y0} {Wwg} 0 0 0 waveguide>\n"
            )
            fid.write(
                f"\t<{x0cpl} {y0cpl+ y0} {x1cpl} {y1cpl+ y0} {Wwg} 0 90degreeBend>\n"
            )
            fid.write(
                f"\t<{x1cpl} {y1cpl+ y0} {x1cpl} {y1cpl-12+ y0} {Wwg} 0 0 0 waveguide>\n"
            )

            # x0cpl = np.min(xtot) - W/2  - G - Wwg/2
            # y0cpl = - yshift - 5
            x2cpl = np.min(xtot) - W / 2 - G - W / 2 + yshift - 2
            y2cpl = y1cpl - 12 - yshift + 2

            fid.write(
                f"\t<{x2cpl} {y2cpl+ y0} {x1cpl} {y1cpl - 12+ y0} {Wwg} 0 90degreeBend>\n"
            )
            # print(Lr)
            fid.write(
                f"\t<{x2cpl} {y2cpl+ y0} {x2cpl + Lr -  2*(yshift + 2)} {y2cpl+ y0} {Wwg} 0 0 0 waveguide>\n"
            )
            xSendrtck = x2cpl + Lr - 2 * (yshift + 2)
            fid.write(f"\t<{xSendrtck} {y2cpl+ y0} {100} {-y2cpl} {Wwg} 0 sBendLH>\n")

            Lstart_right = Ljoin - (xSendrtck + 100)
            fid.write(
                f"\t<{xSendrtck+100} {0+ y0} {xSendrtck+100 + Lstart_right} {0+ y0} {Wwg} 0 0 0 waveguide>\n"
            )

        # ================= SLEEVE  =========
        fid.write(f"<{sleev_struct} struct>\n")
        fid.write("3 layer\n")
        # if not xsleeve[-1] == xtot[-1]:
        #     xsleeve = np.concatenate((xsleeve, [xtot[-1]]))
        #     ysleeve = np.concatenate((ysleeve, [ytot[-1]])
        xsleeve = xysleeve[:, 0]
        ysleeve = xysleeve[:, 1]
        for x, y in zip(xsleeve + x0, ysleeve - yshift + y0):
            fid.write(f"{x:.5f} {y:.5f} ")
        fid.write(f"points2shape\n")

        if not left_coupling:
            y1 = R0 + W / 2 + G + Wwg / 2 - yshift
            x1 = Lcpl / 2
            fid.write(f"\t<{x1} {y1} {Ls} {Hs} {Wwg} 0 sBendLH>\n")

            y1 = R0 + W / 2 + G + Wwg / 2 - yshift

            x1 = -Lcpl / 2
            fid.write(f"\t<{x1} {y1} {-Ls} {Hs} {Wwg} 0 sBendLH>\n")
            fid.write(f"\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg} 0 0 0 waveguide>\n")

            y1 = R0 + W / 2 + G + Wwg / 2 - yshift
            x1 = Lcpl / 2

            fid.write(f"\t<{x1} {y1} {Ls} {Hs} {Wwg+2*sleeve} 0 sBendLH>\n")

            y1 = R0 + W / 2 + G + Wwg / 2 - yshift
            x1 = -Lcpl / 2
            fid.write(f"\t<{x1} {y1} {-Ls} {Hs} {Wwg+2*sleeve} 0 sBendLH>\n")
            fid.write(f"\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg+2*sleeve} 0 0 0 waveguide>\n")

            # ====== Stepper saving space
            stepperArea = f"{Name}RtrckStep{ncell}_{cnt_out}"
            fid.write(f"<{stepperArea} struct>\n")
            fid.write(f"\t{layer_mixmatch} layer\n")

            # Inner of the racetrack
            for x, y in zip(xsleeve, ysleeve - yshift):
                fid.write(f"{x:.5f} {y:.5f} ")
            fid.write(f" points2shape\n")

            # Sleeve

            for x, y in zip(xsleeve, ysleeve - yshift):
                fid.write(f"{x:.5f} {y:.5f} ")
            fid.write(f"{W+2*sleeve-1} 0 1 polypath\n")

            # Coupling region
            y1 = R0 + W / 2 + G + Wwg / 2 - yshift
            x1 = Lcpl / 2
            fid.write(f"\t<{x1} {y1} {Ls} {Hs} {Wwg+2*sleeve-1} 0 sBendLH>\n")

            y1 = R0 + W / 2 + G + Wwg / 2 - yshift
            x1 = -Lcpl / 2
            fid.write(f"\t<{x1} {y1} {-Ls} {Hs} {Wwg+2*sleeve-1} 0 sBendLH>\n")
            fid.write(
                f"\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg+2*sleeve-1} 0 0 0 waveguide>\n"
            )

            # Connection waveguide
            Lstart = Ljoin - Lcpl / 2 - Ls
            wsleeve_stepper = Wwg + 2 * sleeve - 1
            fid.write(
                f"\t<{-Ljoin+ wsleeve_stepper/2} {y0} {-Ljoin + Lstart} {y0} {wsleeve_stepper} 0 1 0 waveguide>\n"
            )
            fid.write(
                f"\t<{Ljoin - Lstart} {y0} {Ljoin-wsleeve_stepper/2} {y0} {wsleeve_stepper} 0 0 1 waveguide>\n"
            )

            Lstart = Ljoin - Lcpl / 2 - Ls
            ystart = y0
            fid.write(
                f"\t<{-Ljoin} {ystart} {-Ljoin + Lstart} {ystart} {Wwg+2*sleeve} {Wwg} 0 1 0 waveguideSlot>\n"
            )
            fid.write(
                f"\t<{Ljoin - Lstart} {ystart} {Ljoin} {ystart} {Wwg+2*sleeve} {Wwg} 0 0 1 waveguideSlot>\n"
            )

        else:
            # Coupling region
            # ================= SLEEVE  =========
            Lr = np.max(xtot) - np.min(xtot)
            x1cpl = np.min(xtot) - G - Wwg / 2
            y1cpl = -yshift + 2
            x0cpl = np.min(xtot) - W / 2 - G - W / 2 - yshift + 2
            Lstart_left = Ljoin + x0cpl
            y0cpl = 0

            fid.write(
                f"\t<{x0cpl-Lstart_left} {y0cpl+ y0} {x0cpl} {y0cpl+ y0} {Wwg+2*sleeve} 0 0 0 waveguide>\n"
            )
            fid.write(
                f"\t<{x0cpl} {y0cpl+ y0} {x1cpl} {y1cpl+ y0} {Wwg+2*sleeve} 0 90degreeBend>\n"
            )
            fid.write(
                f"\t<{x1cpl} {y1cpl+ y0} {x1cpl} {y1cpl-12+ y0} {Wwg+2*sleeve} 0 0 0 waveguide>\n"
            )

            # x0cpl = np.min(xtot) - W/2  - G - Wwg+2*sleeve/2
            # y0cpl = - yshift - 5
            x2cpl = np.min(xtot) - W / 2 - G - W / 2 + yshift - 2
            y2cpl = y1cpl - 12 - yshift + 2

            fid.write(
                f"\t<{x2cpl} {y2cpl+ y0} {x1cpl} {y1cpl - 12+ y0} {Wwg+2*sleeve} 0 90degreeBend>\n"
            )
            # print(Lr)
            fid.write(
                f"\t<{x2cpl} {y2cpl+ y0} {x2cpl + Lr -  2*(yshift + 2)} {y2cpl+ y0} {Wwg+2*sleeve} 0 0 0 waveguide>\n"
            )
            xSendrtck = x2cpl + Lr - 2 * (yshift + 2)
            fid.write(
                f"\t<{xSendrtck} {y2cpl+ y0} {100} {-y2cpl} {Wwg+2*sleeve} 0 sBendLH>\n"
            )

            Lstart_right = Ljoin - (xSendrtck + 100)
            fid.write(
                f"\t<{xSendrtck+100} {0+ y0} {xSendrtck+100 + Lstart_right} {0+ y0} {Wwg+2*sleeve} 0 0 0 waveguide>\n"
            )

        # ================= BOOLEAN OPERATION
        wg_area = f"{Name}RtrkWg{ncell}_{cnt_out}"
        sleeve_area = f"{Name}RtrkSlv{ncell}_{cnt_out}"
        fid.write(f"<{wg_area} {wg_struct} 1 genArea>\n")
        fid.write(f"<{sleeve_area} {sleev_struct} 3 genArea>\n")
        # fid.write(f'{layer_mixmatch} layer\n')

        # ====== FINAL STRUCTURE =====
        struct_name = f"{Name}Rtrck{ncell}_{cnt_out}"
        fid.write(f"<{struct_name} struct>\n")
        # fid.write(f'\t<{stepperArea} 0 0 0 1 0 instance>\n')
        fid.write(f"\t{layer} layer\n")
        fid.write(f"\t<{wg_area} {sleeve_area} {layer} XOR>\n")

    if resist == "negative":
        struct_name = f"{Name}Rtrck{ncell}_{cnt_out}"
        fid.write(f"<{struct_name} struct>\n")
        fid.write(f"{layer} layer\n")
        for x, y in zip(xtot + x0, ytot - yshift + y0):
            fid.write(f"{x:.6f} {y:.6f} ")
        fid.write(f"points2shape\n")

    return [struct_name], xymet, xytot
