# -*- coding: utf-8 -*-
# Rotate SAXIS to new directions about x/y/z axis for SOC calculation
# Written By czf 4/14/2019 
# Only valid for INCAR for VASP
# Usage:python3 [script] [INCAR you wanna process]

import sys
import math
import numpy as np

script, file_to_be_converted = sys.argv 

print ("""
###################################
#                                 #
#  for DFT software VASP          #
#                                 #
###################################
""")
print("Rotate SAXIS to new directions about x/y/z axis for SOC calculation")

axis = input("""Which axis you wanna rotate about, x or y or z ?""")
angle = input("What angle you wanna rotate anticlockwise(in degree measure)?") 
theta = float(angle) * math.pi / 180
content = ''

if axis is "z":
    A = np.array([[math.cos(theta), -1 * math.sin(theta), 0],
                  [math.sin(theta), math.cos(theta), 0],
                  [0, 0, 1]])
elif axis is "x":
    A = np.array([[1, 0, 0],
                  [0, math.cos(theta), -1 * math.sin(theta)],
                  [0, math.sin(theta), math.cos(theta)]])    
elif axis is "y":
    A = np.array([[math.cos(theta), 0, math.sin(theta)],
                  [0, 1, 0],
                  [-1 * math.sin(theta), 0, math.cos(theta)]])
 
with open(str(file_to_be_converted), 'r+') as file:
    for line in file.readlines():
        data = line.split()
        if data == []:  # avoid empty line to bug the "data[0]"
            continue
        if data[0] == "SAXIS":
            # coordinate_str = data[2:5] 
            coordinate = [float(i) for i in data[2:5]]
            x = np.array(coordinate).reshape((-1,1))
            y = np.dot(A,x)
            # print(y)
            # print(y[0,0])
            # print(y[1,0])
            # print(y[2,0])
            for i in [y[0,0], y[1,0], y[2,0]]:
                if abs(i) < 0.001:
                    i = 0
                coordinate.append(i)
            # print(coordinate)
            line = "SAXIS" + ' ' + '=' + ' ' + str(coordinate[3]) + ' ' + str(coordinate[4]) + ' ' + str(coordinate[5]) + '\n'
        content += line
with open(str(file_to_be_converted), 'r+') as file:
    file.writelines(content)
            
               
print ("""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
The INCAR has been converted already. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 """)


