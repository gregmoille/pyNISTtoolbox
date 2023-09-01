from copy import copy
import ipdb
import numpy as np
import scipy.constants as cts
import scipy.signal as signal
from scipy.interpolate import interp1d
from scipy.fft import fft, ifft, ifftshift
from NISTgenerator.Port import CreateThroughDropPortSeparated, CreateThroughPort, CreateThroughDropPortSeparatedFacetoFace
from NISTgenerator.Misc import CreateLabel, CreateBumpStruct



def CreateWGRingsAddDropMutlicolor(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)

    layer_stepper = layer[-1]
    layer_waveguide = layer[-2]
    layer = layer[:-2]

    RR = param.get('RR', None)

    RWetch = param.get('RWetch', None)
    RWin = param.get('RWin', None)
    WetchAdd = param.get('WetchAdd', None)

    W = param.get('W', None)
    G = param.get('G', None)

    Wdrop = param.get('Wdrop', None)
    Gdrop = param.get('Gdrop', None)
    Wbend = param.get('Wbend', Wdrop*1.5)

    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    x_pos_text = param.get('x_pos_text', -1000)

    y_pos_text = param.get('y_pos_text', -20)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)

    Lc = param.get('Lc', None)
    LcDrop = param.get('LcDrop', None)
    exp_w = param.get('exp_w', None)
    exp_w_ring = param.get('exp_w_ring', exp_w)
    exp_w_tapper = param.get('exp_w_tapper',exp_w )
    font_size_pattern = param.get('font_size_pattern', 10)
    font = param.get('font', 'Source Code Pro')

    do_center_etch = param.get('do_center_etch', False)

    y_shift = param.get('y_shift', 0)
    dropshift = param.get('dropshift', 7/4)
    dropxdec = param.get('dropxdec', 100)
    NTopdec = param.get('NTopdec', 3)
    input_inv_taper_length = param.get('input_inv_taper_length', 200)
    input_st_length = param.get('input_st_length', 10)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', input_st_length)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', input_inv_taper_st_length)
    output_inv_taper_length = param.get('output_inv_taper_length', input_inv_taper_length)
    output_inv_taper_W = param.get('output_inv_taper_W', None)
    output_inv_taper_W_drop = param.get('output_inv_taper_W_drop', output_inv_taper_W)
    blockline = param.get('blockline', True)
    dec_block = param.get('dec_block', 0)
    y_blockline_dec = param.get('y_blockline_dec', 10)
    in_tap_etch = param.get('in_tap_etch', 0)
    through_drop = param.get('through_drop', False)
    tapperLength = param.get('tapperLength', None)
    label_out = param.get('label_out', False)
    x_pos_text_out = param.get('x_pos_text_out', 1500)
    tot_length = param.get('tot_length',3850)

    polarity = param.get('polarity', 'positive')
    donanoscribe =  param.get('donanoscribe', False)
    do_bezier_smooth = param.get('do_bezier_smooth', False)
    do_mixmatch = param.get('do_mixmatch', False)


    Nmodulation = param.get('Nmodulation', None)
    Amodulation_list = param.get('Amodulation', None)
    Sigmamodulation_list = param.get('Sigmamodulation', None)
    Gaussmodulation_spread = param.get('Gaussmodulation_spread', None)
    DEMS_fun = param.get('DEMS_fun', None)
    Nfaraday = param.get('Nfaraday', None)
    Wfaraday = param.get('Wfaraday', None)
    Lfaraday = param.get('Lfaraday', None)


    neff_fun = param.get('neff_fun', None)
    neff0 = param.get('neff0', None)
    OAM = param.get('OAM', False)
    Nmod_pts = param.get('Nmod_pts', 20000)
    const_phase = param.get('const_phase', 0)
    ccw_drop = param.get('ccw_drop', True)
    symmetrize = param.get('symmetrize', True)
    ThreeD = param.get('ThreeD', True)
    # print(f'Wfaraday = {Wfaraday}')


    params_port = copy(param)

    debug = param.get('debug', False)

    Wbdg = param.get('Wbdg', None)
    Hbdg = param.get('Hbdg', None)
    Bdg_layer = param.get('Bdg_layer', 98)

    if not type(G) == list:
        G = [G]
    if not type(Gdrop) == list:
        if Gdrop == None:
            Gdrop = [None]
        else:
            Gdrop = [Gdrop]
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
    if not type(Lc) == list:
        if Lc == None:
            Lc = [None]
        else:
            Lc = [Lc]
    if not type(LcDrop) == list:
        if LcDrop == None:
            LcDrop = [None]
        else:
            LcDrop = [LcDrop]
    if not type(Amodulation_list) == list:
        Amodulation_list = [Amodulation_list]
    if not type(Sigmamodulation_list) == list:
        Sigmamodulation_list = [Sigmamodulation_list]

    if not type(layer) == list:
        layer = [layer]

    cnt = 0
    # fid.write('<' + Name +  'Array struct>\n' )
    # fid.write(str(layer) + ' layer\n')
    # print('------------------------------------')

    fid.write('{} layer\n'.format(layer[0]))
    name_loop = []

    y0original = copy(y0)
    y0 = 0
    for g in G:
        for gdrop in Gdrop:
            for rr in RR:
                for rwIn in RWin:
                    for rwetch in RWetch:
                        for lc in Lc:
                            for lcd in LcDrop:
                                for Amodulation in Amodulation_list:
                                    for Sigmamodulation in Sigmamodulation_list:
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

                                        params_port['name'] = Name + 'Ports_' + str(cnt)
                                        params_port['RR'] = rr
                                        params_port['G'] = g
                                        params_port['Gdrop'] = gdrop
                                        params_port['RW'] = rw
                                        params_port['Wthrough'] = W
                                        params_port['Wdrop'] = Wdrop
                                        params_port['Wbend'] = Wbend
                                        params_port['Lc'] = lc
                                        params_port['LcDrop'] = lcd
                                        params_port['inp_WG_L'] = inp_WG_L
                                        params_port['in_tap_etch'] = in_tap_etch


                                        params_port['layer'] = layer_waveguide
                                        params_port['layerWg'] = layer_waveguide
                                        params_port['layerTapper'] = layer[0]
                                        params_port['resist'] = polarity
                                        params_port['donanoscribe'] = donanoscribe
                                        params_port['dropshift'] = dropshift
                                        params_port['dropxdec'] = dropxdec
                                        params_port['output_inv_taper_W_drop'] = output_inv_taper_W_drop
                                        if ThreeD: 
                                            inp_WG_L = 0
                                            params_port['layer'] = layer_waveguide + 1
                                            params_port['layerWg'] = layer_waveguide + 1
                                            params_port['layerTapper'] = layer_waveguide + 1
                                            WG_through_port_y_pos = y_pos + rr - rw/2 + g
                                            params_port['WG_through_port_y_pos'] = WG_through_port_y_pos
                                            params_port['resist'] = 'positive'
                                            params_port['inp_WG_L'] = inp_WG_L
                                            name_out += CreateThroughPort(fid, params_port, ncell, cnt)
                                        else:
                                            if gdrop and not(ccw_drop):
                                                if lc:
                                                    WG_through_port_y_pos = y_pos+rr+g+W/2-2 * (1-np.cos(lc/(rr+g+W/2)/2))*(rr+g+W/2)
                                                else:
                                                    WG_through_port_y_pos = y_pos + rr + g + W/2

                                                if lcd:
                                                    params_port['inp_WG_L_drop'] =inp_WG_L
                                                    params_port['inp_WG_L'] = inp_WG_L-2*np.sin(lcd/(rr+g+W/2)/2)*(rr+g+W/2)
                                                    WG_drop_port_y_pos = y_pos - rr - gdrop - Wdrop/2 + 2 * (1-np.cos(lcd/(rr+g+W/2)/2))*(rr+g+W/2)
                                                else:
                                                    WG_drop_port_y_pos = y_pos - rr - gdrop - Wdrop/2

                                                params_port['WG_drop_port_y_pos'] = WG_drop_port_y_pos
                                                params_port['WG_through_port_y_pos'] = WG_through_port_y_pos
                                                # print('GOING THROUGH')
                                                if through_drop:
                                                    name_out += CreateThroughDropPortSeparatedFacetoFace(fid, params_port, ncell, cnt)
                                                else:
                                                    name_out += CreateThroughDropPortSeparated(fid, params_port, ncell, cnt)

                                            else:
                                                if lc:
                                                    WG_through_port_y_pos = y_pos+rr+g+W/2-2 * (1-np.cos(lc/(rr+g+W/2)/2))*(rr+g+W/2)
                                                else:
                                                    WG_through_port_y_pos = y_pos + rr + g + W/2
                                                params_port['WG_through_port_y_pos'] = WG_through_port_y_pos
                                                name_out += CreateThroughPort(fid, params_port, ncell, cnt)

                                                if do_mixmatch:
                                                    params_port2 = copy(params_port)
                                                    params_port2['layer'] = layer_stepper
                                                    params_port2['layerWg'] = layer_stepper
                                                    params_port2['layerTapper'] = layer_stepper
                                                    params_port2['resist'] = 'negative'

                                                    name_out += CreateThroughPort(fid, params_port2, ncell, cnt)

                                            if gdrop and ccw_drop:
                                                WG_drop_port_y_pos = y_pos - rr - gdrop - Wdrop/2
                                                fid.write('{} layer\n'.format(layer[0]))
                                                name_out.append(
                                                    Name + 'ccwdrop' + str(ncell) + '_' + str(cnt))
                                                fid.write('<' + Name + 'ccwdrop' + str(ncell) +
                                                        '_' + str(cnt) + ' struct>\n')
                                                x0ccw = x0 + 2
                                                y0ccw = WG_drop_port_y_pos + Wdrop/2
                                                x1ccw = x0 - 17
                                                fid.write(f'{x0ccw} {y0ccw} {x1ccw} {y0ccw} {x1ccw} {y0ccw  - Wdrop} {x0ccw} {y0ccw} points2shape \n')
                                                fid.write('\t<{} {} '.format(x0ccw - inp_WG_L-5, WG_drop_port_y_pos) +
                                                        '{} {} '.format(x1ccw, WG_drop_port_y_pos) +
                                                        '{} '.format(Wdrop + 4) +
                                                        '0 1 0 waveguide>\n')
                                            # Create the ring




                                        if not Nmodulation:
                                            name_out.append(Name + 'Cell' + str(ncell) + '_' + str(cnt))
                                            fid.write('<' + Name + 'Cell' + str(ncell) +
                                                      '_' + str(cnt) + ' struct>\n')
                                            fid.write(str(layer[0]) + ' layer\n')
                                            if polarity == 'positive':

                                                if not(lc) == None:
                                                    Ls = inp_WG_L-2*np.sin(lc/(rr+g+W/2)/2)*(rr+g+W/2)

                                                    if gdrop:
                                                        if lcd:

                                                            Lsd = inp_WG_L-2*np.sin(lcd/(rr+g+W/2)/2)*(rr+g+W/2)
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} {} '.format(rr, rw, exp_w_ring) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} {} '.format(W, exp_w_ring) +
                                                                      '{:.4f} {} {} {} '.format(Lsd, gdrop, lcd, Wdrop) +
                                                                      '{} {:.4f} '.format(exp_w, 0) +
                                                                      '0 ringPulInvPLCAPulV>\n')
                                                        else:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} {} '.format(rr, rw, exp_w_ring) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} {} '.format(W, exp_w_ring) +
                                                                      '{:.4f} {} {} '.format(Ls, gdrop, Wdrop) +
                                                                      '{} {:.4f} '.format(exp_w,  2*inp_WG_L) +
                                                                      '0 ringPulInvPLCADSV>\n')
                                                    else:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} {} '.format(rr, rw, exp_w_ring) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} {} '.format(W, exp_w) +
                                                                      '{:.4f} '.format(Ls) +
                                                                      '0 ringPulleyInvPosLCAV>\n')


                                                else:
                                                    if gdrop:
                                                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                  '{} {} {} '.format(rr, rw, exp_w_ring) +
                                                                  '{} {} '.format(g, 2*inp_WG_L) +
                                                                  '{} {} '.format(W, exp_w_ring) +
                                                                  '{} {} '.format(gdrop, 2*inp_WG_L) +
                                                                  '{} {} '.format(Wdrop, exp_w) +
                                                                  '0 ringInfInvPosDSV>\n')
                                                    else:
                                                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                  '{} {} {} '.format(rr, rw, exp_w_ring) +
                                                                  '{} {} '.format(g, 2*inp_WG_L) +
                                                                  '{} {} '.format(W, exp_w) +
                                                              '0 ringInfiniteInvPosV>\n')



                                                #
                                                # if do_center_etch:
                                                #     fid.write('\t{} {} '.format(x0, y_pos) +
                                                #               '{} {} '.format(rr/2 - 2, rr/2) +
                                                #               'torusVector\n')
                                            else:

                                                if lc:
                                                    Ls = inp_WG_L-2*np.sin(lc/(rr+g+W/2)/2)*(rr+g+W/2)

                                                    if gdrop:
                                                        if lcd:
                                                            Lsd = inp_WG_L-2*np.sin(lcd/(rr+g+W/2)/2)*(rr+g+W/2)
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} '.format(rr, rw) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} '.format(W) +
                                                                      '{:.4f} {} {} {} '.format(Ls, gdrop, lcd, Wdrop) +
                                                                      '{:.4f} '.format(Lsd/2) +
                                                                      '1 ringPulPLCAPulV>\n')
                                                        else:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} '.format(rr, rw) +
                                                                      '{} {} '.format(g, lc) +
                                                                      ' {} '.format(W) +
                                                                      '{:.4f} {} {} '.format(Ls, gdrop, Wdrop) +
                                                                      '{:.4f} '.format(2*inp_WG_L) +
                                                                      '1 ringPulPLCADSV>\n')
                                                    else:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} '.format(rr, rw) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} '.format(W) +
                                                                      '{:.4f} '.format(Ls) +
                                                                      '1 ringPulleyPosLCAV>\n')


                                                else:
                                                    if gdrop:
                                                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                  '{} {} '.format(rr-rw, rw) +
                                                                  '{} {} '.format(g, 2*inp_WG_L) +
                                                                  '{} '.format(W) +
                                                                  '{} {} '.format(gdrop, 2*inp_WG_L) +
                                                                  '{} '.format(Wdrop) +
                                                                  '1 ringInfPosDSV>\n')
                                                    else:
                                                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                  '{} {} '.format(rr-rw, rw) +
                                                                  '{} {} '.format(g, 2*inp_WG_L) +
                                                                  '{} '.format(W) +
                                                              '1 ringInfiniteV>\n')

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
                                                if not lc:
                                                    if do_bezier_smooth:
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
                                                if not lc:
                                                    if do_bezier_smooth:
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
                                            fid.write(str(layer[0]) + ' layer\n')
                                            name_out.append(Name + 'Cell' + str(ncell) + '_' + str(cnt))
                                            fid.write('<' + Name + 'Cell' + str(ncell) +
                                                      '_' + str(cnt) + ' struct>\n')
                                            # fid.write('\t<{} {} '.format(x0, y_pos) +
                                            #           '{} {} {} '.format(rr, rw, exp_w) +
                                            #           '{} {} '.format(g, 2*inp_WG_L) +
                                            #           '{} {} '.format(W, exp_w) +
                                            #           '0 ringInfiniteInvPosV>\n')
                                            if polarity == 'positive':

                                                if lc :
                                                    Ls = inp_WG_L-2*np.sin(lc/(rr+g+W/2)/2)*(rr+g+W/2)
                                                    if gdrop:
                                                        if lcd:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} {} '.format(rr, rr/2, exp_w) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} {} '.format(W, exp_w) +
                                                                      '{} {} {} {} '.format(Ls, gdrop, lcd, Wdrop) +
                                                                      '{} {:.4f} '.format(exp_w, Ls) +
                                                                      '1 ringPulInvPLCAPulV>\n')
                                                        else:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} {} '.format(rr, rr/2, exp_w) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} {} '.format(W, exp_w) +
                                                                      '{:.4f} {} {} '.format(Ls, gdrop, Wdrop) +
                                                                      '{} {:.4f} '.format(exp_w,  2*inp_WG_L) +
                                                                      '1 ringPulInvPLCADSV>\n')
                                                    else:
                                                            fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                      '{} {} {} '.format(rr, rw, exp_w) +
                                                                      '{} {} '.format(g, lc) +
                                                                      '{} {} '.format(W, exp_w) +
                                                                      '{:.4f} '.format(Ls) +
                                                                      '1 ringPulleyInvPosLCAV>\n')

                                                else:
                                                    if gdrop:
                                                        # pass
                                                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                  '{} {} {} '.format(rr, rr, exp_w) +
                                                                  '{} {} '.format(g, 2*inp_WG_L) +
                                                                  '{} {} '.format(W, exp_w) +
                                                                  '{} {} '.format(gdrop, 2*inp_WG_L) +
                                                                  '{} {} '.format(Wdrop, exp_w) +
                                                                  '1 ringInfInvPosDSV>\n')
                                                    else:
                                                        # if do_center_etch:
                                                        #     fid.write('\t<{} {} '.format(x0, y_pos) +
                                                        #               '{} {} {} '.format(rr, rr/2, exp_w) +
                                                        #               '{} {} '.format(g, 2*inp_WG_L) +
                                                        #               '{} {} '.format(W, exp_w) +
                                                        #           '1 ringInfiniteInvPosV>\n')
                                                        # else:
                                                        # pass
                                                        if symmetrize and Sigmamodulation: 
                                                            if not Sigmamodulation == 0:
                                                                exp_w_ring = 0
                                                            else: 
                                                                exp_w_ring = exp_w
                                                        else:
                                                            exp_w_ring = exp_w
                                                        fid.write('\t<{} {} '.format(x0, y_pos) +
                                                                  '{} {} {} '.format(rr, rr, exp_w) +
                                                                  '{} {} '.format(g, 2*inp_WG_L) +
                                                                  '{} {} '.format(W, exp_w) +
                                                              '1 ringInfiniteInvPosV>\n')
                                                if Sigmamodulation:
                                                    # compute the modulation needed :

                                                    # print(DEMS_fun)

                                                    AA = Amodulation
                                                    σ = Sigmamodulation
                                                    Mpmp = Nmodulation
                                                    θ = np.linspace(-np.pi, np.pi, int(Nmod_pts))
                                                    θ2 = np.linspace(-np.pi, np.pi, int(200))
                                                    MMM = np.arange(-Mpmp, Mpmp)


                                                    cnt_mod = 0
                                                    # Λ = np.zeros(Nmod_pts)
                                                    modG = np.zeros(Nmod_pts)
                                                    # print(Nmod_pts)

                                                    if OAM:
                                                        NbandMult = 1
                                                    else:
                                                        NbandMult = 2

                                                    
                                                    for mm in MMM:
                                                    
                                                        modG += DEMS_fun(mm, AA, σ)*np.sin(θ*NbandMult*(Mpmp+mm))#+ phase[cnt_mod])
                                                        cnt_mod += 1
                                                    if neff_fun: 
                                                        modG = modG + neff0
                                                        modG = neff_fun(modG)*1e-3 - rw
                                                    else:
                                                        pass

                                                    def subSample(y, thr, subsamp):
                                                        ind_sub = np.where(np.abs(y)<thr)[0]
                                                        ind_norm = np.where(np.abs(y)>=thr)[0]
                                                        ind = np.concatenate([ind_sub[::subsamp], ind_norm])
                                                        ind.sort()
                                                        if not (ind[-1] == modG.size - 1):
                                                            ind = np.concatenate([ind, [modG.size - 1]])
                                                        return ind

                                                    # subsampling away from anti nodes
                                                    envlop = signal.hilbert(modG)
                                                    envlop = np.abs(envlop)
                                                    try:
                                                        ind_evlp = subSample(modG,envlop*0.8, 3)
                                                        modG = modG[ind_evlp]
                                                        θ = θ[ind_evlp]
                                                        envlop = envlop[ind_evlp]
                                                    except:
                                                        pass

                                                    # subsample low modulation
                                                    subsamp = int(modG.size/2000)
                                                    try:
                                                        ind_low = subSample(envlop,0.0005, subsamp)
                                                        θ = θ[ind_low]
                                                        modG = modG[ind_low]
                                                    except:
                                                        pass

                                                    if symmetrize: 
                                                        mod_sign_list = [1, -1]
                                                        mode_shift_list = [-rw, 0]
                                                    else: 
                                                        mod_sign_list = [1]
                                                        mode_shift_list = [-rw]

                                                    if symmetrize: 
                                                        modeGfact = 0.5
                                                    else: 
                                                        modeGfact = 1
                                                    for mod_sign, mod_shift in zip(mod_sign_list, mode_shift_list):
                                                        xmod = (rr + mod_shift + mod_sign*modG*modeGfact)*np.cos(θ + const_phase)
                                                        ymod = (rr + mod_shift + mod_sign*modG*modeGfact)*np.sin(θ + const_phase)
                                                        # θ2 = np.arccos(np.linspace(-1,1,int(Nmod_pts/100)))*2 + np.pi/2
                                                        # θ2 = list(θ[::100]) + θ[-1]
                                                        peaks, _ = signal.find_peaks(modG)
                                                        fsleeve = interp1d(θ[peaks], modG[peaks],  fill_value="extrapolate") 
                                                        sleeve_shift = fsleeve(θ)
                                                        xmod2 = (rr + mod_shift - mod_sign* exp_w - mod_sign*modG[peaks][::-1]*modeGfact) *np.cos(θ[peaks][::-1])
                                                        ymod2 = (rr + mod_shift - mod_sign* exp_w - mod_sign*modG[peaks][::-1]*modeGfact) *np.sin(θ[peaks][::-1])

                                                        xmod = np.append(xmod, xmod2[::2])
                                                        xmod = np.append(xmod, xmod2[0])
                                                        ymod = np.append(ymod, ymod2[::2])
                                                        ymod = np.append(ymod, ymod2[0])
                                                        st = ''

                                                        ymod[ymod>rr+g] = rr+g
                                                        for xx, yy in zip(xmod, ymod):
                                                            st += f'{xx + x0} {yy + y_pos:.5f} '
                                                        st += 'points2shape'
                                                        fid.write('\t{}\n'.format(st))


                                                elif Wfaraday:
                                                    # print(f'Wfaraday = {Wfaraday}')
                                                    σ = Lfaraday
                                                    AA = rw-Wfaraday
                                                    Gauss = lambda xx: AA*np.exp(-(xx)**2/(2*σ**2))
                                                    θ = np.linspace(-np.pi, np.pi, int(Nmod_pts))
                                                    θ2 = np.linspace(-np.pi, np.pi, int(1200))
                                                    modG = np.zeros(θ.size)
                                                    modG2 = np.zeros(θ2.size)

                                                    phase = np.linspace(-np.pi/2, np.pi/2, Nmodulation)
                                                    for ii, φ in zip(range(Nmodulation), phase):
                                                        modG += Gauss(θ - φ)
                                                        modG2 += Gauss(θ2 - φ)
                                                    φ0 = -np.pi/2
                                                    xmod = (rr - rw + modG)*np.cos(θ - φ0)
                                                    ymod = (rr - rw + modG)*np.sin(θ - φ0)
                                                    xmod2 = (rr - rw - exp_w+modG2[::-1]) *np.cos(θ2[::-1] - φ0)
                                                    ymod2 = (rr - rw - exp_w+modG2[::-1]) *np.sin(θ2[::-1] - φ0)

                                                    xmod = np.append(xmod, xmod2)
                                                    ymod = np.append(ymod, ymod2)
                                                    st = ''
                                                    for xx, yy in zip(xmod, ymod):
                                                        st += f'{xx + x0} {yy + y_pos:.5f} '
                                                    st += 'points2shape'
                                                    fid.write('\t{}\n'.format(st))
                                                elif not Sigmamodulation:
                                                    if OAM:
                                                        NbandMult = 1
                                                    else:
                                                        NbandMult = 2

                                                    fid.write('\t{} {} '.format(x0, y_pos) +
                                                            '{} {} '.format(rr-(rw) - exp_w, rr-(rw) ) +
                                                            '{:.0f} '.format(NbandMult*Nmodulation) +
                                                            '{} '.format(Amodulation) +
                                                            f'20000 0 torusWaveIn\n')
                                                # Gaussian Function
                                            else:
                                                fid.write('\t{} {} '.format(x0, y_pos) +
                                                        '{} {} '.format(rr-(rw), rr -rw/2  + Amodulation+rw/10) +
                                                        '{:.0f} '.format(2*Nmodulation) +
                                                        '{} '.format(Amodulation) +
                                                        '20000 0 torusWaveIn\n')


                                                # fid.write('{} {} '.format(x0, y_pos) +
                                                #           '{} {} {} '.format(rr-rw/2, rr, 0) +
                                                #           '{} {} '.format(360, nr) +
                                                #           'torus\n')

                                                fid.write('<{} {} '.format(-inp_WG_L, y_pos + rr + g +W/2) +
                                                          '{} {} '.format(inp_WG_L, y_pos + rr + g +W/2 ) +
                                                          '{} '.format(W) +
                                                          '0 0 0 waveguide>\n')

                                                fid.write('<{} {} '.format(-inp_WG_L, y_pos - rr - g - Wdrop/2) +
                                                          '{} {} '.format(inp_WG_L, y_pos - rr - g - Wdrop/2 ) +
                                                          '{} '.format(Wdrop) +
                                                          '0 0 0 waveguide>\n')





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
                                                if do_bezier_smooth:
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
                                                if do_bezier_smooth:
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


                                        if do_mixmatch:
                                            # ---- Add cut out for the stpper ---
                                            # --------------------------------------------------
                                            # fid.write(str(layer_stepper) + ' layer\n')
                                            # over the ring
                                            # fid.write(f'\t{x0} {y_pos} ' +
                                            #           f'{0} {rr + exp_w - 0.5} ' +
                                                      # 'torusVector\n')

                                            # over the waveguide
                                            wwg_step = 2*exp_w-0.2
                                            if lc:
                                                wwg_step += 2* 2 * (1-np.cos(Lc/(rr+g+W/2)/2))*(rr+g+W/2)

                                            fid.write(f'\t<{x0-inp_WG_L+wwg_step/2} {WG_through_port_y_pos} ' +
                                                      f'{x0+inp_WG_L-wwg_step/2} {WG_through_port_y_pos} ' +
                                                      f'{wwg_step} ' +
                                                      '0 1 1 waveguide>\n')
                                            fid.write(str(layer[0]) + ' layer\n')


                                        # Create the label
                                        if len(RR)>1:
                                            txt_RR = 'RR={:.3g}'.format(rrOut)
                                        else:
                                            txt_RR = ''

                                        if len(G)>1:
                                            txt_G = ' G={:.3g}'.format(g*1e3)
                                        else:
                                            txt_G = ''
                                        try:
                                            if len(Gdrop)>1:
                                                txtGdrop = ' Gdrop={:.3g}'.format(gdrop*1e3)
                                            else:
                                                txtGdrop = ''
                                        except:
                                            txtGdrop = ''
                                        if len(RWetch)>1:
                                            txt_RWetch = ' RWetch={:.3g}'.format(rwetch*1e3)
                                        else:
                                            txt_RWetch = ''
                                        if len(Lc)>1:
                                            txt_Lc = ' Lc={:.3g}'.format(lc)
                                        else:
                                            txt_Lc = ''



                                        if len(Amodulation_list)>1:
                                            txt_Amodulation = f' Amod={Amodulation*1e3:.3g}nm'
                                        else:
                                            txt_Amodulation = ''

                                        if len(Sigmamodulation_list)>1:
                                            txt_Sigmamodulation = f' σ={Sigmamodulation:.3g}'
                                        else:
                                            txt_Sigmamodulation = ''

                                        if len(LcDrop)>1:
                                            txt_LcDrop = f' LcDrop={lcd:.3g}'
                                        else:
                                            txt_LcDrop = ''


                                        if len(RWin)>1:
                                            if len(RWetch)>1:
                                                txt_RWin = ' RWin={:.0f}'.format(rwIn*1e3)
                                            else:
                                                if RWetch[0] == 0:
                                                    txt_RWin = ' RW={:.0f}'.format(rwIn*1e3)

                                        else:
                                            txt_RWin = ''

                                        txt = txt_RR + txt_RWin + txt_RWetch + txt_G + txtGdrop + txt_Lc + txt_LcDrop +  txt_Amodulation + txt_Sigmamodulation

                                        if not txt=='':
                                            if do_mixmatch:
                                                layers_tot = [layer_stepper, layer_waveguide]
                                            else:
                                                layers_tot = [layer_waveguide]
                                            for llyr in layers_tot:
                                                par_lab = {'x_pos_text': x_pos_text,
                                                           'y_pos_text': y_txt,
                                                           'txt': txt,
                                                           'font': font,
                                                           'layer': llyr,
                                                           'name': 'Lbl' + Name.replace('_', '')  + 'Cell' + str(ncell) + '_' + str(cnt)}
                                                name_out += CreateLabel(fid, par_lab, ncell)

                                                if label_out:
                                                    par_lab = {'x_pos_text': x_pos_text_out,
                                                               'y_pos_text': y_txt,
                                                               'txt': txt,
                                                               'font': font,
                                                               'layer': llyr,
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
                                            if do_mixmatch:
                                                layers_tot = [layer_stepper, layer_waveguide]
                                            else:
                                                layers_tot = [layer_waveguide]
                                            for llyr in layers_tot:

                                                fid.write(f'{llyr} layer\n')

                                                name_out.append(Name + 'BottBlckg_' + str(ncell) + '_' + str(cnt))
                                                fid.write('<' + Name + 'BottBlckg_' + str(ncell) +
                                                          '_' + str(cnt) + ' struct>\n')
                                                fid.write('\t<{} {} '.format(x1_in_lin + decblock , y_pos +rr + y_blockline_dec) +
                                                              '{} {} '.format(xend - decblock, y_pos + rr +y_blockline_dec ) +
                                                              '0.5 0 1 1 waveguide>\n')
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
        if gdrop:
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
        else:
            Hstrct  = (len(G)* len(RWin)* len(RWetch) * len(RR)  -1) * -1 * y_shift + \
                    RR[0] + 10.5 + \
                    RR[-1] + 2 + \
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
