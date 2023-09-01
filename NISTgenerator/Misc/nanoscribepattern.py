import numpy

def NanoScribePattern(fid, param, ncell):

    xin = param.get('xin', None)
    yin = param.get('yin', None)
    # xout = param.get('xout', None)
    # yout = param.get('yout', None)
    ECl = param.get('ECl', 1)
    ECr = param.get('ECr', 1)
    W = param.get('W', 19.746)
    We = param.get('We', 2.946)
    layer = param.get('layer', 1)
    Name = param.get('name', 'NS_Ptrn')
    omit = param.get('omit', 1)
    theta = param.get('theta',0)
    wtap = param.get('wtap',0)

    polarity = param.get('polarity', 'positive')
    fid.write(str(layer) + ' layer\n')
    fid.write('<' + Name + 'Cell' + str(ncell) + ' struct>\n')


    y0 = 2.713
    wemark = 0.714
    wmark = 1.428
    wetrench = 2
    ydec = 2.142
    for k in range(omit, 4):
        #--Left side pattern:
        #--------------------
        if polarity == 'positive':
            fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin + y0 + k*ydec) +
                      '{:.3f} {:.3f} '.format(xin + 100, yin + y0 + k*ydec) +
                      '{:.3f} {:.3f} '.format(wmark, wemark) +
                      '{} '.format(theta) +
                      '1 1 waveguideInv>\n')

            fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin - y0 - k*ydec) +
                      '{:.3f} {:.3f} '.format(xin + 100, yin - y0 - k*ydec) +
                      '{:.3f} {:.3f} '.format(wmark, wemark) +
                      '{} '.format(theta) +
                      '1 1 waveguideInv>\n')
        else:
            fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin + y0 + k*ydec) +
                      '{:.3f} {:.3f} '.format(xin + 100, yin + y0 + k*ydec) +
                      '{:.3f} '.format(wmark) +
                      '{} '.format(theta) +
                      '1 1 waveguide>\n')

            fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin - y0 - k*ydec) +
                      '{:.3f} {:.3f} '.format(xin + 100, yin - y0 - k*ydec) +
                      '{:.3f} '.format(wmark) +
                      '{} '.format(theta) +
                      '1 1 waveguide>\n')
            # fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin + 2.713 + k*ydec) +
            #           '{:.3f} {:.3f} '.format(xin + 100, yin + 2.713 + k*ydec) +
            #           '{:.3f} {:.3f} '.format(1.428, wemark) +
            #           '{} '.format(theta) +
            #           '1 0 waveguide\n>')
            #
            # fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin - 2.713 - k*ydec) +
            #           '{:.3f} {:.3f} '.format(xin + 100, yin - 2.713 - k*ydec) +
            #           '{:.3f} {:.3f} '.format(1.428, wemark) +
            #           '{} '.format(theta) +
            #           '1 0 waveguideInv>\n')



#-- Seperators at bound of pattern (left):
#----------------------------------
    if polarity == 'positive':
        fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin) +
                  '{:.3f} {:.3f} '.format(xin + 100, yin) +
                  '{:.3f} {:.3f} '.format(19.706, 2.946) +
                  '{} '.format(theta) +
                  '{:.0f} {:.0f} '.format(ECl, ECr) +
                  ' waveguideInv>\n')
    if polarity == 'negative':
        Wblock = 3
        fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin + y0 + 3*ydec + wmark/2 + 2.946 + Wblock/2) +
                  '{:.3f} {:.3f} '.format(xin + 100, yin + y0 + 3*ydec +  wmark/2 + 2.946 + + Wblock/2) +
                  '{:.3f} '.format(Wblock) +
                  '{} '.format(theta) +
                  '1 1 waveguide>\n')
        fid.write('\t<{:.3f} {:.3f} '.format(xin - 50, yin - y0 - 3*ydec - wmark/2 -2.946 - Wblock/2) +
                  '{:.3f} {:.3f} '.format(xin + 100, yin - y0 - 3*ydec  - wmark/2 - 2.946 - Wblock/2) +
                  '{:.3f} '.format(Wblock) +
                  '{} '.format(theta) +
                  '1 1 waveguide>\n')


    return [Name + 'Cell' + str(ncell)]
