from .utils import *


def DesignRaceTrack():
    Blocks = {}

    Blocks[19] = [
        dict(
            y0=-100,
            racetrack=True,
            heater=True,
            RR=23,
            Lrace=361,
            G=gregArange(300, 50, 650),
            RW=gregArange(800, 10, 1000),
            W=0.460,
            ypitch=10,
            xpitch=165,
            carriage_shift=20,
            Wtapper=0.2,
            xdec=180,
            Label="Rtrack Lc=361 Curve Cpl - 400GHz",
        ),
        dict(
            top_shift=1600,
            racetrack=True,
            RR=23,
            Lrace=361,
            G=gregArange(350, 50, 800),
            RW=gregArange(1700, 50, 2100),
            W=0.460,
            ypitch=10,
            xpitch=165,
            carriage_shift=20,
            Wtapper=0.32,
            xdec=180,
            Label="Rtrack Lc=361 Curve Cpl - 400GHz ª • 1550nm pump",
        ),
    ]

    Blocks[20] = [
        dict(
            y0=-100,
            racetrack=True,
            RR=23,
            Lrace=722,
            G=gregArange(300, 50, 650),
            RW=gregArange(800, 20, 940),
            W=0.460,
            ypitch=10,
            xpitch=400,
            carriage_shift=20,
            Wtapper=0.2,
            xdec=350,
            Label="Rtrack Lc=722 Curve Cpl - 200GHz",
        ),
        dict(
            top_shift=1650,
            racetrack=True,
            RR=23,
            Lrace=722,
            G=gregArange(300, 50, 750),
            RW=gregArange(1700, 50, 2100),
            W=0.460,
            ypitch=10,
            xpitch=400,
            carriage_shift=20,
            Wtapper=0.32,
            xdec=350,
            Label="Rtrack Lc=722 Curve Cpl - 200GHz •1550nm pump",
        ),
    ]

    Blocks[21] = [
        dict(
            y0=-25,
            racetrack=True,
            RR=23,
            Lrace=1445,
            G=gregArange(300, 50, 650),
            RW=gregArange(850, 50, 1000),
            W=0.460,
            ypitch=10,
            xpitch=1650,
            carriage_shift=8,
            Wtapper=0.2,
            xdec=650,
            Label="Rtrack Lc=1445 Curve Cpl - 100GHz",
        ),
        dict(
            top_shift=2100,
            racetrack=True,
            RR=23,
            Lrace=1445,
            G=gregArange(350, 50, 750),
            RW=gregArange(1800, 100, 2100),
            W=0.460,
            ypitch=10,
            xpitch=1650,
            carriage_shift=7,
            Wtapper=0.2,
            xdec=650,
            Label="Rtrack Lc=1445 Curve Cpl - 100GHz •1550nm pump",
        ),
    ]

    Blocks[22] = [
        dict(
            y0=-100,
            racetrack=True,
            RR=150,
            Lrace=2890,
            G=gregArange(250, 100, 650),
            RW=gregArange(1800, 100, 2000),
            W=0.460,
            ypitch=10,
            xpitch=800,
            carriage_shift=10,
            Wtapper=0.32,
            xdec=775,
            Label="Rtrack Lc=2890 Curve Cpl - 50GHz",
        ),
    ]

    return Blocks
