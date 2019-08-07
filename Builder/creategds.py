import subprocess as sub
import os
import platform
import shutil
import gdspy
import warnings
warnings.filterwarnings("ignore")

def CreateGDS(cnst_name, CNSTpath="//Users/greg/GoogleDrive/Work/Techno/NIST/" +
               "CNSTnanoToolboxV2017.05.01/cnst_script_files/",
               ToolBoxPath="/Users/greg/GoogleDrive/Work/Techno/NIST/" +
              "CNSTnanoToolboxV2017.05.01/",
              javaVers = 'CNSTspecialScriptsV2019.05.01',
              ScriptDir='',
              removeRobCell = True):



    dcty = os.path.join(os.getcwd(),'')
    ScriptName = os.path.join(os.path.join(CNSTpath ,ScriptDir,cnst_name))
    JarFile = os.path.join(ToolBoxPath, javaVers)
    gdsName = cnst_name.split('.')[0] + '.gds'
    print('-'*60)
    print('Now creating gds file: '  + gdsName)
    print('-'*60)
    DirGds = os.path.join(os.path.join(ToolBoxPath,'generated_gds_masks'), '')

    # os.system('java -jar ' +
    #          CNSTpath + CNSTtoolbox +
    #          ' cnstscripting' +
    #          ' ' + ScriptName +
    #          ' ./'  +gdsName)


    tocall = 'java -jar ' + JarFile + \
                           ' cnstscripting ' + \
                           ScriptName + ' ' +\
                            gdsName


    return_code = sub.call(tocall,
                           shell=True,
                           cwd=ToolBoxPath)



    # read the log file
    # log_file = os.path.join(DirGds, gdsName) + '.log'
    # log = open(log_file).readlines()
    # if log[0] == 'COMPLETED!'
    # print('-'*60)
    # print(log[0].strip())



    shutil.move(DirGds + gdsName, os.path.join(dcty,'gds','') + gdsName)
    shutil.move(ScriptName, os.path.join(dcty,'cnst','') + cnst_name)
    print('Moving .cnst file to: '  + os.path.join(dcty,'cnst','') + cnst_name)
    print('Moving .gds file to: ' + os.path.join(dcty,'gds','') + gdsName)
    print('-'*60)

    # if log[0].strip() == 'COMPLETED!':
    #     os.remove(log_file)
    #     print('log file ' + gdsName + '.log deleted')
        # ERROR = 'no error'


        # dumping the top cell
    if removeRobCell:
        res = float(open(os.path.join(dcty,'cnst','') + cnst_name, 'r').readlines()[1].split('gds')[0])
        gdsLib = gdspy.GdsLibrary(unit=res, precision=res*1e-6)
        design = gdsLib.read_gds(os.path.join(dcty,'gds','') + gdsName)
        design.cell_dict.pop('top')
        design.write_gds(os.path.join(dcty,'gds','') + 'dum_' +  gdsName)

        # removing former gds
        os.remove(os.path.join(dcty,'gds','') + gdsName)

        # replacing it by the new one without top cell
        shutil.move(os.path.join(dcty,'gds','') + 'dum_' +  gdsName,
                    os.path.join(dcty,'gds','') + gdsName)

    # else:
    #     print('ERROR Generating .gds')
    #     print('Please double check the log file ' +
    #           gdsName + '.log for further details')
    #     ERROR = 'ERROR Generating .gds - double check the .log'

    # if platform.system().lower() == 'darwin':
    #     title = 'CNST NanoToolBox'
    #     subtitle = 'Completed {} GDS'.format(cnst_name.split('.gds')[0])
    #     # message = ERROR
    #     # The notifier function
    #     t = '-title {!r}'.format(title)
    #     s = '-subtitle {!r}'.format(subtitle)
    #     # m = '-message {!r}'.format(message)
    #     os.system("terminal-notifier -group 'CNST Tool Box' {} -sound default -appIcon {}/CNST.jpg".format(' '.join([t, s]),CNSTpath))
