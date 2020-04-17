# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEParser                                                                #
#                                                                           #
#     This file is part of the library EIDEGraphics. Please, refer file     #
#     EIDE.py for further information and LICENSE notice.                   #
#                                                                           #
#############################################################################

"""

Class 'EIDEParser'. It inherits from the class
'configparser.configparser' (configparser python library). Adds to
configparser.configparser a 'bullet proof' method -'optionsListC'- to
filter out any inconsistency in the configuration ('*.txt') files.

"""

import os.path
import configparser
##import ConfigParser # python 2.7
import EIDESystem


############################### EIDEParser #########################
class EIDEParser(configparser.ConfigParser):
    """ Specific parser for EIDE 'txt' files """


# EIDEParser #########################
    def __init__(self, path, fichero, parameters):
        configparser.ConfigParser.__init__(self)

        self.wholePath = os.path.join(path,fichero)
        self.read(self.wholePath)
        self.fichero = fichero
        self.parameters = parameters


# EIDEParser #########################
    def sectionsList(self):
        """ Return a list on the sections in the file """
        return self.sections()


# EIDEParser #########################
    def optionsList(self, seccion):
        """ Return a list with the options -fields- of a given section.
        No check """
        return self.items(seccion)


# EIDEParser #########################
    def optionsListC(self, seccion):
        """ Return a 'converted' list with the options -fields- in the
        section. Checks for existence and validity of data."""


        """
        Key:2nd field in 'parameters'       returns
            -------------------------       -------------------
            - 1: integer                    integer
            - 2: float                      float
            - 3: triad                      triad 
            - 4: text                       text
            - 5: coordinates                coordinates object
            - 6: colour values              colour tuple
            - 7: user print format	    python print format string
            
        """
        
        lista = self.items(seccion)
        retorno = []
        
        for contador, i in enumerate(self.parameters):
            # Check for variable in section
            if not(self.has_option(seccion, i[0])):
                # Variable not in section. Compose error message
                message = EIDESystem.errorTexts.errorTextReturn(
                    '0010', [i[0], seccion])
                raise Exception(message)


            # Check each contents according to type
            if i[1] == 1:
                # Integer
                try:
                    self.getint(seccion, lista[contador][0])
                    retorno.append((lista[contador][0],
                        self.getint(seccion, lista[contador][0])))

                except ValueError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0040', [self.fichero, seccion, i[0]])
                    raise Exception(message)
                except:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0000', "")
                    raise Exception(message)


            elif i[1] == 2:
                # Float
                try:
                    self.getfloat(seccion, lista[contador][0])
                    retorno.append((lista[contador][0],self.getfloat(seccion,
                        lista[contador][0])))

                except ValueError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0050', [self.fichero, seccion, i[0]])
                    raise Exception(message)

                except:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0000', "")
                    raise Exception(message)


            elif i[1] == 3:                 
                # Field is a 'triad': test it for consistency (has to
                # have three fields; last one a valid corner
                # designation)
                x = self.get(seccion, lista[contador][0])
                try:
                    y = EIDESystem.triad1(x.split(",")[0],
                        x.split(",")[1], x.split(",")[2])
                    y.test()
                    retorno.append((lista[contador][0],
                        self.get(seccion, lista[contador][0])))

                except IndexError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0100', [self.fichero, seccion, i[0]])
                    raise Exception(message)

                except ReferenceError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0021', [self.fichero, seccion, i[0]])
                    raise Exception(message)
               

            elif i[1] == 4:
                # Field is a text. No test.
                retorno.append((lista[contador][0], self.get(seccion,
                    lista[contador][0])))


            elif i[1] == 5:
                # Coordinates (two integers)
                x = self.get(seccion, lista[contador][0])
                try:
                    y = EIDESystem.coordinates(x.split(",")[0],
                        x.split(",")[1])
                    retorno.append((lista[contador][0],
                        self.get(seccion, lista[contador][0])))

                except ValueError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0051', [self.fichero, seccion, i[0]])
                    raise Exception(message)

                except IndexError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0100', [self.fichero, seccion, i[0]])
                    raise Exception(message)
               

            elif i[1] == 6:
                # RGB color
                try:
                    rgb = self.get(seccion, lista[contador][0]).split(",")
                    color = tuple(map(int, rgb))
                    for j in color:
                        if j < 0 or j > 255:
                            raise ValueError
                    retorno.append((lista[contador][0], color))

                except ValueError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0080', [self.fichero, seccion, i[0]])
                    raise Exception(message)
               

            elif i[1] == 7:
                # User print (decimals) format
                retorno.append((lista[contador][0], self.get(seccion, lista[contador][0])))

                # Test format for consistency ('0' .. '0.000')
                try:
                    y = EIDESystem.formatoText(self.get(seccion,
                        lista[contador][0]))
                    y.test()

                except ValueError:
                    message = EIDESystem.errorTexts.errorTextReturn(
                        '0110', [self.fichero, seccion, i[0]])
                    raise Exception(message)
                                        
        return retorno

############################### EIDEParser end #####################


