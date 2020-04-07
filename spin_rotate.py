# -*- coding: utf-8 -*-
# Rotate spins to new directions about x/y/z axis 
# Written By czf 2/27/2019 
# Only valid for con.dat in SPILADY
# To use it:python3 [script] [file you wanna process]

import os
import sys
import math

script, file_to_be_converted = sys.argv 

print ("""
###################################
#                                 #
#  for SLD software SPILADY       #
#                                 #
###################################
""")

axis = input("""Which axis you wanna rotate about, x or y or z ?""")
angle = input("What angle you wanna rotate(in degree measure)?") 
theta = float(angle) * math.pi / 180

file_name = str(file_to_be_converted) + "_new"
file_read = open(str(file_to_be_converted), 'r')
file_write = open(file_name,'w')

lines = file_read.readlines()

def x_rotate(a, b, c, d):
    a1 = a
    b1 = math.cos(d) * b - math.sin(d) * c
    c1 = math.sin(d) * b + math.cos(d) * c
    return a1, b1, c1

def y_rotate(a, b, c, d):
    a1 = math.cos(d) * a + math.sin(d) * c
    b1 = b
    c1 = -math.sin(d) * a + math.cos(d) * c

    return a1, b1, c1

def z_rotate(a, b, c, d):
    a1 = math.cos(d) * a - math.sin(d) * b
    b1 = math.sin(d) * a + math.cos(d) * b
    c1 = c
    return a1, b1, c1

for i in range(0,len(lines)):         # both begin from 0
    
    if len(lines[i].split()) >= 4:
        sx_str = lines[i].split()[20]   #the true order beginning from 1.
        sy_str = lines[i].split()[21]
        sz_str = lines[i].split()[22]
        
        if axis is "x":
            (sx_n,sy_n,sz_n) = x_rotate(float(sx_str),float(sy_str),float(sz_str),theta)
        
        elif axis is "y":
            (sx_n,sy_n,sz_n) = y_rotate(float(sx_str),float(sy_str),float(sz_str),theta)
             
        elif axis is "z":
            (sx_n,sy_n,sz_n) = z_rotate(float(sx_str),float(sy_str),float(sz_str),theta)
            
        sx_str_n = str(sx_n)
        sy_str_n = str(sy_n)
        sz_str_n = str(sz_n)
                          
        lines[i] = lines[i].replace(sx_str,sx_str_n)  #python is designed to process datas of high complexity (often without repetition).
        lines[i] = lines[i].replace(sy_str,sy_str_n)
        lines[i] = lines[i].replace(sz_str,sz_str_n)
    
    file_write.write(lines[i])


print ("""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
The file has been converted already with "_new"! 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
""")

file_read.close()
file_write.close()
