from copy import copy
import numpy as np

def BoundingWg(Cells, param, Bloc):
    
    Hextend = param.get('Hextend', 300)
    Wextend = param.get('Wextend', 200)
    Yspace = param.get('Yspace', 125)
    Xspace = param.get('Xspace',Yspace)
    for ii in range(2):
        BoundingParam = {'name': 'Bdg_Bound_{}'.format(ii),
                         'layer': param['layer_waveguide'],
                         'x0': 0,
                         'y0': -param['Hchip'] + Hextend + ii*10 ,
                         'W': param['Wchip'] + Wextend ,
                         'H': param['Hchip']  -  ii*10,
                         'Yspace': Yspace -  ii*10,
                         'Xspace': Xspace - ii*10,
                         'Wwg': 2,
                         }
        Cells['cell_type'].append('Gen.Misc.WgBoundingChip')
        Cells['param'].append(BoundingParam)
        Cells['YSHIFT'].append(0)

    #
