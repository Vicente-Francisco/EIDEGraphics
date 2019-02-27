# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEDisplaysManager                                                       #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################


"""

This module manages the displays (indicators) the program uses.

"""

"""

Sequentially:

1) An object (displaysM) of class 'displaysManager' reads the file
'EIDEDisplaysCurrent.txt' that holds the current indicators configuration. 

2)Then every indicator class is instatiated to initialize every single
indicator. Objects are added to the list '(displaysM.)self.displays'
that is used trhough the whole app to access to them (the displays).


"""
import os.path

import pygame
import math
import time

import EIDEParser
from EIDEParser import EIDEParser

import EIDESystem
import EIDEGUtils

import EIDEWindowManager
from EIDEWindowManager import windowM

import EIDEChannelsManager


############################# indicator ############################
class indicator(object):
    """
    Base class for all types of displays (indicators)
    """

    # Counter to numerate displays (object ordinal)
    ordinal = 0

    # Basic list (common -for every kind of display- parameters). See
    # file "EIDEParser.txt" class "EIDEParser" for details on keys.
    parameters = (
    # Reference size and form factorpixels
    ('referenceSize', 1),
    ('referenceSizeV', 2),
    # Texts offsets (DX, DY, corner). Corner: TL, TR, BR, BL
    ('ofsOrdinal', 3),
    ('ofsNative', 3),
    ('ofsTitle', 3),
    ('ofsUnits', 3),
    ('ofsReadout', 3),
    # Texts sizes
    ('sizeOrdinal', 1),
    ('sizeNative', 1),
    ('sizeTitle', 1),
    ('sizeUnits', 1),
    ('sizeReadout', 1),
    # Background image file,
    ('backgroundImage', 4),
    # Colours
    ('bckgColor', 6),
    ('textColor', 6)
    )

    # Read displays configuration file into the parser.
    parser = EIDEParser(EIDESystem.systemD.projectPath, 'EIDEDisplaysTypes.txt', parameters)


# indicator ############################
    def __init__(self, channel, tipo, size, position, active, topOfScale):
        """ Init common part for every display """

        """

        ordinal:    Ordinal number of the display (automatically assigned)
        channel:    Channel display is tied to (number)
        canal:      Channel display is tied to (object)
        tipo:       Indicator type ('Basic', 'vumeter', ...)
        size:       Indicator horizontal size (See VLED* for exceptions)
        position:   Indicator position in window (X, Y)        
        topOfScale: (Analog indicators) value for the top of the graphic
                    scale.

        """
        
        indicator.ordinal = indicator.ordinal + 1
        self.ordinal = indicator.ordinal
       
        self.channel = channel
        try:
            self.canal = EIDEChannelsManager.channelsM.channelsList[self.channel - 1]
        except IndexError:
            message = EIDESystem.errorTexts.errorTextReturn(
                        '0120', [str(self.channel)])
            raise Exception(message)

            
        self.tipo = tipo                    
        self.size = size
        self.position = position
        self.topOfScale  = topOfScale
        
        self.getGeometricData()
        self.createTextsList()


# indicator ############################
    def getGeometricData(self):
        """ Get geometric data for the specific type of display being
        instantiated. Calculate derived data"""

        # 1) By using the parser load and check for validity the display
        # data.
        self.retornoBData = indicator.parser.optionsListC(self.tipo)

        self.referenceSize = self.retornoBData[0][1]
        self.referenceSizeV = self.retornoBData[1][1]
        self.backgroundImage = self.retornoBData[12][1]
        self.bckgColor = self.retornoBData[13][1]
        self.textColor = self.retornoBData[14][1]
     
        # 2) Calculate overall scale of this display with reference to
        # the 'referenceSize'
        self.generalScale = self.size/float(self.referenceSize)
        self.verticalSize = int(self.referenceSizeV * self.generalScale)
        self.DisplayActualSize = (self.size, self.verticalSize)
                
        # 3) Get display background image
        # First try in project folder
        backgroundFile = os.path.join(EIDESystem.systemD.projectPath,
            self.backgroundImage)

        if not os.path.isfile(backgroundFile):
            # Try in general folder
            backgroundFile =\
                os.path.join(EIDESystem.systemD.graphicFiles,
                self.backgroundImage)

            if not os.path.isfile(backgroundFile):
                message = EIDESystem.errorTexts.errorTextReturn(
                            '0180', [self.backgroundImage])
                raise Exception(message)
            else:
                self.background = pygame.image.load(backgroundFile)
        else:
            self.background = pygame.image.load(backgroundFile)
          
        self.background = self.background.convert()


# indicator ############################
    def createTextsList(self):
        """ Create a list with the indicator texts data (text itself,
        size, position inside the indicator and rectangles to be
        blitted) """
        
        # 1) Gather together the texts (from display and channel info)
        self.displayTexts = [self.ordinal, self.channel, self.canal.title,
            self.canal.units, self.canal.eraseString]
        
        # 2) Generate list ('self.displayTextsList')
        # Text # and positions in 'self.retornoBData'.
        firstText, texts = 2, 5

        self.displayTextsList = []
        for i in range (0, texts):
            # Calculate relative coordinates (into the display) of text.
            x = self.retornoBData[i+firstText][1]
            y = EIDESystem.triad1(x.split(",")[0],
                x.split(",")[1], x.split(",")[2], **{"display": self})
            relPos = (y.TLX, y.TLY)

            # Calculate scale of text
            scale = (self.retornoBData[i+texts+firstText][1]/float(
                EIDESystem.systemD.textStandardSize)) * self.generalScale
            
            # Text itself
            textSurf =\
            EIDESystem.systemD.font.render(str(self.displayTexts[i]),
                True, self.textColor, self.bckgColor)
            
            if i == texts:
                # Correct for readout: rectangle to erase all the readout
                textSurf =\
                EIDESystem.systemD.font.render(self.canal.formatObject.get_eraseString()
                    , True, self.textColor, self.bckgColor)
                
            # Text rectangle
            textRect = textSurf.get_rect()
            textSurf =\
            pygame.transform.scale(textSurf, (int(textRect[2]*scale
                ), int(textRect[3]*scale)))
                
            textRect.topleft = relPos

            # Fill list
            self.displayTextsList.append([str(self.displayTexts[i]),
                scale, relPos, (textSurf, textRect)])


