import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy import constants as cts
import scipy.integrate as itg
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from copy import copy
p = 0.3510190379346744





def GetBend(p, **kwargs):
    R0 = kwargs.get('R0', 10)
    α = kwargs.get('alpha', np.pi)
    Npts = kwargs.get('Npts', 100)

    sp =R0*np.sqrt(p*α)
    s = np.linspace(0, sp, Npts)

    # -- Create the Euler part --
    # ------------------------------------------------------------
    x = np.zeros(s.size)
    y = np.zeros(s.size)
    for ss, iis in zip(s, range(s.size)):
        x[iis],_ = itg.quad(lambda xx: np.cos(xx**2/(2*R0**2)), 0, ss)
        y[iis],_ = itg.quad(lambda xx: np.sin(xx**2/(2*R0**2)), 0, ss)

    # -- Expand the circle part --
    # ------------------------------------------------------------



    xp = x[-1]
    yp = y[-1]

    Rp = R0/np.sqrt(p*α)
    s0 = 2*sp +Rp*α*(1-p)
    Δx = xp - Rp*np.sin(p*α/2)
    Δy = yp - Rp*(1-np.cos(p*α/2))


    sc = np.linspace(sp, s0/2, Npts)

    xc = Rp*np.sin( (sc- sp)/Rp + p*α/2) + Δx
    yc = Rp*(1-np.cos( (sc- sp)/Rp + p*α/2))+ Δy

    # xc_ful = Rp*np.sin(np.linspace(-np.pi, np.pi, Npts)) + Δx
    # yc_ful = Rp*(1-np.cos(np.linspace(-np.pi, np.pi, Npts))) + Δy


    x1 = np.concatenate([x, xc])
    y1 = np.concatenate([y, yc])


    # -- axi symmetry to finish the bend --
    # ------------------------------------------------------------

    # pivot around hte end point of the curve
    xpvt, ypvt  = x1[-1], y1[-1]

    # translate to 0 0 the end of the curve
    xshift = x1- xpvt
    yshift = y1 - ypvt

    # rotat by π/2 - α
    rotα = (np.pi/2- α/2)
    xrot = xshift*np.cos(rotα) - yshift*np.sin(rotα)
    yrot = xshift*np.sin(rotα) + yshift*np.cos(rotα)
    # apply the mirro
    xmir = xrot
    ymir = -yrot
    #
    # # unrotate
    x2 = xmir*np.cos(-rotα) - ymir*np.sin(-rotα)
    y2 = xmir*np.sin(-rotα) + ymir*np.cos(-rotα)

    # reshift to the position
    x2 = x2 + xpvt
    y2 = y2 + ypvt

    xtot = np.concatenate([x1, x2[::-1]])
    ytot = np.concatenate([y1, y2[::-1]])


    return xtot, ytot #, xc_ful, yc_ful


