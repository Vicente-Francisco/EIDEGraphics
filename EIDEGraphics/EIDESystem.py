# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDESystem                                                                #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################


""" Miscellaneous utility classes """

import pygame       
pygame.init()

import time
import os, os.path


################################# system ##############################
class system(object):
    """ According to the platform and project init the system """

    language = 0

    languages = {
    'english': (0),
    'spanish': (1)
    }

    foldersTree = {
    'projects': ('PROJECTS_N_EXAMPLES'),
    'grphFiles': ('GRAPHIC_FILES')
    }


# system #############################
    def __init__(self):
        """ """
        # Dictionary to platform methods 
        self.platformsDict = {
        'windows': (self.setWindows),
        'linux': (self.setLinux)
        }
            

# system #############################
    def setSystem(self, retorno):
        """ Initialize according to user defined 'platform' (O.S.).
        Check for correctness """

        try:
            self.platform = retorno[0][1]
            # Initialize values according to platform
            self.platformsDict[self.platform]()
        except KeyError:
            message = errorTexts.errorTextReturn(
                '0130', [self.platform])
            raise Exception(message)


# system #############################
    def setValues(self, retorno):
        """ Set EIDEGraphics values. Check for correctness """

        # User (selected) project
        self.project = retorno[5][1]

        self.projectPath = os.path.join(self.projects, self.project)
        if not os.path.exists(self.projectPath):
            message = errorTexts.errorTextReturn(
                '0160', [self.project])
            raise Exception(message)

        # Text font and 'normal' size.
        self.textStandardSize = retorno[2][1]
        try:
            self.font = pygame.font.Font(retorno[1][1]
                , self.textStandardSize)
        except IOError:
            message = errorTexts.errorTextReturn(
                '0140', [retorno[1][1]])
            raise Exception(message)
            
        # Indicators maximum readout figures.
        self.sigFigures = retorno[3][1]

        # Language
        try:
            system.language = system.languages[retorno[4][1]]
        except KeyError:
            message = errorTexts.errorTextReturn(
                '0150', [retorno[4][1]])
            raise Exception(message)


# system #############################
    def setProject(self, retorno):
        """ Set project values. Check for correctness """

        # Window size (Hor, Ver; pixels).
        x = retorno[0][1]       
        y = [x.split(",")[0], x.split(",")[1]]
        self.windowSize = [int(y[0]), int(y[1])]
        
        self.windowTitle = retorno[1][1]

        # Get window background image
        # First try in project folder
        self.windowBackground = os.path.join(self.projectPath, retorno[2][1])
        if not os.path.isfile(self.windowBackground):
            # Try in general folder
            self.windowBackground = os.path.join(self.graphicFiles, retorno[2][1])
            if not os.path.isfile(self.windowBackground):
                message = errorTexts.errorTextReturn( '0170',
                    [systemD.windowBackground])
                raise Exception(message)


# system #############################
    def setLinux(self):
        """ Init system for Linux """

        self.getPaths()


# system #############################
    def setWindows(self):
        """ Init system for windows """

        self.getPaths()


# system #############################
    def getPaths(self):
        """ Get project and graphics paths """

        head = os.getcwd()
        self.projects = os.path.join(head, system.foldersTree['projects'])
        self.graphicFiles = os.path.join(head, system.foldersTree['grphFiles'])

################################# system end ##########################




################################ formatoText ##########################
class formatoText(object):
    """

    Manages strings with decimals formats. Accepts 'human readable'
    formats (i.e.: '0.00') and calculates the regular python format
    (i.e.: '%.2f')

    """

    def __init__(self, userFormat):
        
        # String to erase readout. '1.8': temptative value.
        blankString = int(1.8 * systemD.sigFigures) * ' '
    
        self.decimals = {"0": ('%.0f', blankString), "0.0": ('%.1f',
            blankString) , "0.00": ('%.2f', blankString), "0.000":
            ('%.3f', blankString)}

        self.userFormat = userFormat


# formatoText #######################
    def test(self):
        """ Check passed string for validity """
        
        if self.userFormat not in self.decimals:
            raise ValueError

# formatoText #######################
    def get_pythonFormat(self):
        """ Return python format corresponding to user one """
        
        return self.decimals[self.userFormat][0]


# formatoText #######################
    def get_eraseString(self):
        """ Return python format corresponding to user one """
        return self.decimals[self.userFormat][1]

