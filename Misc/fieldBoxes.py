import numpy as np
from copy import copy
from NISTgenerator.Misc import CreateBumpStruct

def FieldBox(fid, param, ncell):
    Nx = param.get('Nx', 3)
    Name = param.get('Name', 'Fld_')
    Wbox = param.get('Wbox', 1e3)
    y0 = param.get('y0', None)
    Hbox = param.get('Hbox', 85)
    layer = param.get('layer', 1)
    yshift0 = param.get('yshift0', 43)
    N = param.get('N', 0)
    name_out = []
    y0original = copy(y0)
    y0 = 0
    for ii in range(N):
        y = y0 +43 - ii*Hbox

        if Nx ==3:
            BoundingParam = {'name': Name,
                             'layer': layer,
                             'corner': (-Wbox/2, y-Hbox),
                             'w_h': (Wbox,np.abs(Hbox)),
                             'Yspace': 0,
                             'Xspace': 0,
                             }
            name_out += CreateBumpStruct(fid, BoundingParam, ncell)

        BoundingParam = {'name': Name,
                         'layer': layer,
                         'corner': (-3*Wbox/2, y-Hbox),
                         'w_h': (Wbox,np.abs(Hbox)),
                         'Yspace': 0,
                         'Xspace': 0,
                         }

        name_out += CreateBumpStruct(fid, BoundingParam, ncell)

        if Nx ==3:
            BoundingParam = {'name': Name,
                             'layer': layer,
                             'corner': (Wbox/2, y-Hbox),
                             'w_h': (Wbox,np.abs(Hbox)),
                             'Yspace': 0,
                             'Xspace': 0,
                             }

            name_out += CreateBumpStruct(fid, BoundingParam, ncell)

        layer += 1
    fid.write('<' + Name + str(ncell) + ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 {:.3f} 0 1 0 instance>\n'.format(yshift0))

    return [Name + str(ncell)]
