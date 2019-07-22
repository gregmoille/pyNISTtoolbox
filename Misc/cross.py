def CrossAlign(fid, param, ncell):

    layer = param.get('layer', 1)
    L = param.get('L', 200)
    W = param.get('W', 2)
    x0 = param.get('x0', 0)
    y0 = param.get('y0', 0)
    dot = param.get('dot', False)
    Name = param.get('name', None)

    if not type(x0) == list:
        x0 = [x0]
    if not type(y0) == list:
        y0 = [y0]

    fid.write('<' + Name  + str(ncell) + ' struct>\n')
    fid.write(str(layer) + ' layer\n')

    for x, y in zip(x0, y0):
        fid.write('\t{:.3f} {:.3f} '.format(x, y) +
                  '{:.3f} {:.3f} '.format(W, L) +
                  '{:.3f} {:.3f} '.format(W, W) +
                  '0 roundrectC\n' )

        fid.write('\t{:.3f} {:.3f} '.format(x, y) +
                  '{:.3f} {:.3f} '.format(L, W) +
                  '{:.3f} {:.3f} '.format(W, W) +
                  '0 roundrectC\n' )

        fid.write('\t{:.3f} {:.3f} '.format(x, y) +
                  '{:.3f} {:.3f} {} '.format(W/2, L*1.1,0) +
                  '{:.3f} {:.3f} '.format(360, 1000) +
                  'torusW\n' )

        if dot:
            for ii in range(dot['N']):
                fid.write('\t{:.3f} {:.3f} '.format(x+L/3, y+L/3 - ii*dot['shift']) +
                          '{:.3f} {:.3f} {} '.format(dot['R'], dot['W'] ,0) +
                          '{:.3f} {:.3f} '.format(360, 1000) +
                          'torusW\n' )



    return [Name + str(ncell)]