# indicator ############################
    def createSurf10(self):
        """ Create layer 10 surface and send it to layerManager """
        # SurfaceA = plain background
        self.surfaceA = pygame.transform.scale(self.background,
            self.DisplayActualSize)

        self.surfaceA = self.surfaceA.convert()

        # Add surface to 'layerManager'
        self.addSurftoLM(self.surfaceA, self.position, 10, self.ordinal)


# indicator ############################
    def createSurf20(self):
        """ Create layer 20 surfaces and send it to layerManager  """
        # SurfaceB = SurfaceA + fixed texts
        self.surfaceB = self.surfaceA
        # 'blit' individual surfaces into 'surfaceB'
        for i in (self.displayTextsList):
            self.surfaceB.blit(i[3][0], i[3][1])

        # Add surface to 'layerManager'
        self.addSurftoLM(self.surfaceB, self.position, 20, self.ordinal)


# indicator ############################
    def createSurf40(self):
        """ Create layer 40 surface and send it to layerManager """
        # SurfaceD = rectangle to erase readout

        # Readout is the 5th position in 'self.displayTextsList'
        readoutList = self.displayTextsList[4]
        textRect = readoutList[3][1]
        textRect.topleft = (self.position[0]+readoutList[2][0],
            self.position[1]+readoutList[2][1])
        self.surfaceD = readoutList[3][0]
        
        # Add surface to 'layerManager'
        self.addSurftoLM(self.surfaceD, textRect.topleft, 40, self.ordinal)

        # Explicit variables to speed up readout print
        self.readoutScale = readoutList[1]
        self.readoutRectTL = (self.position[0] + readoutList[2][0],
            self.position[1] + readoutList[2][1])


# indicator ############################
    def addSurftoLM(self, superficie, posicion, capa, numero):
        """ Add the passed surface ('superficie', 'posicion') of the
        display # 'numero' to the passed layer ('capa')  """
        
        rectangulo = superficie.get_rect()
        rectangulo.topleft = posicion
        EIDEWindowManager.layerM.addSurface([capa, [numero, superficie,
        rectangulo]])


# indicator ############################
    def drawGElements(self):
        """ Plot the graphic elements of the indicator """
        # Every graphic display has its own
        pass


# indicator ############################
    def printReadout(self):
        """ Directly prints the display (channel) readout onto main window"""

        lectura = self.canal.formatObject.get_pythonFormat() %\
        self.readout

        if len(lectura) > EIDESystem.systemD.sigFigures:
            lectura = "######"
            
        textSurf = EIDESystem.systemD.font.render(lectura, True,
            self.textColor, self.bckgColor)
        textRect = textSurf.get_rect()
        textSurf = pygame.transform.scale(textSurf,
            (int(textRect[2]*self.readoutScale ),
            int(textRect[3]*self.readoutScale)))
        
        textRect.topleft = self.readoutRectTL

        windowM.ventanaPygame.blit(textSurf, textRect)
        
####################### Indicator end ###################################

      


####################### Basic ############################
class Basic(indicator):
    """ Numeric (only) readout """

    def __init__(self, channel, tipo, size, position, active,
        displayTopOfScale):

        indicator.__init__(self, channel, 'Basic', size, position,
            active, displayTopOfScale)
        
        self.createSurf10()
        self.createSurf20()
        self.createSurf40()

####################### Basic end ########################




################################# vumeter ############################
class vumeter(indicator):
    """
    Needle indicator (vumeter)

    """
    
    # Specific parameters list for vumeter indicators
    specificParameters = (
    ('needleCenter', 3), 
    ('initialAngle', 2),
    ('finalAngle', 2),
    ('needleLength1', 1),
    ('needleWidth1', 1),
    ('needleColor1', 6),
    ('needleLength2', 1),
    ('needleWidth2', 1),
    ('needleColor2', 6),
    # NeedleMovement
    ('needleSpeed', 2),
    ('needleViscose', 2),
    # Needle "phisical" stops
    ('needlePhStLeft', 2),
    ('needlePhStRight', 2)
    )


# vumeter ############################
    def __init__(self, channel, tipo, size, position, active,
        displayTopOfScale):

        indicator.__init__(self, channel, 'vumeter', size, position,
            active, displayTopOfScale)
        
        self.calculateDisplay()
        self.createSurf10()
        self.createSurf20()
        self.createSurf30()
        self.createSurf40()

        # Initialize variables to simulate real needle movement
        self.lastAngle = 0
        self.lastUpdateTime = time.time()
        self.lastNeedleSpeed = 0

