
import numpy as np
from NISTgenerator.Misc import NanoScribePattern


def CreateThroughDropPortSeparatedFacetoFace(fid, param, ncell, cnt_out):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    layerWg = param.get('layerWg', layer)
    layerTapper = param.get('layerTapper', layer)
    polarity = param.get('polarity', 'positive')

    RR = param.get('RR', None)
    RW = param.get('RW', None)
    G = param.get('G', None)
    Gdrop = param.get('Gdrop', None)
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    Lc = param.get('Lc', None)
    LcDrop = param.get('LcDrop', None)
    resist = param.get('resist', 'positive')
    # y_pos = param.get('y_pos', None)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)
    Wthrough = param.get('Wthrough', None)
    Wdrop = param.get('Wdrop', Wthrough)
    cap = param.get('cap', True)
    exp_w = param.get('exp_w', None)
    exp_w_tapper = param.get('exp_w_tapper',exp_w )
    in_tap_etch = param.get('in_tap_etch',0 )
    dropshift = param.get('dropshift', 7/4)
    dropxdec = param.get('dropxdec', 100)
    tot_length = param.get('tot_length', None)
    WG_through_port_y_pos = param.get('WG_through_port_y_pos', None)
    WG_drop_port_y_pos = param.get('WG_drop_port_y_pos', None)
    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', 1)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    input_inv_taper_W_drop = param.get('input_inv_taper_W_drop', None)
    output_st_length = param.get('output_st_length', input_st_length)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', input_inv_taper_st_length)
    output_inv_taper_length = param.get('output_inv_taper_length', input_inv_taper_length)
    output_inv_taper_W = param.get('output_inv_taper_W', input_inv_taper_W_drop)
    output_inv_taper_W_drop = param.get('output_inv_taper_W_drop', input_inv_taper_W_drop)

    donanoscribe = param.get('donanoscribe', False)
    tapperLength = param.get('tapperLength', None)
    name_out = []

    input_surplus_taper = param.get('input_surplus_taper', 50)
    output_surplus_taper = param.get('output_surplus_taper', 50)

    # ---------------------------------------------------------
    #     -- Compute coordinate for the through port --
    # ---------------------------------------------------------
    # Through port
    #    <--------------------------------------------------- total length ----------------------------------------------------------------->
    #    <- input_inv_taper_length  ->                                                                      <-  output_inv_taper_length ->
    #                                   <-input_st_length->
    #                                                       <  2*inp_WG_L >
    #                                                                       <----------   automatic --------->
    # -- ------------------------------ ------------------- -------^------- --------------------------------- ------------------------------- ---    y_thrgh
    #
    #    ^                             ^                   ^       x0      ^                                  ^                              ^
    # x1_in_lin                    x2_in_lin           x2_in_wg         x1_out_wg                       x1_out_lin                       x2_out_lin


    if input_st_length == None :
        input_st_length = tot_length/2 - (inp_WG_L) - input_inv_taper_length
        output_st_length = input_st_length



    input_WG_length = input_inv_taper_st_length + \
        input_inv_taper_length+input_st_length
    final_WG_length = output_inv_taper_st_length + \
        output_inv_taper_length+output_st_length


    x1_in_lin = x0 - inp_WG_L - input_st_length - input_inv_taper_length
    x2_in_lin = x0 - inp_WG_L - input_st_length
    x2_in_wg = x0 - inp_WG_L
    x1_out_wg = x0 + inp_WG_L
    x2_out_lin = tot_length + x1_in_lin
    x1_out_lin = x2_out_lin - output_inv_taper_length

    y_thrgh = WG_through_port_y_pos
    y_drop = WG_drop_port_y_pos

    x1_in_lin = param.get('x1_in_lin', x1_in_lin)
    x2_in_lin = param.get('x2_in_lin', x2_in_lin)
    x2_in_wg = param.get('x2_in_wg', x2_in_wg)
    x1_out_wg = param.get('x1_out_wg', x1_out_wg)
    x2_out_lin = param.get('x2_out_lin', x2_out_lin)
    x1_out_lin = param.get('x1_out_lin', x1_out_lin)
    Wbend = param.get('Wbend', 1.5*Wdrop)





    # ---------------------------------------------------------
    #             -- Create the Through port --
    # ---------------------------------------------------------
    #  -- Create the left cap- --



    if tapperLength:
        x1_in_lin = x1_in_lin - tapperLength




    if donanoscribe:
        param_ns={'xin':x1_in_lin,  'yin': y_thrgh,
                'polarity': polarity}
        name_out += NanoScribePattern(fid, param_ns, ncell)
    if input_surplus_taper > 0:
        x1_in_cap = x1_in_lin - input_inv_taper_st_length - input_surplus_taper
    else:
        x1_in_cap = x1_in_lin - input_inv_taper_st_length


    name_out.append(Name + 'ICp' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))

    fid.write(str(layerTapper) + ' layer\n')
    fid.write('<' + Name + 'ICp' + 'Cell' +
            str(ncell) + '_' + str(cnt_out) + ' struct>\n')


    if polarity == 'positive':

        fid.write('\t<{} {} '.format(x1_in_cap, y_thrgh) +
                '{} {} '.format(x1_in_lin, y_thrgh) +
                '{} {} '.format(input_inv_taper_W, exp_w_tapper + in_tap_etch) +
                '0 1 0 waveguideInv>\n')
    else:
        fid.write('\t<{} {} '.format(x1_in_cap, y_thrgh) +
                '{} {} '.format(x1_in_lin, y_thrgh) +
                '{} '.format(input_inv_taper_W) +
                '0 1 0 waveguide>\n')

    if tapperLength:
        name_out.append(Name + 'Tl_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
        fid.write(str(layerWg) + ' layer\n')
        fid.write('<' + Name + 'Tl_' + 'Cell' +
                str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        if polarity == 'positive':
            fid.write('\t<{} {} '.format(x1_in_lin, y_thrgh) +
                    '{} {} '.format(x1_in_lin+tapperLength, y_thrgh) +
                    '{} {} '.format(input_inv_taper_W, exp_w_tapper) +
                    '0 0 0 waveguideInv>\n')
        else:
            fid.write('\t<{} {} '.format(x1_in_lin, y_thrgh) +
                    '{} {} '.format(x1_in_lin+tapperLength, y_thrgh) +
                    '{} '.format(input_inv_taper_W) +
                    '0 0 0 waveguide>\n')
    #  -- Create the left linear tapper- --
    if tapperLength:
        x1_in_lin = x1_in_lin + tapperLength
    W1_in_lin = input_inv_taper_W+2*(exp_w_tapper+in_tap_etch)
    W2_in_lin = Wthrough+2*exp_w
    Ws1_in_lin = input_inv_taper_W
    Ws2_in_lin = Wthrough


    fid.write(str(layerTapper) + ' layer\n')
    name_out.append(Name + 'InLin' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InLin' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('\t<{} {} '.format(x1_in_lin, y_thrgh) +
                  '{} {} '.format(x2_in_lin, y_thrgh) +
                  '{} {} '.format(W1_in_lin, W2_in_lin) +
                  '{} {} '.format(Ws1_in_lin, Ws2_in_lin) +
                  '0 linearTaperSlot>\n')
    else:
        fid.write('\t<{} {} '.format(x1_in_lin, y_thrgh) +
                  '{} {} '.format(x2_in_lin, y_thrgh) +
                  '{} {} '.format(input_inv_taper_W, Wthrough) +
                  '0 linearTaper>\n')

    # -- Create Left waveguide --
    W_in_wg = Wthrough
    We_in_wg = exp_w

    name_out.append(Name + 'InWg1_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write(str(layerWg) + ' layer\n')
    fid.write('<' + Name + 'InWg1_' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('\t<{} {} '.format(x2_in_lin, y_thrgh) +
                  '{} {} '.format(x2_in_wg, y_thrgh) +
                  '{} {} '.format(Wthrough, We_in_wg) +
                  '0 0 0 waveguideInv>\n')
    else:
        fid.write('\t<{} {} '.format(x2_in_lin, y_thrgh) +
                  '{} {} '.format(x2_in_wg, y_thrgh) +
                  '{} '.format(Wthrough) +
                  '0 0 0 waveguide>\n')


    # -- Create Right waveguide --
    W_in_wg = Wthrough
    We_in_wg = exp_w

    name_out.append(Name + 'InWg1_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write(str(layerWg) + ' layer\n')
    fid.write('<' + Name + 'InWg1_' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('\t<{} {} '.format(x1_out_wg, y_thrgh) +
                  '{} {} '.format(x1_out_lin, y_thrgh) +
                  '{} {} '.format(Wthrough, We_in_wg) +
                  '0 0 0 waveguideInv>\n')
    else:
        fid.write('\t<{} {} '.format(x1_out_wg, y_thrgh) +
                  '{} {} '.format(x1_out_lin, y_thrgh) +
                  '{} '.format(Wthrough) +
                  '0 0 0 waveguide>\n')


    # -- Create the output linear tapper --
    W1_in_lin = output_inv_taper_W+2*(exp_w_tapper+in_tap_etch)
    W2_in_lin = Wthrough+2*exp_w
    Ws1_in_lin = output_inv_taper_W
    Ws2_in_lin = Wthrough
    name_out.append(Name + 'OutLin' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write(str(layerTapper) + ' layer\n')
    fid.write('<' + Name + 'OutLin' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('<{} {} '.format(x1_out_lin, y_thrgh) +
                  '{} {} '.format(x2_out_lin, y_thrgh) +
                  '{} {} '.format(W2_in_lin, W1_in_lin) +
                  '{} {} '.format(Ws2_in_lin, Ws1_in_lin) +
                  '0 linearTaperSlot>\n')
    else:
        fid.write('<{} {} '.format(x1_out_lin, y_thrgh) +
                  '{} {} '.format(x2_out_lin, y_thrgh) +
                  '{} {} '.format(Wthrough, output_inv_taper_W) +
                  '0 linearTaper>\n')


    if tapperLength:
        name_out.append(Name + 'Tr_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
        fid.write(str(layerWg) + ' layer\n')
        fid.write('<' + Name + 'Tr_' + 'Cell' +
                str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        if polarity == 'positive':
            fid.write('\t<{} {} '.format(x2_out_lin, y_thrgh) +
                    '{} {} '.format(x2_out_lin+tapperLength, y_thrgh) +
                    '{} {} '.format(input_inv_taper_W, exp_w_tapper+in_tap_etch) +
                    '0 0 0 waveguideInv>\n')
        else:
            fid.write('\t<{} {} '.format(x2_out_lin, y_thrgh) +
                    '{} {} '.format(x2_out_lin+tapperLength, y_thrgh) +
                    '{} '.format(input_inv_taper_W) +
                    '0 0 0 waveguide>\n')

    # #  -- Create end cap --
    if tapperLength:
        x2_out_lin = x2_out_lin + tapperLength
    # x2_out_cap = x2_out_lin + output_inv_taper_st_length
    if output_surplus_taper > 0:
        x2_out_cap = x2_out_lin + output_inv_taper_st_length + output_surplus_taper
    else:
        x2_out_cap = x2_out_lin + output_inv_taper_st_length
    W_out_tap = output_inv_taper_W
    We_out_tap = (W1_in_lin - W_out_tap)/2



    name_out.append(Name + 'Cp' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write(str(layerTapper) + ' layer\n')
    fid.write('<' + Name + 'Cp' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('<{} {} '.format(x2_out_lin, y_thrgh) +
                  '{} {} '.format(x2_out_cap, y_thrgh) +
                  '{} {} '.format(output_inv_taper_W, We_out_tap) +
                  '0 0 1 waveguideInv>\n')
    else:
        fid.write('<{} {} '.format(x2_out_lin, y_thrgh) +
                  '{} {} '.format(x2_out_cap, y_thrgh) +
                  '{} '.format(output_inv_taper_W) +
                  '0 0 1 waveguide>\n')




    # ██████╗ ██████╗  ██████╗ ██████╗     ██████╗  ██████╗ ██████╗ ████████╗
    # ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
    # ██║  ██║██████╔╝██║   ██║██████╔╝    ██████╔╝██║   ██║██████╔╝   ██║
    # ██║  ██║██╔══██╗██║   ██║██╔═══╝     ██╔═══╝ ██║   ██║██╔══██╗   ██║
    # ██████╔╝██║  ██║╚██████╔╝██║         ██║     ╚██████╔╝██║  ██║   ██║
    # ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝
    #


    # if tapperLength:
    #     x1_in_lin = x1_in_lin - tapperLength




    if donanoscribe:
        param_ns={'xin':x1_in_lin,  'yin': y_thrgh,
                'polarity': polarity}
        name_out += NanoScribePattern(fid, param_ns, ncell)
    # x1_in_cap = x1_in_lin - input_inv_taper_st_length


    name_out.append(Name + 'ICp' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))

    fid.write(str(layerTapper) + ' layer\n')
    fid.write('<' + Name + 'ICp' + 'Cell' +
            str(ncell) + '_' + str(cnt_out) + ' struct>\n')


    if polarity == 'positive':

        fid.write('\t<{} {} '.format(x1_in_cap, y_drop) +
                '{} {} '.format(x1_in_lin, y_drop) +
                '{} {} '.format(input_inv_taper_W_drop, exp_w_tapper + in_tap_etch) +
                '0 1 0 waveguideInv>\n')
    else:
        fid.write('\t<{} {} '.format(x1_in_cap, y_drop) +
                '{} {} '.format(x1_in_lin, y_drop) +
                '{} '.format(input_inv_taper_W_drop) +
                '0 1 0 waveguide>\n')

    if tapperLength:
        name_out.append(Name + 'Tl_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
        fid.write(str(layerWg) + ' layer\n')
        fid.write('<' + Name + 'Tl_' + 'Cell' +
                str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        if polarity == 'positive':
            fid.write('\t<{} {} '.format(x1_in_lin, y_drop) +
                    '{} {} '.format(x1_in_lin+tapperLength, y_drop) +
                    '{} {} '.format(input_inv_taper_W_drop, exp_w_tapper) +
                    '0 0 0 waveguideInv>\n')
        else:
            fid.write('\t<{} {} '.format(x1_in_lin, y_drop) +
                    '{} {} '.format(x1_in_lin+tapperLength, y_drop) +
                    '{} '.format(input_inv_taper_W_drop) +
                    '0 0 0 waveguide>\n')
    #  -- Create the left linear tapper- --
    if tapperLength:
        x1_in_lin = x1_in_lin + tapperLength
    W1_in_lin = input_inv_taper_W_drop+2*(exp_w_tapper+in_tap_etch)
    W2_in_lin = Wdrop+2*exp_w
    Ws1_in_lin = input_inv_taper_W_drop
    Ws2_in_lin = Wdrop


    fid.write(str(layerTapper) + ' layer\n')
    name_out.append(Name + 'InLin' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InLin' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('\t<{} {} '.format(x1_in_lin, y_drop) +
                  '{} {} '.format(x2_in_lin, y_drop) +
                  '{} {} '.format(W1_in_lin, W2_in_lin) +
                  '{} {} '.format(Ws1_in_lin, Ws2_in_lin) +
                  '0 linearTaperSlot>\n')
    else:
        fid.write('\t<{} {} '.format(x1_in_lin, y_drop) +
                  '{} {} '.format(x2_in_lin, y_drop) +
                  '{} {} '.format(input_inv_taper_W_drop, Wdrop) +
                  '0 linearTaper>\n')

    # -- Create Left waveguide --
    W_in_wg = Wdrop
    We_in_wg = exp_w

    name_out.append(Name + 'InWg1_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write(str(layerWg) + ' layer\n')
    fid.write('<' + Name + 'InWg1_' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('\t<{} {} '.format(x2_in_lin, y_drop) +
                  '{} {} '.format(x2_in_wg, y_drop) +
                  '{} {} '.format(Wdrop, We_in_wg) +
                  '0 0 0 waveguideInv>\n')
    else:
        fid.write('\t<{} {} '.format(x2_in_lin, y_drop) +
                  '{} {} '.format(x2_in_wg, y_drop) +
                  '{} '.format(Wdrop) +
                  '0 0 0 waveguide>\n')


    # -- Create Right waveguide --
    W_in_wg = Wdrop
    We_in_wg = exp_w

    name_out.append(Name + 'InWg1_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write(str(layerWg) + ' layer\n')
    fid.write('<' + Name + 'InWg1_' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('\t<{} {} '.format(x1_out_wg, y_drop) +
                  '{} {} '.format(x1_out_lin, y_drop) +
                  '{} {} '.format(Wdrop, We_in_wg) +
                  '0 0 0 waveguideInv>\n')
    else:
        fid.write('\t<{} {} '.format(x1_out_wg, y_drop) +
                  '{} {} '.format(x1_out_lin, y_drop) +
                  '{} '.format(Wdrop) +
                  '0 0 0 waveguide>\n')


    # -- Create the output linear tapper --
    W1_in_lin = output_inv_taper_W+2*(exp_w_tapper+in_tap_etch)
    W2_in_lin = Wdrop+2*exp_w
    Ws1_in_lin = output_inv_taper_W
    Ws2_in_lin = Wdrop
    name_out.append(Name + 'OutLin' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write(str(layerTapper) + ' layer\n')
    fid.write('<' + Name + 'OutLin' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('<{} {} '.format(x1_out_lin, y_drop) +
                  '{} {} '.format(x2_out_lin, y_drop) +
                  '{} {} '.format(W2_in_lin, W1_in_lin) +
                  '{} {} '.format(Ws2_in_lin, Ws1_in_lin) +
                  '0 linearTaperSlot>\n')
    else:
        fid.write('<{} {} '.format(x1_out_lin, y_drop) +
                  '{} {} '.format(x2_out_lin, y_drop) +
                  '{} {} '.format(Wdrop, output_inv_taper_W) +
                  '0 linearTaper>\n')


    if tapperLength:
        name_out.append(Name + 'Tr_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
        fid.write(str(layerWg) + ' layer\n')
        fid.write('<' + Name + 'Tr_' + 'Cell' +
                str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        if polarity == 'positive':
            fid.write('\t<{} {} '.format(x2_out_lin, y_drop) +
                    '{} {} '.format(x2_out_lin+tapperLength, y_drop) +
                    '{} {} '.format(output_inv_taper_W_drop, exp_w_tapper+in_tap_etch) +
                    '0 0 0 waveguideInv>\n')
        else:
            fid.write('\t<{} {} '.format(x2_out_lin, y_drop) +
                    '{} {} '.format(x2_out_lin+tapperLength, y_drop) +
                    '{} '.format(output_inv_taper_W_drop) +
                    '0 0 0 waveguide>\n')

    # #  -- Create end cap --
    if tapperLength:
        x2_out_lin = x2_out_lin + tapperLength
    # x2_out_cap = x2_out_lin + output_inv_taper_st_length
    W_out_tap = output_inv_taper_W
    We_out_tap = (W1_in_lin - W_out_tap)/2



    name_out.append(Name + 'Cp' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write(str(layerTapper) + ' layer\n')
    fid.write('<' + Name + 'Cp' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    if polarity == 'positive':
        fid.write('<{} {} '.format(x2_out_lin, y_drop) +
                  '{} {} '.format(x2_out_cap, y_drop) +
                  '{} {} '.format(output_inv_taper_W_drop, We_out_tap) +
                  '0 0 1 waveguideInv>\n')
    else:
        fid.write('<{} {} '.format(x2_out_lin, y_drop) +
                  '{} {} '.format(x2_out_cap, y_drop) +
                  '{} '.format(output_inv_taper_W_drop) +
                  '0 0 1 waveguide>\n')










    fid.write('\n')
    fid.write('<' + Name + 'TghPrt' + str(ncell) +
               '_' +str(cnt_out)+ ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    return [Name + 'TghPrt' + str(ncell) + '_' +str(cnt_out) ]
