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
            Vect_V[i, j] = r.uniform(min, max)
    return Vect_V

# This function initializes all of the variables used during the
# optimization using the PSO algorithm. I borrowed some of it from Jehro.
def main():
    C1 = 2.05
    C2 = 2.05
    W = 0.8
    NP = 100

    # Automate the running Dimensions
    D_array = [2, 5, 10]
    F_array = [HC, BC, Ackley, Discus, Griewank, Katsuura, Rastrigin, Rosenbrock, Weierstrass]
    F_name = ['HC', 'BC', 'Ackleys', 'Discus', 'Griewank', 'Katsuura', 'Rastrigin', 'Rosenbrock', 'Weierstrass']

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
            print ('Running %s dimension:', D, '__Function: ', FunctionName)
            done += PSO(C1, C2, W, D, Max_NFC, NP, funct, FunctionName, NP)
            print ('Finished %s______________', FunctionName)

# EZ MODE.
def PSO(C1, C2, W, D, Max_NFC, NP, fx, fxName, save_freq):
    # Creates an array to hold the current generation and all of their dirty secrets.
    # Each individual (columns) consists of [position][prevVector][personalBest]. Each [set] is size D.
    gen = pop(-10, 10, NP, 3*D)
    popBest = np.array(D)
    popBestFit = 10000
    plot_data = []

    # Literally loops here 3000*D times. weird huh? My processor probably hates me.
    for calls in range(0, Max_NFC + 1):
        for individual in range(0, NP - 1):
            fitness = fx(gen[individual])
            if fitness < popBestFit:
                popBestFit = fitness
                for elem in range(0, D - 1):
                    popBest = gen[individual][elem]
            '''
                This entire section is used for stopping the algorithm early if the optimal solution has been found.
                if popBestFit == 0:
                popBest = gen[individual]
                data = "%s , %s" % (calls, popBestFit)
                # print (data)
                plot_data.append(data)
                print ('RUN:____', calls)
                ofile = open(fxName, "wb")
                writer = csv.writer(ofile, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerow(plot_data, fxName, calls, D)
                print ('file___done...............')
                return 1 
            '''

            # Create arrays for the complex portions of the expression.
            randV1 = np.random.rand(D)
            randV2 = np.random.rand(D)
            position = np.array(D)
            prevVec = np.array(D)
            personalBest = np.array(D)

            # Iterate through the individual and assign the values
            # To the corresponding array.
            for elem in range(0, D-1):
                position = gen[individual][elem]
                prevVec = gen[individual][elem + D]
                personalBest = gen[individual][elem + (2*D)]

            #Surprisingly easy to code vector.
            Vector = W * prevVec + randV1 * C1 * (personalBest - position) + randV2 * C2 * (popBest - position)

            # Update the position of the particle.
            for elem in range(0, D-1):
                gen[individual][elem] += Vector[elem]
                gen[individual][elem + D] = Vector[elem]


        # Save the Best... dunno what info we need. Made assumption.
        if (calls % save_freq == 0):
            data = calls, popBestFit, D, fxName
            # print (data)
            plot_data.append(data)

    # I have no idea what format your want to save the thing as.
    print ('RUN:____', calls)
    ofile = open(fxName +".csv", "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='/')
    for i in range (0, 30*D - 1):
        writer.writerow(plot_data[i])
    print ('file___done...............')
    return 1

# The Beginning
main()
# The End