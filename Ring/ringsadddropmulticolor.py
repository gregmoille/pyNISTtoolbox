from copy import copy
import ipdb
import numpy as np
from NISTgenerator.Port import CreateThroughDropPortSeparated
from NISTgenerator.Misc import CreateLabel, CreateBumpStruct



def CreateWGRingsAddDropMutlicolor(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    RR = param.get('RR', None)

    RWetch = param.get('RWetch', None)
    RWin = param.get('RWin', None)
    WetchAdd = param.get('WetchAdd', None)

    Nmodulation = param.get('Nmodulation', None)
    Amodulation = param.get('Amodulation', None)

    W = param.get('W', None)
    G = param.get('G', None)

    Wdrop = param.get('Wdrop', W)
    Gdrop = param.get('Gdrop', G)
    Wbend = param.get('Wbend', Wdrop*1.5)

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
    NTopdec = param.get('NTopdec', 3)
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

    polarity = param.get('polarity', 'positive')
    donanoscribe =  param.get('donanoscribe', False)

    params_port = copy(param)

    debug = param.get('debug', False)

    Wbdg = param.get('Wbdg', None)
    Hbdg = param.get('Hbdg', None)
    Bdg_layer = param.get('Bdg_layer', 98)

    if not type(G) == list:
        G = [G]
    if not type(Gdrop) == list:
        Gdrop = [Gdrop]*len(G)
        countGdrop = 0
    else:
        if Gdrop == G:
            countGdrop = 0
        else:
            countGdrop = 1
    if not type(RR) == list:
        RR = [RR]
    if not type(RWetch) == list:
        RWetch = [RWetch]
    if not type(RWin) == list:
        RWin = [RWin]

    cnt = 0
    # fid.write('<' + Name +  'Array struct>\n' )
    # fid.write(str(layer) + ' layer\n')
    # print('------------------------------------')

    fid.write('{} layer\n'.format(layer[0]))
    name_loop = []

    y0original = copy(y0)
    y0 = 0
    for g, gdrop in zip(G, Gdrop):
        for rr in RR:
            for rwIn in RWin:
                for rwetch in RWetch:
                    name_out = []
                    rw = rwetch  + rwIn
                    if debug:
                        print('Creating Straight WG coupled to RR: ')
                        print('On the layer {}'.format(layer))
                        print('RR={} RW={} '.format(rr, rw) +
                              'g={}\n'.format(g))

                    y_pos = y_shift * cnt + y0
                    x_xtx = x0 + x_pos_text
                    y_txt = y_pos + y_pos_text

                    # Create the Through port
                    WG_through_port_y_pos = y_pos + rr + g + W/2
                    params_port['name'] = Name + 'Ports_' + str(cnt)
                    params_port['RR'] = rr
                    params_port['G'] = g
                    params_port['RW'] = rw
                    params_port['Wthrough'] = W
                    params_port['Wdrop'] = Wdrop
                    params_port['Wbend'] = Wbend

                    params_port['in_tap_etch'] = in_tap_etch
                    params_port['WG_through_port_y_pos'] = WG_through_port_y_pos
                    params_port['WG_drop_port_y_pos'] = y_pos - rr - gdrop - Wdrop/2
                    params_port['layer'] = layer[0]
                    params_port['polarity'] = polarity
                    params_port['donanoscribe'] = donanoscribe

                    name_out += CreateThroughDropPortSeparated(fid, params_port, ncell, cnt)

                    # Create the ring


                    if not Nmodulation:
                        name_out.append(Name + 'Cell' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'Cell' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')


                        if polarity == 'positive':
                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                      '{} {} {} '.format(rr, rw, exp_w) +
                                      '{} {} '.format(g, 2*inp_WG_L) +
                                      '{} {} '.format(W, exp_w) +
                                      '{} {} '.format(gdrop, 2*inp_WG_L) +
                                      '{} {} '.format(Wdrop, exp_w) +
                                      '0 ringInfInvPosDSV>\n')

                            fid.write('\t{} {} '.format(x0, y_pos) +
                                      '{} {} '.format(rr/2 - 2, rr/2) +
                                      'torusVector\n')
                        else:
                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                      '{} {} '.format(rr-rw, rw) +
                                      '{} {} '.format(g, 2*inp_WG_L) +
                                      '{} '.format(W) +
                                      '{} {} '.format(gdrop, 2*inp_WG_L) +
                                      '{} '.format(Wdrop) +
                                      '0 ringInfDSV>\n')

                        Wcut = 2
                        xcut = x0 - np.sin(np.pi/5.5)*(rr + exp_w - Wcut/2)
                        ycut = y_pos + np.cos(np.pi/5.5)*(rr + exp_w - Wcut/2)
                        xcut2 = xcut - 1
                        ycut2 = y_pos + rr + g - exp_w+Wcut/2

                        xpeak = x0 - np.sin(np.pi/6.5)*(rr + exp_w)
                        xpeak2 = xcut
                        ypeak = ycut2 - exp_w/2
                        ypeak2 = ycut2#y_pos + np.cos(np.pi/7)*(rr + exp_w)

                        if polarity == 'positive':
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

                        if polarity == 'positive':
                            fid.write('\t<{} {} {} {} '.format(xcut, ycut, xpeak, ypeak) +
                                      '{} {} {} {} '.format(xpeak2, ypeak2, xcut2, ycut2) +
                                      '{} '.format(Wcut) +
                                      '0 bezierCurve>\n')

                        # Create the Etch Step
                        if rwetch>0.1:
                            if not WetchAdd:
                                wadd = g/2
                            else:
                                wadd = WetchAdd
                            fid.write('{} layer\n'.format(layer[1]))
                            name_out.append(
                                Name + 'RingEtch' + str(ncell) + '_' + str(cnt))
                            fid.write('<' + Name + 'RingEtch' + str(ncell) +
                                      '_' + str(cnt) + ' struct>\n')
                            if polarity == 'positive':
                                fid.write('{} {} '.format(x0, y_pos) +
                                          '{} {} {} '.format(rr+wadd/2-(rwetch)/2, rwetch+wadd, 0) +
                                          '{} {} '.format(360, nr) +
                                          'torusW\n')

                    else:
                        name_out.append(Name + 'Cell' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'Cell' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        # fid.write('\t<{} {} '.format(x0, y_pos) +
                        #           '{} {} {} '.format(rr, rw, exp_w) +
                        #           '{} {} '.format(g, 2*inp_WG_L) +
                        #           '{} {} '.format(W, exp_w) +
                        #           '0 ringInfiniteInvPosV>\n')
                        if polarity == 'positive':
                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                      '{} {} {} '.format(rr, rr/2, exp_w) +
                                      '{} {} '.format(g, 2*inp_WG_L) +
                                      '{} {} '.format(W, exp_w) +
                                      '{} {} '.format(gdrop, 2*inp_WG_L) +
                                      '{} {} '.format(Wdrop, exp_w) +
                                      '0 ringInfInvPosDSV>\n')

                            fid.write('\t{} {} '.format(x0, y_pos) +
                                    '{} {} '.format(rr-(rw) - exp_w, rr-(rw) ) +
                                    '{:.0f} '.format(Nmodulation) +
                                    '{} '.format(Amodulation) +
                                    '10000 0 torusWaveIn\n')
                        else:
                            fid.write('\t{} {} '.format(x0, y_pos) +
                                    '{} {} '.format(rr-(rw), rr -rw/2  + Amodulation+rw/10) +
                                    '{:.0f} '.format(Nmodulation) +
                                    '{} '.format(Amodulation) +
                                    '10000 0 torusWaveIn\n')
                            fid.write('{} {} '.format(x0, y_pos) +
                                      '{} {} {} '.format(rr-rw/2, rr, 0) +
                                      '{} {} '.format(360, nr) +
                                      'torus\n')

                            fid.write('<{} {} '.format(-inp_WG_L, y_pos + rr + g +W/2) +
                                      '{} {} '.format(inp_WG_L, y_pos + rr + g +W/2 ) +
                                      '{} '.format(W) +
                                      '0 0 0 waveguide>\n')

                            fid.write('<{} {} '.format(-inp_WG_L, y_pos - rr - g - Wdrop/2) +
                                      '{} {} '.format(inp_WG_L, y_pos - rr - g - Wdrop/2 ) +
                                      '{} '.format(Wdrop) +
                                      '0 0 0 waveguide>\n')


                        # fid.write('\t{} {} '.format(x0, y_pos) +
                        #           '{} {} '.format(rr/2 - 2, rr/2) +
                        #           'torusVector\n')
                        # fid.write('{} {} '.format(x0, y_pos) +
                        #           '{} {} {} '.format(rr-(rw) - exp_w/2, exp_w, 0) +
                        #           '{} {} '.format(360, nr) +
                        #           'torusW\n')




                        Wcut = 2
                        xcut = x0 - np.sin(np.pi/5.5)*(rr + exp_w - Wcut/2)
                        ycut = y_pos + np.cos(np.pi/5.5)*(rr + exp_w - Wcut/2)
                        xcut2 = xcut - 1
                        ycut2 = y_pos + rr + g - exp_w+Wcut/2

                        xpeak = x0 - np.sin(np.pi/6.5)*(rr + exp_w)
                        xpeak2 = xcut
                        ypeak = ycut2 - exp_w/2
                        ypeak2 = ycut2#y_pos + np.cos(np.pi/7)*(rr + exp_w)
                        if polarity == 'positive':
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
                        if polarity == 'positive':
                            fid.write('\t<{} {} {} {} '.format(xcut, ycut, xpeak, ypeak) +
                                      '{} {} {} {} '.format(xpeak2, ypeak2, xcut2, ycut2) +
                                      '{} '.format(Wcut) +
                                      '0 bezierCurve>\n')
                        # Create the Etch Step
                        if rwetch>0.1:
                            if not WetchAdd:
                                wadd = g/2
                            else:
                                wadd = WetchAdd
                            fid.write('{} layer\n'.format(layer[1]))
                            name_out.append(
                                Name + 'RingEtch' + str(ncell) + '_' + str(cnt))
                            fid.write('<' + Name + 'RingEtch' + str(ncell) +
                                      '_' + str(cnt) + ' struct>\n')
                            if polarity == 'positive':
                                fid.write('{} {} '.format(x0, y_pos) +
                                          '{} {} {} '.format(rr+wadd/2-(rwetch)/2, rwetch+wadd, 0) +
                                          '{} {} '.format(360, nr) +
                                          'torusW\n')

                            #
                            #
                            # fid.write('\t{} {} '.format(x0, y_pos) +
                            #         '{} {} '.format(rr+wadd-(rwetch), rr+wadd) +
                            #         '{:.0f} '.format(Nmodulation) +
                            #         '{} '.format(Amodulation) +
                            #         '10000 0 torusWaveIn\n')

                    fid.write('{} layer\n'.format(layer[0]))


                    # Create the label
                    if len(RR)>1:
                        txt_RR = 'RR={:.3f}'.format(rrOut)
                    else:
                        txt_RR = ''

                    if len(G)>1:
                        txt_G = ' G={:.0f}'.format(g*1e3)
                    else:
                        txt_G = ''

                    if len(RWetch)>1:
                        txt_RWetch = ' RWetch={:.0f}'.format(rwetch*1e3)
                    else:
                        txt_RWetch = ''

                    if len(RWin)>1:
                        if len(RWetch)>1:
                            txt_RWin = ' RWin={:.0f}'.format(rwIn*1e3)
                        else:
                            if RWetch[0] == 0:
                                txt_RWin = ' RW={:.0f}'.format(rwIn*1e3)

                    else:
                        txt_RWin = ''

                    txt = txt_RR + txt_RWin + txt_RWetch + txt_G

                    if not txt=='':
                        par_lab = {'x_pos_text': x_pos_text,
                                   'y_pos_text': y_txt,
                                   'txt': txt,
                                   'font': font,
                                   'name': 'Lbl' + Name.replace('_', '')  + 'Cell' + str(ncell) + '_' + str(cnt)}
                        name_out += CreateLabel(fid, par_lab, ncell)

                        if label_out:
                            par_lab = {'x_pos_text': x_pos_text_out,
                                       'y_pos_text': y_txt,
                                       'txt': txt,
                                       'font': font,
                                       'name': 'Lbl' + Name.replace('_', '') + 'Cell' + str(ncell) + '_' + str(cnt)}
                            name_out += CreateLabel(fid, par_lab, ncell)


                    # Create Bottom block waveguide

                    if blockline:
                        if donanoscribe:
                            decblock = 110
                        else:
                            decblock = -50
                        y_drop_out = y_pos - rr
                        L = tot_length + 2*input_inv_taper_st_length
                        x1_in_lin = -L/2 + x0 + dec_block
                        xend = L/2 - x0 + dec_block

                        name_out.append(Name + 'BottBlckg_' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'BottBlckg_' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('\t<{} {} '.format(x1_in_lin + decblock , y_pos +rr + 10) +
                                      '{} {} '.format(xend - decblock, y_pos + rr +10 ) +
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

    if Wbdg:
        if countGdrop:
            Hstrct  = (len(G)* len(RWin)* len(RWetch) * len(RR) * len(Gdrop) -1) * -1 * y_shift + \
                    RR[0] + 10.5 + \
                    RR[-1] + Gdrop[-1] + Wdrop + 2 + \
                    0.25* RR[-1]
        else:
            Hstrct  = (len(G)* len(RWin)* len(RWetch) * len(RR)  -1) * -1 * y_shift + \
                    RR[0] + 10.5 + \
                    RR[-1] + Gdrop[-1] + Wdrop + 2 + \
                    0.25* RR[-1]

        if polarity == 'negative':
            Hstrct = Hstrct - 2

        ybgtop =  RR[0] + G[0] + W/2 + NTopdec*y_shift
        ybdg = ybgtop + Hbdg - Hstrct/2




        BoudBox = {'name': 'Bdg' + Name,
                         'layer': Bdg_layer,
                         'corner': (-Wbdg/2, -ybgtop - Hbdg),
                         'w_h': (Wbdg, Hbdg),
                         'Yspace': 0,
                         'Xspace': 0,
                         }
        name_loop += CreateBumpStruct(fid, BoudBox, ncell)

    fid.write('<' + Name + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('\t<' + n + ' 0 {:.3f} 0 1 0 instance>\n'.format(-RR[0] - G[0] - W/2))

    fid.write('\n')
    fid.write('# ******************************\n')

    return [Name + str(ncell)]