# vumeter ############################
    def calculateDisplay(self):
        """ Use special parameters to calculate display"""

        # Get data
        self.vumeterOptParser =\
            EIDEParser(EIDESystem.systemD.projectPath,
            'EIDEDisplaysTypes.txt', vumeter.specificParameters)

        retorno = self.vumeterOptParser.optionsListC('vumeterSpecial')

        # Needle geometrics and color
        self.needleCenter = retorno[0][1]
        self.initialAngle = retorno[1][1]
        self.finalAngle = retorno[2][1]
        self.needleLength1 = retorno[3][1]
        self.needleWidth1 = retorno[4][1]
        self.needleColor1 = retorno[5][1]
        self.needleLength2 = retorno[6][1]
        self.needleWidth2 = retorno[7][1]
        self.needleColor2 = retorno[8][1]
        # Needle movement
        self.needleSpeed = retorno[9][1]
        self.needleViscose = retorno[10][1]
        # Needle "phisical" stops
        self.needlePhStLeft = retorno[11][1]
        self.needlePhStRight = retorno[12][1]

        # Calculate absolute (in window) needle rotation center
        # coordinates
        x = self.needleCenter
        y = EIDESystem.triad1(x.split(",")[0],
            x.split(",")[1], x.split(",")[2], **{"display": self})
        self.needleRotCenter = (self.position[0] + y.TLX,
            self.position[1] + y.TLY)

        # Transform user units (degrees) to rad.
        self.iAngleRad = self.initialAngle * (2 * math.pi)/360
        self.fAngleRad = self.finalAngle * (2 * math.pi)/360
        self.leftStop = self.needlePhStLeft * (2 * math.pi)/360
        self.rightStop = self.needlePhStRight * (2 * math.pi)/360

        # Other angles (mind the sign).
        self.totalSpanRad = self.fAngleRad - self.iAngleRad

        # Needle dimensions (scaled).
        # Tracks 1 & 2 lengths
        self.nTrack1 = self.needleLength1 * self.generalScale
        self.nTrack2 = self.needleLength2 * self.generalScale
        self.tracksRatio = (self.nTrack1 + self.nTrack2) / self.nTrack1
        
        # Needle width (scaled).
        # Tracks 1 & 2 lengths
        self.wTrack1 = 1 + int(self.needleWidth1 * self.generalScale)
        self.wTrack2 = 1 + int(self.needleWidth2 * self.generalScale)
                

# vumeter ############################
    def drawGElements(self):
        """ Directly draw the needle onto main window. Includes a
        section to emulate a real display needle """

        # % present readout to top of scale
        percent = self.readout / self.topOfScale

        # Convert to actual (no inertia, no viscose amortiguation)
        # angle.
        readoutAngle = self.iAngleRad + percent * self.totalSpanRad

        # Simulation (inertia, viscose amortiguation).
        deltaAngle = readoutAngle - self.lastAngle
        deltaTime = time.time() - self.lastUpdateTime

        acceleration = self.needleSpeed * deltaAngle - \
        self.needleViscose * self.lastNeedleSpeed

        currentSpeed = self.lastNeedleSpeed + acceleration * deltaTime
        currentAngle = self.lastAngle + currentSpeed * deltaTime/1000

        # Correct for angle bigger than 360 degrees.
        while currentAngle > 2 * math.pi:
            currentAngle = currentAngle - (2 * math.pi)
      
        # Block the needle in the "phisical" stops.
        if currentAngle > self.leftStop:
            currentAngle = self.leftStop
            
        if currentAngle <self.rightStop:
            currentAngle = self.rightStop
        
        # Calculate needdle final coordinates. Track 1
        needleFTrack1 = (self.needleRotCenter[0] + (self.nTrack1
            * math.cos(currentAngle)), self.needleRotCenter[1]
            -(self.nTrack1 * math.sin(currentAngle)))

        # Draw line. Track 1
        pygame.draw.line(windowM.ventanaPygame, self.needleColor1,
            self.needleRotCenter, needleFTrack1, self.wTrack1)

        # Calculate needdle final coordinates. Track 2
        needleFTrack2 = (self.needleRotCenter[0] +
            (needleFTrack1[0]-self.needleRotCenter[0])*self.tracksRatio,
            self.needleRotCenter[1] +
            (needleFTrack1[1]-self.needleRotCenter[1])*self.tracksRatio)
        
        # Draw line. Track 2
        pygame.draw.line(windowM.ventanaPygame, self.needleColor2,
            needleFTrack1, needleFTrack2, self.wTrack2)

        # Update variables for next calculation                         
        self.lastAngle = currentAngle
        self.lastNeedleSpeed = currentSpeed
        self.lastUpdateTime = time.time()
        
  
# vumeter ############################
    def createSurf30(self):
        """ Create specific vumeter layer 30 surface and send it to
        layerManager  """

        self.surfaceC = self.surfaceB

        # Add surface to 'layerManager'
        self.addSurftoLM(self.surfaceC, self.position, 30, self.ordinal)


######################### vumeter end ############################



        
################################# quadrant ############################
class quadrant(indicator):
    """
    Needle indicator (quadrant)

    """
    
    # Specific parameters list for quadrant indicators
    specificParameters = (
    ('needleCenter', 3), 
    ('initialAngle', 2),
    ('finalAngle', 2),
    ('needleLength1', 1),
    ('needleWidth1', 1),
    ('needleColor1', 6),
    ('needleLength2', 1),
    ('needleWidth2', 1),
    ('needleColor2', 6),
    # NeedleMovement
    ('needleSpeed', 2),
    ('needleViscose', 2),
    # Needle "phisical" stops
    ('needlePhStLeft', 2),
    ('needlePhStRight', 2)
    )

# quadrant ############################
    def __init__(self, channel, tipo, size, position, active,
        displayTopOfScale):

        indicator.__init__(self, channel, 'quadrant', size, position,
            active, displayTopOfScale)
        
        self.calculateDisplay()
        self.createSurf10()
        self.createSurf20()
        self.createSurf30()
        self.createSurf40()

        # Initialize variables to simulate needle movement
        self.lastAngle = 0
        self.lastUpdateTime = time.time()
        self.lastNeedleSpeed = 0

