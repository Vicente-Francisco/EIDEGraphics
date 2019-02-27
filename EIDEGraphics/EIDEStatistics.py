# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEStatistics                                                            #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################


"""

This module calculates the program parameters

"""

import time

import EIDESystem


######################## speeds ############################
class speeds(object):
    """ Calculate EIDE statistics """

    def __init__(self):

        # 1 Sec. flip-flop
        reloj = EIDESystem.clock(1)
        self.ff = EIDESystem.flipFlop(reloj, 0)
        self.ff.reset()

        # loop statistics variables
        self.elapsedTime = 0
        self.statistics = [0.0, 0.0]
        self.empieza = 0
        
        self.lastLoopTime = time.clock()
        self.loopF = 0
        
    
# speeds ############################
    def recalculateLoopSpeed(self):
        """ If called once per loop calculates program overall speed in
        'loops/s' """
        
        self.loopF = 1 / (time.clock() - self.lastLoopTime)
        self.lastLoopTime = time.clock()

        return self.loopF


# speeds ############################
    def parameters(self, event):
        """ Calculate loop statistics """

        """

        This method calculates the time EIDEGraphics takes to update the
        screen (in ms) for every second of program time. The method is
        called before and after the main updating method
        '(EIDE.EIDEGraphics.)EIDEGUWindow' does its job. Results are
        wrong if screen refreshing ratio is less than 1 second.

        """

        # EIDEGraphics consumed time (ms per second of total time)
        # Accumulate time
        if event == 'start':
            # Start cronometer
            self.empieza = time.clock()
        else:
            # Stop cronometer
            self.elapsedTime = self.elapsedTime + time.clock() \
            - self.empieza

        # See if a whole second has transcurred
        self.ff.refresh()
        a = self.ff.output()
        if a[0]:
            # One second lapse. Update statistics.
            self.statistics[0] = self.elapsedTime*1000
            self.ff.reset()
            self.elapsedTime = 0
        
        return self.statistics


######################## speeds end ########################
   
velocidad = speeds()
