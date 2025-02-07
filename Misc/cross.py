from NISTgenerator.Misc.label import CreateLabel

def CrossAlign(fid, param, ncell):

    layer = param.get('layer', 1)
    L = param.get('L', 200)
    W = param.get('W', 2)
    x0 = param.get('x0', 0)
    y0 = param.get('y0', 0)
    dot = param.get('dot', False)
    lbl = param.get('lbl', None)
    font_size_pattern = param.get('font_size_pattern', 12)
    font = param.get('font', 'Source Code Pro')
    circle = param.get('circle', True)
    Name = param.get('name', None)
    if not type(x0) == list:
        x0 = [x0]
    if not type(y0) == list:
        y0 = [y0]


    fid.write(str(layer) + ' layer\n')
    name_out = []
    cnt = 0
    for x, y in zip(x0, y0):
        fid.write('<' + Name  + 'Cr' + str(cnt) + '_' + str(ncell) + ' struct>\n')
        name_out += [Name  + 'Cr' + str(cnt) + '_'+   str(ncell)]
        fid.write('\t{:.3f} {:.3f} '.format(x, y) +
                  '{:.3f} {:.3f} '.format(W, L) +
                  '{:.3f} {:.3f} '.format(W, W) +
                  '0 roundrectC\n' )

        fid.write('\t{:.3f} {:.3f} '.format(x, y) +
                  '{:.3f} {:.3f} '.format(L, W) +
                  '{:.3f} {:.3f} '.format(W, W) +
                  '0 roundrectC\n' )
        if circle:
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
        if lbl:
            par_lab = {'x_pos_text': x+L/3,
                       'y_pos_text': y+L/3,
                       'txt': lbl,
                       'font': font,
                       'font_size_pattern': font_size_pattern,
                       'name': Name + 'Lbl_' + str(ncell)}
            name_out += CreateLabel(fid, par_lab, ncell)

    fid.write('<' + Name + str(ncell) + ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    return [Name + str(ncell)]