# quadrant ############################
    def calculateDisplay(self):
        """ Use special parameters to calculate display"""

        # Get data
        self.quadrantOptParser =\
        EIDEParser(EIDESystem.systemD.projectPath,
            'EIDEDisplaysTypes.txt', quadrant.specificParameters)

        retorno = self.quadrantOptParser.optionsListC('quadrantSpecial')

        # Needle geometrics and color
        self.needleCenter = retorno[0][1]
        self.initialAngle = retorno[1][1]
        self.finalAngle = retorno[2][1]
        self.needleLength1 = retorno[3][1]
        self.needleWidth1 = retorno[4][1]
        self.needleColor1 = retorno[5][1]
        self.needleLength2 = retorno[6][1]
        self.needleWidth2 = retorno[7][1]
        self.needleColor2 = retorno[8][1]
        # NeedleMovement
        self.needleSpeed = retorno[9][1]
        self.needleViscose = retorno[10][1]
        # Needle "phisical" stops
        self.needlePhStLeft = retorno[11][1]
        self.needlePhStRight = retorno[12][1]

        # Calculate absolute (in window) needle rotation center
        # coordinates
        x = self.needleCenter
        y = EIDESystem.triad1(x.split(",")[0],
            x.split(",")[1], x.split(",")[2], **{"display": self})
        self.needleRotCenter = (self.position[0] + y.TLX,
            self.position[1] + y.TLY)

        # Transform user units (degrees) to rad.
        self.iAngleRad = self.initialAngle * (2 * math.pi)/360
        self.fAngleRad = self.finalAngle * (2 * math.pi)/360
        self.leftStop = self.needlePhStLeft * (2 * math.pi)/360
        self.rightStop = self.needlePhStRight * (2 * math.pi)/360

        # Other angles.
        self.totalSpanRad = self.fAngleRad - self.iAngleRad

        # Needle dimensions (scaled).
        # Tracks 1 & 2 lengths
        self.nTrack1 = self.needleLength1 * self.generalScale
        self.nTrack2 = self.needleLength2 * self.generalScale
        self.tracksRatio = (self.nTrack1 + self.nTrack2) / self.nTrack1
        
        # Needle width (scaled).
        # Tracks 1 & 2 lengths
        self.wTrack1 = 1 + int(self.needleWidth1 * self.generalScale)
        self.wTrack2 = 1 + int(self.needleWidth2 * self.generalScale)
                

# quadrant ############################
    def drawGElements(self):
        """ Directly draw the needle onto main window. Includes a
        section to emulate a real display needle """

        # % present readout to top of scale
        percent = self.readout / self.topOfScale

        # Convert to actual (no inertia, no viscose amortiguation)
        # angle.
        readoutAngle = self.iAngleRad + percent * self.totalSpanRad

        # Simulation (inertia, viscose amortiguation).
        deltaAngle = readoutAngle - self.lastAngle
        deltaTime = time.time() - self.lastUpdateTime

        acceleration = self.needleSpeed * deltaAngle - \
        self.needleViscose * self.lastNeedleSpeed

        currentSpeed = self.lastNeedleSpeed + acceleration * deltaTime
        currentAngle = self.lastAngle + currentSpeed * deltaTime/1000

        # Correct for angle bigger than 360 degrees.
        while currentAngle > 2 * math.pi:
            currentAngle = currentAngle - (2 * math.pi)
      
        # Block the needle in the "phisical" stops.
        if currentAngle > self.leftStop:
            currentAngle = self.leftStop
            
        if currentAngle <self.rightStop:
            currentAngle = self.rightStop
        
        # Calculate needdle final coordinates. Track 1
        needleFTrack1 = (self.needleRotCenter[0] + (self.nTrack1
            * math.cos(currentAngle)), self.needleRotCenter[1]
            -(self.nTrack1 * math.sin(currentAngle)))

        # Draw line. Track 1
        pygame.draw.line(windowM.ventanaPygame, self.needleColor1,
            self.needleRotCenter, needleFTrack1, self.wTrack1)

        # Calculate needdle final coordinates. Track 2
        needleFTrack2 = (self.needleRotCenter[0] +
            (needleFTrack1[0]-self.needleRotCenter[0])*self.tracksRatio,
            self.needleRotCenter[1] +
            (needleFTrack1[1]-self.needleRotCenter[1])*self.tracksRatio)
        
        # Draw line. Track 2
        pygame.draw.line(windowM.ventanaPygame, self.needleColor2,
            needleFTrack1, needleFTrack2, self.wTrack2)

        # Update variables for next calculation                         
        self.lastAngle = currentAngle
        self.lastNeedleSpeed = currentSpeed
        self.lastUpdateTime = time.time()
        
  
  
# quadrant ############################
    def createSurf30(self):
        """ Create specific quadrant layer 30 surface and send it to
        layerManager  """

        self.surfaceC = self.surfaceB

        # Add surface to 'layerManager'
        self.addSurftoLM(self.surfaceC, self.position, 30, self.ordinal)

######################### quadrant end ############################




######################### HLEDBar ############################
class HLEDBar(indicator):
    """
    Base class for horizontal LED bar indicators

    """
    
    # Specific parameters list for horizontal LED bar indicators
    specificParameters = (
    # LEDs bar position, dimensions and colours
    ('LEDBarPosition', 3),
    ('LEDBARLength', 1),
    ('LEDsQuantity', 1),
    ('LEDH', 1),
    ('LEDV', 1),
    ('interLED', 1),
    ('baseColour', 6),
    ('warningColour', 6),
    ('alarmColour', 6),
    ('offColour', 6),
    # Colour percentages
    ('percentWarning', 1),
    ('percentAlarm', 1)
    )
    
    HspecificOptionsParser = EIDEParser(EIDESystem.systemD.projectPath,
        'EIDEDisplaysTypes.txt', specificParameters)

        
# HLEDBar ############################
    def __init__(self, channel, tipo, size, position, active, topOfScale):

        # 1) Invoke common "__init__" (indicator).
        indicator.__init__(self, channel, 'HLEDBar', size,
            position, active, topOfScale)

        # 2) Get specific (HLEDBar) data
        retorno = self.HspecificOptionsParser.optionsListC('HLEDBarSpecific')

        self.LEDBarPosition = retorno[0][1]
        self.LEDBARLength = retorno[1][1]
        self.LEDsQuantity = retorno[2][1]
        self.LEDH = retorno[3][1]
        self.LEDV = retorno[4][1]
        self.interLED = retorno[5][1]
        self.baseColour = retorno[6][1]
        self.warningColour = retorno[7][1]
        self.alarmColour = retorno[8][1]
        self.offColour = retorno[9][1]

        self.percentWarning = retorno[10][1]
        self.percentAlarm = retorno[11][1]

        # Locate bar inside display (relative coordinates)
        self.calculateFirstLEDPosition()

        # 3) Calculate LED bar display dimension, number of LED's, ...
        
        # Set "self.generalScale" to '1' so the remaining LED bar
        # calculations are made directly in pixels
        self.generalScale = 1 

        self.calculateLEDsSurfaces()
        self.calculateTotalNOfLEDs()
        self.calculateLEDsList()
        self.createSurf10()
        self.createSurf20()
        self.createSurf21()
        self.createSurf40()
       
        # 4) Init LED bar
        self.lastGraphValue = 0
        self.lastTotalCount = 0


