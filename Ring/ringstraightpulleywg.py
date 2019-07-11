import numpy as np
from copy import copy
from NISTgenerator.Port import CreateThroughDropPort
from NISTgenerator.Misc.label import CreateLabel

def CreateStraightPulleyWgCutOff(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    G = param.get('G', None)
    G2 = param.get('G2', None)
    W2 = param.get('W2', None)
    LC = param.get('Lc', None)
    x0 = param.get('x0', 0)
    y0 = param.get('y0', None)
    Rbend = param.get('Rbend', None)
    tot_length = param.get('tot_length',3850)

    
    x_pos_text = param.get('x_pos_text', -1000)
    y_pos_text = param.get('y_pos_text', -20)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)

    st_WG_Lc = param.get('st_WG_Lc', 2*inp_WG_L)
    W = param.get('W', None)
    exp_w = param.get('exp_w', None)
    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)

    WG_drop_port_U_bend_radius = param.get('WG_drop_port_U_bend_radius', 100)

    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', 5)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', None)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', 5)
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
    # if not type(layer) == li
    #     layer = [layer, layer]st:
 
    name_out = []

    cnt = 0
    name_out = []
    name_loop = []
    
    print('------------------------------------')
    for rr in RR:
        for lc in LC:
            for g in G:
                for rw in RW:
                    print('Creating Ring with Pulley WG: ')
                    print('On the layer {}'.format(layer))
                    print('RR={} RW={} '.format(rr, rw) +
                          'g={} Lc={} '.format(g, lc))

                    fid.write(str(layer) + ' layer\n')

                    y_pos = y_shift * cnt + y0
                    WG_through_port_y_pos = y_pos+rr+g+W/2-2 * \
                        (1-np.cos(lc/(rr+g+W/2)/2))*(rr+g+W/2)
                    x_xtx = x0 + x_pos_text
                    y_txt = y_pos + y_pos_text
                    Ls = inp_WG_L-2*np.sin(lc/(rr+g+W/2)/2)*(rr+g+W/2)
                    name_out = []

                    # Create the Through port
                    params_port['Dodichro'] = False
                    params_port['name'] = Name + '_' + str(cnt)
                    params_port['RR'] = rr
                    params_port['G'] = g
                    params_port['st_WG_Lc'] = st_WG_Lc
                    params_port['RW'] = rw
                    params_port[
                        'WG_through_port_y_pos'] = y_pos+rr+g + W/2
                    params_port['y_drop_in'] = y_pos-rr-G2-W2/2+2* \
                        (1-np.cos(lc/(rr+G2+W2/2)/2))*(rr+G2+W2/2)

                    params_port['y_pos'] = y_pos
                    params_port['Ls'] = Ls
                    params_port['Rbend'] = Rbend
                    params_port['W2'] = W2
                    params_port['W'] = W
                    params_port['y_drop_out']= params_port['y_drop_in'] - 2*params_port['Rbend']
                    name_out += CreateThroughDropPort(fid, params_port, ncell, cnt)

                    # Create Pulley Ring
                    #<x y ri Wr re N g Lc Nwg W We LS EC ringPulleyInvPosLCA>
                    
                    name_out.append(
                        Name + 'Cell' + str(ncell) + '_' + str(cnt))
                    # fid.write('<' + Name + 'Cell' + str(ncell) +
                    #           '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<Ring' + Name + 'Cell' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t\t<{} {} '.format(x0, y_pos) +
                                  '{} {} {} '.format(rr, rw, exp_w) +
                                  '{} {} '.format(G2, lc) +
                                  '{} {} '.format(W2, exp_w) +
                                  '{} {} {} '.format(Ls, g, W) +
                                  '{} {} '.format(exp_w, 2*inp_WG_L) +
                                  '0 ringPulInvPLCADSV>\n')
                    fid.write('<' + Name + 'Cell' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<Ring' + Name + 'Cell' + str(ncell) +
                              '_' + str(cnt) + ' ')
                    fid.write('{:.3f} {:.3f} 0 1 180 instance>\n'.format(x0,2*y_pos))
                    # Create the label
                    txt = 'RR={}um RW={:.3f}um '.format(rr, rw) + \
                        'G={:.3f}um Lc ={:.0f}um '.format(g, lc)
                    par_lab = {'x_pos_text': x_pos_text,
                               'y_pos_text': y_txt,
                               'txt': txt,
                               'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}

                    name_out += CreateLabel(fid, par_lab, ncell)

                    # Create Bottom block waveguide
                    y_drop_out = y_pos - rr - G2 -\
                                    W2/2 - \
                                    2*Rbend

                    x1_in_lin = x0 - inp_WG_L - input_st_length - output_inv_taper_length
                    name_out.append(
                        Name + 'BotBlocking_' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'BotBlocking_' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<{} {} '.format(x1_in_lin - 50, y_drop_out - 15) +
                                  '{} {} '.format(x1_in_lin + tot_length + 50, y_drop_out- 15) +
                                  '1 0 0 0 waveguide>\n')


                    subcell = 'RR{}RW{:.3f}G{}LC{}'.format(rr, rw, g, lc)
                    subcell = subcell.replace('.', 'p')
                    fid.write('<' + subcell + '_' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    for n in name_out:
                        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')
                    fid.write('\n')
                    name_loop.append(
                        subcell + '_' + str(ncell) + '_' + str(cnt))

                    cnt += 1





    fid.write('<RingPulleyWg_MainCell' + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')
    fid.write('# ******************************\n')
    return ['RingPulleyWg_MainCell' + str(ncell)]
