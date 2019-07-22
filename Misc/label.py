def CreateLabel(fid, param, ncell):


    txt = param.get('txt', 'NONE')

    x_pos_text = param.get('x_pos_text', None)
    y_pos_text = param.get('y_pos_text', None)
    theta = param.get('theta', 0)
    margin_fact = param.get('margin_fact', 0.6)
    nr = param.get('nr', 1000)
    Name = param.get('name', None)
    layer = param.get('layer', 1)
    box = param.get('box', True)
    font = param.get('font', 'Arial')
    font_size_pattern = param.get('font_size_pattern', 10)
    name_out = []
    n_txt = len(txt)
    fid.write(str(layer) + ' layer\n')


    fid.write('<LlTxt' + Name + str(ncell) + ' struct>\n')
    name_out.append('LlTxt' + Name + str(ncell))
    fid.write('\t')
    fid.write(r'<{{{{ {} }}}} '.format(txt) +
              r'{{{{{}}}}} {} '.format(font,font_size_pattern) +
              '{} {} textgdsC>\n'.format(x_pos_text, y_pos_text))

    # Create the box around label
    if box:
        fid.write('<LblArnd_' + Name + str(ncell) + ' struct>\n')
        name_out.append('LblArnd_' + Name + str(ncell))
        fid.write('\t<{} {} '.format(x_pos_text, y_pos_text) +
                  '{} 1 {} 0 '.format(n_txt*font_size_pattern*margin_fact, 0.75*font_size_pattern) +
                  '{} raceTrack>\n'.format(nr))

    fid.write('<' +  Name + str(ncell) +
              ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 {:.0f} instance>\n'.format(theta))
    fid.write('\n')

    fid.write('# ******************************\n')
    return [Name + str(ncell)]
