# -*- coding: utf-8 -*-
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('con_dir')
args = parser.parse_args()
N = 800                            # atom number         
d = 2.82987/2                      # 1/2 * lattice parameter

con_list = list()
for root, dirs, files in os.walk(args.con_dir):
    for file in files:
        if (os.path.splitext(file)[1] == '.dat') and ('con' in os.path.splitext(file)[0]):
            con_list.append(os.path.join(root, file))
con_list.sort()
con_list.pop()

for i in range(len(con_list)):
    con_read = open(con_list[i], 'r')
    atom = [[] for j in range(N)]
    for j in range(3):
        line = con_read.readline()
    for j in range(N):
        line = con_read.readline()
        temp = line.split()
        atom[j] = list(map(float, temp[2:5]))
    con_read.close()
    x = sorted(atom, key=lambda a: a[0])
    y = sorted(atom, key=lambda a: a[1])
    z = sorted(atom, key=lambda a: a[2])
    
    con_write = open('dump_'+str(i)+'.atom', 'w')
    con_write.write('ITEM: TIMESTEP\n')
    con_write.write('%i\n' %i)
    con_write.write('ITEM: NUMBER OF ATOMS\n')
    con_write.write('%i\n' %N)
    con_write.write('ITEM: BOX BOUNDS pp pp pp\n')
    con_write.write('%e %e\n' %(x[0][0], x[N-1][0]+d))
    con_write.write('%e %e\n' %(y[0][1], y[N-1][1]+d))
    con_write.write('%e %e\n' %(z[0][2], z[N-1][2]+d))
    con_write.write('ITEM: ATOMS id type x y z\n')
    for j in range(N):
        con_write.write('%i 1 %e %e %e\n' %(j+1, atom[j][0], atom[j][1], atom[j][2]))
    con_write.close()
