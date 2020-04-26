#!/usr/bin/env python3
# coding: utf-8

import array
import math
import os
import sys
import argparse

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from tqdm import tqdm


parser = argparse.ArgumentParser(description="Argon PBC MD")
parser.add_argument("-t", "--typecal", choices=['single','multiple'], default='single', help="MD calculation type")
parser.add_argument("-T", "--Temperature", type=float, default=1.0, help="Target temperature for single calculation")
parser.add_argument("-b", "--begin", type=float, default=0.1, help="Minimum temperature for multiple calculation")
parser.add_argument("-e", "--end", type=float, default=1.0, help="Maximum temperature for multiple calculation")
parser.add_argument("-s", "--step", type=float, default=0.1, help="Temperature step for multiple calculation")
args = parser.parse_args()


def initialize(N, T, rho):
    L, R = initPositions(N, rho)
    V = initVelocities(T, R)
    return L, R, V


@njit('Tuple((float64, float64[:,:]))(uint16, float64)')
def initPositions(N, rho):
    L = (N/rho)**(1/3)
    M = math.ceil((N/4)**(1/3))
    a = L/M
    cell = np.array([[0.25, 0.25, 0.25],
                     [0.75, 0.75, 0.25],
                     [0.75, 0.25, 0.75],
                     [0.25, 0.75, 0.75]])
#     buf = array.array("d")
    R = np.zeros((N, 3))
    p = 0
    for x in range(M):
        for y in range(M):
            for z in range(M):
                for k in range(4):
                    if p < N:
                        R[p] = (np.array([x, y, z]) + cell[k, :])*a
#                         buf.append((x+cell[0, k])*a)
#                         buf.append((y+cell[1, k])*a)
#                         buf.append((z+cell[2, k])*a)
                        p += 1
#     R = np.frombuffer(buf, dtype=np.float).reshape(-1, 3)
    return L, R


@njit("float64[:,:](uint16, float64, float64[:,:])")
def rescaleVelocities(N, T, V):
    vSqdSum = np.sum(V**2)  # reshape is viewing
    lamda = math.sqrt(3 * (N-1) * T / vSqdSum)  # lambda is keyword in py
    V *= lamda
    return V


@njit("float64[:,:](float64, float64[:,:])")
def initVelocities(T, R):
    N = R.shape[0]
    V = np.random.randn(*R.shape)
#     V -= V.mean()  ## not supported by numba
    V -= V.sum()/N
    V = rescaleVelocities(N, T, V)
    return V


@njit('Tuple((float64[:,:], float64))(uint16, float64, float64[:,:])')
def computeAccelerations(N, L, R):
    poten_tot = 0
    A = np.zeros((N, 3))
    for i in range(N-1):
        for j in range(i+1, N):
            rij = R[i]-R[j]
            for k in range(3):
                if rij[k] > 0.5 * L:
                    rij[k] -= L  # PBC
                elif rij[k] < -0.5 * L:
                    rij[k] += L
            rSqd = np.sum(rij**2)
            poten_tot += 4 * (rSqd ** (-6) - rSqd ** (-3))
            f = 24 * (2 * rSqd ** (-7) - rSqd**(-4))
            A[i] += rij * f
            A[j] -= rij * f
    return A, poten_tot


@njit('Tuple((float64[:,:], float64[:,:], float64))(float64, uint16, float64, float64[:,:], float64[:,:])')
def velocityVerlet(dt, N, L, R, V):
    A = computeAccelerations(N, L, R)[0]
    R += V * dt + 0.5 * A * dt ** 2
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            if R[i, j] > L:
                R[i, j] -= L  # PBC
            elif R[i, j] < -0.5 * L:
                R[i, j] += L
#     R = np.where(R < 0, R + L, R)  # PBC
#     R = np.where(R > L, R - L, R)  # PBC
    V += 0.5 * A * dt
    A, poten_tot = computeAccelerations(N, L, R)
    V += 0.5 * A * dt
    return R, V, poten_tot


@njit("Tuple((float64, float64))(uint16, float64[:,:])")
def instantaneousTemperature(N, V):
    T_sum = np.sum(V**2)
    kne_en = T_sum / 2
    return T_sum / (3 * (N-1)), kne_en


@njit("float64(uint16, uint16, float64, float64[:,:])")
def instantaneousEnergy(particle_index, N, L, R):
    poten_sing = 0
    for i in range(N):
        if i != particle_index:
            rij = R[i] - R[particle_index]
            for k in range(3):
                if rij[k] > 0.5 * L:
                    rij[k] -= L  # PBC
                elif rij[k] < -0.5 * L:
                    rij[k] += L
            rSqd = np.sum(rij**2)
            poten_sing += 4 * (rSqd ** (-6) - rSqd ** (-3))
    return poten_sing


@njit('uint16[:,:](uint16)')
def crossindex(N):
    index_array = np.empty((N, N-1), dtype=np.uint16)
    all_index = list(range(N))
    for i in range(N):
        for j, num in enumerate(all_index[:i] + all_index[i+1:]):
            index_array[i, j] = num
    return index_array


@njit('float64(float64[:,:])')
def min_mean(array):
    N = array.shape[0]
    result = 0
    for i in range(N):
        result += np.min(array[i,:])
    return result/N


@njit("float64(uint16, float64, float64[:,:])")
def instantaneousDistance(N, L, R):
    index_array = crossindex(N)
    cross_distance = np.zeros((N, N-1))
    for i in range(N):
        for j in range(N-1):
            rij = R[i]-R[index_array[i, j]]
            for k in range(3):
                if rij[k] > 0.5 * L:
                    rij[k] -= L  # PBC
                elif rij[k] < -0.5 * L:
                    rij[k] += L
            r = np.sqrt(np.sum(rij**2))
            cross_distance[i, j] = r
    dist_mean =  min_mean(cross_distance)
    return dist_mean


