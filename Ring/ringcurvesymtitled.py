import numpy as np
from copy import copy
from NISTgenerator.Port import CreateThroughPort, CreateThroughPortTilted
from NISTgenerator.Misc.label import CreateLabel

def CreateRingCurveWGSymmetricTiltWg(fid, param, ncell):
    Name = param.get('name', None)
    layer = param.get('layer', None)
    layerWg = param.get('layerWg', layer)
    layerTapper = param.get('layerTapper', layer)
    layerLabel = param.get('layerLabel', layer)
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    G = param.get('G', None)
    LC = param.get('Lc', None)
    R1 = param.get('R1', None)
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    W = param.get('W', None)
    tot_length =  param.get('tot_length', 2000)
    αc0 = param.get('alpha_connect', np.pi/3)

    x_pos_text = param.get('x_pos_text', -1000)
    y_pos_text = param.get('y_pos_text', -20)
    nr = param.get('nr', 1000)
    inp_WG_L = param.get('inp_WG_L', None)
    exp_w = param.get('exp_w', None)
    font_size_pattern = param.get('font_size_pattern', 10)
    y_shift = param.get('y_shift', 0)

    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_st_length = param.get('input_st_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    input_inv_taper_W = param.get('input_inv_taper_W', None)
    output_st_length = param.get('output_st_length', None)
    output_inv_taper_st_length = param.get('output_inv_taper_st_length', None)
    output_inv_taper_length = param.get('output_inv_taper_length', None)
    output_inv_taper_W = param.get('output_inv_taper_W', None)

    params_port = copy(param)

    if not type(G) == list:
        G = [G]
    if not type(RR) == list:
        RR = [RR]
    if not type(RW) == list:
        RW = [RW]
    if not type(LC) == list:
        LC = [LC]
    if not type(R1) == list:
        R1 [R1]
    if not type(W) == list:
        W = [W]
    name_out = []

    cnt = 0
    name_out = []
    name_loop = []
    print('------------------------------------')
    for lc in LC:
        for g in G:

            for rw in RW:
                for rr in RR:
                    for r1 in R1:
                        for w in W:
                            print('Creating Pulley WG coupled to RR: ')
                            print('On the layer {}'.format(layer))
                            print('RR={} RW={} '.format(rr, rw) +
                                  'g={} R1={} W={} Lc={}\n'.format(g, r1,w,lc))

                            y_pos = y_shift * cnt + y0
                            θ = r1*np.cos(lc/(2*r1))

                            Δ = r1- (rr + g + w/2)

                            # WG_through_port_y_pos = y_pos + (rr++w/2) - rr/2 * rr/r1
                            WG_through_port_y_pos = y_pos + (θ - Δ)/2
                            # WG_through_port_y_pos = y_pos+rr+g+w/2+-2 * \
                            #     (1-np.cos(lc/(rr+g+w/2)/2))*(rr+g+w/2)
                            x_xtx = x0 + x_pos_text
                            y_txt = y_pos + y_pos_text
                            name_out = []

                            # Create the First Through port
                            yc = y_pos -(r1-rr -g - w)
                            αc = αc0
                            Ls = r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2) + 2*rr

                            xstart =  tot_length/2
                            input_st_length = xstart - input_inv_taper_length - Ls

                            params_port['name'] = Name + '_' + str(cnt)
                            params_port['RR'] = rr
                            params_port['G'] = g
                            params_port['RW'] = rw
                            params_port['W'] = w
                            params_port['inp_WG_L'] = Ls
                            params_port['input_st_length'] = input_st_length
                            params_port['resist'] = 'negative'
                            params_port['cap'] = True
                            params_port['layerWg'] = layerWg
                            params_port['layerTapper'] = layerTapper
                            

                            params_port[
                                'WG_through_port_y_pos'] = WG_through_port_y_pos
                            name_out += CreateThroughPort(fid, params_port, ncell,cnt)


                            # Create second Through port
                            αc = αc0
                            Ls = r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2) + 2*rr

                            xstart =  tot_length/2
                            input_st_length = xstart - input_inv_taper_length - Ls
                            params_port[
                                'WG_through_port_y_pos'] =  y_pos -  (θ - Δ)/2
                            name_out += CreateThroughPortTilted(fid, params_port, ncell,cnt)

                            # Create Pulley Ring
                            #<x y ri Wr re N g Lc Nwg W We LS EC ringPulleyInvPosLCA>
                            
                            
                            # H = r1 *np.sin(θ)/
                            fid.write(str(layer) + ' layer\n')
                            name_out.append(
                                Name + 'Cell' + str(ncell) + '_' + str(cnt))
                            fid.write('<' + Name + 'Cell' + str(ncell) +
                                      '_' + str(cnt) + ' struct>\n')
                            # fid.write('<{} {} '.format(x0, y_pos) +
                            #           '{} {} {} '.format(rr, rw, exp_w) +
                            #           '{} {} {} '.format(nr,g, lc) +
                            #           '{} {} {} '.format(nr,W, exp_w) +
                            #           '{} {} '.format(Ls, -H) +
                            #           '0 ringSymmetricInvPosLC>\n')
                            # Create the ring
                            fid.write('\t{} {} '.format(x0, y_pos) +
                                      '{} {} '.format(rr-rw, rr) +
                                      'torusVector\n')

                            #create the curve coupling
                            θs = 90 + 180*(0.5*lc/r1)/np.pi
                            θe = 90 - 180*(0.5*lc/r1)/np.pi
                            
                            fid.write('\t{} {} '.format(x0, yc) +
                                      '{} {} '.format(r1-w, r1) +
                                      '{} {} {} '.format(θe, θs, nr) +
                                      'torus\n')

                            #create the curve bottom coupling
                            θs = 270 + 180*(0.5*lc/r1)/np.pi
                            θe = 270 - 180*(0.5*lc/r1)/np.pi
                            
                            yc2 = y_pos  + (r1-rr -g - w)
                            fid.write(str(layer) + ' layer\n')
                            fid.write('\t{} {} '.format(x0, yc2) +
                                      '{} {} '.format(r1-w, r1) +
                                      '{} {} {} '.format(θe, θs, nr) +
                                      'torus\n')

                            # conenct right
                            
                            x1 = x0 + (r1-w/2)*np.sin(0.5*lc/r1)
                            y1 = yc + (r1-w/2)*np.cos(0.5*lc/r1) 
                            cx1 = x0 + r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cy1 = yc + r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cx2 = cx1
                            cy2 = y_pos + ((θ - Δ))/2 #y_pos + (rr++w/2) - rr*rr/r1
                            x2 =  cx1+ 2*rr  
                            y2 = cy2
                            fid.write(str(layer) + ' layer\n')
                            fid.write('\t<{} {} '.format(x1, y1) +
                                      '{} {} '.format(cx1, cy1) +
                                      '{} {} '.format(cx2, cy2) +
                                      '{} {} '.format(x2, y2) +
                                      '{} {} '.format(w, 0) +
                                      'bezierCurve>\n')
                            
                            # conenct left
                            αc = αc0
                            x1 = x0 - (r1-w/2)*np.sin(0.5*lc/r1)
                            y1 = yc + (r1-w/2)*np.cos(0.5*lc/r1) 
                            cx1 = x0 - r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cy1 = yc + r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cx2 = cx1
                            cy2 = y_pos + ((θ - Δ))/2 #y_pos + (rr++w/2) - rr*rr/r1
                            x2 =  cx1 - 2*rr  
                            y2 = cy2
                            fid.write(str(layer) + ' layer\n')
                            fid.write('\t<{} {} '.format(x1, y1) +
                                      '{} {} '.format(cx1, cy1) +
                                      '{} {} '.format(cx2, cy2) +
                                      '{} {} '.format(x2, y2) +
                                      '{} {} '.format(w, 0) +
                                      'bezierCurve>\n')


                            # conenct right bottom
                            
                            x1 = x0 + (r1-w/2)*np.sin(0.5*lc/r1)
                            y1 = yc2 - (r1-w/2)*np.cos(0.5*lc/r1) 
                            cx1 = x0 + r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cy1 = yc2 - r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cx2 = cx1
                            cy2 = y_pos - ((θ - Δ))/2 #y_pos + (rr++w/2) - rr*rr/r1
                            x2 =  cx1+ 2*rr  
                            y2 = cy2
                            fid.write(str(layer) + ' layer\n')
                            fid.write('\t<{} {} '.format(x1, y1) +
                                      '{} {} '.format(cx1, cy1) +
                                      '{} {} '.format(cx2, cy2) +
                                      '{} {} '.format(x2, y2) +
                                      '{} {} '.format(w, 0) +
                                      'bezierCurve>\n')
                            
                            # conenct left bottom
                            αc = αc0
                            x1 = x0 - (r1-w/2)*np.sin(0.5*lc/r1)
                            y1 = yc2 - (r1-w/2)*np.cos(0.5*lc/r1) 
                            cx1 = x0 - r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cy1 = yc2 - r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                            cx2 = cx1
                            cy2 = y_pos - ((θ - Δ))/2 #y_pos + (rr++w/2) - rr*rr/r1
                            x2 =  cx1 - 2*rr  
                            y2 = cy2
                            fid.write(str(layer) + ' layer\n')
                            fid.write('\t<{} {} '.format(x1, y1) +
                                      '{} {} '.format(cx1, cy1) +
                                      '{} {} '.format(cx2, cy2) +
                                      '{} {} '.format(x2, y2) +
                                      '{} {} '.format(w, 0) +
                                      'bezierCurve>\n')

                            # Create the label
                            txt = 'RR={:.0f}um RW={:.3f}um '.format(rr, rw) + \
                                'G={:.3f}um W={:.3f} Lc={:.0f}um R1={:.0f}'.format(g, w, lc, r1)
                            par_lab = {'x_pos_text': x_pos_text,
                                       'y_pos_text': y_txt,
                                       'txt': txt,
                                       'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}
                            par_lab['layer'] = layerLabel
                            name_out += CreateLabel(fid, par_lab, ncell)
            
            
                            subcell = 'RR{}RW{}G{}LC'.format(rr, rw, g, lc)
                            subcell = subcell.replace('.', 'p')
                            fid.write('<' + subcell + '_' + str(ncell) +
                                      '_' + str(cnt) + ' struct>\n')
                            for n in name_out:
                                fid.write('<' + n + ' 0 0 0 1 0 instance>\n')
                            fid.write('\n')
                            name_loop.append(
                                subcell + '_' + str(ncell) + '_' + str(cnt))

                            cnt += 1
    fid.write('<RingPulleyWg_MainCell' + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')

    return ['RingPulleyWg_MainCell' + str(ncell)]
