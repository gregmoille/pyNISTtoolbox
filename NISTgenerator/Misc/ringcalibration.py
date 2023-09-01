import numpy as np
from copy import copy
import NISTgenerator as Gen

def CalibrationRings(Cells, pars):
    # ------------------------------------------

    layerField = pars.get('layerField', 1)
    y0 = pars.get('ycalib', -8500)
    # y0 = -8500
    print(pars['ycalib'])
    Wchip = pars.get('Wchip', 0)

    layer_ring = pars.get('layer_ring', 1)
    layer_waveguide = pars.get('layer_waveguide', 1)
    layer_stepper = pars.get('layer_stepper', 3)
    layer_label = pars.get('layer_label', 1)
    resist = pars.get('resist', 'positive')

    BLOCK = [dict(
            R= 23,
            G= [0.150, 0.200, 0.250, 0.300],
            RW= [1.060],
            W = 0.550,
            ypitch = 55,
            Wtapper= 0.150,
            Label= 'Nominal ACES')]

    BLOCK += [{**BLOCK[-1],
            'Label': 'Q test',
            'RW': [2]}]

    BLOCK += [{**BLOCK[-1],
            'Label': 'Mode Splitting  M=259 • λ=965mn • RW=900',
            'RW': [0.900],
            'Nmodulation': 259,
            'Amodulation': [0.075]}]

    BLOCK += [{**BLOCK[-1],
            'Label': 'Mode Splitting 1060 • M = 237 • RW=1060',
            'RW': [1.060],
            'Nmodulation': 237,
            'Amodulation': [0.075]}]

    yTop = [y0]
    for ib in np.arange(1, len(BLOCK)):
        N = len(BLOCK[ib-1].get('G', [1])) \
            * len(BLOCK[ib-1].get('Amodulation', [1])) \
            * len(BLOCK[ib-1].get('Sigmamodulation', [1]))
        Ndevices  = N+1
        Hblock = BLOCK[ib-1]['ypitch'] * Ndevices
        yTop += [yTop[-1] - Hblock + 36]


    ii_ring = 0
    for BB, yt in zip(BLOCK, yTop):
        y0 = yt
        RR = {'name': f"Rcal{ii_ring:02d}_",
                     'x0': 0,'y0': 0,'tot_length' : Wchip,'exp_w': 2,
                     'layer': [layer_ring,0, layer_waveguide, layer_stepper],
                     'RR': BB.get('R', None),
                     'Lc': BB.get('Lc', None),
                     'RWin' : BB.get('RW', None), 'RWetch': 0,
                     'G': BB.get('G', None),
                     'W': BB.get('W', None), 'Wbend':BB.get('Wdrop', 0)+0.35,
                     'Gdrop':BB.get('Gdrop', None), 'Wdrop': BB.get('Wdrop', 0),
                     'Nmodulation': BB.get('Nmodulation', None),
                     'Amodulation': BB.get('Amodulation', None),
                     'Gaussmodulation_spread': BB.get('Gaussmodulation_spread', None),
                     'Sigmamodulation': BB.get('Sigmamodulation', None),
                     'y_shift': -1*BB.get('ypitch', None),
                     'y_pos_text': 0, 'x_pos_text': -Wchip/2 + 400,
                     'label_out': True, 'x_pos_text_out': Wchip/2 - 400,
                     'input_inv_taper_st_length': 5,
                     'input_inv_taper_length': 800,
                     'input_inv_taper_W': BB.get('Wtapper', 0.15),
                     'inp_WG_L': 50,
                     'polarity': resist,
                     'donanoscribe': False, "NTopdec": 50,
                     'Wbdg': None, 'Hbdg':None, 'Bdg_layer': 98,
                     'y_blockline_dec': 6,
                     "blockline": False,
                     'do_bezier_smooth': False,
                     'do_center_etch': False,
                     'Nmod_pts': BB.get('Nmod_pts', 2000),
                     'Nfaraday': BB.get('Nfaraday', None),
                     'Wfaraday': BB.get('Wfaraday', None),
                     'Lfaraday': BB.get('Lfaraday', None),
                     'DEMS_fun': BB.get('DEMS_fun', 'Gauss'),
                     }


                     
        Cells['cell_type'].append('Gen.Ring.CreateWGRingsAddDropMutlicolor')
        Cells['param'].append(RR)
        Cells['YSHIFT'].append(copy(y0))

        # -- get the number of device to increment the field layer
        Ntot = len(BB.get('G', [0])) *  len(BB.get('RW', [0])) * len(BB.get('Lc', [0])) * \
             len(BB.get('Amodulation', [0])) * len(BB.get('Sigmamodulation', [0]))
        Wbox = 1000
        Hbox = BB.get('ypitch', None)
    
        if pars['Wbox']< Hbox:
            Hbox = pars['Wbox']
            
        Fbox = {'Name':f'Rcal{ii_ring:02d}_Fld','Hbox': Hbox,
                'Nx':1,
                'ypitch': BB.get('ypitch', Hbox),
                'Wbox': Wbox, 'y0': -2, 'layer': layerField,
                'yshift0': 5.5,#-BLOCK[0]['ypitch']/2,
                'N': Ntot, 'Wchip': Wchip}
        Cells['cell_type'].append('Gen.Misc.FieldBox')
        Cells['param'].append(Fbox)
        Cells['YSHIFT'].append(copy(y0))

        pars['layerField'] += Ntot
        #
        GdropLabell = {'name': f'Rcal{ii_ring:02d}_Lbl', 'layer': pars['layer_label'],
                     'box': True, 'font': 'Source Code Pro',
                     'font_size_pattern': 20,'txt': BB['Label'],
                     'x_pos_text': -750, 'y_pos_text': BB['ypitch'] - 30,
                     }
        Cells['cell_type'].append('Gen.Misc.CreateLabel')
        Cells['param'].append(GdropLabell)
        Cells['YSHIFT'].append(copy(y0))
        ii_ring += 1
        