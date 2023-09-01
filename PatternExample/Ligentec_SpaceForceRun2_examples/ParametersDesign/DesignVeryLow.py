from .utils import *


def DesignVeryLow():
    Blocks = {}
    Blocks[38] = [
        dict(
            y0=-300,
            RR=230,
            G=gregArange(200, 50, 450),
            RW=gregArange(1700, 200, 2100),
            W=0.460,
            Wtapper=0.32,
            ypitch=12,
            xpitch=600,
            xdec=600,
            Label="RR=230 Straight • 100 GHz",
        )
    ]

    Blocks[39] = [
        dict(
            y0=-400,
            RR=660,
            G=gregArange(200, 50, 300),
            RW=1.800,
            W=0.460,
            Wtapper=0.32,
            ypitch=150,
            xpitch=1200,
            xdec=1900 / 2 - 330 / 2,
            Label="RR=660 Straight • 100 GHz",
        )
    ]
    return Blocks
