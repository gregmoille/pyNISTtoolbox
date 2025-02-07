import subprocess as sub
import os
import sys
import platform
import shutil
import time
import gdspy
import warnings
import ipdb
warnings.filterwarnings("ignore")

def CreateGDS(cnst_name, CNSTpath="//Users/greg/GoogleDrive/Work/Techno/NIST/" +
               "CNSTnanoToolboxV2017.05.01/cnst_script_files/",
               ToolBoxPath="/Users/greg/GoogleDrive/Work/Techno/NIST/" +
              "CNSTnanoToolboxV2017.05.01/",
              javaVers = 'CNSTspecialScriptsV2019.05.01',
              GDSpath = '/Users/greg/gds_files_created/',
              ScriptDir='',
              dcty = None,
              dogds = True, 
              move = True, 
              removeRobCell = True):


    if not dcty:
        dcty = os.path.join(os.getcwd(),'')
    # print(dcty)
    ScriptName = os.path.join(os.path.join(CNSTpath ,ScriptDir,cnst_name))
    JarFile = os.path.join(ToolBoxPath, javaVers)
    gdsName = cnst_name.split('.')[0] + '.gds'
    if dogds:
        print('-'*60)
        print('Now creating gds file: '  + gdsName)
        print('-'*60)

        if platform.node() == 'horus' or  platform.node() == 'hephaistos.local':
            tocall = 'java -jar "' + JarFile + \
                                '" cnstscripting "' + \
                                ScriptName + '" "' +\
                                    gdsName + '"'

            return_code = sub.call(tocall,
                                shell=True,
                                cwd=ToolBoxPath)
        else: 
            tocall = 'xvfb-run -a java -jar "' + JarFile + \
                                '" cnstscripting "' + \
                                ScriptName + '" "' +\
                                    gdsName + '"'

            return_code = sub.call(tocall,
                                shell=True,
                                cwd=ToolBoxPath)


        if move: 
            try:
                time.sleep(2)
                try:
                    shutil.move(os.path.join(GDSpath, gdsName), os.path.join(dcty,'gds','') + gdsName)
                    shutil.move(ScriptName, os.path.join(dcty,'cnst','') + cnst_name)
                except:
                    time.sleep(2)
                    shutil.move(os.path.join(GDSpath, gdsName), os.path.join(dcty,'gds','') + gdsName)
                    shutil.move(ScriptName, os.path.join(dcty,'cnst','') + cnst_name)

                print('Moving .cnst file to: '  + os.path.join(dcty,'cnst','') + cnst_name)
                print('Moving .gds file to: ' + os.path.join(dcty,'gds','') + gdsName)
                print('-'*60)
            except:
                print("Error Moving File", file=sys.stderr)

        # if log[0].strip() == 'COMPLETED!':
        #     os.remove(log_file)
        #     print('log file ' + gdsName + '.log deleted')
            # ERROR = 'no error'



            if removeRobCell:
                # try:
                res = float(open(os.path.join(dcty,'cnst','') + cnst_name, 'r').readlines()[1].split('gds')[0])
                gdsLib = gdspy.GdsLibrary(unit=res, precision=res*1e-6)
                design = gdsLib.read_gds(os.path.join(dcty,'gds','') + gdsName)
                design.cells.pop('top')
                
                keys = design.cells.keys()
                for cell_name in keys:
                    if cell_name.lower().startswith('toremove'):
                        design.cells.pop(cell_name)

                print('just a test')
                design.write_gds(os.path.join(dcty,'gds','') + 'dum_' +  gdsName)
                time.sleep(2)
                # removing former gds
                os.remove(os.path.join(dcty,'gds','') + gdsName)

                
                try:
                    shutil.move(os.path.join(dcty,'gds','') + 'dum_' +  gdsName,
                            os.path.join(dcty,'gds','') + gdsName)
                except:
                    time.sleep(2)
                    shutil.move(os.path.join(dcty,'gds','') + 'dum_' +  gdsName,
                            os.path.join(dcty,'gds','') + gdsName)
                # except:
                #     print("Error Moving Dum File", file=sys.stderr)
    else: 
        shutil.move(ScriptName, os.path.join(dcty,'cnst','') + cnst_name)
        print('Moving .cnst file to: '  + os.path.join(dcty,'cnst','') + cnst_name)