import numpy as np
from copy import copy
from NISTgenerator.Port import CreateThroughPort
from NISTgenerator.Misc.label import CreateLabel

def CreateWGRingMultiColorPulleyWg(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    G = param.get('G', None)
    LC = param.get('Lc', None)
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    rEtch = param.get('rEtch', None)
    rwEtch = param.get('rwEtch', None)
    x_pos_text = param.get('x_pos_text', -1000)
    y_pos_text = param.get('y_pos_text', -20)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)
    W = param.get('W', None)
    exp_w = param.get('exp_w', None)
    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)

    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', None)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', None)
    output_inv_taper_length = param.get('output_inv_taper_length', None)
    output_inv_taper_W = param.get('output_inv_taper_W', None)

    params_port = copy(param)

    if not type(G) == list:
        G = [G]
    if not type(RR) == list:
        RR = [RR]
    if not type(RW) == list:
        RW = [RW]
    if not type(LC) == list:
        LC = [LC]
    if not type(layer) == list:
        layer = [layer, layer]
    elif len(layer) == 1:
        layer = [layer[0], layer[0]]

    name_out = []

    cnt = 0
    name_out = []
    name_loop = []
    
    print('------------------------------------')
    for lc in LC:
        for g in G:
            for rw in RW:
                for rr in RR:

                    print('Creating Pulley WG coupled to RR: ')
                    print('On the layer {}'.format(layer))
                    print('RR={} RW={} '.format(rr, rw) +
                          'g={} Lc={}\n'.format(g, lc))

                    fid.write(str(layer[0]) + ' layer\n')

                    y_pos = y_shift * cnt + y0
                    WG_through_port_y_pos = y_pos+rr+g+W/2-2 * \
                        (1-np.cos(lc/(rr+g+W/2)/2))*(rr+g+W/2)
                    x_xtx = x0 + x_pos_text
                    y_txt = y_pos + y_pos_text
                    name_out = []

                    # Create the Through port
                    params_port['name'] = Name + '_' + str(cnt)
                    params_port['RR'] = rr
                    params_port['G'] = g
                    params_port['RW'] = rw
                    params_port[
                        'WG_through_port_y_pos'] = WG_through_port_y_pos
                    name_out += CreateThroughPort(fid, params_port, ncell)

                    # Create Pulley Ring
                    #<x y ri Wr re N g Lc Nwg W We LS EC ringPulleyInvPosLCA>
                    Ls = inp_WG_L-2*np.sin(lc/(rr+g+W/2)/2)*(rr+g+W/2)
                    name_out.append(
                        Name + 'Cell' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'Cell' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('<{} {} '.format(x0, y_pos) +
                              '{} {} {} '.format(rr, rw, exp_w) +
                              '{} {} {} '.format(nr, g, lc) +
                              '{} {} {} '.format(nr, W, exp_w) +
                              '{} '.format(Ls) +
                              '0 ringPulleyInvPosLCA>\n')

                    # Create the Etch Step
                    fid.write(str(layer[1]) + ' layer\n')
                    name_out.append(
                        Name + 'Cell_Etch' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'Cell_Etch' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('{} {} '.format(x0, y_pos) +
                              '{} {} {} '.format(rEtch, rwEtch, 0) +
                              '{} {} '.format(360, nr) +
                              'torusW\n')

                    fid.write(str(layer[0]) + ' layer\n')
        
                    # Create the label
                    txt = 'RR={}um RW={:.3f}um '.format(rr, rw) + \
                        'G={:.3f}um Lc ={:.0f}um'.format(g, lc)
                    par_lab = {'x_pos_text': x_pos_text,
                               'y_pos_text': y_txt,
                               'txt': txt,
                               'Name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}

                    name_out += CreateLabel(fid, par_lab, ncell)
    
    
                    subcell = 'RR{}RW{}G{}LC'.format(rr, rw, g, lc)
                    subcell = subcell.replace('.', 'p')
                    fid.write('<' + subcell + '_' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    for n in name_out:
                        fid.write('<' + n + ' 0 0 0 1 0 instance>\n')
                    fid.write('\n')
                    name_loop.append(
                        subcell + '_' + str(ncell) + '_' + str(cnt))

                    cnt += 1
    fid.write('<RingPulleyWg_MainCell' + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')

    return ['RingPulleyWg_MainCell' + str(ncell)]
