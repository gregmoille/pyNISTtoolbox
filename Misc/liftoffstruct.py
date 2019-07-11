def CreateLiftOff(fid, param, ncell):
    xout = param.get('xout', 0)
    xin= param.get('xin', 0)
    yout = param.get('yout', 0)
    yin = param.get('yin', 0)
    Name = param.get('Name', 'Bbox')
    layer = param.get('layer', 66)
    print('Creating LiftOff Structure: ')
    print('On the layer {}'.format(layer))

    fid.write(str(111) + ' layer\n')
    fid.write('<' + Name + '_Outer' + str(ncell) + ' struct>\n')
    

    # Create outer struct 
    polyout = '\t'
    for out in range(len(xout)):
        polyout += '{:.3f} {:.3f} '.format(xout[out], yout[out])
    polyout += 'points2shape\n'
    fid.write(polyout)

    fid.write(str(110) + ' layer\n')
    fid.write('<' + Name + '_Inner' + str(ncell) + ' struct>\n')
    polyin = '\t'
    for ii in range(len(xin)):
        polyin += '{:.3f} {:.3f} '.format(xin[ii], yin[ii])

    polyin += 'points2shape\n'
    fid.write(polyin)


    fid.write('<genArea1{}_{} '.format(Name, int(ncell)) + Name + '_Inner' + str(ncell) + ' 110 genArea>\n')
    fid.write('<genArea2{}_{} '.format(Name, int(ncell)) + Name + '_Outer' + str(ncell) + ' 111 genArea>\n')


    fid.write('<{}_{} struct>\n'.format(Name, int(ncell)))
    fid.write('\t<genArea2{}_{} genArea1{}_{} {} subtract>\n'.format(Name, int(ncell),Name, int(ncell), int(layer)))
    # return ['MMI2x2_SiN{}_{} struct>\n'.format(Name, int(ncell))]

    # fid.write('{:.0f} {:.0f} '.format(x0, y0) +
    #           '{:.0f} {:.0f} '.format(x1, y0) +
    #           '{:.0f} {:.0f} '.format(x1, y1) +
    #           '{:.0f} {:.0f} '.format(x0, y1) +
    #           'points2shape\n')

    fid.write('\n')
    return ['{}_{}'.format(Name, int(ncell))]

