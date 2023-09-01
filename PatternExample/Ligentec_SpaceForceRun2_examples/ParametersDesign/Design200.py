from .utils import *


def Design200():
    Blocks = {}
    Blocks[34] = [
        dict(
            y0=-50,
            RR=115,
            G=gregArange(200, 25, 400),
            RW=gregArange(875, 25, 1050),
            W=0.460,
            Wtapper=0.2,
            ypitch=12,
            xpitch=300,
            xdec=300,
            Label="RR=115 Straight • 200 GHz • 1060nm",
        )
    ]

    Blocks[35] = [
        dict(
            y0=-50,
            RR=115,
            G=gregArange(200, 50, 500),
            RW=gregArange(1700, 50, 2150),
            W=0.460,
            Wtapper=0.32,
            ypitch=12,
            xpitch=300,
            xdec=300,
            Label="RR=115 Straight • 200 GHz • 1550nm",
        )
    ]

    Blocks[36] = [
        dict(
            y0=-50,
            RR=[114.5, 115.5],
            G=gregArange(200, 25, 400),
            RW=gregArange(900, 50, 1050),
            W=0.460,
            Wtapper=0.2,
            ypitch=12,
            xpitch=300,
            xdec=300,
            Label="RR=114.5 - 155.5 Straight • 200 GHz • 1060nm",
        )
    ]

    Blocks[37] = [
        dict(
            y0=-50,
            RR=[114.5, 115.5],
            G=gregArange(200, 50, 500),
            RW=gregArange(1700, 100, 2100),
            W=0.460,
            Wtapper=0.32,
            ypitch=12,
            xpitch=300,
            xdec=300,
            Label="RR=114.5 - 155.5 Straight • 200 GHz • 1550nm",
        )
    ]

    return Blocks
