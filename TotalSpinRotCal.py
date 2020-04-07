#!/home/lzhpc/anaconda3/bin/python
# -*- coding: utf-8 -*-
# Obtain the cosine deviation of total spin with respect to the initial spin
# configuration.
# Usage: type "python TotalSpinRotCal.py spn-xxxx.dat"
# Output file: CosineDeviation.dat

import sys
import numpy as np

script, file_to_be_converted = sys.argv 

with open("CosineDeviation.dat",'w') as file_write, open(str(file_to_be_converted), 'r') as file_read:   

    file_write.write("{0}       {1}\n".format("Step", "Cosine"))
    step = -1

    for line in file_read.readlines():
        sx = float(line.split()[2])
        sy = float(line.split()[3])
        sz = float(line.split()[4])
        spin_vector = np.array([sx, sy, sz])
        if step == -1:
            spin_initial = spin_vector
        num = np.dot(spin_vector, spin_initial.T)
        denom = np.linalg.norm(spin_vector) * np.linalg.norm(spin_initial)  
        cos = num / denom 
        if step != -1 :
            file_write.write("{:<10}{:0<18}\n".format(step, cos))
        step = step + 1

print("Done!")
