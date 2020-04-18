# -*- coding: utf-8 -*-

#################### Test ######################
# Este codigo es un remedo de lo que sería el de 'calculo' del usuario
import time, random

import EIDEStatistics
from EIDEStatistics import velocidad

import os, os.path

def simulacion():
    AEIDEG =[0,0,0,0,0,0,0,0,0,0,0]
    periodo = 1
    amplitud = 1
    semiPeriodo = periodo / 2.0
    miTiempo = time.clock() * (1/float(semiPeriodo))
    t2 = time.clock() / 2
    t4 = time.clock() / 4
    t8 = time.clock() / 8
    t16 = time.clock() / 16
    t32 = time.clock() / 32
    bit2 = int(t2 % 2)
    bit4 = int(t4 % 2)
    bit8 = int(t8 % 2)
    bit16 = int(t16 % 2)
    bit32 = int(t32 % 2)
    uno = int(miTiempo % 2)
    if uno:
        rampa = (miTiempo - int(miTiempo) ) * amplitud
    else:
        rampa = amplitud - ((miTiempo - int(miTiempo) ) * amplitud)

    dienteSierra = miTiempo - int(miTiempo)

    escalon = (1/31.0) * (bit2 + bit4* 2 + bit8 *4 + bit16 *8 + bit32 *16)
    AEIDEG[0] = 0.15*rampa + 0.85*random.random()
    AEIDEG[2] = escalon
    AEIDEG[4] = 0.5 - rampa
##    AEIDEG[6] = rampa#AEIDEG[4]/2
    AEIDEG[1] = (AEIDEG[0] + AEIDEG[2])/2
    AEIDEG[3] = (AEIDEG[2] + AEIDEG[4])/2
    AEIDEG[5] = escalon#(AEIDEG[4] + AEIDEG[6])/2
    AEIDEG[6] = velocidad.recalculateLoopSpeed()/100000
    AEIDEG[7] = 0#EIDEGraphics.actually / (time.clock()-empieza)   

## MANUAL
    matriz = [
    [1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00],
    [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    [0.06, 0.13, 0.19, 0.25, 0.31, 0.38, 0.44, 0.50, 0.56, 0.63, 0.69, 0.75, 0.81, 0.88, 0.94, 1.00, 0.94, 0.88, 0.81, 0.75, 0.69, 0.63, 0.56, 0.50, 0.44, 0.38, 0.31, 0.25, 0.19, 0.13, 0.06, 0.00],
    [0.13, 0.25, 0.38, 0.50, 0.63, 0.75, 0.88, 1.00, 0.88, 0.75, 0.63, 0.50, 0.38, 0.25, 0.13, 0.00, 0.13, 0.25, 0.38, 0.50, 0.63, 0.75, 0.88, 1.00, 0.88, 0.75, 0.63, 0.50, 0.38, 0.25, 0.13, 0.00],
    [0.25, 0.50, 0.75, 1.00, 0.75, 0.50, 0.25, 0.00, 0.25, 0.50, 0.75, 1.00, 0.75, 0.50, 0.25, 0.00, 0.25, 0.50, 0.75, 1.00, 0.75, 0.50, 0.25, 0.00, 0.25, 0.50, 0.75, 1.00, 0.75, 0.50, 0.25, 0.00],
    [1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00, 1.00, 1.00, 0.00, 0.00],
    [0.13, 0.25, 0.38, 0.50, 0.63, 0.75, 0.88, 1.00, 0.88, 0.75, 0.63, 0.50, 0.38, 0.25, 0.13, 0.00, 0.13, 0.25, 0.38, 0.50, 0.63, 0.75, 0.88, 1.00, 0.88, 0.75, 0.63, 0.50, 0.38, 0.25, 0.13, 0.00],
    [0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 0.00, 0.25, 0.50, 0.75, 1.00],
    ]

### CAR. Periodo 64
##    matriz = [
##    [0.00, 9.85, 19.10, 27.80, 35.98, 43.67, 50.89, 57.69, 64.07, 70.07, 75.71, 81.02, 86.00, 90.69, 95.09, 99.23, 103.13, 106.79, 110.22, 113.46, 116.50, 119.35, 122.04, 124.56, 126.93, 129.16, 131.26, 133.23, 135.08, 136.82, 138.46, 140.00],
##    [0.00, 9.85, 19.10, 27.80, 17.99, 21.83, 25.45, 28.84, 32.04, 23.36, 25.24, 27.01, 28.67, 30.23, 23.77, 24.81, 25.78, 26.70, 27.56, 28.36, 29.12, 29.84, 30.51, 31.14, 31.73, 25.83, 26.25, 26.65, 27.02, 27.36, 27.69, 28.00],
##    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
##    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
##    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
##    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
##    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
##    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
##    ]

### AUDIO
####    matriz = [
####    [0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06],
####    [0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12],
####    [0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18],
####    [0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20],
####    [0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18],
####    [0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12],
####    [0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06],
####    [0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03],
####    [0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.20, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01],
####    [0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.03, 0.06, 0.12, 0.18, 0.12, 0.06, 0.03, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
####    ]


    indice = int((dienteSierra*32)%32) 
    for i in range (0,8):
        try:
            AEIDEG[i] = matriz[i][indice]
            AEIDEG[0] = velocidad.statistics[0]/100
        except IndexError:
            print (i, indice)

    return AEIDEG
