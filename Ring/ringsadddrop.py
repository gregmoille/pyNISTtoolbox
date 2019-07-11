from copy import copy
import ipdb
import numpy as np
from NISTgenerator.Port import CreateThroughDropPortSeparated
from NISTgenerator.Misc.label import CreateLabel


def CreateWGRingsAddDrop(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    RR = param.get('RR', None)

    RW = param.get('RW', None)

    Nmodulation = param.get('Nmodulation', None)
    Amodulation = param.get('Amodulation', None)

    W = param.get('W', None)
    Wbend = param.get('Wbend', W)
    G = param.get('G', None)

    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    x_pos_text = param.get('x_pos_text', -1000)

    y_pos_text = param.get('y_pos_text', -20)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)

    exp_w = param.get('exp_w', None)
    exp_w_tapper = param.get('exp_w_tapper',exp_w )
    font_size_pattern = param.get('font_size_pattern', 10)
    font = param.get('font', 'Source Code Pro')

    y_shift = param.get('y_shift', 0)
    input_inv_taper_length = param.get('input_inv_taper_length', 200)
    input_st_length = param.get('input_st_length', 10)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', input_st_length)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', input_inv_taper_st_length)
    output_inv_taper_length = param.get('output_inv_taper_length', input_inv_taper_length)
    output_inv_taper_W = param.get('output_inv_taper_W', None)
    blockline = param.get('blockline', True)
    dec_block = param.get('dec_block', 0)
    in_tap_etch = param.get('in_tap_etch', 0)

    tapperLength = param.get('tapperLength', None)
    label_out = param.get('label_out', False)
    x_pos_text_out = param.get('x_pos_text_out', 1500)
    tot_length = param.get('tot_length',3850)

    params_port = copy(param)

    if not type(G) == list:
        G = [G]
    if not type(RR) == list:
        RR = [RR]
    if not type(RW) == list:
        RW = [RW]

    cnt = 0
    # fid.write('<' + Name +  'Array struct>\n' )
    # fid.write(str(layer) + ' layer\n')
    print('------------------------------------')

    fid.write('{} layer\n'.format(layer))
    name_loop = []





    for g in G:
        for rr in RR:
            for rw in RW:

                name_out = []
                print('Creating Straight WG coupled to RR: ')
                print('On the layer {}'.format(layer))
                print('RR={} RW={} '.format(rr, rw) +
                      'g={}\n'.format(g))

                y_pos = y_shift * cnt + y0
                x_xtx = x0 + x_pos_text
                y_txt = y_pos + y_pos_text

                # Create the Through port
                WG_through_port_y_pos = y_pos + rr + g + W/2
                params_port['name'] = Name + '_' + str(cnt)
                params_port['RR'] = rr
                params_port['G'] = g
                params_port['RW'] = rw

                params_port['in_tap_etch'] = in_tap_etch
                params_port['WG_through_port_y_pos'] = WG_through_port_y_pos
                params_port['WG_drop_port_y_pos'] = y_pos - rr - g - W/2
                params_port['layer'] = layer
                params_port['Wbend'] = Wbend

                name_out += CreateThroughDropPortSeparated(fid, params_port, ncell, cnt)

                # Create the ring


                if not Nmodulation:
                    name_out.append(Name + 'Cell' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'Cell' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')

                    fid.write('\t<{} {} '.format(x0, y_pos) +
                              '{} {} {} '.format(rr, rw, exp_w) +
                              '{} {} '.format(g, 2*inp_WG_L) +
                              '{} {} '.format(W, exp_w) +
                              '{} {} '.format(g, 2*inp_WG_L) +
                              '{} {} '.format(W, exp_w) +
                              '0 ringInfInvPosDSV>\n')

                    fid.write('\t{} {} '.format(x0, y_pos) +
                              '{} {} '.format(rr/2 - 2, rr/2) +
                              'torusVector\n')

                    Wcut = 2
                    xcut = x0 - np.sin(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    ycut = y_pos + np.cos(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    xcut2 = xcut - 1
                    ycut2 = y_pos + rr + g - exp_w+Wcut/2

                    xpeak = x0 - np.sin(np.pi/6.5)*(rr + exp_w)
                    xpeak2 = xcut
                    ypeak = ycut2 - exp_w/2
                    ypeak2 = ycut2#y_pos + np.cos(np.pi/7)*(rr + exp_w)

                    fid.write('\t<{} {} {} {} '.format(xcut, ycut, xpeak, ypeak) +
                              '{} {} {} {} '.format(xpeak2, ypeak2, xcut2, ycut2) +
                              '{} '.format(Wcut) +
                              '0 bezierCurve>\n')

                    Wcut = 2
                    xcut = x0 + np.sin(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    ycut = y_pos + np.cos(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    xcut2 = xcut + 1
                    ycut2 = y_pos + rr + g - exp_w+Wcut/2

                    xpeak = x0 + np.sin(np.pi/6.5)*(rr + exp_w)
                    xpeak2 = xcut
                    ypeak = ycut2 - exp_w/2
                    ypeak2 = ycut2#y_pos + np.cos(np.pi/7)*(rr + exp_w)

                    fid.write('\t<{} {} {} {} '.format(xcut, ycut, xpeak, ypeak) +
                              '{} {} {} {} '.format(xpeak2, ypeak2, xcut2, ycut2) +
                              '{} '.format(Wcut) +
                              '0 bezierCurve>\n')


                else:
                    name_out.append(Name + 'Cell' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'Cell' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<{} {} '.format(x0, y_pos) +
                              '{} {} {} '.format(rr, rr/2, exp_w) +
                              '{} {} '.format(g, 2*inp_WG_L) +
                              '{} {} '.format(W, exp_w) +
                              '{} {} '.format(g, 2*inp_WG_L) +
                              '{} {} '.format(W, exp_w) +
                              '0 ringInfInvPosDSV>\n')


                    fid.write('\t{} {} '.format(x0, y_pos) +
                            '{} {} '.format(rr-rw-exp_w, rr-rw) +
                            '{:.0f} '.format(Nmodulation) +
                            '{:.03f} '.format(Amodulation) +
                            '10000 0 torusWaveIn\n')

                    Wcut = 2
                    xcut = x0 - np.sin(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    ycut = y_pos + np.cos(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    xcut2 = xcut - 1
                    ycut2 = y_pos + rr + g - exp_w+Wcut/2

                    xpeak = x0 - np.sin(np.pi/6.5)*(rr + exp_w)
                    xpeak2 = xcut
                    ypeak = ycut2 - exp_w/2
                    ypeak2 = ycut2#y_pos + np.cos(np.pi/7)*(rr + exp_w)

                    fid.write('\t<{} {} {} {} '.format(xcut, ycut, xpeak, ypeak) +
                              '{} {} {} {} '.format(xpeak2, ypeak2, xcut2, ycut2) +
                              '{} '.format(Wcut) +
                              '0 bezierCurve>\n')

                    Wcut = 2
                    xcut = x0 + np.sin(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    ycut = y_pos + np.cos(np.pi/5.5)*(rr + exp_w - Wcut/2)
                    xcut2 = xcut + 1
                    ycut2 = y_pos + rr + g - exp_w+Wcut/2

                    xpeak = x0 + np.sin(np.pi/6.5)*(rr + exp_w)
                    xpeak2 = xcut
                    ypeak = ycut2 - exp_w/2
                    ypeak2 = ycut2#y_pos + np.cos(np.pi/7)*(rr + exp_w)

                    fid.write('\t<{} {} {} {} '.format(xcut, ycut, xpeak, ypeak) +
                              '{} {} {} {} '.format(xpeak2, ypeak2, xcut2, ycut2) +
                              '{} '.format(Wcut) +
                              '0 bezierCurve>\n')





                fid.write('{} layer\n'.format(layer))


                # Create the label
                if len(RR)>1:
                    txt_RR = 'RR={:.3f}'.format(rrOut)
                else:
                    txt_RR = ''

                if len(G)>1:
                    txt_G = ' G={:.3f}'.format(g)
                else:
                    txt_G = ''

                if len(RW)>1:
                    txt_RW = ' RW={:.3f}'.format(rw)
                else:
                    txt_RW = ''

                txt = txt_RR + txt_RW + txt_G

                if not txt=='':
                    par_lab = {'x_pos_text': x_pos_text,
                               'y_pos_text': y_txt,
                               'txt': txt,
                               'font': font,
                               'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}
                    name_out += CreateLabel(fid, par_lab, ncell)

                    if label_out:
                        par_lab = {'x_pos_text': x_pos_text_out,
                                   'y_pos_text': y_txt,
                                   'txt': txt,
                                   'font': font,
                                   'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}
                        name_out += CreateLabel(fid, par_lab, ncell)


                # Create Bottom block waveguide
                if blockline:
                    y_drop_out = y_pos - rr
                    L = tot_length + 2*input_inv_taper_st_length
                    x1_in_lin = -L/2 + x0 + dec_block
                    xend = L/2 - x0 + dec_block

                    name_out.append(Name + 'BottBlckg_' + str(ncell) + '_' + str(cnt))
                    fid.write('<' + Name + 'BottBlckg_' + str(ncell) +
                              '_' + str(cnt) + ' struct>\n')
                    fid.write('\t<{} {} '.format(x1_in_lin-50 , y_pos +rr + 10) +
                                  '{} {} '.format(xend + 50, y_pos + rr +10 ) +
                                  '1 0 1 1 waveguide>\n')
                    # fid.write('<{} {} '.format(x1_in_lin-100, y_pos +rr + 10) +
                    #           '{} {} '.format(x1_in_lin-50, y_pos +rr + 10) +
                    #             '1 0 0 1 {}>\n'.format(wvg_type))

                subcell = 'RR{:.0f}RW{:.3f}W{:.3f}G{:.3f}'.format(rr, W, rw, g)
                subcell = subcell.replace('.', 'p')
                # ipdb.set_trace()
                fid.write('<' + subcell + '_' + str(ncell) +
                          '_' + str(cnt) + ' struct>\n')
                for n in name_out:
                    fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

                fid.write('\n')
                name_loop.append(subcell + '_' + str(ncell) + '_' + str(cnt))

                cnt += 1

    fid.write('<RingStraightWg_MainCell' + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')
    fid.write('# ******************************\n')

    return ['RingStraightWg_MainCell' + str(ncell)]
