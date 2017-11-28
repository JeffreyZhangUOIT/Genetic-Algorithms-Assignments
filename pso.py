import numpy as np
import random as r
import csv

from numba import jit
from numpy import arange

# The following is a parody of PSO + Jehro's work with math functions and plot output.
# Please support the official release!

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
   # product *= np.pow(1 + ((i + 1) * summation), 10 / np.pow(len(x), 1.2))
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
           Vect_V[i, j] = round(r.uniform(min, max), 7)
   return Vect_V

# This function initializes all of the variables used during the
# optimization using the PSO algorithm. I borrowed some of it from Jehro.
def main():
   C1 = 2.05
   C2 = 2.05
   W = 0.9
   NP = 100

   # Automate the running Dimensions
   D_array = [2, 5, 10]
   F_array = [HC, BC, Ackley, Discus, Griewank, Katsuura, Rastrigin, Rosenbrock, Weierstrass]
   F_name = ['HC', 'BC', 'Ackley', 'Discus', 'Griewank', 'Katsuura', 'Rastrigin', 'Rosenbrock', 'Weierstrass']

   # Line 155: done += PSO(C1, C2, W, D, Max_NFC, NP, funct, FunctionName, NP)
   # I do not own the following 12 lines of code, with the exception of line 155
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
           while(run < 51):
               print "Run:", run
               PSO(C1, C2, W, D, Max_NFC, NP, funct, FunctionName, writer)
               run += 1
           print 'Finished function:', FunctionName, ' on dimension: ', D
           done += 1

# EZ MODE.
def PSO(C1, C2, W, D, Max_NFC, NP, fx, fxName, writer):
   # Creates an array to hold the current generation and all of their dirty secrets.
   # Each individual (columns) consists of [position][prevVector][personalBest]. Each [set] is size D.
   gen = pop(-10, 10, NP, 3*D)
   popBest = np.random.rand(D)
   popBestFit = 99999
   plot_data = []
   step = (0.9-0.4) / (3000*D)

   # Literally loops here 3000*D times. weird huh? My processor probably hates me.
   for calls in range(Max_NFC+1):
       W = W - step
       for individual in range(0, NP):
           # Create arrays for the complex portions of the expression.
           randV1 = np.random.rand(D)
           randV2 = np.random.rand(D)
           position = np.zeros(D)
           prevVec = np.zeros(D)
           personalBest = np.zeros(D)

           # Iterate through the individual and assign the values
           # To the corresponding array.
           for elem in range(0, D):
               position[elem] = gen[individual][elem]
               prevVec[elem] = gen[individual][elem + D]
               personalBest[elem] = gen[individual][elem + (2*D)]

           #Surprisingly easy to code vector.
           Vector = (W * prevVec) + (randV1 * C1 * (personalBest - position)) + (randV2 * C2 * (popBest - position))

           # Update the position of the particle.
           for elem in range(0, D):
               gen[individual][elem] += Vector[elem]
               gen[individual][elem + D] = Vector[elem]

           fitness = fx(position)
           if (fx(personalBest) > fitness):
               for elem in range(0, D):
                   gen[individual][elem+ 2*D] = gen[individual][elem]

           if fitness < popBestFit:
               popBestFit = fitness
               for elem in range(0, D):
                   popBest[elem] = position[elem]


       # Save the Best... dunno what info we need. Made assumption.
       if ((calls % NP) == 0):
           data = calls/NP, popBestFit, popBest, D, fxName
           writer.writerow(data)

   return 1

# The Beginning
main()
# The End


