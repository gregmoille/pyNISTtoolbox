import inspect
import numpy as np
import os
from copy import copy
import treepoem
from datetime import date


def PrintMyBloc(key, val, lines, linesqr):
    global Ndevices
    if callable(val):
        txt = (
            "lambda "
            + inspect.getsourcelines(val)[0][0].split("lambda ")[1].strip()
        )
        lines += [f"\t- {key}: {txt}µm"]
    else:
        unit = 'µm'
        if key == 'Nmodulation':
            unit = ''
        if "layer" in key:
            unit = ''
        if type(val) is list:
            Ndevices *= len(val)
            if len(val)>2:
                if np.sum(np.diff( np.diff(val) )) < 1e-3:
                    txt = f"{val[0]} {unit} → {val[1] - val[0]:.3g} {unit} step → {val[-1]} {unit}"
                else:
                    txt = f"{val} {unit}"
                
            else:
                txt = f"{val} {unit}"
            lines += [f"\t- {key}: {txt}"]
        else:
            lines += [f"\t- {key}: {val} {unit}"]
    QRvar = ["RR", "Lc", "W", "RW", "Lrace", "G", "CosAmp"]
    if key in QRvar:
        if type(val) is list:
            if len(val)>2:
                if np.sum(np.diff( np.diff(val) )) < 1e-3:
                    txt = f"{val[0]}-{val[1] - val[0]:.3g}-{val[-1]}"
                else:
                    txt =  f"{val} µm"
            else:
                txt =  f"{val} µm"
            linesqr += [f"{key} {txt} "]
        else:
            linesqr += [f"{key} {val} "]


def LogFile(param, Bloc, Cells=None, design_number=None):
    global Ndevices

    to_remove = [
        "label",
        "ypitch",
        "xpitch",
        "xdec",
        "s_shrink",
        "fontsize",
        "s_in_shift",
        "wvia",
        "nvia",
        "wviablock",
        "heater",
        "x_pos_text",
        "y_pos_text",
        "x_text_left",
        "top_shift",
        "surplus_taper",
        'S_in_shift',
        "ypitch", "xpitch", "yrace_shift", "carriage_shift", "xdec",
    ]

    mdfile = f'{param["pyfile"].replace(".py", "")}.md'
    if "LogPath" in param.keys():
        mdfile = os.path.join(param["LogPath"], os.path.basename(mdfile))
        mdfile = os.path.join(os.path.dirname(param["pyfile"]), mdfile)

    lines = []
    today = date.today()
    linesqr = [f'G. MOILLE - NIST/UMD - {today.strftime("%d.%m.%Y")}']

    lines += [f'## Chip: {param["filename"]}']
    for nn, BB in enumerate(Bloc):
        lines += [f'\n**Block {nn}: {BB["Label"]}**']
        linesqr += [f'\nBlock {nn}: {BB["Label"]}\n']
        Nlabl = len(lines) - 1
        Ndevices = 1
        for key, val in BB.items():
            
            if not key.lower() in to_remove:
                if nn > 0:
                    if key in Bloc[nn - 1].keys():
                        if type(val) == np.ndarray or type(val) == list:
                            if not np.array(Bloc[nn - 1][key] == val).all():
                                PrintMyBloc(key, val, lines, linesqr)
                            else:
                                Ndevices *= len(val)
                        else:
                            if not Bloc[nn - 1][key] == val:
                                PrintMyBloc(key, val, lines, linesqr)
                            else:
                                Ndevices *= 1
                    else:
                        PrintMyBloc(key, val, lines, linesqr)
                else:
                    PrintMyBloc(key, val, lines, linesqr)

        lines[Nlabl] += f" • N devices = {Ndevices:.0f}\n"


    if Cells:
        data = "".join(linesqr)
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
            xdec=(param["Wchip"] / 2 - 275),  # 675,
            y0=0,
        )
        Cells["cell_type"].append("Gen.Misc.QrCodeMaker")
        Cells["YSHIFT"].append(90)
        Cells["param"].append(Qrcode_param)

        Qrcode_param2 = copy(Qrcode_param)
        Qrcode_param2.update(xdec=-(param["Wchip"] / 2 - 170))  # -780)
        Qrcode_param2["codeType"] = "QRleft"
        Cells["cell_type"].append("Gen.Misc.QrCodeMaker")
        Cells["YSHIFT"].append(90)
        Cells["param"].append(Qrcode_param2)

    lines = "\n".join(lines)
    with open(mdfile, "w") as fid:
        fid.write(lines)
    print(lines)
