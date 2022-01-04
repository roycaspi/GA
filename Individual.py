import random

class Individual:
    gene = ""
    fitness = None
    def __init__(self, n): #n = number of cities
        tempGene = random.sample(range(2, n), n - 1) #random numbers array of n - 1 cities
        gene = "1 ".join([str(x) + " " for x in tempGene]) + "1"

    def mutation(self):
        indexesToSwap = random.sample(range(2, len(self.gene) - 1), 2) #generates two random indexes to swap
        l = list(self.gene)
        l[indexesToSwap[0]], l[indexesToSwap[1]] = l[indexesToSwap[1]], l[indexesToSwap[0]]
        gene = "".join([str(x) + " " for x in l])

    def mate(self, partner):

