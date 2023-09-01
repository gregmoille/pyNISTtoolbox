import numpy as np
from copy import copy
from NISTgenerator.Misc import CreateBumpStruct

def FieldBox(fid, param, ncell):
    Nx = param.get('Nx', 3)
    Name = param.get('Name', 'Fld_')
    Wbox = param.get('Wbox', 1e3)
    y0 = param.get('y0', None)
    ypitch = param.get('ypitch', None)
    Hbox = param.get('Hbox', 85)
    layer = param.get('layer', 1)
    yshift0 = param.get('yshift0', 41.5)
    increment = param.get('increment', True)
    Wchip = param.get('Wchip', None) + 100
    N = param.get('N', 0)
    name_out = []
    y0original = copy(y0)
    # y0 = 0
    # print(f'Increment {increment}')
    for ii in range(N):
        y = y0 - ii*ypitch
        if Wchip:
            NBox1_2 = np.ceil(0.5*Wchip/Wbox +0.5)
            for nn in np.arange(NBox1_2):
                BoundingParam = {'name': Name,
                                 'layer': layer,
                                 'corner': (-Wbox/2 + nn*Wbox , y-Hbox),
                                 'w_h': (Wbox,np.abs(Hbox)),
                                 'Yspace': 0,
                                 'Xspace': 0,
                                 }
                name_out += CreateBumpStruct(fid, BoundingParam, ncell)
            #
            for nn in np.arange(1,NBox1_2):
                BoundingParam = {'name': Name,
                                 'layer': layer,
                                 'corner': (-Wbox/2 - nn* Wbox , y-Hbox),
                                 'w_h': (Wbox,np.abs(Hbox)),
                                 'Yspace': 0,
                                 'Xspace': 0,
                                 }
                name_out += CreateBumpStruct(fid, BoundingParam, ncell)

        else:
            BoundingParam = {'name': Name,
                             'layer': layer,
                             'corner': (-Wbox/2, y-Hbox),
                             'w_h': (Wbox,np.abs(Hbox)),
                             'Yspace': 0,
                             'Xspace': 0,
                             }
            name_out += CreateBumpStruct(fid, BoundingParam, ncell)
            if Nx ==3:
                BoundingParam = {'name': Name,
                                 'layer': layer,
                                 'corner': (-3*Wbox/2, y-Hbox),
                                 'w_h': (Wbox,np.abs(Hbox)),
                                 'Yspace': 0,
                                 'Xspace': 0,
                                 }
                name_out += CreateBumpStruct(fid, BoundingParam, ncell)

                BoundingParam = {'name': Name,
                                 'layer': layer,
                                 'corner': (Wbox/2, y-Hbox),
                                 'w_h': (Wbox,np.abs(Hbox)),
                                 'Yspace': 0,
                                 'Xspace': 0,
                                 }

                name_out += CreateBumpStruct(fid, BoundingParam, ncell)

        if increment:
            layer += 1
    fid.write('<' + Name + str(ncell) + ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 {:.3f} 0 1 0 instance>\n'.format(yshift0))

    return [Name + str(ncell)]