################################ formatoText end ######################




################################## triad1 #############################
class triad1(object):
    """ Class to manage objects having a corner reference (plus two
    coordinates) """

    validCorners = ['TL', 'TR', 'BR', 'BL']
    
    def __init__(self, deltaX, deltaY, corner, **kwargs):
        
        self.deltaX = int(deltaX)
        self.deltaY = int(deltaY)
        self.corner = corner.strip()

        if "display" in kwargs:
            self.display = kwargs.get("display")
            self.displaycoordinates()
            
        if "size" in kwargs:
            self.horSize = kwargs.get("size")[0]
            self.verSize = kwargs.get("size")[1]
            self.relativeCoordinates()


# triad1 #######################
    def fromString(self, texto):
        """

        Passed a formatted string (int, int, TL/TR/BR/BL) as a
        parameter, assigns the values to the triad.

        """
        
        texto = texto.split(",")
        self.deltaX = int(texto[0])
        self.deltaY = int(texto[1])
        self.corner = texto[2].strip()
        self.displaycoordinates()
        

# triad1 #######################
    def test(self):
        """
        Further tests to validate data
        """
        if (self.corner not in self.validCorners):
            
            # Treat the error in the upper level.
            raise ReferenceError
        

# triad1 #######################
    def displaycoordinates(self):
        """ Calculates the widget coordinates with respect to the top
        left corner of the display passed as a parameter (TLX, TLY)"""
        
        RX = int(self.deltaX * self.display.generalScale)
        RY = int(self.deltaY * self.display.generalScale)

        if self.corner == 'TL':
            self.TLX = RX
            self.TLY = RY

        elif self.corner == 'TR':
            self.TLX = self.display.DisplayActualSize[0] - RX
            self.TLY = RY

        elif self.corner == 'BR':
            self.TLX = self.display.DisplayActualSize[0] - RX
            self.TLY = self.display.DisplayActualSize[1] - RY

        elif self.corner == 'BL':
            self.TLX = RX
            self.TLY = self.display.DisplayActualSize[1] - RY


# triad1 #######################
    def relativeCoordinates(self):
        """ Calculates the widget coordinates with respect to the top
        left corner of a passed rectangle"""
        
        RX = int(self.deltaX)
        RY = int(self.deltaY)
        
        if self.corner == 'TL':
            self.TRX = RX
            self.TRY = RY

        elif self.corner == 'TR':
            self.TRX = self.horSize - RX
            self.TRY = RY

        elif self.corner == 'BR':
            self.TRX = self.horSize - RX
            self.TRY = self.verSize - RY

        elif self.corner == 'BL':
            self.TRX = self.deltaX
            self.TRY = self.verSize - RY
            
################################## triad1 end #########################




######################### coordinates #######################
class coordinates(object):
    """ Manages two members lists containing coordinates """

    
# coordinates #######################
    def __init__(self, deltaX, deltaY):
        
        self.deltaX = int(deltaX)
        self.deltaY = int(deltaY)


# coordinates #######################
    def fromString(self, texto):
        """ Loads coordinates from a strig """
        
        texto = texto.split(",")
        self.deltaX = int(texto[0])
        self.deltaY = int(texto[1])
        return (self.deltaX, self.deltaY)

######################### coordinates end ####################
        



############################# clock ############################
class clock:
    # An instance is an object that outputs alternativelly True/False as
    # a square "pulse" shape of period "period" (Sec.)

    # "clock10 = clock(10)" instance; clock10.estate() gives True for 5
    # seconds, then False


# class clock -------------------------------------------------
    def __init__(self, period):
        self.period = period


# class clock -------------------------------------------------
    def estate(self):
        if ((time.clock() % self.period) / float(self.period)) > .5:
            return True
        else:
            return False
        
############################# clock end #########################




############################ flipFlop ######################################
class flipFlop:
    # This class implements a kind of FlipFlop:

    # If called inside a loop (which frequency is "much higher" than the
    # associated clock -see class "clock"), detects the 0 -> 1
    # transition ans sets the output to True (refresh). Implements an
    # internal (application) clock/timer.

    # Sets the output to False when reset.

    # Has a number associated (self.number)

    
# class flipFlop -------------------------------------------------
    def __init__(self, clock, number):
        self.clock = clock
        self.new = self.clock.estate()
        self.last = self.new
        self.estate = False
        self.number = number


