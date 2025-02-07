import numpy as np
from copy import copy

def GenerateHeaters(Cells, param, Bloc):
    # ------------------------------------------
    yTop = [150 + 70]
    for ib in np.arange(1, len(Bloc)):
        N = 1
        for k, itm in Bloc[ib-1].items():
            if type(itm) == list or type(itm) == np.array:
                N *= len(itm)
        Ndevices  = N  + 0.5
        Hblock = Bloc[ib-1]['ypitch'] * Ndevices
        yTop += [yTop[-1] - Hblock -20]

    ii_ring = 0

    layerField = 30
    for BB, yt in zip(Bloc, yTop):
        y0 = yt
        RR = {'name': f"R{ii_ring:02d}_",
                     'x0': 0,'y0':0,'tot_length' : param['Wchip'],'exp_w': 2,
                     'layer': [param['layer_ring'],0, param['layer_waveguide'], param['layer_stepper']],
                     'RR': BB.get('R', None),
                     'Lc': BB.get('Lc', None),
                     'Heaterangle': BB.get('Heaterangle', np.pi),
                     'Wheater': BB.get('Wheater', 3),
                     'Wpad': BB.get('Wpad', 40),
                     'LcDrop': BB.get('LcDrop', None),
                     'RWin' : BB.get('RW', None), 'RWetch': 0,
                     'G': BB.get('G', None),
                     'W': BB.get('W', None), 'Wbend':BB.get('Wdrop', 0)+0.35,
                     'Gdrop':BB.get('Gdrop', None), 'Wdrop': BB.get('Wdrop', 0),
                     'Nmodulation': BB.get('Nmodulation', None),
                     'Amodulation': BB.get('Amodulation', None),
                     'Gaussmodulation_spread': BB.get('Gaussmodulation_spread', None),
                     'Sigmamodulation': BB.get('Sigmamodulation', None),
                     'y_shift': -1*BB.get('ypitch', None), 
                     'ytoppad': BB.get('ytoppad', None), 
                     'signpad': BB.get('signpad', None), 
                     }

        Cells['cell_type'].append('Gen.Misc.CreateHeater')
        Cells['param'].append(RR)
        Cells['YSHIFT'].append(copy(y0))
        
        ii_ring += 1
