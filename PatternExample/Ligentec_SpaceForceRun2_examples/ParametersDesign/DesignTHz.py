from .utils import *


def DesignTHz():
    Blocks = {}
    Blocks[1] = [
        dict(
            RR=23,
            G=gregArange(250, 50, 600),
            RW=gregArange(800, 10, 920),
            W=gregArange(360, 100, 660),
            ypitch=9.5,
            xpitch=85,
            xdec=97,
            Label="RR=23 Strg Cpl",
        )
    ]

    # --- Nominal Pulley ----
    Blocks[2] = [
        dict(
            RR=23,
            G=gregArange(400, 50, 700),
            RW=gregArange(810, 10, 900),
            Lc=gregArange(15, 1, 19, microns=True),
            W=0.450,
            ypitch=10,
            xpitch=100,
            xdec=100,
            Label="RR=23 Pulley • 15µm → 18 µm",
        )
    ]

    Blocks[3] = [copy(Blocks[2][0])]
    Blocks[3][0].update(W=0.460)

    Blocks[4] = [copy(Blocks[2][0])]
    Blocks[4][0].update(W=0.470)

    # -- wider variation
    Blocks[5] = [
        dict(
            RR=23,
            G=gregArange(400, 50, 650),
            RW=gregArange(800, 10, 900),
            Lc=gregArange(11, 2, 21, microns=True),
            W=0.460,
            ypitch=10,
            xpitch=90,
            xdec=100,
            Label="RR=23 Pulley ",
        )
    ]

    Blocks[6] = [
        dict(
            RR=23,
            G=gregArange(400, 50, 650),
            RW=gregArange(750, 10, 950),
            Lc=gregArange(15, 2, 19, microns=True),
            W=0.460,
            ypitch=10,
            xpitch=90,
            xdec=100,
            Label="RR=23 Pulley ",
        )
    ]

    # -- fceo variation and vernier ---
    Blocks[23] = [
        dict(
            RR=gregArange(23, 0.05, 23.3, microns=True),
            G=gregArange(450, 50, 650),
            RW=gregArange(800, 10, 900),
            Lc=17,
            W=0.460,
            ypitch=10,
            xpitch=90,
            xdec=100,
            Label="RR=23 Variation Pulley  ",
        )
    ]
    Blocks[24] = [copy(Blocks[23][0])]
    Blocks[24][0].update(RR=gregArange(22.7, 0.05, 23, microns=True))

    Blocks[25] = [
        dict(
            RR=gregArange(23, 0.02, 23.1, microns=True),
            G=gregArange(500, 50, 650),
            RW=gregArange(830, 10, 880),
            Lc=[16, 17, 18],
            W=0.460,
            ypitch=9.5,
            xpitch=80,
            xdec=80,
            Label="RR=23 Variation Pulley  ",
        )
    ]

    Blocks[26] = [copy(Blocks[25][0])]
    Blocks[26][0].update(
        RR=gregArange(22.9, 0.02, 23, microns=True),
    )

    Blocks[27] = [copy(Blocks[25][0])]
    Blocks[27][0].update(
        RR=gregArange(23, 0.01, 23.05, microns=True),
    )

    Blocks[28] = [copy(Blocks[25][0])]
    Blocks[28][0].update(
        RR=gregArange(22.95, 0.01, 23, microns=True),
    )

    # -- Add drop
    Blocks[29] = [
        dict(
            RR=23,
            G=gregArange(400, 100, 1000),
            Drop=True,
            RW=0.850,
            W=0.460,
            ypitch=15,
            y_pos_text=-12,
            xpitch=90,
            xdec=140,
            CosAmp=gregArange(50, 50, 400),
            Nmodulation=0.5,
            CosPhase=[np.pi, 3 * np.pi / 4, np.pi / 2, np.pi / 4, 0],
            Label="RR=23 Pulley • RW=850 nm • Add Drop",
        )
    ]

    Blocks[30] = [copy(Blocks[29][0])]
    Blocks[30][0].update(RW=0.870)

    # --angled facets
    Blocks[41] = [copy(Blocks[2][0])]
    Blocks[41][0].update(
        x_text_left=730,
        x_pos_text=None,
        y_pos_text=+3,
        angled_facets=45,
    )

    Blocks[42] = [copy(Blocks[3][0])]
    Blocks[42][0].update(
        x_text_left=730, x_pos_text=None, y_pos_text=+3, angled_facets=True
    )

    return Blocks
