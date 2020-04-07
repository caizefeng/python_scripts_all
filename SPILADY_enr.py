# -*- coding: utf-8 -*-
#Calculate total energy change during simulation. 
#Writen By czf 2/27/2019 
#Only compatible for enr.dat in SPILADY

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

file_name = str(file_to_be_converted) + "_totenr"
file_read = open(str(file_to_be_converted), 'r')
file_write = open(file_name,'w')

lines = file_read.readlines()

title = "step" + "\t" + "total_time(s)" + "\t" + "total_energy(eV/atom)"
file_write.write(title)              #file.write only for one arg

for i in range(0,len(lines)):         # both begin from 0
    
    energy_list = lines[i].split()
    
    step_num = lines[i].split()[0]
    total_time = lines[i].split()[1]
    del(energy_list[0])       # elements should be deleted one by one 
    del(energy_list[0])
    energy = [float(x) for x in energy_list]
    total_energy = str(sum(energy))
    str_2 = "\n" + step_num + "\t" + total_time  + "\t" + total_energy    
    file_write.write(str_2)

print ("""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
The total energy has been calculated already! 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
""")

file_read.close()
file_write.close()
