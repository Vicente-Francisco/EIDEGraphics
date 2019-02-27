# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEWindowManager                                                         #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################


""" Manage -create, update- window according to passed parameters."""



"""

Class "windowManager": is the fnal stage on what concerns screen
-window- creation and updating.

Class "layerManager": manages the lists holding sorted information on
the objects ('phisical') to be displayed in different 'layers', so that
only the necessary layers are updated when needed.

"""

import pygame
pygame.init()

import EIDESystem               
from EIDESystem import systemD



################################# layerManager ##########################
class layerManager(object):
    """ Screen layers management """

    """ Layer manager. Maintains a "list of lists" -'layerList'- that
    are -each list- the 'layer' to which the (pygame)surfaces composing
    the window belong along with the surfaces themselves definition.
    Manages also 'indexList' and 'updateList' derived from the main one.

    layerList structure: [(layerA, (displayX, surfaceJ, surfaceRectJ),
    (displayY, surfaceK, surfaceRectK)), ..., (layerD, (displayZ,
    surfaceM, surfaceRectM))]

    indexList structure: [layerA, ..., layerD]

    updateList structure: [surfaceRectJ, surfaceRectK, ..., surfaceRectM]

    """


# layerManager ##########################
    def __init__(self):

        self.layerList = []
        self.indexList = []
        self.updateList = []

    
# layerManager ##########################
    def reindexLayers(self):
        """ Build and sort the 'indexList' and create 'updateList' from
        scratch """
        
        self.indexList = []

        if len(self.layerList) > 0:
            self.indexList.append(self.layerList[0][0])
            for i in self.layerList:
                layer = i[0]
                if not(self.layerExist(layer)):
                    self.indexList.append(i[0])
                
        self.indexList.sort()

        
        """ 'updateList' contains the rectangles to speed up screen update """
        self.updateList = []

        for i in self.layerList:
            if i[0] > 20:
                superficies = i[1:]
                # superficies = (displayX, surfaceJ, surfaceRectJ)
                for j in superficies:
                    if j[0]<>0:         # "0": supressed display
                        self.updateList.append(j[2])


# layerManager ##########################
    def layerExist(self, layer):
        """ Check if a layer is already catalogued """
        
        try:
            self.indexList.index(layer)
            return True
        except ValueError:
            return False


# layerManager ##########################
    def addSurface(self, lista):
        """ Passed a list (layer, (display, surface, surfaceRect)), adds
        it to the main 'layerList' list and reindex the list"""

        layer = lista[0]
        if not(self.layerExist(layer)):
            # Layer does not exist. Add 'lista' directly
            self.layerList.append(lista)

        else:
            # Layer exists: add just indicator and surface info.
            for i in (self.layerList):
                if i[0] == layer:
                    i.append(lista[1])
                    break

        self.reindexLayers()


# layerManager ##########################
    def deleteIndicator(self, indicator):
        """ Deletes all the surfaces of the passed indicator by changing
        indicator # to '0' """

        for i in (self.layerList):
            for contador, j in enumerate(i):
                if not(isinstance(j, int)):
                    if j[0] == indicator:
                        i[contador][0] = 0
                        
################################# layerManager end #####################




################################# windowManager ##########################
class windowManager(object):
    """ This class is the last stage on the screen (what you see). """


# windowManager ##########################
    def __init__(self):
        
        # Configure and open pygame window.
        icono = pygame.image.load('EIDEGIcon.jpg')
        pygame.display.set_icon(icono)

        self.ventanaPygame = pygame.display.set_mode(systemD.windowSize)

        pygame.display.set_caption(systemD.windowTitle)

        self.blitBackground()


# windowManager ##########################
    def windowUpdate(self):
        """ Updates the selected rectangles in the screen """
        
        pygame.display.update(layerM.updateList)


# windowManager ##########################
    def blitBackground(self):
        """ Clears the screen by blitting the background image """

        fondoPantalla = pygame.image.load(EIDESystem.systemD.windowBackground)
        fondoPantalla = pygame.transform.smoothscale(fondoPantalla,
            systemD.windowSize)
        self.ventanaPygame.blit(fondoPantalla, fondoPantalla.get_rect())


# windowManager ##########################
    def updateFromLayer(self, layer):
        """ Refreshes the screen by 'bliting' layers from 'layer' upwards """

        for i in layerM.indexList:
            if i > layer:
                for j in layerM.layerList:
                    if j[0] == i:
                        superficies = j[1:]
                        for k in superficies:
                            if k[0]<>0:         # "0": supressed display
                                self.ventanaPygame.blit(k[1], k[2])

        self.windowUpdate()
        
################################# windowManager end ######################

layerM = layerManager()                
            
windowM = windowManager()



