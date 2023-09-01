def WgBoundingChip(fid, param, ncell):

    layer = param.get("layer", 1)
    datatype = param.get("layer", 0)
    H = param.get("H", 0)
    W = param.get("W", 0)
    Xspace = param.get("Xspace", 0)
    x0 = param.get("x0", 0)
    y0 = param.get("y0", 0)
    Yspace = param.get("Yspace", 0)
    Name = param.get("name", None)
    Wwg = param.get("Wwg", 1)

    name_out = []
    fid.write(str(layer) + " layer\n")
    fid.write(str(datatype) + " dataType\n")
    fid.write("<StgtWg" + Name + str(ncell) + " struct>\n")
    name_out.append("StgtWg" + Name + str(ncell))
    xdec = Xspace
    ydec = Yspace

    # -- Create Straight WAveguide --
    # ------------------------------------------------

    if ydec == 0 and xdec == 0:
        x1 = [-W / 2 + Wwg / 2, -W / 2, W / 2 - Wwg / 2, W / 2]
        x2 = [W / 2 - Wwg / 2, -W / 2, -W / 2 + Wwg / 2, W / 2]
        # y1 = [0, +ydec, H + ydec, ydec]
        # y2 = [0, H, H + ydec, H]
        y1 = [-H, -H - Wwg / 2, 0, 0 + Wwg / 2]
        y2 = [-H, +Wwg / 2, 0, -H - Wwg / 2]

        for ii in range(0, len(x1)):
            fid.write(
                "\t<{} {} ".format(x0 + x1[ii], y0 +y1[ii])
                + "{} {} ".format(x0 + x2[ii], y0 + y2[ii])
                + "{} 0 ".format(Wwg)
                + "0 0 waveguide>\n"
            )
    else:
        x1 = [-W / 2, -W / 2 - xdec, W / 2, W / 2 + xdec]
        x2 = [W / 2, -W / 2 - xdec, -W / 2, W / 2 + xdec]
        # y1 = [0, +ydec, H + ydec, ydec]
        # y2 = [0, H, H + ydec, H]
        y1 = [-H, ydec, ydec, -H + ydec]
        y2 = [-H, 0, ydec, 0]

        for ii in range(0, len(x1)):
            fid.write(
                "\t<{} {} ".format(x1[ii], y1[ii])
                + "{} {} ".format(x2[ii], y2[ii])
                + "{} 0 ".format(Wwg)
                + "0 0 waveguide>\n"
            )

        # -- Create 90° BEnd --
        # ------------------------------------------------
        x1 = [-W / 2.0, -W / 2, W / 2, W / 2]
        x2 = [-W / 2 - xdec, -W / 2 - xdec, W / 2 + xdec, W / 2 + xdec]
        y1 = [0, H + ydec, H + ydec, 0]
        y2 = [ydec, H, H, +ydec]
        name_out.append("BoundingClose" + Name + str(ncell))
        fid.write("<BoundingClose" + Name + str(ncell) + " struct>\n")
        for ii in range(0, len(x1)):
            fid.write(
                "\t<{} {} ".format(x1[ii], y1[ii])
                + "{} {} ".format(x2[ii], y2[ii])
                + "{} 0 ".format(Wwg)
                + "90degreeBend>\n"
            )

    fid.write("<" + Name + str(ncell) + " struct>\n")
    for n in name_out:
        fid.write("\t<" + n + " {} {} ".format(x0, y0) + "0 1 0 instance>\n")
    fid.write("\n")

    fid.write("# ******************************\n")

    return [Name + str(ncell)]
