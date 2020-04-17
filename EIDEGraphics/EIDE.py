# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEGraphics                                                              #
#                                                                           #
#     EideGraphics is an OPEN SOFTWARE python library that helps            #
#     translating numeric magnitudes to big format displays and/or graphic  #
#     elements (gauge indicators, LED's bar displays).                      #
#                                                                           #
#    Apart from this file/module (‘EIDE.py’), the libray contains the       #
#    following modules:                                                     #
#         EIDESystem                                                        #
#         EIDEDisplaysManager                                               #
#         EIDEChannesManager                                                #
#         EIDEWindowManager                                                 #
#         EIDEParser                                                        #
#         EIDEStatistics                                                    #
#         EIDEGUtils                                                        #
#                                                                           #
#     Fully operative multiplatform version – Release 1.0                   #
#                                                                           #
#     Prerequisites: Python 3.8; pygame 1.9.4                               #
#                                                                           #
#     Author: Clave Ingenieros, S.L.                                        #
#     email: vicente.fombellida@claveingenieros.es                          #
#                                                                           #
#     Date: April, 2020                                                     #
#                                                                           #
#                                                                           #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros, S.L.;                               #
# (vicente.fombellida@claveingenieros.es)                                   #
#                                                                           #
# Permission is hereby granted, free of charge, to any person obtaining a   #
# copy of this software and associated documentation files (the “           #
# Software"), to deal in the Software without restriction, including        #
# without limitation the rights to use, copy, modify, merge, publish,       #
# distribute, sublicense, and/or sell copies of the Software, and to        #
# permit persons to whom the Software is furnished to do so, subject to     #
# the following conditions:                                                 #
#                                                                           #
# The above copyright notice and this permission notice shall be included   #
# in all copies or substantial portions of the Software.                    #
#                                                                           #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS   #
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF                #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.    #
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY      #
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,      #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE         #
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                    #
#                                                                           #
#############################################################################


"""

EIDEGraphics class. When instantiated EIDEGraphics activates all of its
resources. Namely:

1) Opens the log ('../EIDEGraphics/EIDELog.txt') file that informs on
the EIDE current session parameters.

2) Loads the user defined parameters for the session and project
('../EIDEGraphics/EIDESystem.txt' and
'../EIDEGraphics/PROJECTS_N_EXAMPLES/userProject/EIDEConfig.txt').

3) Loads the user defined channels data
('../EIDEGraphics/PROJECTS_N_EXAMPLES/userProject/EIDEChannelsCurrent.txt')

4) Loads the user defined displays data
('../EIDEGraphics/PROJECTS_N_EXAMPLES/userProject/EIDEDisplaysCurrent.txt'
and
'../EIDEGraphics/PROJECTS_N_EXAMPLES/userProject/EIDEDisplaysTypes.txt')
.

5) Initiates all the EIDEGraphics modules. Namely:
    EIDESystem
    EIDEDisplaysManager
    EIDEChannesManager
    EIDEWindowManager
    EIDEParser
    EIDEStatistics
    EIDEGUtils


A typical usage would be:

...
import EIDE
EIDEGUser = EIDE.EIDEGraphics(timer_value)
...

User loop:
    /// User own code (i.e.: ADC). User places data to be shwon in
    'currentValues' list

    EIDEGUser.EIDEGLoop(currentValues)


NOTE: EIDEGraphics performs an exhaustive spelling control of the
configuration files; some errors in the files cause program abort. Error
messages are recorded in the file '../EIDEGraphics/EIDELog.txt'.
Alternativelly you can catch the 'EIDEError' (see code at the end of
'test.py') and manage it accordingly.

"""



import sys, os, os.path

import time
import pygame

import EIDEStatistics
from EIDEStatistics import velocidad

import EIDEParser



######################## EIDEException ############################
class EIDEException(Exception):
    """ EIDE exception class, See 'test.py' """
    pass

######################## EIDEException end ########################

# Catch working directory ('../EIDEGraphics') and append it to
# 'sys.path'
cwd = os.getcwd()
head = os.path.split(cwd)[0]
sys.path.append(head)

######################## EIDEGraphics ############################
class EIDEGraphics(object):
    """ EIDEGraphics main class """

    # Configuration files structure
    systemParameters = (
    # EIDE general parameters
    # Platform: windows, linux, MAC
    ('Platform', 4),
    # Text font and 'normal' size.
    ('font', 4),
    ('textStandardSize', 1),
    # Significative figures
    ('sigFigures', 1),
    # Language
    ('language', 4),
    # Project
    ('project', 4),
    )

    projectParameters = (
    # EIDE genearal parameters
    # Window size (Hor, Ver; pixels) and title.
    ('windowSize', 5),
    ('windowTitle', 4),
    ('windowBackground', 4),
    )

    actually = 0


