import numpy as np


def QrCodeMaker(fid, param, ncell):

    layer = param.get("layer", 2)
    datatype = param.get("datatype", 2)
    size = param.get("size", 50)
    xdec = param.get("xdec", 750)
    qrcode = param.get("qrcode", [[]])
    CodeType = param.get("codeType", "None")
    design_number = param.get("design_number", None)
    fid.write(f"{layer} layer\n")
    fid.write(f"{datatype} dataType\n")

    ypsize = size / np.shape(qrcode)[0]

    if CodeType == "PDF417":
        xpsize = 3 * ypsize
    else:
        xpsize = ypsize

    if design_number:
        AddedName = f"D{design_number}"
    else:
        AddedName = ""

    fid.write(f"<{AddedName}{CodeType}0_1 struct>\n")
    for ii, col in enumerate(qrcode):
        for jj, value in enumerate(col):
            if value:
                x0, y0 = xdec + jj * xpsize, -ii * ypsize
                fid.write(
                    f"\t{x0} {y0} " + f"{xpsize} {ypsize} " + f"{0} rectangleLH\n"
                )

    return [f"{AddedName}{CodeType}0_1"]
