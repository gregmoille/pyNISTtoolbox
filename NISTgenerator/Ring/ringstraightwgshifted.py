import numpy as np
from copy import copy
from NISTgenerator.Port import CreateThroughPort, CreateThroughPortTilted, CreateThroughPortCurveS
from NISTgenerator.Misc.label import CreateLabel

def CreateWGRingStraightWgShifted(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    layerWg = param.get('layerWg', layer)
    layerTapper = param.get('layerTapper', layer)
    layerLabel = param.get('layerLabel', layer)
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    G = param.get('G', None)
    box = param.get('box', False)
    font = param.get('font', 'Arial')
    LC = param.get('Lc', None)
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    W = param.get('W', None)
    tot_length =  param.get('tot_length', 2000)
    αc0 = param.get('alpha_connect', np.pi/3)

    pulley_dum = param.get('pulley_dum', False)
    Lc_dum = param.get('Lc_dum', None)
    W_dum = param.get('W_dum', None)
    G_dum = param.get('G_dum', None)



    x_pos_text = param.get('x_pos_text', -1000)
    y_pos_text = param.get('y_pos_text', -15)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)
    exp_w = param.get('exp_w', None)
    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)
    x_shift = param.get('x_shift', 0)
    xdec = param.get('xdec', 0)
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', None)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', None)
    output_inv_taper_length = param.get('output_inv_taper_length', None)
    output_inv_taper_W = param.get('output_inv_taper_W', None)





    left_label = param.get('left_label', False)
    x_text_left = param.get('x_text_left', 0)


    params_port = copy(param)

    if not type(G) == list:
        G = [G]
    if not type(RR) == list:
        RR = [RR]
    if not type(RW) == list:
        RW = [RW]
    if not type(W) == list:
        W = [W]
    if not type(input_inv_taper_W) == list:
        input_inv_taper_W = [input_inv_taper_W]


    if pulley_dum:
        if not type(Lc_dum) == list:
            Lc_dum = [Lc_dum]
        if not type(W_dum) == list:
            W_dum = [W_dum]
        if not type(G_dum) == list:
            G_dum = [G_dum]
    else:
        Lc_dum = [0]
        W_dum = [0]
        G_dum = [0]

    name_out = []

    cnt = 0
    cnt_shift = 0
    name_out = []
    name_loop = []
    # print('------------------------------------')
    y_pos = y0

    for g in G:
        for rw in RW:
            for rrOut in RR:
                for w in W:
                    for wtap in input_inv_taper_W:
                        rr  = rrOut - rw
                        for lc_dum in Lc_dum:
                            for w_dum in W_dum:
                                for g_dum in G_dum:

                                    # print('Creating Straight WG coupled to RR: ')
                                    # print('On the layer {}'.format(layer))
                                    # print('RR={} RW={} '.format(rrOut, rw) +
                                    #       'g={} W={}\n'.format(g, w))

                                    # ------------------------------
                                    # fix for the correct RR deifintion with the pulley
                                    # ------------------------------

                                    r1 = rr + g +w/2
                                    x_xtx = x0 + x_pos_text

                                    name_out = []

                                    # Create the First Through port

                                    αc = αc0
                                    # Ls = r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2) + 2*rr
                                    Ls = inp_WG_L#-2*np.sin(lc/(rr+g+w/2)/2)*(rr+g+w/2)
                                    xstart =  tot_length/2
                                    input_st_length = xstart - input_inv_taper_length - Ls
                                    # Y0 = y_shift + y_pos
                                    y_pos = y_shift + y_pos
                                    # y_posR = copy(y_pos)
                                    rext = rr + rw + g+ w/2

                                    WG_through_port_y_pos = y_pos
                                    Rdec = rext

                                    x_pos0 = xdec -  Ls - input_st_length
                                    cx1 = - r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                    if cnt_shift>0:
                                        x_pos = x_shift * cnt_shift + x_pos0# - (cx1 - 3*rr)
                                        xpos1 = x_shift  + x_pos0 - (cx1 - 3*rr)
                                        # x_sleft = xpos1 - 2*x_shift -rr
                                        x_sleft = x_pos0
                                        #
                                        # x_left = x_sleft - x_shift -rr
                                        x_left = x0 - inp_WG_L - input_st_length
                                        x_sleft_out = x_pos - x_shift
                                        x_right = x_pos - (cx1 - rr)
                                        y_sleft = y_pos -2*rr + (rr-Rdec) - rw

                                        # cx1 = x_left + (x_shift -rr)
                                        # cy1 = y_pos + (θ - Δ)/1.25
                                        # cx2 = cx1
                                        # cy2 = y_pos - rr #y_pos + (rr++w/2) - rr*rr/r1

                                        if x_right> tot_length/2  - input_inv_taper_length:
                                            cx1 = 0 #- r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                            y_pos = y_pos - 2*rr
                                            WG_through_port_y_pos = WG_through_port_y_pos - 2*rr
                                            cnt_shift = 0
                                            # y_pos = y_shift * cnt + y0
                                            # x_pos = x_shift * cnt_shift + x_pos0 - (cx1 - 2*rr)
                                            x_pos = x_pos0
                                            x_left = x_pos  + (cx1 - 2*rr)
                                            x_sleft = 0
                                            x_right = x_pos  - (cx1 - rr)
                                            y_sleft = 0
                                            x_sleft_out = 0

                                    else:
                                        x_pos = x_pos0 #- (cx1 - 2*rr)
                                        x_left = x_pos + (cx1 - 2*rr)
                                        x_sleft = 0
                                        x_right = x_pos  - (cx1 - 2*rr)
                                        y_sleft = 0
                                        x_sleft_out = 0

                                    fid.write(str(layer) + ' layer\n')


                                    # fid.write('<{} {} '.format(x_pos, y_pos) +
                                    #           '{} {} {} '.format(rr, rw, nr) +
                                    #           '{} {} {} '.format(g, lc, nr) +
                                    #           '{} {} {} '.format(w, 20, 2) +
                                    #           '0 ringPulleyLC>\n')


                                    name_out.append(
                                        Name + 'C' + str(ncell) + '_' + str(cnt))
                                    fid.write('<' + Name + 'C' + str(ncell) +
                                      '_' + str(cnt) + ' struct>\n')
                                    dec = 0#rr - r1*(1-np.cos(lc/(r1)/2))*(r1) + 1.52888

                                    fid.write('<{} {} '.format(x_pos, y_pos-Rdec ) +
                                              '{} {} '.format(rr, rw) +
                                              '{} '.format(g) +
                                              '{} '.format(20) +
                                              '{} '.format(w) +
                                              '0 ringInfiniteV>\n')

                                    if pulley_dum:
                                        print(f'++++++++ {g_dum} ++++++++=')

                                        # θ = lc_dum/2 / (2*np.pi*rr)
                                        ri = rr + rw + g_dum
                                        r0 = rr + rw + w_dum + g_dum
                                        r_half= (ri + r0) /2


                                        θ = lc_dum/(r_half)

                                        θstart = np.pi/3.5
                                        θend = θstart - θ# -np.pi/2

                                        # Ll = 10*np.cos(θ)
                                        # Lh = 10*np.sin(θ)
                                        # print('Lh')
                                        # print(f"{Lh:.0f}")
                                        # print('Ll')
                                        # print(f"{Ll:.0f}")



                                        fid.write(f'\t{x_pos} {y_pos-Rdec} '+
                                                   f'{ri} {r0} {θend*180/np.pi} {θstart*180/np.pi} 1000 torus \n')

                                        # add an other torud
                                        Rthingy = 4
                                        xcc = x_pos + (r_half + Rthingy) * np.cos(θstart)
                                        ycc = y_pos-Rdec +(r_half + Rthingy) * np.sin(θstart)
                                        θthingy = (θstart+np.pi)*180/np.pi
                                        fid.write(f'\t{xcc} {ycc} '+
                                            f'{Rthingy-w_dum/2} {Rthingy+w_dum/2} {θthingy - 90} {θthingy} 1000 torus \n')


                                        xcc = x_pos + (r_half + Rthingy) * np.cos(θend)
                                        ycc = y_pos-Rdec +(r_half + Rthingy) * np.sin(θend)
                                        θthingy = (θend + np.pi)*180/np.pi
                                        fid.write(f'\t{xcc} {ycc} '+
                                            f'{Rthingy-w_dum/2} {Rthingy+w_dum/2} {θthingy} {θthingy+90} 1000 torus \n')


                                    yc = y_pos -(r1-rr -g - w)
                                    y_txt = WG_through_port_y_pos + y_pos_text
                                    params_port['name'] = Name + '_' + str(cnt)
                                    params_port['RR'] = rr
                                    params_port['G'] = g
                                    params_port['RW'] = rw
                                    params_port['W'] = w
                                    params_port['inp_WG_L'] = Ls
                                    params_port['input_st_length'] = input_st_length
                                    params_port['input_inv_taper_W'] = wtap
                                    if output_inv_taper_W == input_inv_taper_W:
                                        params_port['output_inv_taper_W'] = wtap
                                    else:
                                        params_port['output_inv_taper_W'] = output_inv_taper_W
                                    params_port['resist'] = 'negative'
                                    params_port['cap'] = False
                                    params_port['layerWg'] = layerWg
                                    params_port['layerTapper'] = layerTapper
                                    params_port['x2_in_wg'] = x_left
                                    params_port['x1_out_wg'] = x_right
                                    params_port['xin_c'] = x_sleft
                                    params_port['yin_c'] = y_sleft
                                    params_port['x_sleft_out'] = x_sleft_out
                                    params_port['xR'] = x_pos #- np.sin(lc/(rr+g+w/2)/2)*(rr+g+w/2)
                                    params_port[
                                        'WG_through_port_y_pos'] = WG_through_port_y_pos

                                    if cnt_shift>0:
                                        name_out += CreateThroughPortCurveS(fid, params_port, ncell,cnt)
                                    else:
                                        # print('ICI')
                                        name_out += CreateThroughPort(fid, params_port, ncell,cnt)


                                    # # conenct left
                                    αc = αc0
                                    x1 = x_pos #- 2*np.sin(lc/(rext)/2)*rext #- 20
                                    if cnt_shift>0:
                                        αc = 2*αc
                                        # x1 = x_pos - (r1-w/2)*np.sin(0.5*lc/r1) #- np.sin(lc/(rr+g+w/2)/2)*(rr+g+w/2)

                                        y1 = yc #+ (r1-w/2)*np.cos(0.5*lc/r1)
                                        cx1 = x_pos - 2*rr #- r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                        cy1 = yc #+ r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                        cx2 = x_pos - x_shift + rr
                                        # cy2 = y_pos - rr - Rdec #y_pos + (rr++w/2) - rr*rr/r1
                                        cy2 = y_sleft
                                        x2 =  x_pos - x_shift
                                    # else:
                                    #     x1 = x_pos #- (r1-w/2)*np.sin(0.5*lc/r1)
                                    #     y1 = yc + (r1-w/2)*np.cos(0.5*lc/r1)
                                    #     cx1 = x_pos - r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                    #     cy1 = yc + r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                                    #     cx2 = cx1
                                    #     cy2 = y_pos + ((θ - Δ))/1.25
                                    #     x2 =  cx1 - 2*rr
                                        y2 = cy2
                                        fid.write(str(layer) + ' layer\n')
                                        fid.write('\t<{} {} '.format(x2, y2) +
                                                  '{} {} '.format(x1-10, WG_through_port_y_pos) +
                                                  '{} {} '.format(w, 0) +
                                                  'sBend>\n')


                                    else:
                                        fid.write(str(layerWg) + ' layer\n')
                                        fid.write('<{} {} '.format(x_left, WG_through_port_y_pos) +
                                                '{} {} '.format(x1-10, WG_through_port_y_pos) +
                                                '{} '.format(w) +
                                                  '0 0 0 waveguide>\n')

                                     # conenct right
                                    x1r = x_pos #+ 2*np.sin(lc/(rext)/2)*rext #+ 20
                                    fid.write(str(layerWg) + ' layer\n')
                                    fid.write('<{} {} '.format(x1r+10, WG_through_port_y_pos) +
                                            '{} {} '.format(x_right, WG_through_port_y_pos) +
                                            '{} '.format(w) +
                                              '0 0 0 waveguide>\n')


                                    # conen
                                    # Create the label
                                    if len(RR)>1:
                                        txt_RR = 'RR={:.3f}'.format(rrOut)
                                    else:
                                        txt_RR = ''

                                    if len(G)>1:
                                        txt_G = ' G={:.0f}'.format(g*1e3)
                                    else:
                                        txt_G = ''

                                    if len(W)>1:
                                        txt_W = ' W={:.0f}'.format(w*1e3)
                                    else:
                                        txt_W= ''

                                    if len(RW)>1:
                                        txt_RW = ' RW={:.1f}'.format(rw*1e3)
                                    else:
                                        txt_RW = ''

                                    if len(input_inv_taper_W)>1:
                                        txt_input_inv_taper_W = ' Wtap={:.3f}'.format(wtap*1e3)
                                    else:
                                        txt_input_inv_taper_W = ' '

                                    if len(G_dum)>1:
                                        txt_Gdum = ' Gpul={:.0f}'.format(g_dum*1e3)
                                    else:
                                        txt_Gdum = ''
                                    if len(Lc_dum)>1:
                                        txt_Lcdum = ' Lpul={:.0f}'.format(lc_dum)
                                    else:
                                        txt_Lcdum = ''
                                    if len(W_dum)>1:
                                        txt_Wdum = ' Wpul={:.0f}'.format(w_dum*1e3)
                                    else:
                                        txt_Wdum = ''


                                    txt = txt_RR + txt_RW + txt_G + txt_W + txt_input_inv_taper_W + txt_Lcdum + txt_Wdum + txt_Gdum
                                    # txt = 'RR={:.3f}um RW={:.3f}um '.format(rr, rw) + \
                                    #     'G={:.3f}um W={:.3f} Wtap={:.0f}'.format(g, w, wtap*1e3)
                                    par_lab = {'x_pos_text': x_pos_text,
                                               'y_pos_text': y_txt,
                                               'txt': txt,
                                               'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}
                                    par_lab['layer'] = layerLabel
                                    par_lab['box'] = box
                                    par_lab['font'] = font
                                    par_lab['font_size_pattern'] = 8
                                    name_out += CreateLabel(fid, par_lab, ncell)




                                    if left_label:

                                        # subcell = subcell.replace('.', 'p')

                                        par_lab = {'x_pos_text': x_text_left,
                                                   'y_pos_text': y_txt,
                                                   'txt': txt,
                                                   'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}
                                        par_lab['layer'] = layerLabel
                                        par_lab['box'] = box
                                        par_lab['font'] = font
                                        par_lab['font_size_pattern'] = 8
                                        name_out += CreateLabel(fid, par_lab, ncell)





                                    # subcell = '{}RR{:.0f}RW{:.0f}G{:.0f}Wtap{:.0f}'.format(Name,rr*1e3, rw*1e3, g*1e3, wtap*1e3)
                                    subcell = '{}Rg{}'.format(Name, cnt)


                                    subcell = subcell.replace('.', 'p')
                                    fid.write('<' + subcell + '_' + str(ncell) +
                                                  '_' + str(cnt) + ' struct>\n')
                                    for n in name_out:
                                        fid.write('<' + n + ' 0 0 0 1 0 instance>\n')
                                    fid.write('\n')
                                    name_loop.append(
                                        subcell + '_' + str(ncell) + '_' + str(cnt))







                                    cnt += 1
                                    cnt_shift += 1
    fid.write('<'+ Name + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')

    return [Name + str(ncell)]