# EIDEGraphics ############################
    def __init__ (self, temporizador):
        """ Init EIDEGraphics itself """
        # Change current directory to "../EIDEGraphics"
        dirAnterior = os.getcwd()
        os.chdir(os.path.join(dirAnterior,"EIDEGraphics"))

        # 1) Open log file ('EIDELog.txt'). First line. 
        try:
            self.ins = open('EIDELog.txt','r+')

            # File already exists. Completely erase file contents
            self.ins.seek(0)
            self.ins.truncate()                        

        except IOError:
            # File does not exist. Create it.
            self.ins = open('EIDELog.txt','w')

        # Log first line
        line = 'EIDEGraphics session intiated at ' +\
        time.asctime(time.localtime()) + "\n"
        self.EIDEGLog(line)


        # 2) Load EIDEGraphics system parameters.
        try:
            mainParser = EIDEParser.EIDEParser('', 'EIDESystem.txt',
                EIDEGraphics.systemParameters)
            retorno = mainParser.optionsListC('EIDESystem')
            line = 'System parameters succesfully loaded' + "\n"
            self.EIDEGLog(line)
            # Traspass system and project parameters values to 'EIDESystem'
            # (class 'system')
            import EIDESystem
            EIDESystem.systemD.setSystem(retorno)
            EIDESystem.systemD.setValues(retorno)

        except Exception as erroron:
            x = erroron.args[0]
            self.EIDEGAbort(x)


        # 3) Load project parameters.
        try:
            projectParser =\
                EIDEParser.EIDEParser(EIDESystem.systemD.projectPath,
                'EIDEConfig.txt', EIDEGraphics.projectParameters)
            line = 'Project: ' + EIDESystem.systemD.project
            self.EIDEGLog(line)
            retorno = projectParser.optionsListC('EIDEProject')
            line = 'Project parameters succesfully loaded' + "\n"
            self.EIDEGLog(line)
            # Traspass system parameters values to 'EIDESystem' (class 'system')
            EIDESystem.systemD.setProject(retorno)
        except Exception as erroron:
            x = erroron.args[0]
            self.EIDEGAbort(x)


        # 4) import 'EIDEChannelsManager'. Check 'EIDEChannelsCurrent.txt'
        try:
            import EIDEChannelsManager
            from EIDEChannelsManager import channelsM
            self.cM = channelsM

            line = 'EIDEChannelsManager module succesfully initiated' + "\n"
            self.EIDEGLog(line)

            for i in self.cM.listChannels():
                self.EIDEGLog(i)

            line = "\n" + "\n"
            self.EIDEGLog(line)

        except Exception as erroron:
            x = erroron.args[0]
            self.EIDEGAbort(x)

              
        # 5) import 'EIDEDisplaysManager'. Check 'EIDEDisplaysCurrent.txt'
        try:
            import EIDEDisplaysManager
            from EIDEDisplaysManager import displaysM
            self.dM = displaysM

            line = 'EIDEDisplaysManager module succesfully initiated' + "\n"
            self.EIDEGLog(line)

            for i in self.dM.listDisplays():
                self.EIDEGLog(i)
            
        except Exception as erroron:
            x = erroron.args[0]
            self.EIDEGAbort(x)


        # 6) import 'EIDEWindowManager'
        # (As EIDEWindowManager does not check any data no 'try' is needed)
        import EIDEWindowManager
        from EIDEWindowManager import windowM
        self.wM = windowM


        # 5) Load initial image into window.
        windowM.blitBackground()
        windowM.updateFromLayer(0)
        EIDEWindowManager.pygame.display.update()
        

        # 7) If user specifies timer init it
        if temporizador != 0:
            self.userTimer = True
            import EIDESystem
            reloj = EIDESystem.clock(temporizador)
            self.ff = EIDESystem.flipFlop(reloj, 0)

        else:
            self.userTimer = False


        # 7) Close log file ('EIDELog.txt')
        self.ins.close()

        # Restore current directory at entrance of "__init__"
        os.chdir(dirAnterior)

            
# EIDEGraphics ############################
    def EIDEGLog(self, line):
        """ Records a line in the file 'EIDELog.txt' """
        
        line = line + "\n"
        self.ins.write(line)


# EIDEGraphics ############################
    def EIDEGAbort(self, message):
        """ Records error in the file 'EIDELog.txt' and closes it.
        Raises error """

        line = message + "\n"
        self.EIDEGLog(line)
        line = 'EIDEGraphics execution aborted'
        self.EIDEGLog(line)
        self.ins.close()
        
        print (message)
##        raise EIDEException(message)


# EIDEGraphics ############################
##    def show(self, valores):
    def EIDEGLoop(self, valores):
        """ Method to be called every time user wants to update screen """

        if self.userTimer:
            # EIDE instantiated with timer
            self.ff.refresh()
            a = self.ff.output()
            if a[0]:
                self.EIDEGUWindow(valores)
                self.ff.reset()
        else:
            # EIDE instantiated without timer
            self.EIDEGUWindow(valores)


# EIDEGraphics ############################
    def EIDEGUWindow(self, valores):
        """ Method to be called every time screen has to be actually
        updated """

        velocidad.parameters('start')

##        pygame.event.pump()

        EIDEGraphics.actually = EIDEGraphics.actually + 1
        self.cM.updateReadouts(valores)
        self.dM.updateDispReadouts()
        self.wM.updateFromLayer(21)

        for i in self.dM.displays:
            i.drawGElements()
            i.printReadout()

        self.wM.windowUpdate()            

        velocidad.parameters('end')

######################## EIDEGraphics end ########################

