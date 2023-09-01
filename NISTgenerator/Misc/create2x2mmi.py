import numpy as np
from copy import copy

def Create2x2Mmi(fid, param, ncell):

    x_pos = param.get('x_pos', 0 )
    y_pos = param.get('y_pos', 0 )
    Wmmi = param.get('Wmmi', 0 )
    Dist = param.get('Dist', 0 )
    Wwg = param.get('Wwg', 0 )
    Lmmi = param.get('Lmmi', 0 )
    Wblock_MMI = param.get('Wblock_MMI', 8 )
    debug = param.get('debug', False)
    polarity = param.get('polarity', 0)
    LWg = param.get('LWg', 6) 
    layer = param.get('layer', 1)
    Name = param.get('name', '')
    Ltap = param.get('Ltap',1.25)
    α_wg = param.get('α_wg',np.pi/4)
    Geo = {}
    x0 = x_pos + Lmmi/2 + LWg
    y0 = y_pos
    Geo['TopIn'] = np.array([[-Lmmi/2 - LWg,  3*Dist/2 + Wwg],
                    [-Lmmi/2 - 3*LWg/4, Wmmi/2 + 2*Ltap*np.sin(α_wg)],
                    [-Lmmi/2 - LWg/4, Wmmi/2 + 2*Ltap*np.sin(α_wg)],
                    [-Lmmi/2 + Ltap*np.cos(α_wg), Dist/2 + Wwg + Dist/2],
                    [-Lmmi/2, Dist/2+ Wwg],
                    [-Lmmi/2 - LWg, Dist/2 + Wwg ]])

    Geo['CentIn'] = np.array([[-Lmmi/2 - LWg, Dist/2],
                      [-Lmmi/2, Dist/2],
                      [-Lmmi/2 + Ltap*np.cos(α_wg), 0],
                      [-Lmmi/2, -Dist/2],
                      [-Lmmi/2 - LWg, -Dist/2]])

    Geo['Bott']  = np.array([[-Lmmi/2 + 2*Ltap*np.cos(α_wg), -Wmmi/2 - 4*Ltap*np.sin(α_wg)],
                     [-Lmmi/2, -Wmmi/2 - 2*Ltap*np.sin(α_wg)],
                     [-Lmmi/2 + 2*Ltap*np.cos(α_wg), -Wmmi/2],
                     [Lmmi/2 - 2*Ltap*np.cos(α_wg), -Wmmi/2],
                     [Lmmi/2, -Wmmi/2 - 2*Ltap*np.sin(α_wg)],
                     [Lmmi/2 - 2*Ltap*np.cos(α_wg), -Wmmi/2 - 4*Ltap*np.sin(α_wg)]])

    Geo['BottIn'] = copy(Geo['TopIn'])
    Geo['BottIn'][:,1] = - Geo['BottIn'][:,1]

    Geo['Top'] = copy(Geo['Bott'])
    Geo['Top'][:,1]  = -Geo['Top'][:,1]

    Geo['TopOut'] = copy(Geo['TopIn'])
    Geo['TopOut'][:,0] = -Geo['TopOut'][:,0]

    Geo['CentOut'] = copy(Geo['CentIn'])
    Geo['CentOut'][:,0] = -Geo['CentOut'][:,0]

    Geo['BottOut'] = copy(Geo['TopOut'])
    Geo['BottOut'][:,1] = -Geo['BottOut'][:,1]


    Geo['TopIn'][:,0] = Geo['TopIn'][:,0] + x0
    Geo['CentIn'][:,0] = Geo['CentIn'][:,0] + x0
    Geo['Bott'][:,0] = Geo['Bott'][:,0] + x0
    Geo['BottIn'][:,0] = Geo['BottIn'][:,0] + x0
    Geo['Top'][:,0] = Geo['Top'][:,0] + x0
    Geo['TopOut'][:,0] = Geo['TopOut'][:,0] + x0
    Geo['CentOut'][:,0] = Geo['CentOut'][:,0] + x0
    Geo['BottOut'][:,0] = Geo['BottOut'][:,0] + x0

    Geo['TopIn'][:,1] = Geo['TopIn'][:,1] + y0
    Geo['CentIn'][:,1] = Geo['CentIn'][:,1] + y0
    Geo['Bott'][:,1] = Geo['Bott'][:,1] + y0
    Geo['BottIn'][:,1] = Geo['BottIn'][:,1] + y0
    Geo['Top'][:,1] = Geo['Top'][:,1] + y0
    Geo['TopOut'][:,1] = Geo['TopOut'][:,1] + y0
    Geo['CentOut'][:,1] = Geo['CentOut'][:,1] + y0
    Geo['BottOut'][:,1] = Geo['BottOut'][:,1] + y0

    if debug:
        f, ax = plt.subplots()
        for k, V in Geo.items():
            ax.plot(V[:,0], V[:,1])

        f.show()

    
    if polarity == 1:
        fid.write('111 layer\n');
        fid.write('<BOX_{}_{} struct>\n'.format(Name, int(ncell)));
        Bbox = np.array([[-Lmmi/2 - LWg, -(Wmmi/2 + Wblock_MMI/2)],
                [-Lmmi/2, -Wmmi/2 - Wblock_MMI],
                [Lmmi/2, -Wmmi/2 - Wblock_MMI],
                [Lmmi/2 + LWg, -(Wmmi/2 + Wblock_MMI/2)],
                [Lmmi/2 + LWg, (Wmmi/2 + Wblock_MMI/2)],
                [Lmmi/2, Wmmi/2 + Wblock_MMI],
                [-Lmmi/2, Wmmi/2 + Wblock_MMI],
                [-Lmmi/2 - LWg, (Wmmi/2 + Wblock_MMI/2)]])
        to_write = '';
        for jj in range(Bbox.shape[0]):
            to_write += '{:.3f} {:.3f}'.format((Bbox[jj,0]+x0),(Bbox[jj,0]+y0))
        
        to_write +='  points2shape\n'
        fid.write(to_write)
    if polarity == 1:
        fid.write('112 layer\n')
    else:
        fid.write('{} layer\n'.format(int(layer)))
    fid.write('<MmmiW{:.1f}L{:.1f}D{:.1f}Ox{}_{} struct>\n'.format(Wmmi, Lmmi, Dist, Name, int(ncell)));
    for k, V in Geo.items():
        to_write = '\t'
        for jj in range(V.shape[0]):
            to_write += '{:.3f} {:.3f} '.format(V[jj,0],V[jj,1])
        to_write +='points2shape\n'
        fid.write(to_write)
    if polarity == 1:
        pass
        # fid.write('<genArea1{}_{} MmmiW{:.3f}L{:.3f}D{:.3f}Ox{}_{} 112 genArea>\n'.format(Name, int(ncell),Name, int(ncell)))
        # fid.write('<genArea2{}_{} BOX{}_{} 111 genArea>\n'.format(Name, int(ncell),Name, int(ncell)))

        # fid.write('MMI2x2_SiN{}_{} struct>\n'.format(Name, int(ncell)))
        # fid.write('\tgenArea2{}_{} genArea1{}_{} {} subtract>\n'.format(Name, int(ncell),Name, int(ncell), int(layer)))
        # return ['MMI2x2_SiN{}_{} struct>\n'.format(Name, int(ncell))]
    else:
        return ['MmmiW{:.1f}L{:.1f}D{:.1f}Ox{}_{}'.format(Wmmi, Lmmi, Dist, Name, int(ncell))]

