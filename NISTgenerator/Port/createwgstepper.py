import numpy as np
from copy import copy
from NISTgenerator.Port import CreateThroughPort

def CreateWgStepper(fid, param, ncell):
    # params['layer'] = layer_waveguide
    param['layerWg'] = param['layer']
    param['layerTapper'] = param['layer']
    param['Name'] = param['name']
    param['input_inv_taper_length'] = param['Ltapper']
    param['input_inv_taper_W'] = param['Wtapper']
    param['resist'] = 'negative'
    param['tot_length'] = param['Wchip'] - 2*param['EBLtapper']
    param['x0'] = 0
    param['y0'] = 0
    param['cap'] = False
    # params_port['WG_drop_port_y_pos'] = WG_drop_port_y_pos
    # params_port['WG_through_port_y_pos'] = WG_through_port_y_pos
    name_out = CreateThroughPort(fid, param, ncell, 0)[0]


    N = int(param['Hchip']/param['ypitch'])

    fid.write(f"<{param['name']}_{ncell} struct>\n")
    yy = 0
    for nn in range(N):
        yy -= param['ypitch']
        fid.write(f'\t<{name_out} 0 {yy} 0 1 0 instance>\n')


    return [f"{param['name']}_{ncell}"]
