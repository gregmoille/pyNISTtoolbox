def CreateLabel(fid, param, ncell):

    txt = param.get("txt", "NONE")

    x_pos_text = param.get("x_pos_text", None)
    y_pos_text = param.get("y_pos_text", None)
    x_pos_left = param.get("x_pos_left", None)
    theta = param.get("theta", 0)
    margin_fact = param.get("margin_fact", 0.6)
    nr = param.get("nr", 1000)
    Name = param.get("name", None)
    layer = param.get("layer", 1)
    datatype = param.get("datatype", 0)
    box = param.get("box", True)
    nist_logo = param.get("nist_log", False)
    xnist = param.get("xnist", 0)
    ynist = param.get("ynist", 0)
    logo = param.get("logo", None)
    logo_shift = param.get("logo_shift", -300)
    font = param.get("font", "Arial")
    font_size_pattern = param.get("font_size_pattern", 10)
    name_out = []
    n_txt = len(txt)
    fid.write(str(layer) + " layer\n")
    fid.write(str(datatype) + " dataType\n")
    if x_pos_text:
        fid.write("<" + Name + "LlTxt" + str(ncell) + " struct>\n")
        name_out.append(Name + "LlTxt" + str(ncell))
        fid.write("\t")
        fid.write(
            r"<{{{{ {} }}}} ".format(txt)
            + r"{{{{{}}}}} {} ".format(font, font_size_pattern)
            + "{} {} textgds>\n".format(x_pos_text, y_pos_text)
        )

    if x_pos_left:
        fid.write("<" + Name + "LlTxtLeft" + str(ncell) + " struct>\n")
        name_out.append(Name + "LlTxtLeft" + str(ncell))
        fid.write("\t")
        fid.write(
            r"<{{{{ {} }}}} ".format(txt)
            + r"{{{{{}}}}} {} ".format(font, font_size_pattern)
            + "{} {} textgds>\n".format(x_pos_left, y_pos_text)
        )

    if nist_logo:
        fid.write("<" + Name + "NIST" + str(ncell) + " struct>\n")
        name_out.append(Name + "NIST" + str(ncell))
        fid.write(f"{xnist} {ynist} 0.3 nistLogo \n")

    if logo:
        # name_out.append(f"Custom{logo}")
        # fid.write(" ".join(logo))
        fid.write(f"<{logo} readGDS>\n")
        fid.write("<" + Name + "Logo" + str(ncell) + " struct>\n")
        name_out.append(Name + "Logo" + str(ncell))
        fid.write("\t<" + f"Custom{logo} {xnist+logo_shift} {ynist} 0 1 0 instance>\n")

    # Create the box around label
    if box:
        fid.write("<LblArnd_" + Name + str(ncell) + " struct>\n")
        name_out.append("LblArnd_" + Name + str(ncell))
        fid.write(
            "\t<{} {} ".format(x_pos_text, y_pos_text)
            + "{} 1 {} 0 ".format(
                n_txt * font_size_pattern * margin_fact, 0.75 * font_size_pattern
            )
            + "{} raceTrack>\n".format(nr)
        )

    fid.write("<" + Name + "LblDev_" + str(ncell) + " struct>\n")
    for n in name_out:
        fid.write("\t<" + n + " 0 0 0 1 {:.0f} instance>\n".format(theta))
    fid.write("\n")

    fid.write("# ******************************\n")
    return [Name + "LblDev_" + str(ncell)]
