import os
from itertools import compress
import numpy as np
import ipdb

def CreateCNST(cell_type, param, cnstname,
               CNSTpath="//Users/greg/GoogleDrive/Work/Techno/NIST/" +
               "CNSTnanoToolboxV2017.05.01/cnst_script_files/",
               top_cell_name = 'TOP',
               xdec = 0,
               ydec = 0,
               res = 0.001):


    # retrieve what was the name we import the NISTgenerator module
    name_to_import = cell_type[0].split('.')[0]
    # import the NISTgenerator as in the main file
    exec(name_to_import + ' = __import__("NISTgenerator")')


    fid = open(os.path.join(CNSTpath,cnstname), 'w')
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
    cell_list = []
    # ipdb.set_trace()
    while not name_full.size == 0:
      test = [xx.startswith(name_full[0].split('_')[0])for xx in name_full]
      ind = np.argwhere(test).flatten()
      cell_list += [name_full[ind]]
      name_full = np.delete(name_full, ind)

    # ipdb.set_trace()

    for cell in cell_list:
        if len(cell)>1:
            fid.write('\n<{} struct>\n'.format(cell[0].split('_')[0]))
            for n in cell:
                fid.write('\t<{} 0 0 0 1 0 instance>\n'.format(n))



    if not top_cell_name == None:
        fid.write('\n<{} struct>\n'.format(top_cell_name))
        for cell in cell_list:
            if len(cell)>1:
                fid.write('\t<{} {:.3f} {:.3f}  0 1 0 instance>\n'.format(cell[0].split('_')[0], xdec, ydec))
            else:
                fid.write('\t<{} {:.3f} {:.3f}  0 1 0 instance>\n'.format(cell[0], xdec, ydec))
    fid.close()
