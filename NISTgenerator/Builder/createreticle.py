import subprocess as sub
import os
import sys
import shutil
import time
import matplotlib.pyplot as plt
import gdspy
import numpy as np
import ipdb
from copy import copy
import re
import warnings
import ipdb
import textwrap
from .creategds import CreateGDS

warnings.filterwarnings("ignore")

def WriteDesigns(fid, params, Nrow, Ncol, xshift0, yshift0, Folder, Files):
    W = params.get('W')
    H = params.get('H')
    street = params.get('street', 150)
    Hchip = params.get('Hchip')
    Wchip = params.get('Wchip')


    DsgnCnt = 0
    Dsgn_name = []
    x0 = []
    y0 = []
    cnt = 0
    for iN in range(Nrow):
        for iC in range(Ncol):
            if DsgnCnt >= len(Files):
                break
            # shift of the design on the reticle
            x0 += [+ iC*(Wchip+street) + xshift0 - W/2 -10 ]
            y0 += [- H/2 + iN*(Hchip+street) + yshift0]
            Dsgn_name += [f'Design{DsgnCnt+1}']

            # get the individual design
            reFile = os.path.join(Folder, Files[DsgnCnt])

            to_append = f'<{reFile} fileName>\n'
            to_append += f'<{Dsgn_name[-1]} struct>\n'
            to_append += f'\t<D{DsgnCnt+1}TOP 0 0 0 1 0 instance>\n\n'

            fid.write(to_append)
    
            DsgnCnt += 1
        
        if DsgnCnt >= len(Files):
                break

    return Dsgn_name, x0, y0

def AMSmark(fid):
    center_top ='-5.00000 -50.00000 ' +\
                '-5.00000 0.50000 ' +\
                '-2.50000 0.50000 ' +\
                '-2.50000 -0.50000 ' +\
                '-0.50000 -0.50000 ' +\
                '-0.50000 -2.50000 ' +\
                '0.50000 -2.50000 ' +\
                '0.50000 -0.50000 ' +\
                '2.50000 -0.50000 ' +\
                '2.50000 0.50000 ' +\
                '0.50000 0.50000 ' +\
                '0.50000 2.50000 ' +\
                '-0.50000 2.50000 ' +\
                '-0.50000 0.50000 ' +\
                '-5.00000 0.50000 ' +\
                '-5.00000 50.00000 ' +\
                '5.00000 50.00000 ' +\
                '5.00000 -50.00000 ' + \
                '-5.00000 -50.00000 '




    AMS = reticle = f'''
    <AMSmark struct>
        2 layer
        {center_top} 0 0 0 points2shape
        <5 0 50 0 10 0 0 0 waveguide>
        <-5 0 -50 0 10 0 0 0 waveguide>
    '''


    for ii in range(11):
        AMS += f'<-209 {-28.6-ii*17.6} -18 {-28.6-ii*17.6} 8.8 0 0 0 waveguide>\n'
        AMS += f'<{-28.6-ii*17.6} 14 {-28.6-ii*17.6} 204 8.8 0 0 0 waveguide>\n'

    for ii in range(12):
        AMS += f'<204 {+24+ii*16} 14 {+24+ii*16} 8 0 0 0 waveguide>\n'
        AMS += f'<{+24+ii*16} -18 {+24+ii*16} -209 8 0 0 0 waveguide>\n'


    AMS += '5 layer\n<-250 0 250 0 500 0 0 0 waveguide>\n'
    fid.write(textwrap.dedent(AMS))


