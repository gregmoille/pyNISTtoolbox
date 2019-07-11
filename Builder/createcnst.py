import os

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

    fid.write('\n<{} struct>\n'.format(top_cell_name))
    for n in name_full:
        fid.write('<' + n + ' {:.3f} {:.3f} 0 1 0 instance>\n'.format(xdec, ydec))

    fid.close()