# HLEDBar ############################
    def calculateLEDsSurfaces(self):
        """ Creates the different coloured surfaces for LEDs and the
        thresholds used later to use one or another (surface)"""

        # 1) Generate (coloured) surfaces for LEDs (list "self.colouredLED")
        self.coloursList = (self.baseColour, self.warningColour,
            self.alarmColour, self.offColour)

        self.colouredLED = [None] * 4 
        for counter, colour in enumerate(self.colouredLED):
            self.colouredLED[counter] = pygame.Surface((self.LEDH, self.LEDV))
            self.colouredLED[counter].fill(self.coloursList[counter])

        # 2) Use warning and alarm percents either from display type or
        # channel data
        if self.canal.channelPercentWarning <> 0 or\
        self.canal.channelPercentAlarm <> 0:
            # From channel 
            self.warningLimit = self.canal.channelPercentWarning
            self.alarmLimit = self.canal.channelPercentAlarm
        else:
            # From display type
            self.warningLimit = self.percentWarning
            self.alarmLimit = self.percentAlarm


# HLEDBar ############################
    def calculateFirstLEDPosition(self):
        """ calculate First LED position and bar available length """
        
        # Create First LED 'triad' object 
        self.FLEDBL = EIDESystem.triad1( 0, 0,'TL', **{"display": self})
        self.FLEDBL.fromString(self.LEDBarPosition)
        
        # First LED TL (relative; inside display) coordinates.
        self.FLEDTL = (self.FLEDBL.TLX, self.FLEDBL.TLY)

        # Available space for the bar
        self.availableSpace = self.LEDBARLength * self.generalScale

        # Resize LED's
        self.LEDV = int(self.LEDV * self.generalScale)


# HLEDBar ############################
    def calculateTotalNOfLEDs(self):
        """ Calculate final quantity of LED's """
        
        # Pitch (LED width plus 'interLED' space)
        self.pitch = self.LEDH + self.interLED

        # Total # of LEDs
        if self.LEDsQuantity == 0:
            # Automatic quantity assigned
            self.totalLED = int((self.availableSpace)/ float(self.pitch))
        else:
            # User fixed # of LEDs
            self.totalLED = self.LEDsQuantity

            
# HLEDBar ############################
    def calculateLEDsList(self):     
        """ Create a list with every LED TL corners (absolute
        coordinates) and their colours """

        # List structure (((TopLeftX, TopLeftY), colour), ((X, Y), C), .. )
        self.LEDsInfo = []
        # First LED (always base color: self.colouredLED[0])
        self.LEDsInfo.append([[self.position[0] + self.FLEDTL[0],
            self.position[1] + self.FLEDTL[1]], self.colouredLED[0]])

        for i in range(1, self.totalLED):
            porCiento = (100*i)/float(self.totalLED)
            if (porCiento <= self.warningLimit):
                colouredSurface = self.colouredLED[0]
            elif (porCiento <= self.alarmLimit):
                colouredSurface = self.colouredLED[1]
            else:
                colouredSurface = self.colouredLED[2]

            self.LEDsInfo.append([[self.position[0] + self.FLEDTL[0] +
                i*self.pitch, self.position[1] + self.FLEDTL[1]],
                colouredSurface])


# HLEDBar ############################
    def createSurf21(self):
        """ Create layer 21 (just LEDs) surface and send it to
        layerManager  """

        rectangleTL = ((self.position[0] + self.FLEDTL[0],
            self.position[1] + self.FLEDTL[1]))
        rectangleDim = (self.totalLED * self.pitch - self.interLED, self.LEDV)
        surfaceB2 = pygame.Surface((rectangleDim))
        colouredSurface = self.colouredLED[3]       # "offColour"
        for i in range(0, self.totalLED):
            surfaceB2.blit(colouredSurface, (i*self.pitch, 0))
        
        # Add surface to 'layerManager'
        self.addSurftoLM(surfaceB2, rectangleTL, 21, self.ordinal)


# HLEDBar ############################
    def drawGElements(self):
        """ Directly draw coloured LEDs bar into the window """
        
        # Translate readout to # of LEDs
        self.graphValue = self.readout/float(self.topOfScale)
        self.totalCount = int(self.graphValue * self.totalLED)

        # Update accordingly
        if self.totalCount > self.totalLED:
            self.totalCount = self.totalLED

        if self.totalCount < 0:
            self.totalCount = 0

        if self.totalCount == self.lastTotalCount:
            pass
        
        elif self.totalCount > self.lastTotalCount:
            for i in range(self.lastTotalCount, self.totalCount):
                windowM.ventanaPygame.blit(self.LEDsInfo[i][1],
                    self.LEDsInfo[i][0])
                
        else:
            # self.totalCount < self.lastTotalCount:
            colouredSurface = self.colouredLED[3]       # "offColour"
            for i in range(self.totalLED, self.totalCount, -1):
                windowM.ventanaPygame.blit(colouredSurface,
                    self.LEDsInfo[i-1][0])

        self.lastGraphValue = self.graphValue
        self.lastTotalCount = self.totalCount

######################### HLEDBar end ############################




######################### HBareLEDBar ############################
class HBareLEDBar(HLEDBar):
    """
    Horizontal bare LED bar indicator

    """
    
    # Specific parameters list for VbareLEDBar indicators
    specificParameters = (
    # Drawn surface parameters
    ('frame', 1),
    ('contourWidth', 1),
    ('roundCorner', 1),
    ('backColour', 6),
    ('frameColour', 6),
    ('edgeColour', 6)
    )

    HBareLEDBarParser = EIDEParser(EIDESystem.systemD.projectPath,
        'EIDEDisplaysTypes.txt', specificParameters)