def CreateReticle(cnst_name, reticle_params,
                 CNSTpath="//Users/greg/GoogleDrive/Work/Techno/NIST/" +
                         "CNSTnanoToolboxV2017.05.01/cnst_script_files/",
                 javaVers = 'CNSTspecialScriptsV2019.05.01',
                 GDSpath = '/Users/greg/gds_files_created/',
                 dcty = None,
                 doCross = False,
                 doAMSmark = False,
                 doPhotronics = False,
                 doReadableReticle = True,
                 Ncol = None,
                 Nrow = None, 
                 layer_bool = 2):

    W = reticle_params.get('W', None)
    H = reticle_params.get('H', None)
    street = reticle_params.get('street', 150)
    Hchip = reticle_params.get('Hchip', None)
    Wchip = reticle_params.get('Wchip', None)
    cnstFileFolder = reticle_params.get('cnstFileFolder', None)
    cnstFiles = reticle_params.get('cnstFiles', None)
    MLA_corner_marks = reticle_params.get('MLA_corner_marks', False)

    with open(os.path.join(CNSTpath,'../CNSTdefaultValues.xml'), 'r') as cnstdef:
        lines = ''.join(cnstdef.readlines())
        cnstdefPath = re.findall('  <OpenDirectory>(.*)</OpenDirectory>', lines)[0]
        cnstdefPath = cnstdefPath.replace(' System.getProperty("user.home") + ', os.path.expanduser('~')) 
    relCnstFileFolder = os.path.relpath(cnstFileFolder, cnstdefPath)
    # relCnstFileFolder = './cnst_script_files/'

    if not Ncol: 
        Ncol = int(W/(Wchip+street))
    if not Nrow: 
        Nrow = int(H/(Hchip+street))

    xshift0 = (W - ((Wchip+street)*Ncol - street))/2
    yshift0 = (H - ((Hchip+street)*Nrow - street))/2




    # assert Ncol*Nrow == len(cnstFiles)

    # -- Create the reticle cnst that is readble --
    # ---------------------------------------------------
    if doReadableReticle:
        idRet = open(os.path.join(CNSTpath, cnst_name), 'w')
        header = '''
        # ******************************
        0.001 gdsReso
        0.001 shapeReso
        # ******************************
        '''
        idRet.write(textwrap.dedent(header))

        Dsgn_name, x0, y0 = WriteDesigns(idRet, reticle_params,
                                        Nrow, Ncol,
                                        xshift0, yshift0,
                                        relCnstFileFolder,
                                        cnstFiles)

        # create the reticle bonding box
        reticle = f'''
        <ReticleBonding struct>
            100 layer
            2 datatype
        	{0} {0} {W} {H} 0 0 0 roundRect
        '''
        
        16750.00000

        idRet.write(textwrap.dedent(reticle))


        Htest = 1490
        Wtest = 2990
        testChip = f'''
        <TestChip struct>
            100 layer
            0 dataype
        	{W - Wtest - 60} {H - Htest - 60} {Wtest} {Htest} 0 0 0 roundRect
        '''
        idRet.write(textwrap.dedent(testChip))

        idRet.write('#'*60 + '\n')
        idRet.write('#'*60 + '\n')


        if doCross:
            cross_points = '-250 17.5 ' + \
                        '-17.5 17.5 ' + \
                        '-17.5 250 ' + \
                        '17.5 250 ' + \
                        '17.5 17.5 ' + \
                        '250 17.5 ' + \
                        '250 -17.5 ' + \
                        '17.5 -17.5 ' + \
                        '17.5 -250 ' + \
                        '-17.5 -250 ' + \
                        '-17.5 -17.5 ' + \
                        '-250 -17.5'

        
            cross = f'''
            <MLAcross struct>
                2 layer
                {cross_points} points2shape
                <0 {Hchip/2-250} 0 {Hchip/2+250} 35 0 0 0 waveguide>
                5 layer
                <-500 0 500 0 600 0 0 0 waveguide>
                <0 {Hchip/2-300} 0 {Hchip/2+300} 80 0 0 0 waveguide>
            '''
            idRet.write(textwrap.dedent(cross))


            botom_cross_points = '-250 17.5 ' + \
                        '-17.5 17.5 ' + \
                        '-17.5 250 ' + \
                        '17.5 250 ' + \
                        '17.5 17.5 ' + \
                        '250 17.5 ' + \
                        '250 0 ' + \
                        '-250 0'

            botom_cross = f'''
            <MLAbottom struct>
                2 layer
                {botom_cross_points} points2shape
                <0 {Hchip/2-250} 0 {Hchip/2+250} 35 0 0 0 waveguide>
                5 layer
                <-500 150 500 150 300 0 0 0 waveguide>
                <0 {Hchip/2-300} 0 {Hchip/2+300} 80 0 0 0 waveguide>
            '''
            idRet.write(textwrap.dedent(botom_cross))

            top_cross_points = '-250 0 ' + \
                        '250 0 ' + \
                        '250 -17.5 ' + \
                        '17.5 -17.5 ' + \
                        '17.5 -250 ' + \
                        '-17.5 -250 ' + \
                        '-17.5 -17.5 ' + \
                        '-250 -17.5'

            top_cross = f'''
            <MLAtop struct>
                2 layer
                {top_cross_points} points2shape
            '''
            top_cross += '5 layer\n<-500 -150 500 -150 300 0 0 0 waveguide>\n'
            idRet.write(textwrap.dedent(top_cross))


            left_cross_points ='0 250 ' + \
                            '17.5 250 ' + \
                            '17.5 17.5 ' + \
                            '250 17.5 ' + \
                            '250 -17.5 ' + \
                            '17.5 -17.5 ' + \
                            '17.5 -250 ' + \
                            '0 -250 '

            left_cross = f'''
            <MLAleft struct>
                2 layer
                {left_cross_points} points2shape
                <8.75 {Hchip/2-250} 8.75 {Hchip/2+250} 17.5 0 0 0 waveguide>
                5 layer
                <0 0 500 0 600 0 0 0 waveguide>
                <20 {Hchip/2-300} 20 {Hchip/2+300} 40 0 0 0 waveguide>
            '''
            idRet.write(textwrap.dedent(left_cross))

            right_cross_points = '-250 17.5 ' + \
                            '-17.5 17.5 ' + \
                            '-17.5 250 ' + \
                            '0 250 ' + \
                            '0 -250 ' + \
                            '-17.5 -250 ' + \
                            '-17.5 -17.5 ' + \
                            '-250 -17.5'

            right_cross = f'''
            <MLAright struct>
                2 layer
                {right_cross_points} points2shape
                <-8.75 {Hchip/2-250} -8.75 {Hchip/2+250} 17.5 0 0 0 waveguide>
                5 layer
                <-500 0 0 0 600 0 0 0 waveguide>
                <-20 {Hchip/2-300} -20 {Hchip/2+300} 40 0 0 0 waveguide>
            '''

            idRet.write(textwrap.dedent(right_cross))



        if doAMSmark: 
            AMSmark(idRet)

        # structure everyhting and shift on the regular grid
        idRet.write('<Reticle struct>\n')
        for dd, xx, yy in zip(Dsgn_name, x0, y0):

            idRet.write(f'\t<{dd} {xx+W/2} {yy+H/2} 0 1 0 instance>\n')

            leftcond = np.abs(xx-street/2)> W/2 - Wchip/2
            rightcond = np.abs(xx+Wchip+street/2)> W/2 - Wchip/2
            bottomcond = np.abs(yy-street/2)> H/2 - Hchip/2
            topcond = np.abs(yy+Hchip+street/2)> H/2 - Hchip/2
            if doCross:
                if not(bottomcond):
                    idRet.write(f'\t<AMSmark {xx+Wchip/2} {yy-street/2} 0 1 0 instance>\n')
                    if not(leftcond):
                        idRet.write(f'\t<MLAcross {xx-street/2} {yy-street/2} 0 1 0 instance>\n')
                    else:
                        idRet.write(f'\t<MLAleft {xx-street/2} {yy-street/2} 0 1 0 instance>\n')
                    if rightcond:
                        idRet.write(f'\t<MLAright {xx+Wchip+street/2} {yy-street/2} 0 1 0 instance>\n')
                else:
                    if not(leftcond):
                        idRet.write(f'\t<MLAbottom {xx-street/2} {yy-street/2} 0 1 0 instance>\n')

                if topcond:
                    # print('topcond')
                    if not(leftcond):
                        idRet.write(f'\t<MLAtop {xx-street/2} {yy+Hchip + street/2} 0 1 0 instance>\n')

                corner_tile = f'''
                    2 layer
                    <{W/2-8.75} {-H/2+ Hchip/2-250} {W/2-8.75} {-H/2 + Hchip/2+250} 17.5 0 0 0 waveguide>
                    <{-W/2+8.75} {-H/2+ Hchip/2-250} {-W/2+8.75} {-H/2 + Hchip/2+250} 17.5 0 0 0 waveguide>

                    5 layer
                    <{-W/2} {-H/2 +150} {-W/2+500} {-H/2 +150} 300 0 0 0 waveguide>
                    <{W/2} {-H/2 +150} {W/2-500} {-H/2 +150} 300 0 0 0 waveguide>
                    <{-W/2} {H/2 -150} {-W/2+500} {H/2 -150} 300 0 0 0 waveguide>
                    <{W/2} {H/2 - 150} {W/2-500} {H/2 -150} 300 0 0 0 waveguide>
                    <{-W/2+20} {-H/2 + Hchip/2-300} {-W/2+20} {-H/2 +  Hchip/2+300} 40 0 0 0 waveguide>
                    <{W/2-20} {-H/2 + Hchip/2-300} {W/2-20} {-H/2 +  Hchip/2+300} 40 0 0 0 waveguide>
                '''
                idRet.write(textwrap.dedent(corner_tile))

        idRet.write(f'\t<ReticleBonding 0 0 0 1 0 instance>\n')
        idRet.write(f'\t<TestChip 0 0 0 1 0 instance>\n')
        # idRet.write(f'\t<AMSmark 0 0 0 1 0 instance>\n')



        # create the gds now
        idRet.close()
        CreateGDS(cnst_name, CNSTpath = CNSTpath,
                         GDSpath = GDSpath,
                         ToolBoxPath = CNSTpath.split('cnst_')[0],
                         javaVers= javaVers,
                         dcty =dcty,
                         move = True, 
                         removeRobCell = False)


    if doPhotronics:
        cnst_name = cnst_name.replace('.cnst' ,'_Photronics.cnst')

        idRet = open(os.path.join(CNSTpath, cnst_name), 'w')
        header = '''
        # ******************************
        0.001 gdsReso
        0.001 shapeReso
        # ******************************
        '''

        idRet.write(textwrap.dedent(header))

        Dsgn_name, x0, y0 = WriteDesigns(idRet, reticle_params,
                                        Nrow, Ncol,
                                        xshift0, yshift0,
                                        relCnstFileFolder,
                                        cnstFiles)

        idRet.write('#'*60 + '\n')
        idRet.write('#'*60 + '\n')
        # create the reticle bonding box
        reticle = f'''
        <ReticleBonding struct>
            99 layer
        	{-W/2} {-H/2} {W} {H} 0 0 0 roundRect
        '''
        idRet.write('#'*60 + '\n')
        idRet.write('#'*60 + '\n')

        # structure only photonics and shift on the regular grid
        idRet.write('<Reticle struct>\n')
        # for dd, xx, yy in zip(Dsgn_name, x0, y0):
        #     idRet.write(f'\t<{dd} {xx} {yy} 0 1 0 instance>\n')
        idRet.write(textwrap.dedent(reticle))

        # create the photonic genAre
        phot_area = f'''
        ####
        <photonicArea Reticle {layer_bool} genArea>

        '''
        idRet.write(textwrap.dedent(phot_area))

        # create the Reticle genAre
        ret_area = f'''
        <reticleArea ReticleBonding 99 genArea>

        ###
        '''
        idRet.write(textwrap.dedent(ret_area))

        finalmask = '''
        <reticlePhotronix struct>
            <reticleArea photonicArea 1 subtract>
        '''
        idRet.write(textwrap.dedent(finalmask))


        idRet.close()
        CreateGDS(cnst_name, CNSTpath = CNSTpath,
                         GDSpath = GDSpath,
                         ToolBoxPath = CNSTpath.split('cnst_')[0],
                         javaVers= javaVers,
                         dcty =dcty,
                         removeRobCell = False)
