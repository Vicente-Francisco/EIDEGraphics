# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEChannesManager                                                        #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################


"""
This module manages the channels the program uses.

"""


"""

At init:
Reads and keeps into memory -object attributes- the information in file
'EIDEChannelsCurrent.txt' that holds the basic information of every channel
defined.

At loop:
Recalculates channels readouts according to passed list.

"""

import EIDEParser
import EIDESystem


############################ channel ##################################
class channel(object):
    """
    Base class for all the channels. 
    """

    def __init__(self, channelTitle, channelUnits, channelGain,
        channelZero, channelLastReadout, channelPercentWarning,
        channelPercentAlarm, channelFormat):
        
        self.title = channelTitle
        self.units = channelUnits
        self.gain = channelGain
        self.zero = channelZero
        self.readout = channelLastReadout
        self.channelPercentWarning = channelPercentWarning
        self.channelPercentAlarm = channelPercentAlarm
        self.channelFormat = channelFormat

        self.formatObject = EIDESystem.formatoText(
            self.channelFormat)
        self.eraseString = self.formatObject.get_eraseString()
            

# channel ##################################
    def calculateReadout(self, value):
        """ Scales and shifts passed value. """
        
        self.readout = value * self.gain + self.zero
            

# channel ##################################
    def channelInfo(self):
        """ Return a text line of info regarding the channel contents """
        
        return self.title + "\t" + self.units + "\t" + str(self.gain) + "\t" +\
        str(self.zero) + "\t" + str(self.channelPercentWarning) + "\t" +\
        str(self.channelPercentAlarm) + "\t" + self.channelFormat

############################ channel end ##############################



############################ channelsManager ##########################
class channelsManager(object):

    """

    - Read info in 'EIDEChannelsCurrent.txt'. This file has the data of the
    connected channels.

    - Instantiates the class 'channel' to create the corresponding
    objects. Manages the list 'channelsList' that holds these objects.


    """

    channelsFile = 'EIDEChannelsCurrent.txt'

    # Basic list (user channel parameters)
    parameters = (
    ('ChannelTitle', 4),
    ('channelUnits', 4),
    ('channelGain', 2),
    ('channelZero', 2),
    ('channelLastReadout', 2),
    ('channelpercentWarning', 1),
    ('channelpercentAlarm', 1),
    ('channelDecimals', 7)
    )


# channelsManager ############################
    def __init__(self):
        """ Read data from 'EIDEChannelsCurrent.txt'. Instantiate channels
        """

        # Read file
        parser = EIDEParser.EIDEParser(EIDESystem.systemD.projectPath,\
            'EIDEChannelsCurrent.txt', channelsManager.parameters)
        lista = parser.sectionsList()

        # Instantiate channels
        self.channelsList = []
        
        for i in lista:
            data = parser.optionsListC(i)
            channelTitle = data[0][1]
            channelUnits = data[1][1]
            channelGain = float(data[2][1])
            channelZero = float(data[3][1])
            channelLastReadout = float(data[4][1])
            channelPercentWarning = int(data[5][1])
            channelPercentAlarm = int(data[6][1])
            channelDecimals = data[7][1]

            canal = channel(channelTitle, channelUnits, channelGain,
                channelZero, channelLastReadout, channelPercentWarning,
                channelPercentAlarm, channelDecimals)

            self.channelsList.append(canal)


# channelsManager ############################
    def listChannels(self):
        """ Build and return a (printable) list with channels info """
        lista = []
        
        line = '#'
        lista.append(line)
        line = '[Channels defined]'
        lista.append(line)
        line = 'Number' + "\t" + 'Title' + "\t" + 'Units' + "\t" +\
        'Gain' + "\t" + 'Zero' + "\t" + 'Warn. %' + "\t" +\
        'Alarm %' + "\t" + 'Format'
        
        lista.append(line)

        line = '-------' + "\t" + '-------' + "\t" + '-------' +\
        "\t" + '-------' + "\t" + '-------' + "\t" + '-------' +\
        "\t" + '-------' + "\t" + '-------'
        
        lista.append(line)

        for counter, i in enumerate(self.channelsList):
            line = str(counter+1)+"\t"+ i.channelInfo()
            lista.append(line)
    
        return lista



# channelsManager ############################
    def updateReadouts(self, AEIDEG):
        """ Scans channels to reacalculate readouts """

        """
        Acts as a filter for wrong or incomplete lists of values passed to
        EIDE:
        1) If values are not numbers substitutes them by '0'
        2) If passed list is incomplete (less values than channels) uses '0'
           to complete channels.
        3) Ignores values in excess (more values than channels) of defined
           channels.
        """
        
        for counter, i in enumerate(self.channelsList):
            try:
                value = float(AEIDEG[counter])
                i.calculateReadout(value)
            except ValueError:
                i.calculateReadout(0)
            except IndexError:
                i.calculateReadout(0)
                
############################ channelsManager end ######################
            
channelsM = channelsManager()
