def CreateBumpStruct(fid, param, ncell):
    x0, y0 = param.get('corner', None)
    W, H = param.get('w_h', None)
    rx, ry = param.get('rx_y', (0,0))
    theta = param.get('theta', 0)
    Name = param.get('name', None)
    layer = param.get('layer', None)

    print('Creating Bump Structure: ')
    print('On the layer {}'.format(layer))
    print('W={:.0f} H={:.0f} '.format(W, H) +
          'x0={:.0f} y0={:.0f} '.format(x0, y0) +
          'rx={:.0f} ry{:.0f} '.format(rx, ry) +
          'theta={}\n'.format(theta))

    fid.write(str(layer) + ' layer\n')
    fid.write('<' + Name + 'Cell' + str(ncell) + ' struct>\n')
    fid.write('{:.0f} {:.0f} '.format(x0, y0) +
              '{:.0f} {:.0f} '.format(W, H) +
              '{:.0f} {:.0f} '.format(rx, ry) +
              '{:.0f} roundrect\n'.format(theta))

    fid.write('\n')
    return [Name + 'Cell' + str(ncell)]

