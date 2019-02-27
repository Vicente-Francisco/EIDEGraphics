# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# test.py                                                                   #
#                                                                           #
#                                                                           #
#     This file launches a demonstrating execution of 'EIDEGraphics'.       #
#                                                                           #
#     This file is fully docummented so that you can make a precise idea    #
#     on how to execute the examples included and/or write your own         #
#     program to use/evaluate EIDEGraphics. Please, refer file EIDE.py for  #
#     further information and LICENSE notice.                               #
#                                                                           #
#                                                                           #
#############################################################################


import os
import os.path
import sys
import time

import pygame


#############
# INIT CODE #
#############

# Catch working directory ('../EIDEGraphics') and append it to
# 'sys.path'
cwd = os.getcwd()
head = os.path.split(cwd)[0]
os.chdir(head)
sys.path.append(head)

import EIDE


############################
# OPTIONAL ADDRESSING CODE #
############################
"""

Next lines of code serve to direct the rest of the code ('core'
EIDEGraphics usage) to execute different examples/projects. In case you
leave tham as they are (1), the project to execute is taken from
'EIDESystem.txt' file. There are two options:

 1) To adhere the proposed EIDEGraphics examples arquitecture:
    ('../EIDEGraphics/PROJECTS_N_EXAMPLES/YOUR_PROJECT) to check/develop
    your own project using EIDEGraphics. Such a case just modify
    'EIDESystem.txt' 'project' field entering your project name and the
    file 'currentValues = example.simulacion()' below with the suitable
    module.instrucion (or object method or whatever).

 2) You use a more sophisticated arquitecture: your project resides somewhere
    else (may be it even is a remote code/data structure) and
    EIDEGraphics is used as an utility module just to show the data.
    This case the included code ('OPTIONAL ADDRESSING CODE') is useless
    for you: you have your own way to address your code and data; skip
    to the "CORE CODE" section.

"""

import EIDEParser

# Get project to test.
# EIDE general parameters
systemParameters = (
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

mainParser = EIDEParser.EIDEParser(head, 'EIDESystem.txt',
systemParameters)

project = mainParser.get('EIDESystem', 'project')

# Add project path to 'sys.path'
projectPath = os.path.join(os.path.join(head, 'PROJECTS_N_EXAMPLES'), project)
sys.path.append(projectPath)
import example              # User program code mock.



#############
# CORE CODE #
#############

"""
At this point code has either addressed the example whose name has been
taken from 'EIDESystem.txt' or the project -your project- you want to
execute. Now follows the main part of the code; whatever it is designed,
it has to include next lines or the equivalent to them.

Should some error is found in the configuration files, EIDEGraphics
terminates issuing a detailed error message. You can find more
information in the file 'EIDELog.txt'.
"""

# Init EIDEGraphics by instancing it. Create object EIDEGUser

try:
    EIDEGUser = EIDE.EIDEGraphics(0.04)     # 25 frames/s (1 / 0.04)
except Exception as herror:
    # An error (probably a bad configuration file contents) has happened
    print ('*' * len(herror.args[0]))
    print herror.args[0]
    print ('*' * len(herror.args[0]))
    pygame.quit()   # Quits pygame
    sys.exit()      # Quit module
    


while True:
    """

    Main loop: fist line ('currentValues = example.simulacion()') calls
    the example (or user_project) to update the values to be represented
    using EIDEGraphics. Second line
    ('EIDEGUser.EIDEGLoop(currentValues)') effectively calls
    EIDEGraphics to represent them into the EIDEGraphics window. In any
    form you write your program using EIDEGraphics, those two lines -or
    quite similar ones- have to exist.

    """
    currentValues = example.simulacion()
    EIDEGUser.EIDEGLoop(currentValues)

  
    ########################
    # EXAMPLE EXITING CODE #
    ########################

    """

    Next lines use the pygame event manager to detect that the user has
    pressed any key to terminate EIDEGraphics exercising. You can modify
    them to enter any interactive command instead of just leaving the
    session.

    """
    evento = pygame.event.get()
    if (len (evento) > 0) and (evento[0].type == 2):
        break

pygame.quit()   # Quits pygame
sys.exit()      # Quit module


