import ipdb
import numpy

def CreatePortShapeSymmetric(fid, param, ncell, cnt_out):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    # y_pos = param.get('y_pos', None)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)
    W = param.get('W', None)
    exp_w = param.get('exp_w', None)
    tot_length = param.get('tot_length', None)


    drop_through = param.get('drop_through', 1)
    y_shift = param.get('y_shift', 0)
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', None)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', None)
    output_inv_taper_length = param.get('output_inv_taper_length', None)
    output_inv_taper_W = param.get('output_inv_taper_W', None)
    PortDist = param.get('PortDist', None)
    y_connect = param.get('y_connect', None)


    # input_WG_length = input_inv_taper_st_length + \
    #     input_inv_taper_length+input_st_length
    # final_WG_length = output_inv_taper_st_length + \
    #     output_inv_taper_length+output_st_length

    name_out = []


    # ---------------------------------------------------------
    #     -- Compute coordinate for the through port --
    # ---------------------------------------------------------
    # Through port
    #    <--------------------------------------------------- total length ----------------------------------------------------------------->
    #    <- input_inv_taper_length  ->                                                                      <-  output_inv_taper_length ->
    #                                   <-input_st_length->
    #                                                       <  2*inp_WG_L >
    #                                                                       <----------   automatic --------->
    #                                             /--------- -------^------- --------------\    
    #-- ------------------------------   -------/                                           \------------------------------------------------ --- y_thrgh
    #    ^                             ^                   ^       x0      ^                                  ^                              ^
    # x1_in_lin                    x2_in_lin           x2_in_wg         x1_out_wg                       x1_out_lin                       x2_out_lin


    Lauto = tot_length/2 - (inp_WG_L/2 + input_inv_taper_length)
    x1_in_lin = x0 - inp_WG_L/2 - Lauto - input_inv_taper_length
    x2_in_lin = x0 - inp_WG_L/2 - Lauto
    x2_in_wg = x0 - inp_WG_L/2
    x1_out_wg = x0 + inp_WG_L/2
    x2_out_lin = tot_length + x1_in_lin
    x1_out_lin = x2_out_lin - input_inv_taper_length

    y_thrgh = y0 + drop_through*PortDist/2

    # ---------------------------------------------------------
    #             -- Create the Through port --
    # ---------------------------------------------------------
    #  -- Create the left cap- --
    x1_in_cap = x1_in_lin - input_inv_taper_st_length
    name_out.append(Name + 'InCapSt' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InCapSt' + 'Cell' +
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

    name_out.append(Name + 'InLin' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'InLin' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('\t<{} {} '.format(x1_in_lin, y_thrgh) +
              '{} {} '.format(x2_in_lin, y_thrgh) +
              '{} {} '.format(W1_in_lin, W2_in_lin) +
              '{} {} '.format(Ws1_in_lin, Ws2_in_lin) +
              '0 linearTaperSlot>\n')

    # # -- Create Left S waveguide --
    name_out.append(Name + 'SIn_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write('<' + Name + 'SIn_' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    L = x2_in_wg - x2_in_lin
    H = y_connect - y_thrgh
    fid.write('\t<{} {} '.format(x2_in_lin, y_thrgh) +
              '{} {} '.format(L, H) +
              '{} {} '.format(W, exp_w) +
              '0 sBendInv>\n')

    # -- Create Right S waveguide --
    name_out.append(Name + 'Sout_' + 'Cell' +
                    str(ncell)+ '_' + str(cnt_out))
    fid.write('<' + Name + 'Sout_' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    L = x1_out_lin - x1_out_wg
    H = y_thrgh - y_connect
    fid.write('\t<{} {} '.format(x1_out_wg, y_connect) +
              '{} {} '.format(L, H) +
              '{} {} '.format(W, exp_w) +
              '0 sBendInv>\n')


    # -- Create the output linear tapper --
    W1_in_lin = input_inv_taper_W+2*exp_w
    W2_in_lin = W+2*exp_w
    Ws1_in_lin = input_inv_taper_W
    Ws2_in_lin = W
    name_out.append(Name + 'OutLin' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'OutLin' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('<{} {} '.format(x1_out_lin, y_thrgh) +
              '{} {} '.format(x2_out_lin, y_thrgh) +
              '{} {} '.format(W2_in_lin, W1_in_lin) +
              '{} {} '.format(Ws2_in_lin, Ws1_in_lin) +
              '0 linearTaperSlot>\n')


    # #  -- Create end cap --
    x2_out_cap = x2_out_lin + input_inv_taper_st_length
    W_out_tap = input_inv_taper_W
    We_out_tap = (W1_in_lin - W_out_tap)/2

    name_out.append(Name + 'OutCapSt' + 'Cell' +
                    str(ncell) + '_' + str(cnt_out))
    fid.write('<' + Name + 'OutCapSt' + 'Cell' +
              str(ncell) + '_' + str(cnt_out) + ' struct>\n')
    fid.write('<{} {} '.format(x2_out_lin, y_thrgh) +
              '{} {} '.format(x2_out_cap, y_thrgh) +
              '{} {} '.format(input_inv_taper_W, We_out_tap) +
    '0 0 1 waveguideInv>\n')

    # ---------------------------------------------------------
    #        -- Merge everything in 1 structure --
    # ---------------------------------------------------------
    fid.write('\n')
    fid.write('<' + Name + '_ThroughPort' + str(ncell) +
               '_' +str(cnt_out)+ ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    return [Name + '_ThroughPort' + str(ncell) + '_' +str(cnt_out) ]
