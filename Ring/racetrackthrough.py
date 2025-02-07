from copy import copy
import ipdb
import numpy as np
import scipy.constants as cts
import scipy.signal as signal
from scipy.fft import fft, ifft, ifftshift
from NISTgenerator.Port import CreateThroughDropPortSeparated, CreateThroughPort
from NISTgenerator.Misc import CreateLabel, CreateBumpStruct

from .racetrack import GenerateRaceTrack

def CreateRaceTrackThrough(fid, param, ncell):


    resist = param.get('resist', 'positive')
    # -- General Parameters --
    Name = param.get('name', None)
    layer = param.get('layer', None)
    if resist == 'positive':
        layer_stepper = layer[-1]
        layer_waveguide = layer[-2]
        layerWg = layer[-2]
        layerTapper = layer[-2]
        layer = layer[:-2]
    # layerWg = param.get('layerWg', layer)
    # layerTapper = param.get('layerTapper', layer)

    RR = param.get('RR', None)
    x0 = param.get('x0', None)
    y0 = param.get('y0', None)
    y_shift = param.get('y_shift', 0)
    x_shift = param.get('x_shift', 50)
    xdec = param.get('xdec', x_shift)

    # -- Racetrack Parameters --
    W = param.get('W', None)
    G = param.get('G', None)
    Lrace = param.get('Lrace', None)
    Lc = param.get('Lc', None)
    RR = param.get('RR', None)
    RW = param.get('RW', None)
    p = param.get('p', 0.3553535)
    αc0 = param.get('alpha_connect', np.pi/3)

    # -- Bus parameters --s
    inp_WG_L = param.get('inp_WG_L', None)
    exp_w = param.get('exp_w', None)
    exp_w_tapper = param.get('exp_w_tapper',exp_w )
    tot_length = param.get('tot_length',3850)
    in_tap_etch = param.get('in_tap_etch', 0)
    tapperLength = param.get('tapperLength', None)
    input_inv_taper_length = param.get('input_inv_taper_length', None)
    input_inv_taper_st_length = param.get('input_inv_taper_st_length', None)
    # -- Modulation Parameters --
    Nmodulation = param.get('Nmodulation', None)
    Amodulation = param.get('Amodulation', None)
    Sigmamodulation = param.get('Sigmamodulation', None)
    Gaussmodulation_spread = param.get('Gaussmodulation_spread', None)
    Nmod_pts = param.get('Nmod_pts', 2000)


    # -- Block Between Devices Parameters --
    blockline = param.get('blockline', True)
    y_blockline_dec = param.get('y_blockline_dec', 10)
    x_dec_block = param.get('x_dec_block', 0)


    # -- Label Parameters
    x_pos_text = param.get('x_pos_text', -1000)
    y_pos_text = param.get('y_pos_text', -20)
    x_pos_text_out = param.get('x_pos_text_out', 1500)
    label_out = param.get('label_out', False)
    font_size_pattern = param.get('font_size_pattern', 10)
    font = param.get('font', 'Source Code Pro')



    polarity = param.get('polarity', 'positive')
    params_port = copy(param)
    params_track = copy(param)


    if not type(G) == list:
        G = [G]
    if not type(RW) == list:
        RW = [RW]
    if not type(Lc) == list:
        Lc = [Lc]

    cnt = 0

    if resist == 'positive':
        fid.write('{} layer\n'.format(layer[0]))
    else:
        fid.write('{} layer\n'.format(layer))
    name_loop = []

    y0original = copy(y0)
    # y0 =


    cnt_shift = 0

    # print('tot_length/2  - input_inv_taper_length')
    # print(tot_length/2  - input_inv_taper_length)
    for g in G:
        for rw in RW:
            for lc in Lc:
                name_out = []



                y_pos = y_shift * cnt + y0
                x_xtx = x0 + x_pos_text
                y_txt = y_pos + y_pos_text

                x_pos0 = -tot_length/2 + xdec #-  Lrace/2 - RR
                cx1 = 0 #- r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)

                if cnt_shift>0:
                    x_pos = x_shift * cnt_shift + x_pos0# - (cx1 - 3*rr)
                    x_right = x_pos + Lrace/2 + RR
                    # print(x_right)

                    if x_right >= tot_length/2  - xdec/2:
                        cx1 = 0 #- r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                        y_pos = y_pos
                        # WG_through_port_y_pos = WG_through_port_y_pos - 2*RR
                        cnt_shift = 0
                        # y_pos = y_shift * cnt + y0
                        # x_pos = x_shift * cnt_shift + x_pos0 - (cx1 - 2*rr)
                        x_pos = x_pos0

                else:
                    x_pos = x_pos0 #- (cx1 - 2*rr)



                # Create the Through port
                params_port['name'] = Name + 'Ports_' + str(cnt)
                params_port['RR'] = RR
                params_port['G'] = g
                params_port['RW'] = rw
                params_port['Wthrough'] = W
                params_port['Lc'] = lc
                params_port['in_tap_etch'] = in_tap_etch

                if resist == 'positive':
                    params_port['layer'] = layer_waveguide
                    params_port['layerWg'] = layer_waveguide
                    params_port['layerTapper'] = layer[0]
                else:
                    params_port['layer'] = layer
                    params_port['cap'] = False
                params_port['resist'] = resist
                params_port['WG_through_port_y_pos'] = y_pos
                params_port['inp_WG_L'] = inp_WG_L -2
                name_out += CreateThroughPort(fid, params_port, ncell, cnt)

                if resist == 'positive':
                    # create the bus for the mix and match :
                    params_port2 = copy(params_port)
                    params_port2['layer'] = layer_stepper
                    params_port2['layerWg'] = layer_stepper
                    params_port2['layerTapper'] = layer_stepper
                    params_port2['resist'] = 'negative'

                # name_out += CreateThroughPort(fid, params_port2, ncell, cnt)



                # -- Create the Racetrack
                params_track['G'] = g
                params_track['Lc'] = lc
                params_track['RW'] = rw
                params_track['Ljoin'] = inp_WG_L
                if resist == 'positive':
                    params_track['layer'] = layer[0]
                    params_track['layer_mixmatch'] = layer_stepper
                else:
                    params_track['layer'] = layer
                params_track['y0'] = y_pos
                params_track['x0'] = 0

                name_out += GenerateRaceTrack(fid, params_track, ncell, cnt)
                yc = y_pos

                αc = αc0
                x1 = x_pos #- 2*np.sin(lc/(rext)/2)*rext #- 20
                if cnt_shift>0:
                    αc = 2*αc
                    # x1 = x_pos - (r1-w/2)*np.sin(0.5*lc/r1) #- np.sin(lc/(rr+g+w/2)/2)*(rr+g+w/2)

                    y1 = yc #+ (r1-w/2)*np.cos(0.5*lc/r1)
                    cx1 = x_pos - 2*RR #- r1* np.cos(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                    cy1 = yc #+ r1 * np.sin(np.pi/2 - 0.5*lc/r1 - αc/2)/np.cos(αc/2)
                    cx2 = x_pos - x_shift + RR
                    # cy2 = y_pos - rr - Rdec #y_pos + (rr++w/2) - rr*rr/r1
                    cy2 = x_pos - Lrace/2 - RR
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
                    # fid.write(str(layer) + ' layer\n')
                    # fid.write('\t<{} {} '.format(x2, y2) +
                    #           '{} {} '.format(x1-10, y_pos) +
                    #           '{} {} '.format(w, 0) +
                    #           'sBend>\n')


                # else:
                #     fid.write(str(layerWg) + ' layer\n')
                    # fid.write('<{} {} '.format(x_left, y_pos) +
                    #         '{} {} '.format(x1-10, y_pos) +
                    #         '{} '.format(w) +
                    #           '0 0 0 waveguide>\n')


                # Create the label

                if len(G)>1:
                    txt_G = ' G={:.0f}'.format(g*1e3)
                else:
                    txt_G = ''
                if len(RW)>1:
                    txt_RW = ' RW={:.0f}'.format(rw*1e3)
                else:
                    txt_RW = ''
                if len(Lc)>1:
                    txt_Lc = ' Lc={:.0f}'.format(lc)
                else:
                    txt_Lc = ''



                txt = txt_RW + txt_G + txt_Lc

                if not txt=='':
                    if resist == 'positive':
                        layer_loop = [layer_waveguide]
                        box = True
                    else:
                        layer_loop = [layer]
                        box = False

                    for llyr in layer_loop:
                        par_lab = {'x_pos_text': x_pos_text,
                                   'y_pos_text': y_txt,
                                   'txt': txt,
                                   'font': font,
                                   'layer': llyr,
                                   'box': box,
                                   'name': 'Lbl' + Name.replace('_', '')  + 'Cell' + str(ncell) + '_' + str(cnt)}
                        name_out += CreateLabel(fid, par_lab, ncell)

                        if label_out:
                            par_lab = {'x_pos_text': x_pos_text_out,
                                       'y_pos_text': y_txt,
                                       'txt': txt,
                                       'font': font,
                                       'box': box,
                                       'layer': llyr,
                                       'name': 'Lbl' + Name.replace('_', '') + 'Cell' + str(ncell) + '_' + str(cnt)}
                            name_out += CreateLabel(fid, par_lab, ncell)


                # Create Bottom block waveguide

                if blockline:
                    if resist == 'positive':
                        layer_loop = [layer_stepper, layer_waveguide]
                    else:
                        layer_loop = [layer]
                    for llyr in layer_loop:
                        fid.write(f'{llyr} layer\n')
                        decblock = -50
                        y_drop_out = y_pos - RR
                        L = tot_length + 2*input_inv_taper_st_length
                        x1_in_lin = -L/2 + x0 + x_dec_block
                        xend = L/2 - x0 + x_dec_block

                        name_out.append(Name + 'BottBlckg_' + str(ncell) + '_' + str(cnt))
                        fid.write('<' + Name + 'BottBlckg_' + str(ncell) +
                                  '_' + str(cnt) + ' struct>\n')
                        fid.write('\t<{} {} '.format(x1_in_lin + decblock , y_pos +RR + y_blockline_dec) +
                                      '{} {} '.format(xend - decblock, y_pos + RR +y_blockline_dec ) +
                                      '1 0 1 1 waveguide>\n')


                subcell = 'RR{:.0f}RW{:.3f}W{:.3f}G{:.3f}'.format(RR, W, rw, g)
                subcell = subcell.replace('.', 'p')

                fid.write('<' + subcell + '_' + str(ncell) +
                          '_' + str(cnt) + ' struct>\n')
                for n in name_out:
                    fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

                fid.write('\n')
                name_loop.append(subcell + '_' + str(ncell) + '_' + str(cnt))

                cnt += 1
                cnt_shift += 1


    fid.write('<' + Name + str(ncell) + ' struct>\n')
    for n in name_loop:
        fid.write('\t<' + n + ' 0 {:.3f} 0 1 0 instance>\n'.format(-RR - G[0] - W/2))

    fid.write('\n')
    fid.write('# ******************************\n')

    return [Name + str(ncell)]
