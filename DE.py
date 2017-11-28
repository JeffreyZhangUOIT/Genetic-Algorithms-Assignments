'''
Differential Evolution Implementation
'''
 
from __future__ import division
from numpy import  *
 
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import math
import csv
 
from numba import jit
from numpy import arange
 
# High Conditioned Function
@jit(nopython=True)
def HC(x):
	sum = 0.0
	for i in range(1, len(x) + 1):
    	sum += (10 ** 6) ** ((i - 1) / (len(x) - 1)) * x[i - 1] ** 2
	return sum
 
 
# Bent Cigar
@jit(nopython=True)
def BC(x):
	sum = 0.0
	sum += x[0] ** 2
	for i in range(2, len(x) + 1):
    	sum += x[i - 1] ** 2
	sum *= 10
	return sum
 
 
# Ackley
@jit(nopython=True)
def Ackley(x):
	sum = 0.0
	sumSquare = 0.0
	sumCos = 0.0
	for i in range(len(x)):
    	sumSquare += x[i] * x[i]
    	sumCos += np.cos(2 * np.pi * x[i])
	sum = -20.0 * np.exp(-0.2 * np.sqrt(sumSquare / len(x))) - np.exp(sumCos / len(x)) + 20 + np.e
	return sum
 
 
# Disucs
@jit(nopython=True)
def Discus(x):
	sum = 0.0
	for i in range(1, len(x)):
    	sum += x[i] ** 2
	sum += 1e6 * x[i] ** 2
	return sum
 
 
# Griewank
@jit(nopython=True)
def Griewank(x):
	sum = 1.0
	innerSum = 0.0
	innerProduct = 1.0
	for i in range(len(x)):
    	innerSum += x[i] ** 2
    	innerProduct *= np.cos(x[i] / np.sqrt(i + 1))
	sum += innerSum * (1.0 / 4000.0) - innerProduct
	return sum
 
 
# Katsurra
@jit(nopython=True)
def Katsuura(x):
	sum = 0.0
	product = 1.0
	for i in range(len(x)):
        summation = 0
    	for j in range(1, 32):
        	term = 2 ** j * x[i]
        	summation += np.fabs(term - round(term)) / (2 ** j)
    	#product *= np.pow(1 + ((i + 1) * summation), 10 / np.pow(len(x), 1.2))
    	product *= (1 + ((i + 1) * summation) ** (10 / (len(x) ** 1.2)))
	sum = (10.0 / len(x) * len(x)) * product - (10.0 / len(x) * len(x))
	return sum
 
 
# Rastrigin
@jit(nopython=True)
def Rastrigin(x):
	sum = 0.0
	for i in range(len(x)):
    	sum += x[i] ** 2 - (10.0 * np.cos(2 * np.pi * x[i]))
	sum += 10 * len(x)
	return sum
 
 
# Rosenbrock
@jit(nopython=True)
def Rosenbrock(x):
	sum = 0.0
	for i in range(len(x) - 1):
    	sum += ((100 * (x[i + 1] - x[i] ** 2) * (x[i + 1] - x[i] ** 2)) + ((x[i] - 1.0) * (x[i] - 1.0)));
	return sum
 
 
# Weisertrass
@jit(nopython=True)
def Weierstrass(x):
	a = 0.5
	b = 3
	k_max = 20
 
	sum = 0
	for i in range(len(x)):
    	for k in range(k_max):
        	sum += a ** k * np.cos(2 * np.pi * b ** k * (x[i] + 0.5))
 
	constant = 0
	for k in range(k_max):
    	constant += a ** k * np.cos(2 * np.pi * b ** k * 0.5)
	sum -= len(x) * constant
	return sum
 
# End of function list
@jit(nopython=True)
def pop(min, max, Np, D):
   # Population Generation
   Vect_V = np.zeros((Np, D))
   for i in range(Np):
   	for j in range(D):
       	Vect_V[i, j] = round(rand.uniform(min, max), 7)
   return Vect_V
 
