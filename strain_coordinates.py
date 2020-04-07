# -*- coding: utf-8 -*-
#Convert old coordiates to new ones after given strains 
#Writen By czf 2/26/2019 
#Only valid for con.dat in SPILADY

import os
import sys

script, file_to_be_converted = sys.argv 

print ("""
###################################
#                                 #
#  for SLD software SPILADY       #
#                                 #
###################################
""")

strain = input("""input three normal strains e_xx e_yy e_zz sequentially""")
strain_val = [float(x) for x in strain.split()]

#command = "cp " + str(file_to_be_converted) + " " + str(file_to_be_converted) + "_new"
#os.system(command)

file_name = str(file_to_be_converted) + "_new"
file_read = open(str(file_to_be_converted), 'r')
file_write = open(file_name,'w')

lines = file_read.readlines()

for i in range(0,len(lines)):         # both begin from 0
    
    if i == 1 :
        old_xx = lines[i].split()[0]   
        old_yy = lines[i].split()[2]
        xx = str(float(lines[i].split()[0])*(1 + strain_val[0]))
        yy = str(float(lines[i].split()[2])*(1 + strain_val[1]))
        lines[i] = lines[i].replace(old_xx,xx)
        lines[i] = lines[i].replace(old_yy,yy)
    
    elif i == 2 :
        old_zz = lines[i].split()[2] 
        zz = str(float(lines[i].split()[2])*(1 + strain_val[2]))
        lines[i] = lines[i].replace(old_zz,zz)
    
    elif len(lines[i].split()) >= 4:
        old_a = lines[i].split()[2]   #the true order beginning from 1.
        old_b = lines[i].split()[3]
        old_c = lines[i].split()[4]
        a = str(float(lines[i].split()[2])*(1 + strain_val[0]))
        b = str(float(lines[i].split()[3])*(1 + strain_val[1]))
        c = str(float(lines[i].split()[4])*(1 + strain_val[2]))
        lines[i] = lines[i].replace(old_a,a)
        lines[i] = lines[i].replace(old_b,b)
        lines[i] = lines[i].replace(old_c,c)
    
    file_write.write(lines[i])

print ("""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
This file has been converted with "_new" already! 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
""")

file_read.close()
file_write.close()
