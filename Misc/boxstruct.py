def CreateBox(fid, param, ncell):
    x0, y0 = param.get('LeftTop', (0,0))
    x1, y1 = param.get('RightBottom', (0,0))
    Name = param.get('Name', 'Bbox')
    layer = param.get('layer', 2)
    print('Creating Box Structure: ')
    print('On the layer {}'.format(layer))

    fid.write(str(layer) + ' layer\n')
    fid.write('<' + Name + 'Cell' + str(ncell) + ' struct>\n')
    fid.write('{:.0f} {:.0f} '.format(x0, y0) +
              '{:.0f} {:.0f} '.format(x1, y0) +
              '{:.0f} {:.0f} '.format(x1, y1) +
              '{:.0f} {:.0f} '.format(x0, y1) +
              'points2shape\n')

    fid.write('\n')
    return [Name + 'Cell' + str(ncell)]

