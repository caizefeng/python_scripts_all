#!/usr/bin/env python3
# coding: utf-8

import math
import os
import sys
import argparse

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import *
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Argon MD")
parser.add_argument("-v", "--vmax", default=0.1, type=float, help="Maximum velocity component at initialization")
args = parser.parse_args()

N = 64
R = np.zeros((N, 3))
V = np.zeros((N, 3))
A = np.zeros((N, 3))
L = 10
vMax = args.vmax
dt = 0.01
particle_index = 32


def initialize():
    global R
    global V
    n = math.ceil(N**(1/3))
    a = L/n
    p = 0
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if p < N:
                    R[p] = (np.array([x, y, z]) + 0.5) * a
                    p += 1
    V = vMax*(2 * np.random.random(V.shape) - 1)


def computeAccelerations():
    global A
    A = np.zeros((N, 3))
    for i in range(N-1):
        for j in range(i+1, N):
            rij = R[i]-R[j]
            rSqd = np.sum(rij**2)
            f = 24 * (2 * rSqd ** (-7) - rSqd**(-4))
            A[i] += rij * f
            A[j] -= rij * f


def velocityVerlet(dt):
    global R
    global V
    computeAccelerations()
    R += V * dt + 0.5 * A * dt ** 2
    V += 0.5 * A * dt
    computeAccelerations()
    V += 0.5 * A * dt


def instantaneousTemperature():
    T_sum = np.sum((V**2).reshape((1, -1)))
    kne_en = T_sum / 2
    return T_sum / (3 * (N-1)), kne_en


def instantaneousProperty(particle_index):
    Distance = pdist(R, 'euclidean')
    Potential = 4 * (Distance ** (-12) - Distance**(-6))
    single_Distance = cdist(np.array([R[particle_index]]),
                            np.delete(R, particle_index, 0), 'euclidean')
    single_Potential = 4 * (single_Distance ** (-12) - single_Distance**(-6))
    poten_sing = np.sum(single_Potential)
    poten_tot = np.sum(Potential)

    all_single_Distance = cdist(R, R, 'euclidean')
    dist_mean = np.sort(all_single_Distance)[-2].mean()  # smallest distance
    return poten_sing, poten_tot, dist_mean


def plot_gen():
    plt.title("Instantaneous Temperature")
    plt.xlabel("step")
    plt.ylabel("temperature")
    y = np.loadtxt('T.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('1_temp_{}.png'.format(vMax), dpi=300)
    plt.close()

    plt.title("Potential Energy of A single Particle")
    plt.xlabel("step")
    plt.ylabel("potential energy")
    y = np.loadtxt('poten_sing.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('1_poten_sing_{}.png'.format(vMax), dpi=300)
    plt.close()

    plt.title("Total Potential Energy")
    plt.xlabel("step")
    plt.ylabel("potential energy")
    y = np.loadtxt('poten_tot.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('1_poten_tot_{}.png'.format(vMax), dpi=300)
    plt.close()

    plt.title("Total Energy")
    plt.xlabel("step")
    plt.ylabel("total energy")
    y = np.loadtxt('en_tot.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('1_en_tot_{}.png'.format(vMax), dpi=300)
    plt.show()
    plt.close()
    
    plt.title("Mean Distance between Adjacent Particles")
    plt.xlabel("step")
    plt.ylabel("distance")
    y = np.loadtxt('dist_mean.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('1_dist_mean_{}.png'.format(vMax), dpi=300)
    plt.close()

def main():
    dir_name = 'md1_{}'.format(vMax)
    os.makedirs(dir_name, exist_ok=True)
    os.chdir(dir_name)
    initialize()
    with open("T.data", 'w') as f_t, open('poten_sing.data', 'w') as f_s, open('poten_tot.data', 'w') as f_p,  open('dist_mean.data', 'w') as f_d, open('en_tot.data', 'w') as f_a:
        for i in tqdm(range(1000)):
            velocityVerlet(dt)
            T, kne_en = instantaneousTemperature()
            poten_sing, poten_tot, dist_mean = instantaneousProperty(particle_index)
            f_t.write(str(T) + '\n')
            f_s.write(str(poten_sing) + '\n')
            f_p.write(str(poten_tot) + '\n')
            f_d.write(str(dist_mean) + '\n')
            f_a.write(str(poten_tot + kne_en) + '\n')
    plot_gen()
    os.chdir(sys.path[0])


if __name__ == '__main__':
    main()





