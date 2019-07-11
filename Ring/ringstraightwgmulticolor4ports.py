import numpy as np
from copy import copy
from NISTgenerator.Port import CreatePortShapeSymmetric
from NISTgenerator.Misc.label import CreateLabel
import ipdb
def CreateWGRingMultiColorStraightWg4ports(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)

    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    exp_w = param.get('exp_w', None)
    tot_length = param.get('tot_length',3850)
    # Ring parameter
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    nr = param.get('nr', 1000)
    # Coupling Parameter

    G1 = param.get('G1', None)
    G2 = param.get('G2', None)
    W1 = param.get('W1', None)
    W2 = param.get('W2', None)

    # Waveguides parameters
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', None)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', None)
    output_inv_taper_length = param.get('output_inv_taper_length', None)
    output_inv_taper_W = param.get('output_inv_taper_W', None)

    PortDist = param.get('PortDist', 10)
    rEtch = param.get('rEtch', None)
    RWETCH = param.get('rwEtch', None)
    RWIN = param.get('rwIn', None)
    WetchAdd = param.get('WetchAdd', 0)
    x_pos_text = param.get('x_pos_text', -1000)
    y_pos_text = param.get('y_pos_text', -20)

    inp_WG_L = param.get('inp_WG_L', None)
    W = param.get('W', None)

    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)



    params_port = copy(param)

    if not type(G1) == list:
        G1 = [G1]
    if not type(RR) == list:
        RR = [RR]
    if not type(RWETCH) == list:
        RWETCH = [RWETCH]
    if not type(RWIN) == list:
        RWIN = [RWIN]

    if not type(layer) == list:
        layer = [layer, layer]
    elif len(layer) == 1:
        layer = [layer[0], layer[0]]

    name_out = []

    cnt = 0
    cnt_gap = -1
    name_out = []
    name_loop = []

    print('------------------------------------')
    for g in G1:
        cnt_gap += 1
        for rr in RR:
            for rwIn in RWIN:
                for rwetch in RWETCH:

                    rw = rwetch  + rwIn
                    name_out = []
                    y_pos = y_shift * cnt + y0 + cnt_gap*1.5*y_shift
                    y_txt = y_pos + y_pos_text

                    print('Creating Straight and Pulley WG coupled to RR step profile: ')
                    print('\tOn the layer {}'.format(layer))
                    print('\tRR={} Win={:.3f} '.format(rr, rwIn) +
                          'Wout={:.3f} g={}\n'.format(rwetch, g))

                    fid.write(str(layer[0]) + ' layer\n')

                    # Create Through Port
                    params_through = copy(param)
                    params_through['name'] = Name + 'Th' + str(cnt)
                    params_through['y0'] = y_pos
                    params_through['y_connect'] = y_pos + rr + g + W1/2
                    params_through['W'] = W1
                    params_through['drop_through'] = 1
                    params_through['input_inv_taper_W'] = param['input_inv_taper_W'][0]
                    name_out += CreatePortShapeSymmetric(fid, params_through, ncell, cnt)

                    # Create Drop port Port
                    params_drop = copy(param)
                    params_drop['name'] = Name + 'Drop' + str(cnt)
                    params_drop['y0'] = y_pos
                    params_drop['y_connect'] = y_pos - rr - G2 - W2/2

                    params_drop['W'] = W2
                    params_drop['drop_through'] = -1
                    params_drop['input_inv_taper_W'] = param['input_inv_taper_W'][1]
                    name_out += CreatePortShapeSymmetric(fid, params_drop, ncell, cnt)

                    # Create  Ring
                    Ls = inp_WG_L
                    name_out.append(
                        Name + 'Ring' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'Ring' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<{} {} '.format(-x0, y_pos) +
                              '{} {} {} '.format(rr, rw, exp_w) +
                              '{} {} '.format(G2, Ls) +
                              '{} {} '.format(W2, exp_w) +
                              '{} {} '.format(g, Ls) +
                              '{} {} '.format(W1, exp_w) +
                              '0 ringInfInvPosDSV>\n')


                    # <x y ri Wr re g1 Lc W1 We1 LS g2 W2 We2 L2 EC ringPulInvPLCADSV>

                    # Create the Etch Step
                    if rwetch>0.1:

                        fid.write(str(layer[1]) + ' layer\n')
                        name_out.append(
                            Name + 'RingEtch' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'RingEtch' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('{} {} '.format(x0, y_pos) +
                                  '{} {} {} '.format(rEtch+WetchAdd/2-(rwetch)/2, rwetch+WetchAdd, 0) +
                                  '{} {} '.format(360, nr) +
                                  'torusW\n')

                    fid.write(str(layer[0]) + ' layer\n')

                    # Create the label
                    txt = 'RR={}um Win={:.3f}um Wout={:.3f}'.format(rr, rwIn, rwetch) + \
                        ' G={:.0f}nm'.format(g*1e3)
                    par_lab = {'x_pos_text': input_inv_taper_length/2+15,
                               'y_pos_text': y_txt,
                               'txt': txt,
                               'font_size_pattern': 7,
                               'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}


                    name_out += CreateLabel(fid, par_lab, ncell)

                    # Create bottom block waveguide
                    yblock = y_pos - rr - G2 - W2/2 - 20
                    x1_in_lin = 0
                    name_out.append(
                        Name + 'BottomBlock_' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'BottomBlock_' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<{} {} '.format(x1_in_lin-50, yblock) +
                                  '{} {} '.format(x1_in_lin + tot_length+50, yblock) +
                                  '1 0 0 0 waveguide>\n')




                    subcell = 'RR{}RW{:.3f}G{}'.format(rr, rw, g)
                    subcell = subcell.replace('.', 'p')
                    fid.write('<' + subcell + '_' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    for n in name_out:
                        # need to rotate the ring
                        if n ==  Name + 'Ring' + str(ncell) + '_' + str(cnt):
                            fid.write('\t<' + n + ' {} {} 0 1 180 instance>\n'.format(0,2*y_pos))
                        else:
                            fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')
                    fid.write('\n')
                    name_loop.append(
                        subcell + '_' + str(ncell) + '_' + str(cnt))

                    cnt += 1
    fid.write('<RingPulleyWg_MainCell' + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')

    return ['RingPulleyWg_MainCell' + str(ncell)]
