from .utils import *


def DesignDimer():
    Blocks = {}
    Blocks[31] = [
        dict(
            RR=31,
            G=gregArange(350, 100, 850),
            RW=gregArange(900, 50, 1100),
            Gdimer=gregArange(350, 100, 750),
            W=0.460,
            ypitch=15,
            xpitch=150,
            y_pos_text=-12,
            xdec=160,
            Drop=True,
            Label="Dimer RR=31",
        )
    ]

    Blocks[32] = [copy(Blocks[31][0])]
    Blocks[33] = [copy(Blocks[31][0])]

    return Blocks
