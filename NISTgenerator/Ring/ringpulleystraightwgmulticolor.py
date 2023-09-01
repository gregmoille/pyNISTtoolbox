import numpy as np
from copy import copy
import pdb
from NISTgenerator.Port import CreateThroughDropPort
from NISTgenerator.Misc.label import CreateLabel

def CreateWGRingMultiColorPulleyStraightWg(fid, param, ncell):
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

    tot_length = param.get('tot_length',3850)

    st_WG_Lc = param.get('st_WG_Lc', None)

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
    if not type(rEtch) == list:
        rEtch = [rEtch]
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
                    for _retch in rEtch:

                        print('Creating Notch Ring with Pulley WG: ')
                        print('On the layer {}'.format(layer))
                        print('RR={} RW={} '.format(rr, rw) +
                              'g={} Lc={} '.format(g, lc) + 
                              'Wout={:.3f}\n'.format(rr-_retch))

                        fid.write(str(layer[0]) + ' layer\n')

                        y_pos = y_shift * cnt + y0
                        WG_through_port_y_pos = y_pos+rr+g+W/2-2 * \
                            (1-np.cos(lc/(rr+g+W/2)/2))*(rr+g+W/2)
                        x_xtx = x0 + x_pos_text
                        y_txt = y_pos + y_pos_text
                        Ls = inp_WG_L-2*np.sin(lc/(rr+g+W/2)/2)*(rr+g+W/2)
                        name_out = []

                        # Create the Through port
                        params_port['Name'] = Name + '_' + str(cnt)
                        params_port['RR'] = rr
                        params_port['G'] = g
                        params_port['RW'] = rw
                        params_port[
                            'WG_through_port_y_pos'] = WG_through_port_y_pos
                        params_port['y_pos'] = y_pos
                        params_port['Ls'] = Ls
                        name_out += CreateThroughDropPort(fid, params_port, ncell, cnt)

                        # Create Pulley Ring
                        #<x y ri Wr re N g Lc Nwg W We LS EC ringPulleyInvPosLCA>
                        
                        name_out.append(
                            Name + 'Cell' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'Cell' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                  '{} {} {} '.format(rr, rw, exp_w) +
                                  '{} {} {} '.format(nr, g, lc) +
                                  '{} {} {} '.format(nr, W, exp_w) +
                                  '{} '.format(Ls) +
                                  '{} {} '.format(G2, W2) +
                                  '{} {} '.format(exp_w, st_WG_Lc) + 
                                  '0 ringPulInvPLCADS>\n')

                        # Create the Etch Step
                        fid.write(str(layer[1]) + ' layer\n')
                        name_out.append(
                            Name + 'Cell_Etch' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'Cell_Etch' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('\t{} {} '.format(x0, y_pos) +
                                  '{} {} {} '.format(_retch - rwEtch/2, rwEtch, 0) +
                                  '{} {} '.format(360, nr) +
                                  'torusW\n')

                        fid.write(str(layer[0]) + ' layer\n')
            
                        # Create the label
                        txt = 'RR={}um RW={:.3f}um '.format(rr, rw) + \
                            'G={:.3f}um Lc ={:.0f}um '.format(g, lc) + \
                            'Wout={:.2f}um'.format(rr-_retch)
                        par_lab = {'x_pos_text': x_pos_text,
                                   'y_pos_text': y_txt,
                                   'txt': txt,
                                   'Name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}

                        name_out += CreateLabel(fid, par_lab, ncell)
        

                        # Create top block waveguide
                        x1_in_lin = x0 - inp_WG_L - input_st_length - output_inv_taper_length
                        name_out.append(
                            Name + 'TopBlocking_' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'TopBlocking_' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('\t<{} {} '.format(x1_in_lin, y_pos + rr/2  + 50) +
                                      '{} {} '.format(x1_in_lin + tot_length, y_pos +  rr/2  + 50) +
                                      '1 0 0 0 waveguide>\n')

                        # Create Bottom block waveguide
                        y_drop_out = y_pos - rr - G2 -\
                                        W2/2 - \
                                        2*WG_drop_port_U_bend_radius

                        x1_in_lin = x0 - inp_WG_L - input_st_length - output_inv_taper_length
                        name_out.append(
                            Name + 'BottomBlocking_' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'BottomBlocking_' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('\t<{} {} '.format(x1_in_lin, y_drop_out - 30) +
                                      '{} {} '.format(x1_in_lin + tot_length, y_drop_out- 30) +
                                      '1 0 0 0 waveguide>\n')


                        subcell = 'RR{}RW{}G{}LC{}Wout{:.3f}'.format(rr, rw, g, lc,rr-_retch)
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

    return ['RingPulleyWg_MainCell' + str(ncell)]
