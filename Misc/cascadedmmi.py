import numpy as np


def CreateVernier(fid, param, ncell):
    Name = param.get('name',None)
    H_long = param.get('H_long', 100)
    H_short = param.get('H_short', 50)
    W = param.get('W', 2)
    Ltot = param.get('Ltot', 200)
    longspace = param.get('longspace', 50)
    shortspace = param.get('shortspace', 5)
    layer = param.get('layer',1)
    y0 = param.get('y0', 0)
    x0 = param.get('x0', 0)
    xdec = param.get('xdec', 50)

    name_out = []
    fid.write(str(layer) + ' layer\n')

    # -- Creating the bounding box -- 
    # ------------------------------------------------------------
    #      xa.       xb
    #       ----------   yb
    #      |          |
    #.     |          |
    #       ----------   ya 

    xspace = 10
    yspace = 10
    xa = 0
    xb = Ltot
    ya = 0
    yb = H_long 

    x1 = [xa+xspace, xb + xspace, xb -xspace, xa-xspace]
    x2 = [xb - xspace, xb + xspace , xa + xspace, xa-xspace]
    y1 = [yb+yspace, yb-yspace, ya-yspace, ya+yspace]
    y2 = [yb+yspace, ya+yspace, ya-yspace, yb-yspace] 

    Wbd = 1
    name_out.append('BoundingVernier' + Name + str(ncell))
    fid.write('<BoundingVernier' + Name + str(ncell) + ' struct>\n')
    for ii in range(0, len(x1)):
        fid.write('\t<{} {} '.format(x1[ii], y1[ii]) +
                  '{} {} '.format(x2[ii], y2[ii]) +
                  '{} 0 '.format(Wbd) +
                  '0 0 waveguide>\n')

    # -- Close the boudning box with 90° bended --
    # ------------------------------------------------------------
    x1 = [xspace, xspace, Ltot-xspace, Ltot-xspace]
    x2 = [-xspace, -xspace, Ltot+xspace, Ltot+xspace]
    y1 = [-yspace, H_long + yspace, H_long+yspace, -yspace]
    y2 = [yspace, H_long - yspace, H_long-yspace, yspace]
    name_out.append('BoundingVernierClose' + Name + str(ncell))
    fid.write('<BoundingVernierClose' + Name + str(ncell) + ' struct>\n')
    for ii in range(0, len(x1)):
        fid.write('\t<{} {} '.format(x1[ii], y1[ii]) +
                  '{} {} '.format(x2[ii], y2[ii]) +
                  '{} 0 '.format(Wbd) +
                  '90degreeBend>\n')

#     fprintf(fid,['<0 -5 -5 0 1 0 90degreeBend>\n']); %Bottom left curve of blocking box
# fprintf(fid,['<205 -5 210 0 1 0 90degreeBend>\n']); %Bottom right curve of blocking box
# fprintf(fid,['<0 105 -5 100 1 0 90degreeBend>\n']); %Top left curve of blocking box
# fprintf(fid,['<205 105 210 100 1 0 90degreeBend>\n']); %Top right curve of blocking box


    # -- Create the major and minor tick --
    # ------------------------------------------------------------
    # name_out.append('Long_vernier' + Name + str(ncell))
    fid.write('<Long_vernier' + Name + str(ncell) + ' struct>\n')
    fid.write('\t<0 0 ' +
              '{} 0 '.format(H_long) +
              '{} 90 '.format(W) +
              '1 1 waveguide>\n')
    # name_out.append('Short_vernier' + Name + str(ncell))
    fid.write('<Short_vernier' + Name + str(ncell) + ' struct>\n')
    fid.write('\t<0 0 ' +
              '{} 0 '.format(H_short) +
              '{} 90 '.format(W) +
              '1 1 waveguide>\n')

    # -- Create the array for vernier --
    # ------------------------------------------------------------
    Nmajor = int(np.floor(Ltot/longspace)) + 1
    name_out.append('Comb_vernier' + Name + str(ncell))
    fid.write('<Comb_vernier' + Name + str(ncell) + ' struct>\n')
    fid.write('\t<Long_vernier' + Name + str(ncell) +
              ' 0 0 ' +
              '{} 1 '.format(Nmajor) +
              '{} 0 1 '.format(longspace) +
              'arrayRect>\n')

    Nminor = int(np.floor(longspace/shortspace))-1
    ydec = (H_long - H_short)/2
    for ii in range(0, Nmajor-1):
        fid.write('\t<Short_vernier' + Name + str(ncell) +
                  ' {} {} '.format(ii*longspace + shortspace, ydec) +
                  '{} 1 '.format(Nminor) +
                  '{} 0 1 '.format(shortspace) +
                  'arrayRect>\n')

   

    
    # fprintf(fid,'\t<0 -5 205 -5 1 0 0 0 waveguide>\n');      %Bottom straight
    # fprintf(fid,'\t<210 0 310 0 1 90 0 0 waveguide>\n');    %Right straight
    # fprintf(fid,'\t<205 105 0 105 1 0 0 0 waveguide>\n');    %Top straight
    # fprintf(fid,'<-5 100 95 100 1 270 0 0 waveguide>\n');  %Left straight
    # fprintf(fid,['<0 -5 -5 0 1 0 90degreeBend>\n']); %Bottom left curve of blocking box
    # fprintf(fid,['<205 -5 210 0 1 0 90degreeBend>\n']); %Bottom right curve of blocking box
    # fprintf(fid,['<0 105 -5 100 1 0 90degreeBend>\n']); %Top left curve of blocking box
    # fprintf(fid,['<205 105 210 100 1 0 90degreeBend>\n']); %Top right curve of blocking box



    # -- Wrap up everything -- 
    # ------------------------------------------------------------
    fid.write('<VernierFull' + Name + '_' + str(ncell) +
              ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' {} {} 0 1 0 instance>\n'.format(x0-3*Ltot/2 +xdec,y0))
    fid.write('\n')

    fid.write('# ******************************\n')

    return ['VernierFull' + Name + '_' + str(ncell)]
