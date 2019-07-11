from .create2x2mmi import Create2x2Mmi
from NISTgenerator.Misc.label import CreateLabel
from copy import copy
import numpy as np

def Create2x2MmiCascaded(fid, param, ncell):

    N = param.get('N', 5)
    x0 = param.get('x0', 0 )
    y0_ = param.get('y0', 0 )
    y_shift = param.get('y_shift', -50)
    x_shift = param.get('x_shift', 150)
    Wmmi = param.get('Wmmi', [0] )
    Dist = param.get('Dist', [0] )
    Wwg = param.get('Wwg', 0 )
    Lmmi = param.get('Lmmi', [0] )
    Wblock_MMI = param.get('Wblock_MMI', 8 )
    debug = param.get('debug', False)
    polarity = param.get('polarity', 0)
    LWg = param.get('LWg', 6) 
    layer = param.get('layer', 1)
    Name = param.get('name', None)
    Ltap = param.get('Ltap',1.25)
    W_guide = param.get('W_guide',Wwg )
    α_wg = param.get('α_wg',np.pi/4)
    exp_w = param.get('exp_w',2)
    tot_length = param.get('tot_length',3800)
    xInput = param.get('xInput', -900)
    wInput = param.get('Wtaper', 100)
    Hdec = param.get('Hdec', 20)
    youtdec = param.get('youtdec', 20)

    BarCross = param.get('type', 'Bar')
    Geo = {}

    if type(Wmmi) is not list:
        try:
            Wmmi = list(Wmmi)
        except:
            Wmmi = [Wmmi]

    if type(Dist) is not list:
        try:
            Dist = list(Dist)
        except:
            Dist = [Dist]

    if type(Lmmi) is not list:
        try:
            Lmmi = list(Lmmi)
        except:
            Lmmi = [Lmmi]
    
    cnt = 0
    name_out = []
    for ll in Lmmi:
        for w in Wmmi:
            for dd in Dist:
                Ltot = 2*LWg + ll
                name_struct = []
                y_pos = y0_ + cnt *y_shift
                rdm = int(np.floor(np.random.rand(1)*1000)[0])
                for n in range(N):
                    x_pos = x0 + n*x_shift
                    param_mmi = copy(param)
                    param_mmi['x_pos'] = x_pos
                    param_mmi['y_pos'] = y_pos
                    param_mmi['Wmmi'] = w
                    param_mmi['Lmmi'] = ll
                    param_mmi['Dist'] = dd
                    param_mmi['name'] = '{}{}_{}'.format(Name,n,rdm)
                    name_struct += Create2x2Mmi(fid, param_mmi, ncell)

                y0 = y_pos + dd/2 + Wwg/2
                if BarCross.lower() == 'bar':
                    for n in range(N-1):
                        
                        xin = x0 +  (n*x_shift) + Ltot
                        xout = x0 +  ((n+1)*x_shift)
                        

                        name_struct.append('CascadedMMI' + str(ncell) + 'Connect1' + str(cnt) + str(n))
                        fid.write('<CascadedMMI' + str(ncell) + 'Connect1' + str(cnt) + str(n) + ' struct>\n')
                        fid.write('\t<{} {} '.format(xin, y0) +
                          '{} {} '.format((xin + xout)/2, y0) +
                          '{} {} '.format(Wwg, W_guide) +
                          '{} {} '.format(2*dd + Wwg,2*exp_w + W_guide) +
                          '0 linearTaperSlot>\n')
                        name_struct.append('CascadedMMI' + str(ncell) + 'Connect1' + str(cnt) + str(n))
                        fid.write('<CascadedMMI' + str(ncell) + 'Connect1' + str(cnt) + str(n) +' struct>\n')
                        fid.write('\t<{} {} '.format((xin + xout)/2, y0) +
                          '{} {} '.format(xout, y0) +
                          '{} {} '.format(W_guide, Wwg) +
                          '{} {} '.format(2*exp_w + W_guide,2*dd + Wwg) +
                          '0 linearTaperSlot>\n')

                elif BarCross.lower() == 'cross':
                    for n in range(N-1):
                        xin = x0 +  (n*x_shift) + Ltot
                        xout = x0 +  ((n+1)*x_shift)
                        y0_in = y_pos + (2*np.mod(n,2)-1)*(dd/2 + Wwg/2)

                        H  =  -1*(2*np.mod(n,2)-1)*(dd + Wwg)

                        name_struct.append('CascadedMMI' + str(ncell) + 'SConnect' + str(cnt) + str(n))
                        fid.write('<CascadedMMI' + str(ncell) + 'SConnect' + str(cnt) + str(n) +' struct>\n')
                        fid.write('\t<{} {} '.format(xin, y0_in) +
                          '{} {} '.format(x_shift-Ltot, H) +
                          '{} {} '.format(Wwg,dd) +
                          '0 sBendInv>\n')

                name_struct.append('InMMI' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<InMMI' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('\t<{} {} '.format(xInput, y0) +
                  '{} {} '.format(x0, y0) +
                  '{} {} '.format(wInput, Wwg) +
                  '{} {} '.format(2*exp_w + wInput,2*dd + Wwg) +
                  '0 linearTaperSlot>\n')


                xout = x0 + (N-1)*x_shift + Ltot
                xend = tot_length + xInput
                yout = y_pos + (2*np.mod(N,2)-1)*(dd/2 + Wwg/2)

                name_struct.append('OutMMI' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<OutMMI' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('\t<{} {} '.format(xout, yout) +
                  '{} {} '.format(xend, yout) +
                  '{} {} '.format(Wwg,wInput) +
                  '{} {} '.format(2*dd + Wwg,2*exp_w + wInput) +
                  '0 linearTaperSlot>\n')

                xout2 = x0 + Ltot
                if BarCross.lower() == 'bar':
                    yout2 =  y_pos - (dd/2 + Wwg/2)
                    yend2 =  Hdec-youtdec
                    H = -Hdec
                if BarCross.lower() == 'cross':
                    yout2 =  y_pos + (dd/2 + Wwg/2)
                    yend2 =  -(Hdec-youtdec)
                    H = +Hdec
                
                
                name_struct.append('OutMMI' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<OutMMI' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('\t<{} {} '.format(xout, yout) +
                  '{} {} '.format(xend, yout) +
                  '{} {} '.format(Wwg,wInput) +
                  '{} {} '.format(2*dd + Wwg,2*exp_w + wInput) +
                  '0 linearTaperSlot>\n')

                name_struct.append('Out2MMI1' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<Out2MMI1' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('\t<{} {} '.format(xout2, yout2) +
                          '{} {} '.format(x_shift, H) +
                          '{} {} '.format(Wwg,dd) +
                          '0 sBendInv>\n')

                name_struct.append('Out2MMI2' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<Out2MMI2' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('\t<{} {} '.format(xout2 + x_shift, yout2+H) +
                          # '{} {} '.format(xend - xout2 - x_shift, yend2) +
                          '{} {} '.format((N-2)*x_shift, yend2) +
                          '{} {} '.format(Wwg,dd) +
                          '0 sBendInv>\n')


                name_struct.append('Out2MMI3' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<Out2MMI3' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('\t<{} {} '.format(xout, yout2+H+yend2) +
                  '{} {} '.format(xend, yout2+H+yend2) +
                  '{} {} '.format(Wwg,wInput) +
                  '{} {} '.format(2*dd + Wwg,2*exp_w + wInput) +
                  '0 linearTaperSlot>\n')

                name_struct.append('CapInMMI' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<CapInMMI' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('<{} {} '.format(xInput-5, y0) +
                  '{} {} '.format(xInput, y0) +
                  '{} {} '.format(wInput, exp_w) +
                  '0 1 0 waveguideInv>\n')

                name_struct.append('CapOUt1MMI' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<CapOUt1MMI' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('<{} {} '.format(xend, yout) +
                  '{} {} '.format(xend+5, yout) +
                  '{} {} '.format(wInput, exp_w) +
                  '0 0 1 waveguideInv>\n')

                name_struct.append('CapOUt2MMI' + str(ncell) + 'Connect' + str(cnt))
                fid.write('<CapOUt2MMI' + str(ncell) + 'Connect' + str(cnt)+ ' struct>\n')
                fid.write('<{} {} '.format(xend, yout2+H+yend2) +
                  '{} {} '.format(xend+5, yout2+H+yend2) +
                  '{} {} '.format(wInput, exp_w) +
                  '0 0 1 waveguideInv>\n')



                # Create the label
                x_pos_text = xInput + 150
                y_txt = y0 -20
                txt = 'Wmmi={:.2f}um Lmmi={:.1f}um '.format(w, ll) + \
                    'Dist={:.2f}um Wwg ={:.0f}nm '.format(dd, Wwg*1e3)
                par_lab = {'x_pos_text': x_pos_text,
                           'y_pos_text': y_txt,
                           'txt': txt,
                           'font_size_pattern': 8,
                           'name': Name + 'Cell' + str(ncell) + '_' + str(cnt)}

                name_struct += CreateLabel(fid, par_lab, ncell)



                name_out.append('CascadedMMI' + str(ncell) + str(cnt))
                fid.write('<CascadedMMI' + str(ncell) + str(cnt) + ' struct>\n')
                for n in name_struct:
                    fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')
                cnt += 1


    fid.write('<CascadedMMI' + str(ncell) + ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')

    fid.write('\n')
    fid.write('# ******************************\n')
    return ['CascadedMMI' + str(ncell)]


