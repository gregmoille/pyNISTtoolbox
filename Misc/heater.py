import numpy as np

def CreateHeater(fid, param, ncell):
    file = param.get('file', None)
    Name = param.get('name', None)
    layer = param.get('layer', None)
    N = param.get('N', 1)
    x0 = param.get('x0', 0)
    y0 = param.get('y0', 0)
    y_shift = param.get('y_shift', 100)
    xmir = param.get('xmiror',1)

    if not type(file) == list:
        file = [file]
    if not type(xmir) == list:
        xmir = [xmir] * len(file)


    fid.write(str(layer) + ' layer\n')
    x = {}
    y = {}
    for nf in range(0, len(file)):
        lines = open(file[nf], 'r').readlines()
        x['f' + str(nf)] = x0 + np.array([1e6*float(ii.split()[0])
                                          for ii in lines])
        y['f' + str(nf)] = y0 + np.array([1e6*float(ii.split()[1])
                                          for ii in lines])

    name_loop = []
    print('------------------------------------')
    for ii in range(0, N):
        print('Create Heater shifted by y_shift: {}um'.format(ii*y_shift))
        name_part = []
        for nfile in range(0, len(file)):
            fid.write('<HeaterPart_' + Name + str(ncell) +
                      '_' + str(ii) + '_' + str(nfile) + ' struct>\n')
            name_part.append('HeaterPart_' + Name + str(ncell) +
                             '_' + str(ii) + '_' + str(nfile))
            fid.write('\t')
            for n in range(0, len(x['f' + str(nfile)])):
                fid.write('{} {} '.format(xmir[nfile]*x['f' + str(nfile)][n],
                                          y['f' + str(nfile)][n]))
            fid.write(' points2shape\n')

        fid.write('<Heater_' + Name + str(ncell) + '_' + str(ii) + ' struct>\n')
        name_loop.append('Heater_' + Name + str(ncell) + '_' + str(ii))
        for part in name_part:
            fid.write('<' + part + ' 0 0 0 1 0 instance>\n')

        for k in y.keys():
            y[k] = y[k] + y_shift

    fid.write('<Heater_MainCell' + Name + str(ncell) + ' struct>\n')
    # ipdb.set_trace()
    for nme in name_loop:
        fid.write('\t<' + nme + ' 0 0 0 1 0 instance>\n')

    fid.write('# ******************************\n')
    return ['Heater_MainCell' + Name + str(ncell)]