# HBareLEDBar ############################
    def __init__(self, channel, tipo, size, position, active, topOfScale):

        self.getSpecificData()

        HLEDBar.__init__(self, channel, 'HBareLEDBar', size,
            position, active, topOfScale)

        # Delete previous surfaces from layerManager
        EIDEWindowManager.layerM.deleteIndicator(self.ordinal)

        # Correct type
        self.tipo = 'HBareLEDBar'

        self.createSurf10()
        self.createSurf21()
        
   
# HBareLEDBar ############################
    def getSpecificData(self):
        """ Get specific parameters for this display"""
        
        retorno = self.HBareLEDBarParser.optionsListC('HbareLEDBarSpecific')

        self.frame = retorno[0][1]
        self.contourWidth = retorno[1][1]
        self.roundCorner = retorno[2][1]
        self.backColour = retorno[3][1]
        self.frameColour = retorno[4][1]
        self.edgeColour = retorno[5][1]


# HBareLEDBar ############################
    def calculateFirstLEDPosition(self):
        """ Set the First LED position for the 'bare' bar """
        
        self.FLEDTL = [self.roundCorner, self.roundCorner]

        # Resize LED's
        self.LEDV = int(self.LEDV * self.generalScale)


# HBareLEDBar ############################
    def calculateTotalNOfLEDs(self):
        """ Calculate final quantity of LED's """

        self.pitch = self.LEDH + self.interLED
        # Calculate how many LEDs fit into the display
        self.totalLED = int((self.size - 1 * (self.roundCorner) -
            self.LEDH)/ float(self.pitch))

        # Adjust display size to hold just LEDs
        self.recalculatedHS = self.totalLED * self.pitch \
        + 2 * (self.roundCorner) + self.LEDH        
        self.recalculatedVS = self.LEDV + 2*self.roundCorner

        self.DisplayActualSize = [self.recalculatedHS, self.recalculatedVS]
        
        
# HBareLEDBar ############################
    def createSurf10(self):
        """ Create new layer 10 surface and send it to layerManager """
        
        self.surfaceA = EIDEGUtils.roundedS(self.DisplayActualSize[0],
            self.DisplayActualSize[1], self.roundCorner,
            self.contourWidth, self.backColour, self.frameColour,
            self.edgeColour)
        
        self.addSurftoLM(self.surfaceA, self.position, 10, self.ordinal)


# HBareLEDBar ############################
    def createSurf20(self):
        """ surface 20 """

        # Not exactly surface20 but surfaceB (needed in ancestors)
        self.surfaceB = self.surfaceA


# HBareLEDBar ############################
    def printReadout(self):
        """ DO NOT print readout """
        pass

        
######################### HBareLEDBar end #########################




######################### VLEDBar ############################
class VLEDBar(indicator):
    """
    Base class for vertical LED bar indicators

    """
    
    # Specific parameters list for vertical LED bar indicators
    specificParameters = (
    # LEDs bar position, dimensions and colours
    ('LEDBarPosition', 3),
    ('LEDBARLength', 1),
    ('LEDsQuantity', 1),
    ('LEDH', 1),
    ('LEDV', 1),
    ('interLED', 1),
    ('baseColour', 6),
    ('warningColour', 6),
    ('alarmColour', 6),
    ('offColour', 6),
    # Colour percentages
    ('percentWarning', 1),
    ('percentAlarm', 1),
    )
    
    VspecificOptionsParser = EIDEParser(EIDESystem.systemD.projectPath,
        'EIDEDisplaysTypes.txt', specificParameters)


        
# VLEDBar ############################
    def __init__(self, channel, tipo, size, position, active, topOfScale):

        # 1) Invoke common "__init__" (indicator).
        indicator.__init__(self, channel, 'VLEDBar', size,
            position, active, topOfScale)

        # 2) Change parameters for vertical orientation
        self.recalculateForPortrait()
        self.createTextsList()

        # 3) Get specific (VLEDBar) data
        retorno = self.VspecificOptionsParser.optionsListC('VLEDBarSpecific')

        self.LEDBarPosition = retorno[0][1]
        self.LEDBARLength = retorno[1][1]
        self.LEDsQuantity = retorno[2][1]
        self.LEDH = retorno[3][1]
        self.LEDV = retorno[4][1]
        self.interLED = retorno[5][1]
        self.baseColour = retorno[6][1]
        self.warningColour = retorno[7][1]
        self.alarmColour = retorno[8][1]
        self.offColour = retorno[9][1]
        self.percentWarning = retorno[10][1]
        self.percentAlarm = retorno[11][1]

        # 4) Calculate LED bar display
        # 4.1) First LED relative position
        self.calculateFirstLEDPosition()

        # 4.2) Set "self.generalScale" to '1' so the remaining LED bar
        # calculations are made directly in pixels
        self.generalScale = 1 

        self.calculateLEDsSurfaces()
        self.calculateTotalNOfLEDs()
        self.calculateLEDsList()

        self.createSurf10()
        self.createSurf20()
        self.createSurf21()
        self.createSurf40()

        # 5) Init variables to refresh LED bar
        self.lastGraphValue = 0
        self.lastTotalCount = 0


# VLEDBar ############################
    def recalculateForPortrait(self):
        """ Reassign dimensions to change from landscape (horizontal) to
        portrait (vertical)"""

        formFactor = self.referenceSizeV/float(self.referenceSize)
        self.generalScale = self.size/float(self.referenceSizeV)

        self.DisplayActualSize = (int(self.size / formFactor),
            self.size)


