import inspect
import numpy as np
import os
from copy import copy
import treepoem
from datetime import date


def PrintMyBloc(key, val, lines, linesqr):

    notLog = ["ypitch", "xpitch", "yrace_shift", "carriage_shift", "xdec"]

    if not key in notLog:
        if callable(val):
            txt = (
                "lambda "
                + inspect.getsourcelines(val)[0][0].split("lambda ")[1].strip()
            )
            lines += [f"\t- {key}: {txt}µm"]
        else:
            if type(val) is list:
                txt = f"{val[0]}µm → {val[1] - val[0]:.3g} µm step → {val[-1]}µm"
                lines += [f"\t- {key}: {txt}"]
            else:
                lines += [f"\t- {key}: {val}µm"]
        QRvar = ["RR", "Lc", "W", "RW", "Lrace", "G", "CosAmp"]
        if key in QRvar:
            if type(val) is list:
                txt = f"{val[0]} - {val[1] - val[0]:.3g} - {val[-1]}"
                linesqr += [f"{key} {txt}"]
            else:
                linesqr += [f"{key} {val}"]


def LogFile(param, Bloc, Cells=None, design_number=None):
    mdfile = f'{param["pyfile"].replace(".py", "")}.md'
    if "LogPath" in param.keys():
        mdfile = os.path.join(param["LogPath"], os.path.basename(mdfile))
        mdfile = os.path.join(os.path.dirname(param["pyfile"]), mdfile)

    lines = []
    today = date.today()
    linesqr = [f'G. MOILLE {today.strftime("%d.%m.%Y")}']
    # with open(mdfile, 'w') as fid:

    lines += [f'## Chip: {param["filename"]}\n']
    for nn, BB in enumerate(Bloc):
        lines += [f'**Block {nn}: {BB["Label"]}**\n']
        # if 'Label' in BB.keys():
        #     PrintMyBloc('Label', BB['Label'], fid)
        for key, val in BB.items():
            if not key == "Label":
                if nn > 0:
                    if key in Bloc[nn - 1].keys():
                        if type(val) == np.ndarray:
                            if not (Bloc[nn - 1][key] == val).all():
                                PrintMyBloc(key, val, lines, linesqr)
                        else:
                            if not Bloc[nn - 1][key] == val:
                                PrintMyBloc(key, val, lines, linesqr)
                    else:
                        PrintMyBloc(key, val, lines, linesqr)
                else:
                    PrintMyBloc(key, val, lines, linesqr)
        # fid.write(f'\n')

    if Cells:
        # q = qrcode.QRCode()

        # q.add_data(data)
        data = "\n".join(linesqr)
        qrcode = treepoem.generate_barcode(
            barcode_type="qrcode",
            options=dict(showborder=True),
            data=data,
        ).convert("1")

        # qrcode = '\n'.join([ii[2::] for ii in qrcode.getvalue().split('\n')[:-1] if ii[0] == '4'])
        # Bloc[0]['qrcode'] = qrcode
        Qrcode_param = dict(
            qrcode=np.array(qrcode),
            size=100,
            layer=Bloc[0].get("layer", 2),
            datatype=Bloc[0].get("datatype", 0),
            design_number=design_number,
            codeType="QR",
            xdec=(param['Wchip']/2 - 275),#675,
            y0=0,
        )
        Cells["cell_type"].append("Gen.Misc.QrCodeMaker")
        Cells["YSHIFT"].append(-5)
        Cells["param"].append(Qrcode_param)

        Qrcode_param2 = copy(Qrcode_param)
        Qrcode_param2.update(xdec=-(param['Wchip']/2 - 170))#-780)
        Qrcode_param2["codeType"] = "QRleft"
        Cells["cell_type"].append("Gen.Misc.QrCodeMaker")
        Cells["YSHIFT"].append(-5)
        Cells["param"].append(Qrcode_param2)

    lines = "\n".join(lines)
    with open(mdfile, "w") as fid:
        fid.write(lines)
    print(lines)
