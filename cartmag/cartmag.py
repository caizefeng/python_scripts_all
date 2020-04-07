# -*- coding: utf-8 -*-
# return the components of the magnetization with respect to the Cartesian lattice vectors
# run with genmag.sh
# genmag.sh needs OSZICAR and INCAR
# Written by CZF
# output file "magnetization_cartesian".
# file structure: [initial magnetic unit vector] [vector after optimization]

import os
import numpy as np
import math


def Normalize(array):
    return array / np.linalg.norm(array)


os.system('sh genmag.sh')

data = np.loadtxt('magnetization', delimiter=' ')

mag, saxis = np.split(data, 2, axis=0)
mag_car = np.zeros((20, 3))

arr_alpha = np.arctan(saxis.T[1] / (saxis.T[0] + 1e-8))
arr_beta = np.arctan(
    np.sqrt(np.square(saxis.T[0]) + np.square(saxis.T[1])) /
    (saxis.T[2] + 1e-8))

for i in range(10):
    alpha = arr_alpha[i]
    beta = arr_beta[i]
    convmat = np.array([[
        math.cos(beta) * math.cos(alpha), -math.sin(alpha),
        math.sin(beta) * math.cos(alpha)
    ],
                        [
                            math.cos(beta) * math.sin(alpha),
                            math.cos(alpha),
                            math.sin(beta) * math.sin(alpha)
                        ], [-math.sin(beta), 0,
                            math.cos(beta)]])
    mag_car[i] = Normalize(np.dot(convmat, mag[i]))  # Normalization
    mag_car[i + 10] = Normalize(saxis[i])

cartes, direct = np.vsplit(mag_car, 2)
mag_car_new = np.hstack((direct, cartes))

np.savetxt('magnetization_cartesian', mag_car_new)

print("Done!")
