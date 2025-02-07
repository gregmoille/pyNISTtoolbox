import os
from itertools import compress
import numpy as np
import ipdb
import re
def CreateCNST(cell_type, param, cnstname,
               yshift = None,
               CNSTpath="//Users/greg/GoogleDrive/Work/Techno/NIST/" +
               "CNSTnanoToolboxV2017.05.01/cnst_script_files/",
               top_cell_name = 'TOP',
               xdec = 0,
               ydec = 0,
               res = 0.001,
               removelayers = None,
               return_cnst = True):


    # retrieve what was the name we import the NISTgenerator module
    name_to_import = cell_type[0].split('.')[0]
    # import the NISTgenerator as in the main file
    exec(name_to_import + ' = __import__("NISTgenerator")')

    print(os.path.join(CNSTpath,cnstname))
    with open(os.path.join(CNSTpath,cnstname), 'w') as fid: 
        ncell = len(cell_type)
        #  -- Create Header --
        # -------------------------------------------------------
        # fid.write('logFileTimeDate\n')
        fid.write('# ******************************\n')
        fid.write('{} gdsReso\n'.format(res))
        fid.write('{} shapeReso\n'.format(res))

        name_full = []
        for ii in range(0, ncell):
            fun = eval(cell_type[ii])
            name_full += fun(fid, param[ii], ii)


        name_full = np.array(name_full)

        if not yshift:
            yshift = np.zeros(name_full.size)
        yshift = np.array(yshift)
        cell_list = []
        ysh_list = []
        while not name_full.size == 0:
        # ipdb.set_trace()

            pattern = re.compile(f"{name_full[0].split('_')[0]}.*")
            test = list(filter(pattern.match, name_full))

            # [xx.startswith(name_full[0].split('_')[0]) for xx in name_full]
            ind = [list(name_full).index(tt) for tt in test]
            cell_list += [name_full[ind]]
            ysh_list += [yshift[ind]]
            name_full = np.delete(name_full, ind)
            yshift = np.delete(yshift, ind)


        for cell, ysh in zip(cell_list, ysh_list):
            if len(cell)>1:
                fid.write('\n<{} struct>\n'.format(cell[0].split('_')[0]))
                for n, y in zip(cell, ysh):
                    fid.write('\t<{} 0 0 0 1 0 instance>\n'.format(n, y))
            else:
                fid.write('\n<{} struct>\n'.format(cell[0].split('_')[0]))
                fid.write('\t<{} 0 0 0 1 0 instance>\n'.format(cell[0], ysh[0]))


        if not top_cell_name == None:
            fid.write('\n<{} struct>\n'.format(top_cell_name))
            for cell, y  in zip(cell_list, ysh_list):
                if len(cell)>1:
                    fid.write('\t<{} {:.3f} {:.3f}  0 1 0 instance>\n'.format(cell[0].split('_')[0], xdec, ydec + y[0]))
                else:
                    fid.write('\t<{} {:.3f} {:.3f}  0 1 0 instance>\n'.format(cell[0].split('_')[0], xdec, ydec + y[0]))

    if return_cnst:
        with open(os.path.join(CNSTpath,cnstname), 'r') as fid:
            lines = fid.read()
            return lines
    return None