# class flipFlop -------------------------------------------------
    def refresh(self):
        self.new = self.clock.estate()
        if (self.new - self.last) == 1:        # True - False = 1
            self.estate = True
        self.last = self.new


# class flipFlop -------------------------------------------------
    def reset(self):
        self.estate = False


# class flipFlop -------------------------------------------------
    def output(self):
        return (self.estate, self.number)

############################ flipFlop end #################################




######################### Languagedictionary ####################
class Languagedictionary(object):

    LanguageDict = {
    'EE': ['EIDE error ', 'Error en EIDE '],
    'ES': ['" in section ', '"en la seccion '],
    'CH': ['channel number ', 'el canal numero '],
    'FL': ['File: "', 'Fichero: "'],
    'FO': ['Font: "', 'Tipo de letra: "'],
    'HOLA': ['hello world', 'hola mundo'],
    'INC': ['" is not a valid integers couple', '" no es una pareja de enteros'],
    'INF': ['" is not a number', '" no es un numero'],
    'ING': ['" is not a valid format', '" no es un formato valido'],
    'INI': ['" is not an integer', '" no es un entero'],
    'INR': ['" is not a valid reference.', ' no es una referencia valida.'],
    'INT': ['" has not a valid corner reference.', ' no tiene una referencia valida.'],
    'LNS': ['" not supported language', '" lenguaje no incluido'],
    'NE': [' does not exist', ' no existe'],
    'NEQ': ['" does not exist', '" no existe'],
    'NF': ['No field "', 'No existe el campo" '],
    'OQ': ['"', '"'],
    'OSN': ['" not supported S.O.', '" sistema operativo no incluido'],
    'PR': ['Project: "', 'Proyecto: "'],
    'SC': ['"; Section: "', '"; Seccion: "'],
    'SM': ['": "', '": "'],
    'UE': ['"Unknown error"', 'Error desconocido'],
    'VC': ['" is not a valid RGB color.', '" no es un color RGB valido.'],
    'VE': ['Value error in "', 'Valor erroneo en "'],
    }


# Languagedictionary ####################
    def phraseReturn(self, key, language):
        """ Return the correspondant phrase to key according to language
        """
        
        return self.LanguageDict[key][language]
    
######################### Languagedictionary end ################




######################### EIDEErrorTexts ########################
class EIDEErrorTexts(object):
    """ Holds the key texts to compose the error messages """

    dictionary = {
    '0000': ['UE'],
    '0010': ['NF', 'ES'],
    '0021': ['FL', 'SC', 'SM', 'INT'],
    '0040': ['FL', 'SC', 'SM', 'INI'],
    '0050': ['FL', 'SC', 'SM', 'INF'],
    '0051': ['FL', 'SC', 'SM', 'INC'],
    '0080': ['FL', 'SC', 'SM', 'VC'],
    '0100': ['FL', 'SC', 'SM', 'INR'],
    '0110': ['FL', 'SC', 'SM', 'ING'],
    '0120': ['CH', 'NE'],
    '0130': ['OQ', 'OSN'],
    '0140': ['FO', 'NEQ'],
    '0150': ['OQ', 'LNS'],
    '0160': ['PR', 'NEQ'],
    '0170': ['FL', 'NEQ'],
    '0180': ['FL', 'NEQ'],
    }


# EIDEErrorTexts ########################
    def errorTextReturn(self, error, lista):

        """ Return the complete error text """

        """
        
        EIDE error messages are composed of one or more texts mixed with
        the data sent by the calling routine. The standard message has
        the form text & data (& text (& data ...) ...). Texts are taken
        from the dictionary while data is the list passed by the calling
        routine. For a given error (i.e.: '0050'), the number of text
        keys (['FL', 'SC', 'SM', 'INF']), has to be equal or greater
        than the number of elements in the passed list.
        
        """

        # Check for valid language
        try:
            errorLanguage = systemD.language
        except NameError:
            errorLanguage = 0 

        texto = languageDictionary.phraseReturn('EE', errorLanguage) +\
        error + ": "
        
        for contador, i in enumerate(self.dictionary[error]):
            texto = texto + \
            languageDictionary.phraseReturn(self.dictionary[error][contador],
                errorLanguage)
            if contador < len(lista):
                texto = texto + lista[contador]
                
        return texto
    
######################### EIDEErrorTexts end ################
            

systemD = system()

languageDictionary = Languagedictionary()

errorTexts = EIDEErrorTexts()
