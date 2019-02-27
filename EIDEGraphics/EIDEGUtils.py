# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEGUtils                                                                #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################

import pygame
pygame.init()

import math

import EIDESystem


def roundedS(HSize, VSize, roundCorner, edgeWidth, backColour,
    frameColour, edgeColour):

    """

    Routine that returns a rectangular surface of HSize, VSize with
    roundCorner radius rounded corners and outlined with a edgeWidth
    width line. Foreground colour = backColour; rectangle colour =
    frameColour; line colour = edgeColour.

    """

    # Vertex (not rounded rectangle)
    P1 = EIDESystem.triad1(roundCorner, 0, 'TL',
        **{"size": (HSize, VSize)})
    P2 = EIDESystem.triad1(roundCorner, 0, 'TR',
        **{"size": (HSize, VSize)})
    P3 = EIDESystem.triad1(0, roundCorner, 'TR',
        **{"size": (HSize, VSize)})
    P4 = EIDESystem.triad1(0, roundCorner, 'BR',
        **{"size": (HSize, VSize)})
    P5 = EIDESystem.triad1(roundCorner, 0, 'BR',
        **{"size": (HSize, VSize)})
    P6 = EIDESystem.triad1(roundCorner, 0, 'BL',
        **{"size": (HSize, VSize)})
    P7 = EIDESystem.triad1(0, roundCorner, 'BL',
        **{"size": (HSize, VSize)})
    P8 = EIDESystem.triad1(0, roundCorner, 'TL',
        **{"size": (HSize, VSize)})

    # Rounded corners centers
    centers = []
    C1 = EIDESystem.triad1(roundCorner, roundCorner, 'TL',
        **{"size": (HSize, VSize)})
    centers.append(C1)
    C2 = EIDESystem.triad1(roundCorner, roundCorner, 'TR',
        **{"size": (HSize, VSize)})
    centers.append(C2)
    C3 = EIDESystem.triad1(roundCorner, roundCorner, 'BR',
        **{"size": (HSize, VSize)})
    centers.append(C3)
    C4 = EIDESystem.triad1(roundCorner, roundCorner, 'BL',
        **{"size": (HSize, VSize)})
    centers.append(C4)

    # 'Init' surface
    superficie = pygame.Surface((HSize, VSize))

    # Draw inner rectangles
    pygame.draw.rect(superficie, frameColour, ((P1.TRX, P1.TRY),
        (HSize - 2 * roundCorner, VSize)), 0)
    pygame.draw.rect(superficie, frameColour, ((P8.TRX, P8.TRY),
        (HSize, VSize - 2 * roundCorner)), 0)

    # Draw rounded corners
    for i in centers:
        pygame.draw.circle(superficie, frameColour, (i.TRX, i.TRY), roundCorner, 0)

    pygame.draw.line(superficie, edgeColour, (P1.TRX, P1.TRY), (P2.TRX, P2.TRY), edgeWidth)
    pygame.draw.line(superficie, edgeColour, (P3.TRX-1, P3.TRY), (P4.TRX-1, P4.TRY), edgeWidth)
    pygame.draw.line(superficie, edgeColour, (P5.TRX, P5.TRY-1), (P6.TRX, P6.TRY-1), edgeWidth)
    pygame.draw.line(superficie, edgeColour, (P7.TRX, P7.TRY), (P8.TRX, P8.TRY), edgeWidth)

    pygame.draw.arc(superficie, edgeColour, ((0,0),(2 * roundCorner,
        2 * roundCorner)), (90*(math.pi/180)), (180*(math.pi/180)), edgeWidth)
    pygame.draw.arc(superficie, edgeColour, ((HSize - 2 * roundCorner, 0),
        (2 * roundCorner, 2 * roundCorner)), (0*(math.pi/180)), (90*(math.pi/180)), edgeWidth)
    # "359,99" instead of 360 in next line is (to circumvent) a pygame bug.
    pygame.draw.arc(superficie, edgeColour, ((HSize - 2 * roundCorner, VSize - 2 * roundCorner),
        (2 * roundCorner, 2 * roundCorner)), (270*(math.pi/180)),
            (359.99*(math.pi/180)), edgeWidth)
    
    pygame.draw.arc(superficie, edgeColour, ((0, VSize - 2 * roundCorner),
        (2 * roundCorner, 2 * roundCorner)), (180*(math.pi/180)), (270*(math.pi/180)), edgeWidth)

    return superficie

