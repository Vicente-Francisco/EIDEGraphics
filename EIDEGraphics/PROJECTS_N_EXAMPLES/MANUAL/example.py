# -*- coding: utf-8 -*-

#################### Test ######################
# Mockery of user main program.
import time, math

matriz = [
[0.60, 0.70, 0.79, 0.87, 0.93, 0.97, 1.00, 1.00, 0.98, 0.94, 0.88, 0.80, 0.71, 0.61, 0.51, 0.40, 0.31, 0.21, 0.14, 0.07, 0.03, 0.00, 0.00, 0.02, 0.06, 0.12, 0.19, 0.28, 0.38, 0.48, 0.59, 0.69],
[0.26, 0.52, 0.69, 0.80, 0.88, 0.94, 0.97, 0.99, 0.98, 0.95, 0.91, 0.84, 0.76, 0.67, 0.57, 0.47, 0.37, 0.28, 0.19, 0.12, 0.07, 0.03, 0.01, 0.02, 0.04, 0.09, 0.15, 0.23, 0.32, 0.42, 0.52, 0.62],
[0.28, 0.43, 0.58, 0.71, 0.81, 0.89, 0.94, 0.97, 0.98, 0.96, 0.93, 0.88, 0.81, 0.73, 0.63, 0.54, 0.44, 0.34, 0.25, 0.17, 0.11, 0.06, 0.03, 0.02, 0.04, 0.07, 0.12, 0.19, 0.27, 0.36, 0.45, 0.55],
[0.33, 0.39, 0.51, 0.63, 0.74, 0.83, 0.89, 0.94, 0.96, 0.96, 0.94, 0.90, 0.85, 0.77, 0.69, 0.60, 0.50, 0.41, 0.31, 0.23, 0.16, 0.10, 0.06, 0.04, 0.04, 0.05, 0.09, 0.15, 0.22, 0.30, 0.39, 0.49],
[0.39, 0.39, 0.46, 0.56, 0.67, 0.76, 0.84, 0.90, 0.94, 0.95, 0.95, 0.92, 0.88, 0.82, 0.74, 0.66, 0.56, 0.47, 0.38, 0.29, 0.21, 0.14, 0.09, 0.06, 0.05, 0.05, 0.08, 0.12, 0.18, 0.25, 0.34, 0.43],
[0.45, 0.41, 0.44, 0.51, 0.60, 0.70, 0.78, 0.85, 0.90, 0.93, 0.94, 0.93, 0.90, 0.85, 0.78, 0.71, 0.62, 0.53, 0.44, 0.35, 0.26, 0.19, 0.13, 0.09, 0.06, 0.06, 0.07, 0.10, 0.15, 0.21, 0.29, 0.37],
[0.49, 0.44, 0.44, 0.48, 0.56, 0.64, 0.73, 0.80, 0.86, 0.90, 0.93, 0.93, 0.91, 0.87, 0.82, 0.75, 0.67, 0.59, 0.50, 0.41, 0.32, 0.24, 0.18, 0.12, 0.09, 0.07, 0.07, 0.09, 0.12, 0.18, 0.24, 0.32],
[0.52, 0.48, 0.46, 0.47, 0.52, 0.59, 0.67, 0.75, 0.82, 0.87, 0.90, 0.92, 0.91, 0.89, 0.85, 0.79, 0.72, 0.64, 0.55, 0.47, 0.38, 0.30, 0.23, 0.16, 0.12, 0.09, 0.08, 0.08, 0.11, 0.15, 0.20, 0.27],
[0.54, 0.50, 0.47, 0.47, 0.50, 0.56, 0.63, 0.70, 0.77, 0.83, 0.87, 0.90, 0.91, 0.90, 0.87, 0.82, 0.76, 0.69, 0.61, 0.52, 0.44, 0.35, 0.28, 0.21, 0.15, 0.11, 0.09, 0.09, 0.10, 0.13, 0.17, 0.23],
[0.55, 0.99, 0.68, 0.59, 1.00, 0.62, 0.65, 1.00, 0.57, 0.71, 0.98, 0.53, 0.78, 0.94, 0.51, 0.84, 0.89, 0.50, 0.90, 0.83, 0.51, 0.95, 0.76, 0.54, 0.98, 0.70, 0.58, 1.00, 0.64, 0.63, 1.00, 0.58],
]

AEIDEG =[0,0,0,0,0,0,0,0,0,0,0,0]

def simulacion():

    N = 32                      # Number of samples
    t = time.clock()            # System time   
    per = 32                     # Period
    mt = t * (float(2.0/per))   # My time   
    ram = (mt - int(mt)) * N    # Ramp value

    ind = int(ram)              # Sample index

    for i in range (0,10):
        AEIDEG[i] = 0.5*math.sin((0.1*(i+1))*ram) + 0.501

    AEIDEG[8] = ram*0.5 + 50
    AEIDEG[9] = (0.5*math.sin((1*(i+1))*ram) + 0.5 + AEIDEG[1])/2

    return AEIDEG

