from .utils import *


def Design750():
    Blocks = {}
    Blocks[16] = [
        dict(
            RR=31,
            G=gregArange(300, 50, 600),
            RW=gregArange(800, 10, 930),
            W=gregArange(360, 100, 660),
            ypitch=10,
            xpitch=110,
            xdec=110,
            Label="RR=31 Straight",
        )
    ]

    Blocks[17] = [
        dict(
            RR=31,
            G=gregArange(350, 50, 650),
            RW=gregArange(800, 20, 900),
            Lc=gregArange(15, 19, 2),
            W=[0.520, 0.540],
            ypitch=10,
            xpitch=90,
            Label="RR=31 Pulley ",
        )
    ]

    Blocks[18] = [copy(Blocks[16][0])]
    Blocks[18][0].update(W=[0.480, 0.500])
    return Blocks