def main():
	NP = 100
	Cr = 0.9
	F = 0.8
 
	# Automate the running Dimensions
	D_array = [2, 5, 10]
	F_array = [HC, BC, Ackley, Discus, Griewank, Katsuura, Rastrigin, Rosenbrock, Weierstrass]
	F_name = ['HC', 'BC', 'Ackleys', 'Discus', 'Griewank', 'Katsuura', 'Rastrigin', 'Rosenbrock', 'Weierstrass']
 
	for function in range(len(F_array)):
    	# Plot function
    	funct = F_array[function]
    	# Plot function name
    	FunctionName = F_name[function]
    	done = 0  # reset the function completion
    	while (done < 3):
        	D = D_array[done]
        	Max_NFC = 3000 * D
        	run = 0
        	print 'Running function:', FunctionName, 'on dimension:', D
 	       ofile = open(FunctionName + str(D) + ".csv", "wb")
        	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='/')
        	while (run < 51):
            	print "Run:", run
            	DE(Cr, F, D, Max_NFC, NP, funct, FunctionName, writer)
            	run += 1
        	print 'Finished function:', FunctionName, ' on dimension: ', D
        	done += 1
 
 
@jit(nopython=True)
def Mutate(Vect_V, F, Np, D):
	# Mutation
	Vect_U = zeros((Np, D))
 
	for i in range(Np):
    	# picking a random point from pop
    	Xa = i
    	while (Xa == i):
        	Xa = rand.randint(0, Np - 1)
 
    	Xb = Xa
    	while (Xb == i or Xb == Xa):
        	Xb = rand.randint(0, Np - 1)
 
    	Xc = Xb
    	while (Xc == i or Xc == Xa or Xc == Xb):
        	Xc = rand.randint(0, Np - 1)
 
    	# Mutation Vi = Xa + F * (Xb - Xc)
    	for j in range(D):
        	Vect_U[i, j] = Vect_V[Xa, j] + F * (Vect_V[Xb, j] - Vect_V[Xc, j])
 
	return Vect_U
 
 
@jit(nopython=True)
def Crossover(Vect_V, Vect_U, Cr, Np, D):
	# Crossover
	Vect_Xi = zeros((Np, D))
	for i in range(Np):
    	for j in range(D):
        	if (rand.random() < Cr):
            	Vect_Xi[i, j] = Vect_U[i, j]
        	else:
            	Vect_Xi[i, j] = Vect_V[i, j]
	return Vect_Xi
 
 
def Selection(Vect_V, Vect_Xi, Vect_X, Np, D, fx):
	# Selection
	tempVectorX = zeros((Np, 1))
	for i in range(Np):
    	# get cross over points from function
    	tempVectorX[i, 0] = fx(Vect_Xi[i])
 
    	if (tempVectorX[i, 0] < Vect_X[i, 0]):
        	for j in range(D):
            	Vect_V[i, j] = Vect_Xi[i, j]
            	Vect_X[i, 0] = tempVectorX[i, 0]
	return Vect_V, Vect_X
 
 
def BestFitness(Vect_X, popBest, Np):
	# Best Fitness
	tmp = 0
	for i in range(1, Np):
    	if (Vect_X[tmp] > Vect_X[i]):
        	tmp = i
        	for elem in range(0, Np):
            	popBest[elem] = Vect_X[elem]
	return Vect_X[tmp][0], popBest
 
 
def VectX(Np, Vect_V, fx):
	# VectorX
	Vect_X = zeros((Np, 1))
	for i in range(Np):
    	Vect_X[i, 0] = fx(Vect_V[i])
	return Vect_X
 
def DE(Cr, F, D, Max_NFC, NP, fx, fxName, writer):
   Vect_V = pop(-10, 10, NP, D)
   popBest = np.random.rand(D)

 
   for calls in range(Max_NFC + 1):
   	# Perform the Mutation
   	Vect_U = Mutate(Vect_V, F, NP, D)
 
   	# Perform the Crossover
   	Vect_Xi = Crossover(Vect_V, Vect_U, Cr, NP, D)
 
   	# temporary VectX
   	Vect_X = VectX(NP, Vect_V, fx)
 
   	# Perform the Best Selection
   	Vect_V, Vect_X = Selection(Vect_V, Vect_Xi, Vect_X, NP, D, fx)
 
   	# Save BestFitness
   	BestFit, popBest = BestFitness(Vect_X, popBest, D)
 
   	if ((calls % NP) == 0):
       	data = calls / NP, BestFit, popBest, D, fxName
       	writer.writerow(data)
 
   return 1
 
 
# The Beginning
main()
# The EndT
