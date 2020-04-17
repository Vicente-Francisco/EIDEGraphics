# -*- coding: utf-8 -*-
"""


"""


class triad1(object):
    """
    """

    validCorners = ['TL', 'TR', 'BR', 'BL']
    
    def __init__(self, deltaX, deltaY, corner):
        self.deltaX = int(deltaX)
        self.deltaY = int(deltaY)
        self.corner = corner


    def test(self, deltaX, deltaY, corner):
        """
        Further tests to validate object
        """
        if (corner not in validCorners):
            raise Exception('0020')
