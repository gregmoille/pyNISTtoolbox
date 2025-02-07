from copy import copy
import numpy as np

def Vernier(Cells, param, Bloc):
    x0_vernier = [-param['Wchip']/2, param['Wchip']/2]
    VernierLtot = param.get('VernierLtot', 200) 
    
    # xdec = [149, 251]
    xdec = [VernierLtot/2 + 50 -1, VernierLtot/2 + 150 + 1]
    y_0 = [260, -param['Hchip']+ 340]
    cnt = 0
    VernierLtot = param.get('VernierLtot', 200) 
    for ii in range(0, len(x0_vernier)):
        for jj in range(0, len(y_0)):
            VernierParam = {'name': 'Vrnr{}_'.format(cnt),
                            'layer': param['layer_label'],
                            'x0': x0_vernier[ii],
                            'y0': y_0[jj],
                            'longspace': 50,
                            'shortspace': 5,
                            'Ltot': VernierLtot,
                            'W': 2,
                            'H_long': 100,
                            'H_short': 50,
                            'xdec': xdec[ii],
                            }
            Cells['cell_type'].append('Gen.Misc.CreateVernier')
            Cells['param'].append(VernierParam)
            Cells['YSHIFT'].append(0)
    cnt += 1