def GenerateRaceTrack(fid, param, ncell, cnt_out):

    circle_coupling = param.get('circle_coupling', False)
    resist = param.get('resist', 'positive')
    Name = param.get('name')
    R0 = param.get('RR')
    Ltot = param.get('Lrace')
    y0 = param.get('y0')
    x0 = param.get('x0')

    left_coupling = param.get('left_coupling', False)
    



    # print(x0)
    layer = param.get('layer')
    layer_mixmatch = param.get('layer_mixmatch', None)

    W = param.get('RW')
    sleeve = param.get('exp_w')
    G = param.get('G')
    Wwg = param.get('W')
    Lcpl = param.get('Lc')
    Ljoin = param.get('Ljoin')

    Ls = 25
    Hs = param.get('Hs', 7)

    α = np.pi
    sp = R0*np.sqrt(p*α)
    Rp = R0 /np.sqrt(p*α)
    Sc = Rp*α*(1-p)
    Seuler = 2*sp
    Stot = Seuler + Sc

    Lstraight = Ltot/2 - Stot


    xbs = Lstraight/2
    ybs =  R0
    xtot = np.array([-Lstraight/2, Lstraight/2])
    ytot = np.array([R0, R0])
    xbend, ybend  = GetBend(p, R0=R0, alpha = α, Npts = 50)


    xtot = np.concatenate([xtot, xbs + xbend[::-1] ])
    ytot = np.concatenate([ytot, - ybs + ybend[::-1] ])

    xtot = np.concatenate([xtot, [-Lstraight/2]])
    ytot = np.concatenate([ytot, [-R0]])

    xtot = np.concatenate([xtot, -xbs - xbend])
    ytot = np.concatenate([ytot, - ybs + ybend ] )

    Wtot = np.max(xtot) - np.min(xtot)
    if not circle_coupling:
        yshift = -y0 + (R0 + Wwg/2 + W/2 + G + Hs)
    if left_coupling: 
        yshift = -y0 - R0 - Wwg/2 
    else:
        yshift = -y0 + Wtot/2 +W/2 + Wwg/2 + G

    print(yshift)

    # with open('racetrack_test.cnst', 'w') as fid:
    

    if resist == 'positive':
        wg_struct = f'{Name}Wg{ncell}_{cnt_out}'
        sleev_struct = f'{Name}Slv{ncell}_{cnt_out}'

        fid.write(f'{layer} layer\n')
        fid.write(f'<{wg_struct} struct>\n')
        for x, y in zip(xtot + x0, ytot-yshift):
            fid.write(f'{x:.3f} {y:.3f} ')
        fid.write(f'{W}  0 1 polypath\n')

        fid.write(f'{layer} layer\n')
        xsleeve =  xtot[::10]
        ysleeve = ytot[::10]


        if left_coupling:
            Lr = np.max(xtot) - np.min(xtot)
            x1cpl = np.min(xtot) - W/2  - G - Wwg/2
            y1cpl = -yshift - 2
            x0cpl = np.min(xtot) - W/2  - G - W/2 - 20
            Lstart_left = Ljoin + x0cpl
            y0cpl = 0 
            fid.write(f'\t<{x0cpl-Lstart_left} {y0cpl} {x0cpl} {y0cpl} {Wwg} 0 0 0 waveguide>\n')
            fid.write(f'\t<{x0cpl} {y0cpl} {x1cpl} {y1cpl} {Wwg} 0 90degreeBend>\n')
            fid.write(f'\t<{x1cpl} {y1cpl} {x1cpl} {y1cpl+12} {Wwg} 0 0 0 waveguide>\n')
            x0cpl = np.min(xtot) - W/2  - G - Wwg/2
            y0cpl = - yshift + 10
            x1cpl = np.min(xtot) - W/2  - G - W/2 + 25
            y1cpl = - 2 * yshift + 7
            fid.write(f'\t<{x1cpl} {y1cpl} {2*x1cpl-x0cpl} {2*y1cpl-y0cpl} {Wwg} 180 90degreeBend>\n')
            print(Lr)
            fid.write(f'\t<{x1cpl} {y1cpl} {x1cpl + Lr - 40} {y1cpl} {Wwg} 0 0 0 waveguide>\n')
            xSendrtck = x1cpl + Lr - 40
            fid.write(f'\t<{xSendrtck} {y1cpl} {100} {-y1cpl} {Wwg} 0 sBendLH>\n')

            Lstart_right = Ljoin - (xSendrtck+100)
            fid.write(f'\t<{xSendrtck+100} {0} {xSendrtck+100 + Lstart_right} {0} {Wwg} 0 0 0 waveguide>\n')




        # ================= SLEEVE  =========
        fid.write(f'<{sleev_struct} struct>\n')
        fid.write('3 layer\n')
        if not xsleeve[-1] == xtot[-1]:
            xsleeve = np.concatenate((xsleeve, [xtot[-1]]))
            ysleeve = np.concatenate((ysleeve, [ytot[-1]]))
        for x, y in zip(xsleeve + x0, ysleeve-yshift):
            fid.write(f'{x:.5f} {y:.5f} ')
        fid.write(f'{W+2*sleeve} 0 1 polypath\n')

        

        if not left_coupling:
            y1 = R0+ W/2 + G + Wwg/2 - yshift
            x1 = Lcpl/2
            fid.write(f'\t<{x1} {y1} {Ls} {Hs} {Wwg} 0 sBendLH>\n')


            y1 = R0+ W/2 + G + Wwg/2 - yshift

            x1 = -Lcpl/2
            fid.write(f'\t<{x1} {y1} {-Ls} {Hs} {Wwg} 0 sBendLH>\n')
            fid.write(f'\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg} 0 0 0 waveguide>\n')

    


            y1 = R0+ W/2 + G + Wwg/2 - yshift
            x1 = Lcpl/2

            fid.write(f'\t<{x1} {y1} {Ls} {Hs} {Wwg+2*sleeve} 0 sBendLH>\n')

            y1 = R0+ W/2 + G + Wwg/2 - yshift
            x1 = -Lcpl/2
            fid.write(f'\t<{x1} {y1} {-Ls} {Hs} {Wwg+2*sleeve} 0 sBendLH>\n')
            fid.write(f'\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg+2*sleeve} 0 0 0 waveguide>\n')

            # ====== Stepper saving space
            stepperArea = f'{Name}RtrckStep{ncell}_{cnt_out}'
            fid.write(f'<{stepperArea} struct>\n')
            fid.write(f'\t{layer_mixmatch} layer\n')

            # Inner of the racetrack
            for x, y in zip(xsleeve, ysleeve-yshift):
                fid.write(f'{x:.5f} {y:.5f} ')
            fid.write(f' points2shape\n')

            # Sleeve
            
            for x, y in zip(xsleeve, ysleeve-yshift):
                fid.write(f'{x:.5f} {y:.5f} ')
            fid.write(f'{W+2*sleeve-1} 0 1 polypath\n')

            # Coupling region
            y1 = R0+ W/2 + G + Wwg/2 - yshift
            x1 = Lcpl/2
            fid.write(f'\t<{x1} {y1} {Ls} {Hs} {Wwg+2*sleeve-1} 0 sBendLH>\n')

            y1 = R0+ W/2 + G + Wwg/2 - yshift
            x1 = -Lcpl/2
            fid.write(f'\t<{x1} {y1} {-Ls} {Hs} {Wwg+2*sleeve-1} 0 sBendLH>\n')
            fid.write(f'\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg+2*sleeve-1} 0 0 0 waveguide>\n')

            # Connection waveguide
            Lstart = Ljoin - Lcpl/2 - Ls
            wsleeve_stepper = Wwg+2*sleeve - 1
            fid.write(f'\t<{-Ljoin+ wsleeve_stepper/2} {y0} {-Ljoin + Lstart} {y0} {wsleeve_stepper} 0 1 0 waveguide>\n')
            fid.write(f'\t<{Ljoin - Lstart} {y0} {Ljoin-wsleeve_stepper/2} {y0} {wsleeve_stepper} 0 0 1 waveguide>\n')


            Lstart = Ljoin - Lcpl/2 - Ls
            ystart = y0
            fid.write(f'\t<{-Ljoin} {ystart} {-Ljoin + Lstart} {ystart} {Wwg+2*sleeve} {Wwg} 0 1 0 waveguideSlot>\n')
            fid.write(f'\t<{Ljoin - Lstart} {ystart} {Ljoin} {ystart} {Wwg+2*sleeve} {Wwg} 0 0 1 waveguideSlot>\n')

        else: 
            # Coupling region
                # ================= SLEEVE  =========
            Lr = np.max(xtot) - np.min(xtot)
            x1 = np.min(xtot) - W/2  - G - Wwg/2
            y1 = -yshift - 2
            x0 = np.min(xtot) - W/2  - G - W/2 - 20
            Lstart_left = Ljoin + x0
            y0 = 0 
            fid.write(f'\t<{x0-Lstart_left} {y0} {x0} {y0} {Wwg+2*sleeve} 0 0 0 waveguide>\n')
            fid.write(f'\t<{x0} {y0} {x1} {y1} {Wwg+2*sleeve} 0 90degreeBend>\n')
            fid.write(f'\t<{x1} {y1} {x1} {y1+12} {Wwg+2*sleeve} 0 0 0 waveguide>\n')
            x0 = np.min(xtot) - W/2  - G - Wwg/2
            y0 = - yshift + 10
            x1 = np.min(xtot) - W/2  - G - W/2 + 25
            y1 = - 2 * yshift + 7
            fid.write(f'\t<{x1} {y1} {2*x1-x0} {2*y1-y0} {Wwg+2*sleeve} 180 90degreeBend>\n')
            print(Lr)
            fid.write(f'\t<{x1} {y1} {x1 + Lr - 40} {y1} {Wwg+2*sleeve} 0 0 0 waveguide>\n')
            xSendrtck = x1 + Lr - 40
            fid.write(f'\t<{xSendrtck} {y1} {100} {-y1} {Wwg+2*sleeve} 0 sBendLH>\n')

            Lstart_right = Ljoin - (xSendrtck+100)
            fid.write(f'\t<{xSendrtck+100} {0} {xSendrtck+100 + Lstart_right} {0} {Wwg+2*sleeve} 0 0 0 waveguide>\n')

        # ================= BOOLEAN OPERATION
        wg_area = f'{Name}RtrkWg{ncell}_{cnt_out}'
        sleeve_area = f'{Name}RtrkSlv{ncell}_{cnt_out}'
        fid.write(f'<{wg_area} {wg_struct} 1 genArea>\n')
        fid.write(f'<{sleeve_area} {sleev_struct} 3 genArea>\n')
        # fid.write(f'{layer_mixmatch} layer\n')

        # ====== FINAL STRUCTURE =====
        struct_name = f'{Name}Rtrck{ncell}_{cnt_out}'
        fid.write(f'<{struct_name} struct>\n')
        # fid.write(f'\t<{stepperArea} 0 0 0 1 0 instance>\n')
        fid.write(f'\t{layer} layer\n')
        fid.write(f'\t<{wg_area} {sleeve_area} {layer} XOR>\n')



    if resist == 'negative':
        struct_name = f'{Name}Rtrck{ncell}_{cnt_out}'
        fid.write(f'<{struct_name} struct>\n')
        fid.write(f'{layer} layer\n')

        
        if circle_coupling:
            # x0 = x0 - Wtot
            xdum = copy(xtot)
            xtot = copy(ytot)
            ytot = xdum

        for x, y in zip(xtot + x0, ytot-yshift):
            fid.write(f'{x:.3f} {y:.3f} ')
        fid.write(f'{W} 1 1 polypath\n')

        # for x, y in zip(xtot + x0, ytot-yshift):
        #     fid.write(f'{x:.3f} {y:.3f} ')
        # fid.write(f' points2shape\n')
        if not left_coupling:
            y1 = R0+ W/2 + G + Wwg/2 - yshift
            x1 = Lcpl/2 + x0
            if not circle_coupling:
                fid.write(f'\t<{x1} {y1} {Ls} {Hs} {Wwg} 0 sBendLH>\n')


            y1 = R0+ W/2 + G + Wwg/2 - yshift

            x1 = -Lcpl/2  + x0
            if not circle_coupling:
                fid.write(f'\t<{x1} {y1} {-Ls} {Hs} {Wwg} 0 sBendLH>\n')
                fid.write(f'\t<{x1} {y1} {x1+Lcpl} {y1} {Wwg} 0 0 0 waveguide>\n')


            if circle_coupling:
                ystart = y0
                Ljoin = R0/2
                fid.write(f'\t<{-Ljoin+x0} {ystart} {25+x0} {ystart} {Wwg} 0 0 0 waveguide>\n')
    

        # Lstart = Ljoin - Lcpl/2 - Ls
        # ystart = y0
        # fid.write(f'\t<{-Ljoin+x0} {ystart} {-Ljoin + Lstart+x0} {ystart} {Wwg} 0 0 0 waveguide>\n')
        # fid.write(f'\t<{Ljoin - Lstart +x0} {ystart} {Ljoin + x0} {ystart} {Wwg} 0 0 0 waveguide>\n')


    if left_coupling: 
        return [struct_name]
    else:
        return [struct_name]
