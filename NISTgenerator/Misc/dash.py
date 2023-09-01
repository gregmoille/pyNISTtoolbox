import numpy as np

def Dash(fid, param, ncell):
    y0 = param.get('y0', 0)
    y_shift = param.get('y_shift',10)
    N = param.get('N', 0)
    x0 = param.get('x0', 0)
    W = param.get('W', 10)
    L = param.get('L', 1)
    Name = param.get('Name', '')
    layer = param.get('layer', 1)
    Wend = param.get('Wend', 1)
    Ltap = param.get('Ltap', 1)
    Lt = param.get('Ltip', 1)
    name_out = []

    def Bez(Px,Py,N): 
        t = np.linspace(0,1,N)
        x = (1-t)**3 * Px[0] + 3*(1-t)**2*t*Px[1] + 3*(1-t)*t**2*Px[2] + t**3*Px[3]
        y = (1-t)**3 * Py[0] + 3*(1-t)**2*t*Py[1] + 3*(1-t)*t**2*Py[2] + t**3*Py[3]

        return list(x),list(y)

    for ii in range(N):
        # y = ii*y_shift + y0
        fid.write(str(layer) + ' layer\n')
        name_cell = Name + 'dash' + 'C' + str(ncell)+  '_' + str(ii)
        name_out.append(name_cell)
        fid.write('<' + name_cell + ' struct>\n')

        α = np.pi/2 - np.arctan((W-Wend)/(2*Ltap) )
        
        # Do tip of the dash
        Pxup = Lt*  np.cos(α)
        Pyup = Lt*  np.sin(α)
        Px = [-Wend/2, -Wend/2 + Pxup ,Wend/2 - Pxup,Wend/2]
        Py = [L/2+Ltap,  L/2+Ltap+Pyup, L/2+Ltap+Pyup, L/2+Ltap]
        xtip, ytip = Bez(Px,Py,30)

        # # Do the angle of the dash
        Px = [-W/2, -W/2, -W/2 , -Wend/2]
        Py = [L/3, L/2, L/2, L/2+Ltap]
        xangle_lu,yangle_lu = Bez(Px,Py,30)

        # Do tip of the dash
        Pxup = Lt*  np.cos(α)
        Pyup = Lt*  np.sin(α)
        Px = [-Wend/2, -Wend/2 + Pxup ,Wend/2 - Pxup,Wend/2]
        Py = [L/2+Ltap,  L/2+Ltap+Pyup, L/2+Ltap+Pyup, L/2+Ltap]
        xtip_t, ytip_t = Bez(Px,Py,30)

        # # Do the angle of the dash
        Px = [Wend/2, W/2, W/2, W/2]
        Py = [L/2+Ltap, L/2, L/2,L/3]
        xangle_ru,yangle_ru = Bez(Px,Py,30)

        # # Do the angle of the dash
        Px = [W/2, W/2, W/2, Wend/2]
        Py = [-L/3, -L/2, -L/2, - L/2-Ltap]
        xangle_rb,yangle_rb = Bez(Px,Py,30)

        # Do tip of the dash
        Pxup = Lt*  np.cos(α)
        Pyup = Lt*  np.sin(α)
        Px = [Wend/2, Wend/2 - Pxup , - Wend/2 + Pxup,-Wend/2]
        Py = [-L/2-Ltap,  -L/2-Ltap-Pyup, -L/2-Ltap-Pyup, -L/2-Ltap]
        xtip_b,ytip_b = Bez(Px,Py,30)


        # # Do the angle of the dash
        Px = [-Wend/2, -W/2, -W/2, -W/2]
        Py = [- L/2-Ltap, -L/2, -L/2, -L/3]
        xangle_lb,yangle_lb = Bez(Px,Py,30)

        xdash = []
        ydash = []
        xdash += xangle_lu
        ydash += yangle_lu
        xdash += xtip_t
        ydash += ytip_t
        xdash += xangle_ru
        ydash += yangle_ru
        xdash += xangle_rb
        ydash += yangle_rb
        xdash += xtip_b
        ydash += ytip_b
        xdash += xangle_lb
        ydash += yangle_lb

        xdash = np.array(xdash)
        ydash = np.array(ydash)

        xdash = xdash + x0
        ydash = ydash + ii*y_shift + y0
        fid.write('\t')
        for xx, yy in zip(xdash,ydash):
            fid.write('{:.3f} {} '.format(xx, yy))
        fid.write('points2shape\n')

    fid.write('\n')
    fid.write('<' + Name + 'Dash' + str(ncell) + ' struct>\n')
    for n in name_out:
        fid.write('\t<' + n + ' 0 0 0 1 0 instance>\n')
    return [Name + 'Dash' + str(ncell)]