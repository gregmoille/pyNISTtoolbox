def CreateBumpStruct(fid, param, ncell):
    x0, y0 = param.get('corner', None)
    W, H = param.get('w_h', None)
    rx, ry = param.get('rx_y', (0,0))
    theta = param.get('theta', 0)
    Name = param.get('name', None)
    layer = param.get('layer', None)
    datatype = param.get('datatype', 0)
    debug = param.get('debug', False)
    if debug:
        print('Creating Bump Structure: ')
        print('On the layer {}'.format(layer))
        print('W={:.3f} H={:.3f} '.format(W, H) +
              'x0={:.3f} y0={:.3f} '.format(x0, y0) +
              'rx={:.3f} ry{:.3f} '.format(rx, ry) +
              'theta={}\n'.format(theta))

    fid.write(str(layer) + ' layer\n')
    fid.write(f'{datatype} datatype\n')

    fid.write('<' + Name + 'Cell' + str(ncell) + ' struct>\n')
    fid.write('{:.3f} {:.3f} '.format(x0, y0) +
              '{:.3f} {:.3f} '.format(W, H) +
              '{:.3f} {:.3f} '.format(rx, ry) +
              '{:.3f} roundrect\n'.format(theta))

    fid.write('\n')
    fid.write(f'{0} datatype\n')
    return [Name + 'Cell' + str(ncell)]
