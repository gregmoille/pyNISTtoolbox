from copy import copy
import numpy as np

def LiftOff(Cells, param, Bloc):
    HLiftBox = param['Hchip'] + 300
    WLiftBox = 1000
    LiftBox = {'name': 'Lift_off',
                     'layer': param['layerLiftOff'],
                     'corner': (-WLiftBox/2, -param['Hchip']+200),
                     'w_h': (WLiftBox,HLiftBox),
                     'Yspace': 0,
                     'Xspace': 0,
                     }

    Cells['cell_type'].append('Gen.Misc.CreateBumpStruct')
    Cells['param'].append(LiftBox)
    Cells['YSHIFT'].append(0)
