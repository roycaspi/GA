import numpy as np


class Individual:

    def __init__(self, permutation, n, t_func, rand_state):
        """
        An Individual is a permutation of the numbers 1 -150.
        :param n:       number of cities
        :param t_func:  target function to determine the fitness of the individual.
        """
        # tempGene = random.sample(range(2, n), n - 1) #random numbers array of n - 1 cities
        # self.__gene = "1".join([f' {x}' for x in tempGene])
        self.__n = n
        # self.__map = map
        self.__gene = permutation
        self.__fitness = t_func(self.__gene)
        self.__local_state = rand_state

    @staticmethod
    def mutate(permutation, rand_state, mute_p=-1):
        """
        A single mutation is a swap of two numbers in the permutation. A mutation occurs before an Individual
        is initialized, therefore the function is static.
        :param permutation:
        :param rand_state:
        :param mute_p: float - the probability for a mutation
        :return:
        """
        if mute_p == -1:
            mute_num = 1
        else:
            mute_num = int(len(permutation) * rand_state.normal(mute_p) + 1)  # the number of mutations to preform
        for __ in range(mute_num):
            i, j = rand_state.randint(0, len(permutation), 2)
            while i == j:
                i, j = rand_state.randint(0, len(permutation), 2)
            permutation[i], permutation[j] = permutation[j], permutation[i]

    def mappedCrossover(self, partner):
        lb, ub = self.__local_state.randint(0, self.__n, 2)  # step 1:generates the range for crossover
        while lb == ub:
            lb, ub = self.__local_state.randint(0, self.__n, 2)
        if lb > ub:
            lb, ub = ub, lb
        # todo think if the size of the crossover ( j - i ) is important - maybe we need to limit it
        child1 = np.ones(len(self.__gene), dtype=int) * -1  # -1 is a dummy value
        child2 = np.ones(len(self.__gene), dtype=int) * -1
        child1[lb:ub] = self.__gene[lb:ub]  # step 2: copies parents' segments into children
        child2[lb:ub] = partner.__gene[lb:ub]
        midds = [list(self.__gene[lb:ub]), list(partner.__gene[lb:ub])]
        # print(lb, ub)
        # step 3 + 4
        for i in list(range(lb)) + list(range(ub, self.__n)):
            if self.__gene[i] not in midds[1]:
                child2[i] = self.__gene[i]
            else:
                num_to_fill = midds[0][midds[1].index(self.__gene[i])]  # the parallel letter in self.__gene
                while num_to_fill in midds[1]:
                    num_to_fill = midds[0][midds[1].index(num_to_fill)]
                child2[i] = num_to_fill
            if partner.__gene[i] not in midds[0]:
                child1[i] = partner.__gene[i]
            else:
                num_to_fill = midds[1][midds[0].index(partner.__gene[i])]  # the parallel letter in self.__gene
                while num_to_fill in midds[0]:
                    num_to_fill = midds[1][midds[0].index(num_to_fill)]
                child1[i] = num_to_fill
        return child1, child2

    def orderCrossover(self, partner):
        lb, ub = self.__local_state.randint(0, self.__n, 2)  # step 1:generates the range for crossover
        while lb == ub:
            lb, ub = self.__local_state.randint(0, self.__n, 2)
        if lb > ub:
            lb, ub = ub, lb
        print(lb, ub)
        # todo think if the size of the crossover ( j - i ) is important - maybe we need to limit it
        child1 = np.ones(len(self.__gene), dtype=int) * -1  # -1 is a dummy value
        child2 = np.ones(len(self.__gene), dtype=int) * -1
        child1[lb:ub] = self.__gene[lb:ub]  # step 2: copies parents' segments into children
        child2[lb:ub] = partner.__gene[lb:ub]
        child1Seg = []
        child2Seg = []
        j = ub
        for i in range(len(self.__gene)): #step 3: gets the genes from the dominant parent
            if partner.__gene[j] not in child1:
                child1Seg.append(partner.__gene[j])
            if self.__gene[j] not in child2:
                child2Seg.append((self.__gene[j]))
            j += 1
            if j == len(self.__gene):
                j = 0
        j = ub
        for i in range(len(child1Seg)): #finalizes the gene
            child1[j] = child1Seg[i]
            child2[j] = child2Seg[i]
            j += 1
            if j == len(self.__gene):
                j = 0
        print(self.__gene, partner.__gene)
        return child1, child2

    def crossover(self, partner, imp=0):
        if imp == 0:
            return self.mappedCrossover(partner)
        if imp == 1:
            return self.orderCrossover(partner)

    @property
    def get_gene(self):
        return self.__gene

    @property
    def fitness(self):
        return self.__fitness


if __name__ == "__main__":
    x = Individual(np.array([2, 5, 3, 6, 0, 1, 4]) + 1, 7, lambda x: sum(x), np.random.RandomState(None))
    y = Individual(np.array([5, 6, 0, 1, 2, 3, 4]) + 1, 7, lambda x: sum(x), np.random.RandomState(None))
    print("am i here?")
    print(x.fitness)
    print(type(x.fitness))
    print(x.orderCrossover(y))
