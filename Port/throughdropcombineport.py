
import numpy


def CreateThroughDropPort(fid, param, ncell, cnt_out):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    G = param.get('G', None)
    G2 = param.get('G2', None)
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    Ls = param.get('Ls', None)
    st_WG_Lc = param.get('st_WG_Lc', None)
    W_drop = param.get('W2', None)
    y_pos = param.get('y_pos', None)
    y_drop_out = param.get('y_drop_out', None)
    y_drop_in = param.get('y_drop_in', None)
    x_dichro = param.get('x_dichro', 1500)
    Dodichro = param.get('Dodichro', True)

    dichroic_L = param.get('dichroic_L', None)
    dichr_bend_R = param.get('dichr_bend_R', RR)
    dichroic_g = param.get('dichroic_g', 300)

    through_tapper_dich_length = param.get('through_tapper_dich_length', None)

    tot_length = param.get('tot_length', None)

    WG_drop_port_U_bend_radius = param.get('Rbend', 100)

    drop_port_S_bend_l = param.get('drop_port_S_bend_l', 300)
    drop_port_S_bend_h = param.get('drop_port_S_bend_h', 100)
    drop_port_S_tapper_L = param.get('drop_port_S_tapper_L', 200)

    # y_pos = param.get('y_pos', None)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)
    W = param.get('W', None)
    exp_w = param.get('exp_w', None)
    WG_through_port_y_pos = param.get('WG_through_port_y_pos', )
    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', 5)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', 5)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', None)
    output_inv_taper_length = param.get('output_inv_taper_length', None)
    output_inv_taper_W = param.get('output_inv_taper_W', None)

    input_WG_length = input_inv_taper_st_length + \
        input_inv_taper_length+input_st_length
    final_WG_length = output_inv_taper_st_length + \
        output_inv_taper_length+output_st_length

    name_out = []

    name_out.append(Name + 'InTap' + 'C' +
                    str(ncell))
    fid.write('<' + Name + 'InTap' + 'C' +
              str(ncell) + ' struct>\n')

    # ---------------------------------------------------------
    #     -- Compute coordinate for the through port --
    # ---------------------------------------------------------
    # Through port
    #    <--------------------------------------------------- total length ----------------------------------------------------------------->
    #    <- input_inv_taper_length  ->                                                                      <-  output_inv_taper_length ->
    #                                   <-input_st_length->
    #                                                       <  2*inp_WG_L >
    #                                                                       <- automatic>
    # -- ------------------------------ ------------------- -------^------- -------------┐          ┍-------- ------------------------------- ---    y_thrgh
    #                                                                                     |        |
    #                                                                                     |        |
    #                                                                                     └--------┘                                                y_coup1
    #                                                               2*dichr_bend_R    -->  <--    ->  <-- 2*dichr_bend_R
    #    ^                             ^                   ^       x0      ^              ^        ^         ^                              ^
    # x1_in_lin                    x2_in_lin           x2_in_wg         x1_out_wg     x_dichro  x_dic_out   x1_out_lin               x2_out_lin

    # L_out_wg = tot_length - 2*st_WG_Lc - input_st_length - \
    #     input_inv_taper_length -\
    #     output_inv_taper_length
    L_coupl = 200
    L_out = x_dichro - (x0 + inp_WG_L) - L_coupl - through_tapper_dich_length

    x1_in_lin = x0 - inp_WG_L - input_st_length - input_inv_taper_length
    x2_in_lin = x0 - inp_WG_L - input_st_length
    x2_in_wg = x0 - inp_WG_L
    x1_out_wg = x0 + inp_WG_L
    x2_out_wg = x1_out_wg + L_out
    x2_out_tap_dich = x2_out_wg + through_tapper_dich_length
    
    
    
    x_dic_out = x0 + x_dichro + dichroic_L
    

    # x1_out_lin = x_dic_out + L_out_dichr
    x2_out_lin = tot_length + x1_in_lin
    if y_drop_in == None:
        y_drop_in = y_pos -RR - G2 - W_drop/2

    if y_drop_out == None:
        y_drop_out = y_pos - RR - G2 -\
            W_drop/2 - \
            2*WG_drop_port_U_bend_radius
    y_thrgh = WG_through_port_y_pos
    y_coup = (y_thrgh+y_drop_out)/2 
    Hcoup = y_thrgh - y_coup - dichroic_g/2  -W_drop/2
    
    x2_out_auto = x2_out_lin - output_inv_taper_length

    #y_thrgh - y_coup  -2*dichr_bend_R -W_drop/2 - dichroic_g/2


    # ---------------------------------------------------------
    #             -- Create the Through port --
    # ---------------------------------------------------------
    #  -- Create the left cap- --
    x1_in_cap = x1_in_lin - input_inv_taper_st_length

    name_out.append(Name + 'InCapSt' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InCapSt' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x1_in_cap, y_thrgh) +
              '{} {} '.format(x1_in_lin, y_thrgh) +
              '{} {} '.format(input_inv_taper_W, exp_w) +
              '0 1 0 waveguideInv>\n')

    #  -- Create the left linear tapper- --
    W1_in_lin = input_inv_taper_W+2*exp_w
    W2_in_lin = W+2*exp_w
    Ws1_in_lin = input_inv_taper_W
    Ws2_in_lin = W

    name_out.append(Name + 'InLin' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InLin' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x1_in_lin, y_thrgh) +
              '{} {} '.format(x2_in_lin, y_thrgh) +
              '{} {} '.format(W1_in_lin, W2_in_lin) +
              '{} {} '.format(Ws1_in_lin, Ws2_in_lin) +
              '0 linearTaperSlot>\n')

    # -- Create Left waveguide --
    W_in_wg = W
    We_in_wg = exp_w

    name_out.append(Name + 'InWg1_' + 'C' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write('<' + Name + 'InWg1_' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x2_in_lin, y_thrgh) +
              '{} {} '.format(x2_in_wg, y_thrgh) +
              '{} {} '.format(W, We_in_wg) +
              '0 0 0 waveguideInv>\n')

    # -- Create the Bend to Dichroic --
    W_out_wg = W
    We_out_wg = exp_w

    name_out.append(Name + 'OutWg' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'OutWg' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x1_out_wg, y_thrgh) +
              '{} {} '.format(x2_out_wg, y_thrgh) +
              '{} {} '.format(W, exp_w) +
              '0 0 0 waveguideInv>\n')

    # -- Create Taper to Dichroic --
    if Dodichro:
        We_in_wg = exp_w

        name_out.append(Name + 'InTap2DicWg_' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'InTap2DicWg_' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(x2_out_wg, y_thrgh) +
                  '{} {} '.format(x2_out_tap_dich, y_thrgh) +
                  '{} {} '.format(W+2*exp_w, W_drop+2*exp_w) +
                  '{} {} '.format(W, W_drop) +
                  '0 linearTaperSlot>\n')
    else:
        We_in_wg = exp_w

        name_out.append(Name + 'InTap2DicWg_' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'InTap2DicWg_' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(x2_out_wg, y_thrgh) +
                  '{} {} '.format(x2_out_auto, y_thrgh) +
                  '{} {} '.format(W+2*exp_w, W_drop+2*exp_w) +
                  '{} {} '.format(W, W_drop) +
                  '0 linearTaperSlot>\n')
    if Dodichro:
        

        # -- Create bending to go to dichroic --
        x1 = x0 + x_dichro - 2*dichr_bend_R
        # name_out.append(Name + 'ThInWg90_1_' + 'C' +
        #                 str(ncell) + '_' + str(cnt_out))
        # fid.write('<' + Name + 'ThInWg90_1_' + 'C' +
        #           str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        

        # fid.write('\t<{} {} '.format(x1, y_thrgh) +
        #           '{} {} '.format(dichr_bend_R,
        #                           -dichr_bend_R) +
        #           '{} {} '.format(W_drop, exp_w) +
        #           '0 90degreeBendInv>\n')


        # fid.write('\t<{} {} '.format(x2S, y_drop_in) +
        #       '{} {} '.format(drop_port_S_bend_l, -WG_drop_port_U_bend_radius) +
        #       '{} {} '.format(W_drop, We_in_wg) +
        #       '0 sBendInv>\n')


        # -- Create bending out from dichroic --

        # name_out.append(Name + 'ThOutWg90_1_' + 'C' +
        #                 str(ncell) + '_' + str(cnt_out))
        # fid.write('<' + Name + 'ThOutWg90_1_' + 'C' +
        #           str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        # fid.write('\t<{} {} '.format(x_dic_out+2*dichr_bend_R, y_thrgh) +
        #           '{} {} '.format(-dichr_bend_R,
        #                           -dichr_bend_R) +
        #           '{} {} '.format(W_drop, exp_w) +
        #           '0 90degreeBendInv>\n')



        # -- Create Waveguide to the output taper --
        name_out.append(Name + 'Out2TapWg' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'Out2TapWg' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(x_dic_out+L_coupl, y_thrgh) +
                  '{} {} '.format(x2_out_auto, y_thrgh) +
                  '{} {} '.format(W_drop, exp_w) +
                  '0 0 0 waveguideInv>\n')

    # -- Create the output linear tapper --
    W1 = W_drop+2*exp_w
    W2 = W_drop+2*exp_w
    name_out.append(Name + 'OutLin' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'OutLin' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('<{} {} '.format(x2_out_auto, y_thrgh) +
              '{} {} '.format(x2_out_lin, y_thrgh) +
              '{} {} '.format(W1, W2) +
              '{} {} '.format(W_drop, output_inv_taper_W) +
              '0 linearTaperSlot>\n')

    # #  -- Create end cap --
    x2_out_cap = x2_out_lin + output_inv_taper_st_length
    W_out_tap = output_inv_taper_W
    We_out_tap = (W2 - W_out_tap)/2

    name_out.append(Name + 'OutCapSt' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'OutCapSt' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('<{} {} '.format(x2_out_lin, y_thrgh) +
              '{} {} '.format(x2_out_cap, y_thrgh) +
              '{} {} '.format(output_inv_taper_W, We_out_tap) +
    '0 0 1 waveguideInv>\n')

    # ---------------------------------------------------------
    #     -- Compute coordinate for the Drop port --
    # ---------------------------------------------------------
    #                                   <st_WG_Lc>
    #                                       O
    #   y_drop_in                       /-------◝
    #                                  /          \
    #                                 |            \
    #   yS                            |              ◟--------
    #   y_coup2                       \                               ┍--------┐
    #                                  \                              |        |
    #   y_drop_out                      ------------------------------┘        └- ---- --------------- --
    #                                   ^       ^      ^      ^
    #                                  xCrv    x2S     x1S   x1Stap   ^     ^       ^                ^
    #                                                           x_dichro  x_dic_out x1_out_lin       x2_out_lin

    x2S = x0 + st_WG_Lc/2
    x1S = x2S + drop_port_S_bend_l
    x1Stap = x1S + drop_port_S_tapper_L
    xCrv = x0 - st_WG_Lc/2
    yS = y_drop_in - WG_drop_port_U_bend_radius

    # ---------------------------------------------------------
    #                   -- Create drop --
    # ---------------------------------------------------------

    # -- S bend for add port--
    name_out.append(Name + 'Sbd' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'Sbd' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x2S, y_drop_in) +
              '{} {} '.format(drop_port_S_bend_l, -WG_drop_port_U_bend_radius) +
              '{} {} '.format(W_drop, We_in_wg) +
              '0 sBendInv>\n')

    # -- Tapper for S bend --
    name_out.append(Name + 'SbdTap' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'SbdTap' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x1S, yS) +
              '{} {} '.format(x1Stap, yS) +
              '{} {} '.format(W_drop, 0) +
              '{} {} '.format(2*We_in_wg+W_drop, 2*We_in_wg) +
              '0 linearTaperSlot>\n')

    # -- End cap --
    name_out.append(Name + 'SbdTapCap1' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'SbdTapCap1' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('{} {} '.format(x1Stap, yS+exp_w/2) +
              '{} {} '.format(exp_w/2, exp_w/2) +
              '{} {} '.format(-90, 90) +
              '{} '.format(nr) +
              '0 arc\n')

    name_out.append(Name + 'SbdTapCap2' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'SbdTapCap2' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t{} {} '.format(x1Stap, yS-exp_w/2) +
              '{} {} '.format(exp_w/2, exp_w/2) +
              '{} {} '.format(-90, 90) +
              '{} '.format(nr) +
              '0 arc\n')

    # -- Add half circle --
    name_out.append(Name + 'InWg90_1_' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InWg90_1_' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(xCrv, y_drop_in) +
              '{} {} '.format(-WG_drop_port_U_bend_radius,
                              -WG_drop_port_U_bend_radius) +
              '{} {} '.format(W_drop, We_in_wg) +
              '0 90degreeBendInv>\n')

    name_out.append(Name + 'InWg90_2_' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InWg90_2_' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(xCrv - WG_drop_port_U_bend_radius,
                                 y_drop_in - WG_drop_port_U_bend_radius) +
              '{} {} '.format(WG_drop_port_U_bend_radius,
                              WG_drop_port_U_bend_radius) +
              '{} {} '.format(W_drop, We_in_wg) +
              '-90 90degreeBendInv>\n')

    # -- Straight drop port to 90 ben before coupler --
    if Dodichro:
        name_out.append(Name + 'DpWgBeCpl_' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'DpWgBeCpl_' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(xCrv, y_drop_out) +
                  '{} {} '.format(x2_out_tap_dich, y_drop_out) +
                  '{} {} '.format(W_drop, We_in_wg) +
                  '0 0 0 waveguideInv>\n')
    else:
        name_out.append(Name + 'DpWgBeCpl_' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'DpWgBeCpl_' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(xCrv, y_drop_out) +
                  '{} {} '.format(x2_out_auto, y_drop_out) +
                  '{} {} '.format(W_drop, We_in_wg) +
                  '0 0 0 waveguideInv>\n')

    if Dodichro:
        # -- Create bending to go to dichroic --
        # x1 = x0 + x_dichro - 2*dichr_bend_R
        # name_out.append(Name + 'DDhInWg90_1_' + 'C' +
        #                 str(ncell) + '_' + str(cnt_out))
        # fid.write('<' + Name + 'DDhInWg90_1_' + 'C' +
        #           str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        # fid.write('\t<{} {} '.format(x1, y_drop_out) +
        #           '{} {} '.format(dichr_bend_R,
        #                           dichr_bend_R) +
        #           '{} {} '.format(W_drop, exp_w) +
        #           '0 90degreeBendInv>\n')


        ############

        x_coupl = x_dichro + dichroic_L/2 
        name_out.append(Name + 'Coupler_' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'Coupler_' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(x_coupl,y_coup) + 
                  '{} {} '.format(W_drop, exp_w) +
                  '{} {} '.format(dichroic_g,
                                  dichroic_L) +
                  '{} {} '.format(L_coupl, Hcoup) + 
                  '0 directionalCoupler4>\n')

        # -- Create bending out from dichroic --
        # name_out.append(Name + 'DDhOutWg90_1_' + 'C' +
        #                 str(ncell) + '_' + str(cnt_out))
        # fid.write('<' + Name + 'DDhOutWg90_1_' + 'C' +
        #           str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        # fid.write('\t<{} {} '.format(x_dic_out+dichr_bend_R, y_drop_out+dichr_bend_R) +
        #           '{} {} '.format(-dichr_bend_R,
        #                           -dichr_bend_R) +
        #           '{} {} '.format(W_drop, exp_w) +
        #           '90 90degreeBendInv>\n')

        
        # -- Create Waveguide to the output taper --
        name_out.append(Name + 'DOut2TpWg' + 'C' +
                        str(ncell) + '_' + str(cnt_out))
        fid.write('<' + Name + 'DOut2TpWg' + 'C' +
                  str(ncell) + '_' + str(cnt_out) + ' struct>\n')
        fid.write('\t<{} {} '.format(x_dic_out+L_coupl, y_drop_out) +
                  '{} {} '.format(x2_out_auto, y_drop_out) +
                  '{} {} '.format(W_drop, exp_w) +
                  '0 0 0 waveguideInv>\n')

    # -- Create the output linear tapper --
    W1 = W_drop+2*exp_w
    W2 = W_drop+2*exp_w
    name_out.append(Name + 'DOutLin' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'DOutLin' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')

    fid.write('<{} {} '.format(x2_out_auto, y_drop_out) +
              '{} {} '.format(x2_out_lin, y_drop_out) +
              '{} {} '.format(W1, W2) +
              '{} {} '.format(W_drop, output_inv_taper_W) +
              '0 linearTaperSlot>\n')

    # #  -- Create end cap --
    x2_out_cap = x2_out_lin + output_inv_taper_st_length
    W_out_tap = output_inv_taper_W
    We_out_tap = (W2 - W_out_tap)/2

    name_out.append(Name + 'DOutCapSt' + 'C' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'DOutCapSt' + 'C' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('<{} {} '.format(x2_out_lin, y_drop_out) +
              '{} {} '.format(x2_out_cap, y_drop_out) +
              '{} {} '.format(output_inv_taper_W, We_out_tap) +
    '0 0 1 waveguideInv>\n')

    # ---------------------------------------------------------
    #        -- Merge everything in 1 structure --
    # ---------------------------------------------------------
    fid.write('\n')
    fid.write('<' + Name + '_ThPort' + str(ncell) +
               '_' +str(cnt_out)+ ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    return [Name + '_ThPort' + str(ncell) + '_' +str(cnt_out) ]
