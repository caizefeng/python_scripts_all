#!/usr/bin/env python3
# Get Lattice parameters from Birch-Murnaghan state equation
# Written by czf 2018-9-27
# To use it : python3 bm.py (before that you should change constant in x to your own parameters) 

import math 
import numpy as np

print("""
Warning!!!

Remember to change a*Const in x to your own lattice parameters before use it!

""")
# get lattice parameters and corresponding energies from data file
# a is the list of scaling factors in the test calculations
# E is the list of related energies

a, E = np.loadtxt('data', usecols=(0,1), delimiter='\t', unpack = True)

# Change item below a*2.8664 into your parameters

x = a**(-2)

# if column 1 in data file is not a list of scaling factors,
# for example, it is a list of parameters or something like that, use x = a**(-2), actually constant coefficients do not make
# any difference to derivatives.

# equation fitting: https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html
# 3 means the degree of the equation is three

p = np.polyfit(x, E, 3)

c0 = p[3]
c1 = p[2]
c2 = p[1]
c3 = p[0]

print('The fitted BM equation is:')
print(' y = %.4f * (x**3) + %.4f * (x**2) + %.4f * (x) + %.4f' %(c3,c2,c1,c0))

# Get the results of c_1 + 2c_2x + 3c_3x^2 = 0
x1 = (math.sqrt(4*c2**2 - 12*c1*c3) - 2*c2)/(6*c3)
para = 1/math.sqrt(x1)

print('The final lattice parameter is: %s  ' %(para))
