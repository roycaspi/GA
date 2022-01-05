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


    def mate(self, partner):
        i, j = np.random.randint(0, self.__n, 2) #step 1:generates the range for crossover
        if i > j:
            i, j = j, i
        child1 = np.ones(len(self.__gene)) * -1
        child2 = np.ones(len(self.__gene)) * -1
        child1[i:j] = self.__gene[i:j] #step 2: copies parents' segments into children
        child2[i:j] = partner.__gene[i:j] #todo: check if reachable or need to remove '__'
        numbers_done = set(np.concatenate((child1, child2)))
        for i in range(1, len(self.__gene) + 1): #step 3: copies the numbers not in 'numbers_done' to children
            if i not in numbers_done:
                index1 = list(partner.__gene).index(i)
                child1[index1] = i
                index2 = list(self.__gene).index(i)
                child1[index2] = i
                numbers_done.add(i) #maybe a waste of memory
        for i in range(child1): #step4: fills in the rest of childrens' gene
            if child1[i] == -1:
                num_to_fill = partner.__gene[i]
                if num_to_fill not in child1:
                    child1[i] = num_to_fill
                else:
                    while (True):
                        num_to_fill = child2[list(child1).index(num_to_fill)]
                        if num_to_fill not in child1:
                            child1[i] = num_to_fill
                            break;
            if child2[i] == -1:
                num_to_fill = self.__gene[i]
                if num_to_fill not in child2:
                    child2[i] = num_to_fill
                else:
                    while (True):
                        num_to_fill = child1[list(child2).index(num_to_fill)]
                        if num_to_fill not in child2:
                            child2[i] = num_to_fill
                            break;
        return child1, child2




