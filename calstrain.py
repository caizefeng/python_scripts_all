# -*- coding: utf-8 -*-

import sys

input_dir = sys.argv[1]
input_file = input_dir + "/" + "CONTCAR"
with open(input_file, 'r') as file:

	lines = file.readlines()
	vector_x = float(lines[2].split()[0])
	vector_y = float(lines[3].split()[1])
	std = 2.83337

	strain_xx = (vector_x - std)/std * 100
	strain = (vector_x - vector_y)/std * 100

	print("exx-eyy:",format(strain, '0.3f'), "%" , '\t' , "exx:",format(strain_xx, '0.3f'),"%")

