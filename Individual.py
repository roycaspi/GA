import random
import numpy as np

class Individual:

    def __init__(self, n, t_func):
        """
        An Individual is a permutation of the numbers 1 -150.
        :param n:       number of cities
        :param t_func:  target function to determine the fitness of the individual.
        """
        # tempGene = random.sample(range(2, n), n - 1) #random numbers array of n - 1 cities
        # self.__gene = "1".join([f' {x}' for x in tempGene])
        self.__n = n
        self.__gene = np.random.permutation(n) + 1
        self.__fitness = t_func(self.__gene)

    def mutate(self, mute_p):
        """
        A single mutation is a swap of two numbers in the permutation.
        :param mute_p: float - the probability for a mutation
        :return:
        """
        """
        indexesToSwap = random.sample(range(2, len(self.gene) - 1), 2) #generates two random indexes to swap
        l = list(self.gene)
        l[indexesToSwap[0]], l[indexesToSwap[1]] = l[indexesToSwap[1]], l[indexesToSwap[0]]
        gene = "".join([str(x) + " " for x in l])
        """
        mute_num = int(self.__n * np.random.normal(mute_p) + 1)     # the number of mutations to preform
        for __ in range(mute_num):
            i, j = np.random.randint(0, 150, 2)
            while i == j:
                i, j = np.random.randint(0, 150, 2)
            self.__gene[i], self.__gene[j] = self.__gene[j], self.__gene[i]


    # def mate(self, partner):