# VLEDBar ############################
    def calculateLEDsSurfaces(self):
        """ Creates the different coloured surfaces for LEDs and the
        theresholds used later to use one or another (surface)"""

        # 1) Generate (coloured) surfaces for LEDs (list "self.colouredLED")
        self.coloursList = (self.baseColour, self.warningColour,
            self.alarmColour, self.offColour)

        self.colouredLED = [None] * 4 
        for counter, colour in enumerate(self.colouredLED):
            self.colouredLED[counter] = pygame.Surface((self.LEDH, self.LEDV))
            self.colouredLED[counter].fill(self.coloursList[counter])

        # 2) Use warning and alarm percents either from display type or channel data
        if self.canal.channelPercentWarning <> 0 or self.canal.channelPercentAlarm <> 0:
            # From channel 
            self.warningLimit = self.canal.channelPercentWarning
            self.alarmLimit = self.canal.channelPercentAlarm
        else:
            # From display type
            self.warningLimit = self.percentWarning
            self.alarmLimit = self.percentAlarm


# VLEDBar ############################
    def calculateFirstLEDPosition(self):
        """ calculate First LED position and bar available length """
        
        # Create First LED 'triad' object 
        self.FLEDBL = EIDESystem.triad1( 0, 0,'TL', **{"display": self})
        self.FLEDBL.fromString(self.LEDBarPosition)
        
        # First LED TL (relative; inside display) coordinates.
        self.FLEDTL = (self.FLEDBL.TLX, self.FLEDBL.TLY - self.LEDV)

        # Available space for the bar
        self.availableSpace = self.LEDBARLength * self.generalScale

        # Resize LED's
        self.LEDH = int(self.LEDH * self.generalScale)


# VLEDBar ############################
    def calculateTotalNOfLEDs(self):
        """ Calculate final quantity of LED's """
        
        # Pitch (LED heigth plus 'interLED' space)
        self.pitch = self.LEDV + self.interLED

        # Total # of LEDs
        if self.LEDsQuantity == 0:
            # Automatic quantity assigned
            self.totalLED = int((self.availableSpace)/ float(self.pitch))
        else:
            # User fixed # of LEDs
            self.totalLED = self.LEDsQuantity

            
# VLEDBar ############################
    def calculateLEDsList(self):     
        """ Create a list with led TL corners (absolute coordinates) and
        their colours """

        # List structure (((TopLeftX, TopLeftY), colour), ((X, Y), C), .. )
        self.LEDsInfo = []
        # First LED (always base color: self.colouredLED[0])
        self.LEDsInfo.append([[self.position[0] + self.FLEDTL[0],
            self.position[1] + self.FLEDTL[1]], self.colouredLED[0]])

        for i in range(1, self.totalLED):
            porCiento = (100*i)/float(self.totalLED)
            if (porCiento <= self.warningLimit):
                colouredSurface = self.colouredLED[0]
            elif (porCiento <= self.alarmLimit):
                colouredSurface = self.colouredLED[1]
            else:
                colouredSurface = self.colouredLED[2]

            self.LEDsInfo.append([[self.position[0] + self.FLEDTL[0],
                self.position[1] + self.FLEDTL[1]  - i*self.pitch],
                colouredSurface])


# VLEDBar ############################
    def createSurf21(self):
        """ Create layer 21 ("off" LEDs) surface and send it to
        layerManager  """

        rectangleTL = ((self.position[0] + self.FLEDTL[0],
            self.position[1] + self.FLEDTL[1] - (self.totalLED - 1) *
            self.pitch))
        
        rectangleDim = (self.LEDH, self.totalLED * self.pitch - self.interLED)
        surfaceB2 = pygame.Surface((rectangleDim))
        colouredSurface = self.colouredLED[3]       # "offColour"
        for i in range(0, self.totalLED):
            surfaceB2.blit(colouredSurface, (0, i*self.pitch))
        
        # Add surface to 'layerManager'
        self.addSurftoLM(surfaceB2, rectangleTL, 21, self.ordinal)


# VLEDBar ############################
    def drawGElements(self):
        """ Draw coloured LEDs bar directly onto the screen """
        
        # Translate readout to # of LEDs
        self.graphValue = self.readout/float(self.topOfScale)
        self.totalCount = int(self.graphValue * self.totalLED)

        # Update accordingly
        if self.totalCount > self.totalLED:
            self.totalCount = self.totalLED

        if self.totalCount < 0:
            self.totalCount = 0
            
        if self.totalCount == self.lastTotalCount:
            pass
        
        elif self.totalCount > self.lastTotalCount:
            for i in range(self.lastTotalCount, self.totalCount):
                windowM.ventanaPygame.blit(self.LEDsInfo[i][1],
                    self.LEDsInfo[i][0])

        else:
            # self.totalCount < self.lastTotalCount:
            colouredSurface = self.colouredLED[3]       # "offColour"
            for i in range(self.totalLED, self.totalCount, -1):
                windowM.ventanaPygame.blit(colouredSurface,
                    self.LEDsInfo[i-1][0])

        self.lastGraphValue = self.graphValue
        self.lastTotalCount = self.totalCount

######################### VLEDBar end ############################




######################### VBareLEDBar ############################
class VBareLEDBar(VLEDBar):
    """
    Vertical bare LED bar indicator

    """
    
    # Specific parameters list for VbareLEDBar indicators
    specificParameters = (
    # Drawn surface parameters
    ('frame', 1),
    ('contourWidth', 1),
    ('roundCorner', 1),
    ('backColour', 6),
    ('frameColour', 6),
    ('edgeColour', 6)
    )

    VBareLEDBarParser = EIDEParser(EIDESystem.systemD.projectPath,
        'EIDEDisplaysTypes.txt', specificParameters)


# VBareLEDBar ############################
    def __init__(self, channel, tipo, size, position, active, topOfScale):

        self.getSpecificData()

        VLEDBar.__init__(self, channel, 'VBareLEDBar', size,
            position, active, topOfScale)

        # Delete previous surfaces from layerManager
        EIDEWindowManager.layerM.deleteIndicator(self.ordinal)

        # Correct type
        self.tipo = 'HBareLEDBar'

        self.createSurf10()
        self.createSurf21()

   
