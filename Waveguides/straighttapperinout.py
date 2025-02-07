import numpy
from NISTgenerator.Misc.label import CreateLabel

def StraightTapperInOut(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    layerTapper = param.get('layerTapper', layer)

    xIn = param.get('xIn', None)
    y0 = param.get('y0', None)
    dolabel = param.get('dolabel', True)
    W = param.get('W', None)
    exp_w = param.get('exp_w', None)
    tot_length = param.get('tot_length', None)
    y_shift = param.get('y_shift', 0)
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    
    output_inv_taper_length = input_inv_taper_length
    output_inv_taper_st_length = input_inv_taper_st_length
    output_inv_taper_W = input_inv_taper_W
    
    exp_w_tapper = param.get('exp_w_tapper', exp_w)

    cap = param.get('cap', True)

    tapperLength = param.get('tapperLength', None)

    x_pos_text = param.get('x_pos_text',0)
    y_pos_text = param.get('y_pos_text', -10)
    if not type(W) is list: 
        W = [W]
    if not type(output_inv_taper_W) is list:
        output_inv_taper_W = [output_inv_taper_W]
    if not type(input_inv_taper_W) is list:
        input_inv_taper_W = [input_inv_taper_W]

    name_out = []
    cnt = 0
    # ========================================================================================
    #                       -- How tings are coded --- 
    # ========================================================================================
    #
    #
    #               :---------------=======================================---------------:
    #               ^              ^                                     ^               ^
    #              xIn            xEndTap                               xEndStr          xOut


    xEndTap = xIn + input_inv_taper_length
    xOut = xIn  + tot_length
    xEndStr = xOut - output_inv_taper_length

    cnt = -3

    for wtap in input_inv_taper_W:
        cnt += 2

        par_lab = {'x_pos_text': x_pos_text + 200,
                   'y_pos_text': y0 + cnt * y_shift + 2*y_pos_text,
                   'txt': 'Wtap = {:.3f}um'.format(wtap),
                   'name': Name + 'TapLbl' + str(ncell) + '_' + str(cnt)}
        if dolabel:
            name_out += CreateLabel(fid, par_lab, ncell)
        for w in W:
            y_thrgh = y0 + cnt * y_shift
            name_out.append(Name + 'StrVar' + 'Cell' +
                              str(ncell) + '_' + str(cnt))
            fid.write('<' + Name + 'StrVar' + 'Cell' +
                        str(ncell) + '_' + str(cnt) + ' struct>\n')

            if tapperLength:
                xIn = xIn - tapperLength
            if cap: 
                wvg_type = 'waveguideInv'
                x1_in_cap = xIn - input_inv_taper_st_length
                
                fid.write(str(layerTapper) + ' layer\n')
                
                fid.write('\t<{} {} '.format(x1_in_cap, y_thrgh) +
                        '{} {} '.format(xIn, y_thrgh) +
                        '{} {} '.format(wtap, exp_w_tapper) +
                        '0 1 0 waveguideInv>\n')


            if tapperLength:
                name_out.append(Name + 'Tl_' + 'Cell' +
                            str(ncell)+ '_' + str(cnt))
                fid.write('<' + Name + 'Tl_' + 'Cell' +
                        str(ncell) + '_' + str(cnt) + ' struct>\n')
                fid.write('\t<{} {} '.format(xIn, y_thrgh) +
                        '{} {} '.format(xIn+tapperLength, y_thrgh) +
                        '{} {} '.format(wtap, exp_w_tapper) +
                        '0 0 0 {}>\n'.format(wvg_type))

                xIn = xIn + tapperLength

            fid.write('\t<{} {} '.format(xIn, y_thrgh) +
              '{} {} '.format(xEndTap, y_thrgh) +
              '{} {} '.format(wtap+2*exp_w_tapper, w+2*exp_w) +
              '{} {} '.format(wtap, w) +
              '0 linearTaperSlot>\n')

            fid.write('\t<{} {} '.format(xEndTap, y_thrgh) +
                  '{} {} '.format(xEndStr, y_thrgh) +
                  '{} {} '.format(w, exp_w) +
                  '0 0 0 waveguideInv>\n')

            fid.write('\t<{} {} '.format(xOut, y_thrgh) +
              '{} {} '.format(xEndStr, y_thrgh) +
              '{} {} '.format(wtap+2*exp_w_tapper, w+2*exp_w) +
              '{} {} '.format(wtap, w) +
              '0 linearTaperSlot>\n')

            if tapperLength:
                name_out.append(Name + 'Tr_' + 'Cell' +
                            str(ncell)+ '_' + str(cnt))
                fid.write('<' + Name + 'Tr_' + 'Cell' +
                        str(ncell) + '_' + str(cnt) + ' struct>\n')
                fid.write('\t<{} {} '.format(xOut, y_thrgh) +
                        '{} {} '.format(xOut+tapperLength, y_thrgh) +
                        '{} {} '.format(wtap, exp_w_tapper) +
                        '0 0 0 {}>\n'.format(wvg_type))

                xOut = xOut + tapperLength

            if cap: 
                wvg_type = 'waveguideInv'
                x_out_cap = xOut + output_inv_taper_st_length
                    


                fid.write(str(layerTapper) + ' layer\n')
                
                fid.write('\t<{} {} '.format(xOut, y_thrgh) +
                        '{} {} '.format(x_out_cap, y_thrgh) +
                        '{} {} '.format(wtap, exp_w_tapper) +
                        '0 0 1 waveguideInv>\n')

            
            par_lab = {'x_pos_text': x_pos_text,
                       'y_pos_text': y_thrgh + y_pos_text,
                       'txt': 'W = {:.3f}um'.format(w),
                       'font_size_pattern': 8,
                       'name': Name + 'WLbl' + str(ncell) + '_' + str(cnt)}
            if dolabel:
                name_out += CreateLabel(fid, par_lab, ncell)
            
            if tapperLength:
                xOut = xOut - tapperLength
            cnt += 1

        
    # ---------------------------------------------------------
    #        -- Merge everything in 1 structure --
    # ---------------------------------------------------------
    fid.write('\n')
    fid.write('<' + Name + 'WgTap' + str(ncell) + ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')
    return [Name + 'WgTap' + str(ncell)]