def plot_gen(T):
    plt.title("Instantaneous Temperature")
    plt.xlabel("step")
    plt.ylabel("temperature")
    y = np.loadtxt('T_2.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('2_temp_{}.png'.format(T), dpi=300)
    plt.close()

    plt.title("Potential Energy of A single Particle")
    plt.xlabel("step")
    plt.ylabel("potential energy")
    y = np.loadtxt('poten_sing_2.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('2_poten_sing_{}.png'.format(T), dpi=300)
    plt.close()

    plt.title("Total Potential Energy")
    plt.xlabel("step")
    plt.ylabel("potential energy")
    y = np.loadtxt('poten_tot_2.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('2_poten_tot_{}.png'.format(T), dpi=300)
    plt.close()

    plt.title("Total Energy")
    plt.xlabel("step")
    plt.ylabel("total energy")
    y = np.loadtxt('en_tot_2.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('2_en_tot_{}.png'.format(T), dpi=300)
    plt.close()
    
    plt.title("Mean Distance between Adjacent Particles")
    plt.xlabel("step")
    plt.ylabel("distance")
    y = np.loadtxt('dist_mean_2.data')
    plt.xlim((0, 1000))
    plt.xticks(np.arange(0, 1100, 100))
    plt.plot(np.arange(1000), y)
    plt.savefig('2_dist_mean_{}.png'.format(T), dpi=300)
    plt.close()


def main(T=1.0, iter_T=False):
    if not iter_T:
        dir_name = 'md2_{}'.format(T)
        os.makedirs(dir_name, exist_ok=True)
        os.chdir(dir_name)
    N = 64
    rho = 1.0
    dt = 0.01
    L, R, V = initialize(N, T, rho)
    particle_index = 32
    if not iter_T:
        with open("T_2.data", 'w') as f_t, \
                open('poten_sing_2.data', 'w') as f_s, \
                open('poten_tot_2.data', 'w') as f_p, \
                open('dist_mean_2.data', 'w') as f_d, \
                open('en_tot_2.data', 'w') as f_a:
            for i in tqdm(range(1000)):
                R, V, poten_tot = velocityVerlet(dt, N, L, R, V)
                T_ins, kne_en = instantaneousTemperature(N, V)
                poten_sing = instantaneousEnergy(particle_index, N, L, R)
                dist_mean = instantaneousDistance(N, L, R)
                f_t.write(str(T_ins) + '\n')
                f_s.write(str(poten_sing) + '\n')
                f_p.write(str(poten_tot) + '\n')
                f_d.write(str(dist_mean) + '\n')
                f_a.write(str(poten_tot + kne_en) + '\n')
                
                if (i % 200 == 0):
                    V = rescaleVelocities(N, T, V)
                if i == 999:
                    last_step = [poten_sing, poten_tot,
                             poten_tot + kne_en, dist_mean]
        plot_gen(T)
        os.chdir(sys.path[0])

    elif iter_T:
        for i in range(1000):
            R, V, poten_tot = velocityVerlet(dt, N, L, R, V)
            T_ins, kne_en = instantaneousTemperature(N, V)
            poten_sing = instantaneousEnergy(particle_index, N, L, R)
            dist_mean = instantaneousDistance(N, L, R)
            if (i % 200 == 0):
                V = rescaleVelocities(N, T, V)
            if i == 999:
                last_step = [poten_sing, poten_tot,
                             poten_tot + kne_en, dist_mean]
    return last_step


def iter_T(list_T=[0.1*(i+1) for i in range(10)]):
    dir_name = 'md2_iter_{0}_{1}'.format(list_T[0], list_T[-1])
    os.makedirs(dir_name, exist_ok=True)
    os.chdir(dir_name)
    list_singpen = []
    list_totpen = []
    list_toten = []
    list_dist = []
    for T in tqdm(list_T):
        last_step = main(T, iter_T=True)
        list_singpen.append(last_step[0])
        list_totpen.append(last_step[1])
        list_toten.append(last_step[2])
        list_dist.append(last_step[3])
    plot_gen_iter(list_T, list_singpen, list_totpen, list_toten, 
                  list_dist)
    os.chdir(sys.path[0])


def plot_gen_iter(list_T, list_singpen, list_totpen, list_toten,
                  list_dist):
    array_T = np.array(list_T)

    plt.title("Potential Energy of A single Particle")
    plt.xlabel("temperature")
    plt.ylabel("potential energy")
    plt.plot(array_T, np.array(list_singpen))
    plt.savefig('2_poten_sing.png', dpi=300)
    plt.close()

    plt.title("Total Potential Energy")
    plt.xlabel("temperature")
    plt.ylabel("potential energy")
    plt.plot(array_T, np.array(list_totpen))
    plt.savefig('2_poten_tot.png', dpi=300)
    plt.close()

    plt.title("Total Energy")
    plt.xlabel("temperature")
    plt.ylabel("total energy")
    plt.plot(array_T, np.array(list_toten))
    plt.savefig('2_en_tot.png', dpi=300)
    plt.close()
    
    plt.title("Mean Distance between Adjacent Particles")
    plt.xlabel("temperature")
    plt.ylabel("distance")
    plt.plot(array_T, np.array(list_dist))
    plt.savefig('2_dist_mean.png', dpi=300)
    plt.close()
    

os.chdir(sys.path[0])
if args.typecal == 'single':
    main(args.Temperature)
elif args.typecal == 'multiple':
    list_T = np.arange(args.begin, args.end + args.step, args.step).tolist()
    iter_T(list_T)
else:
    print("only two types of calculation 'single' and 'multi' available now")