# VBareLEDBar ############################
    def getSpecificData(self):
        """ Get specific parameters for this display"""
        retorno = self.VBareLEDBarParser.optionsListC('VBareLEDBarSpecific')

        self.frame = retorno[0][1]
        self.contourWidth = retorno[1][1]
        self.roundCorner = retorno[2][1]
        self.backColour = retorno[3][1]
        self.frameColour = retorno[4][1]
        self.edgeColour = retorno[5][1]


# VBareLEDBar ############################
    def calculateFirstLEDPosition(self):
        """ Set the First LED position for the 'bare' bar """
        self.FLEDTL = [self.roundCorner, self.size - self.roundCorner]

        # Resize LED's
        self.LEDH = int(self.LEDH * self.generalScale)


# VBareLEDBar ############################
    def calculateTotalNOfLEDs(self):
        self.pitch = self.LEDV + self.interLED
        # Calculate how many LEDs fit into the display
        self.totalLED = int((self.size - 1 * (self.roundCorner) -
            self.LEDV)/ float(self.pitch))

        self.recalculatedHS = self.LEDH + 2*self.roundCorner        
        self.recalculatedVS = self.totalLED * self.pitch \
        + 2 * (self.roundCorner) + self.LEDV

        self.DisplayActualSize = [self.recalculatedHS, self.recalculatedVS]

        
# VBareLEDBar ############################
    def createSurf10(self):
        """ Create new layer 10 surface and send it to layerManager """
        self.surfaceA = EIDEGUtils.roundedS(self.DisplayActualSize[0],
            self.DisplayActualSize[1], self.roundCorner,
            self.contourWidth, self.backColour, self.frameColour,
            self.edgeColour)
        
        self.addSurftoLM(self.surfaceA, self.position, 10, self.ordinal)

 
# VBareLEDBar ############################
    def createSurf20(self):
        """ surface 20 """

        # Not exactly surface20 but surfaceB (needed in ancestors)
        self.surfaceB = self.surfaceA

 
# VBareLEDBar ############################
    def printReadout(self):
        """ DO NOT print readout """
        pass

######################### VBareLEDBar end ###################




######################## displaysManager ############################
class displaysManager(object):
    """ Manages user defined indicators """

    """
    Typical usage. At init:

    - Read info in 'EIDEDisplaysCurrent.txt'. This file holds the basic
    characteristics of the current displays.

    - Instantiates the correspondent classes ('vumeter', 'Basic',
    etcetera) to create the indicator objects. Manages the list
    'displaysList' that holds these objects.

    Loop:

    - When asked by the main loop routine ('EIDEGraphics.EIDEGUWindow')
    calls the corresponding (indicators) methods to refresh channel
    readout ('updateDispReadouts').

    """



    # Basic list (user display parameters)
    parameters = (
    ('displayType', 4),
    ('displayChannel', 1),
    ('displaySize', 1),
    ('displayPosition', 5),
    ('displayTopOfScale', 1)
    )


# displaysManager ############################
    def __init__(self):
        """ Read data from 'EIDEDisplaysCurrent.txt'. Instantiate displays
        """

        # Read file
        parser = EIDEParser(EIDESystem.systemD.projectPath,
            'EIDEDisplaysCurrent.txt', displaysManager.parameters)
        lista = parser.sectionsList()

        # Instantiate displays
        self.displays = []
        for i in lista:
            retorno = parser.optionsListC(i)
            displayChannel = retorno[1][1]
            displayType = retorno[0][1]
            displaySize = int(retorno[2][1])
            coordinates = EIDESystem.coordinates(0,0)
            displayPosition = coordinates.fromString(retorno[3][1])
            displayTopOfScale = int(retorno[4][1])

            if displayType == 'vumeter':
                newDisplay = vumeter(displayChannel, 'vumeter',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)
            elif displayType == 'quadrant':
                newDisplay = quadrant(displayChannel, 'quadrant',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)
            elif displayType == 'Basic':
                newDisplay = Basic(displayChannel, 'Basic',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)
            elif displayType == 'HLEDBar':
                newDisplay = HLEDBar(displayChannel, 'HLEDBar',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)
            elif displayType == 'HBareLEDBar':
                newDisplay = HBareLEDBar(displayChannel, 'HBareLEDBar',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)
            elif displayType == 'VLEDBar':
                newDisplay = VLEDBar(displayChannel, 'VLEDBar',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)
            elif displayType == 'VBareLEDBar':
                newDisplay = VBareLEDBar(displayChannel, 'VBareLEDBar',
                    displaySize, displayPosition, 0, displayTopOfScale)
                self.displays.append(newDisplay)


# displaysManager ############################
    def listDisplays(self):
        """ Build and return a (printable) list with displays info """
        lista = []
        
        line = '#'
        lista.append(line)
        line = '[Displays defined]'
        lista.append(line)
        line = 'Ordinal' + "\t" + 'Top Sc.' + "\t" + 'Channel' + "\t"\
        + 'Size' + "\t" + 'Pos. X' + "\t" + 'Pos. Y' + "\t" + 'Type'
        lista.append(line)
        line = '-------' + "\t" + '-------' + "\t" + '-------' + "\t"\
        + '-------' + "\t" + '-------' + "\t" + '-------' + "\t" + '-------'
        lista.append(line)

        for i in self.displays:
            line = str(i.ordinal)+ "\t" + str(i.topOfScale) + "\t" +\
            str(i.channel) + "\t" + str(i.size) + "\t" +\
            str(i.position[0]) + "\t" + str(i.position[1]) + "\t" + i.tipo
            
            lista.append(line)

        return lista


# displaysManager ############################
    def updateDispReadouts(self):
        """ Update 'readout' attribute in all the displays (objects)"""
        
        for i in self.displays:
            i.readout = i.canal.readout

######################## displaysManager end #########################

# Single displaysManager object.
displaysM = displaysManager()
