import numpy as np
import Individual

class Population:

    def __init__(self, pop, lam, elitism=True, seed=None):
        """

        :param pop:
        :param lam:
        :param elitism:
        """
        self.__population = pop
        # self.__population = [ind.get_gene for ind in pop]
        self.__mu = len(pop)
        self.__lambda = lam
        self.__elitism = elitism
        self.__local_state = np.random.RandomState(seed)
        self.__fitness_sum = None
        self.set_roulette_ratios()

    def set_roulette_ratios(self):
        self.__fitness_sum = sum([ind.get_fitness for ind in self.__population])

    def sexual_select(self):
        max = self.__population[0]
        for individual in self.__population:
            if self.__local_state.uniform() < individual.get_fitness() / self.__fitness_sum:
                return individual
            if individual.get_fitness() > max.get_fitness():
                max = individual
        return max

    def generate_generation(self):
        new_gen = []
        for __ in range(self.__lambda // 2):
            p1, p2 = self.sexual_select(), self.sexual_select()
            c1, c2 = p1.crossover(p2)
            ind = Individual(c1, )


