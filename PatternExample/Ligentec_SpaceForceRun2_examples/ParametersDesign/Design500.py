from .utils import *


def Design500():
    Blocks = {}
    Blocks[7] = [
        dict(
            RR=46,
            G=gregArange(250, 50, 600),
            RW=gregArange(820, 20, 960),
            W=gregArange(360, 100, 660),
            ypitch=10,
            xpitch=145,
            xdec=135,
            Label="RR=46 Straight",
        )
    ]

    # --- Nominal Pulley ----
    Blocks[8] = [
        dict(
            RR=46,
            G=gregArange(400, 50, 700),
            RW=gregArange(820, 10, 890),
            Lc=gregArange(15, 1, 19, microns=True),
            W=0.550,
            ypitch=9.3,
            xpitch=145,
            xdec=135,
            y_pos_text=-7,
            Label="RR=46 Pulley • 15µm → 19 µm",
        )
    ]

    Blocks[9] = [copy(Blocks[8][0])]
    Blocks[9][0].update(W=0.560)

    Blocks[10] = [copy(Blocks[8][0])]
    Blocks[10][0].update(W=0.570)

    Blocks[11] = [
        dict(
            RR=46,
            G=gregArange(450, 50, 650),
            RW=gregArange(830, 10, 880),
            Lc=gregArange(6, 2, 22, microns=True),
            W=0.560,
            ypitch=9.3,
            xpitch=140,
            xdec=135,
            y_pos_text=-7,
            Label="RR=46 Pulley • 15µm → 19 µm",
        )
    ]

    return Blocks
