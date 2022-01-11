from Individual import *


class Population:

    def __init__(self, pop, lam, t_func, rand_state, elitism=True):
        """

        :param pop:
        :param lam:
        :param elitism:
        """
        self.__population = pop
        self.__fitnesses = np.array([ind.fitness for ind in pop])
        # self.__population = [ind.get_gene for ind in pop]
        self.__mu = len(pop)
        self.__lambda = lam
        self.__fitness_func = t_func
        self.__local_state = rand_state
        self.__elitism = elitism
        # self.__fitness_sum = sum([ind.get_fitness for ind in self.__population])

    def sexual_select(self):
        """ select an individual for recombination using roulette probabilities """
        fitness_sum = np.sum(self.__fitnesses)
        cumsum = np.cumsum(self.__fitnesses)
        probs = np.array([(cumsum[i] / fitness_sum) for i in range(self.__mu)])
        roulette = np.random.rand()         # uniform [0-1]
        for i in range(self.__mu):          # todo - binary search if needed
            if probs[i] > roulette:
                return self.__population[i]

    def generate_generation(self, mute_prob, cross_prob):
        """ returns a new generation of lambda permutations """
        new_gen = []
        for __ in range(self.__lambda // 2):
            p1, p2 = self.sexual_select(), self.sexual_select()
            if np.random.rand() < cross_prob:
                c1, c2 = p1.crossover(p2)           # todo - set crossover implementation, from main
            else:
                c1, c2 = np.copy((p1.get_gene, p2.get_gene))
            Individual.mutate(c1, self.__local_state, mute_prob)
            new_gen.append(Individual(c1, len(c1), self.__fitness_func, self.__local_state))
            Individual.mutate(c2, self.__local_state, mute_prob)
            new_gen.append(Individual(c2, len(c2), self.__fitness_func, self.__local_state))
            # ind = Individual(c1, len(c1), self.__fitness_func, self.__local_state)
        return new_gen

    def select_generation(self, new_gen):
        """ sets population for the mu best individuals """
        if self.__elitism:
            new_gen += self.__population
        next_gen = []
        fitness = []
        for i in range(len(new_gen)):
            if len(next_gen) < self.__mu:
                next_gen.append(new_gen[i])
                fitness.append(new_gen[i].fitness)
            else:
                worst = fitness.index(np.max(fitness))
                if new_gen[i].fitness < fitness[worst]:         # replace worst individual with new_gen[i]
                    next_gen[worst] = new_gen[i]
                    fitness[worst] = new_gen[i].fitness
        self.__population = next_gen
        self.__fitnesses = np.array(fitness)

    def best(self):
        best = self.__population[list(self.__fitnesses).index(np.min(self.__fitnesses))]
        return best.fitness, best.get_gene

    def print(self):
        for i in range(self.__mu):
            print(f"{i}: {self.__population[i].get_gene}")


if __name__ == "__main__":
    mu = 10
    lam = 10
    t_func = lambda x: np.sum(x)
    local_state = np.random.RandomState(None)
    inds = [Individual(np.random.permutation(10) + 1, 10, t_func, local_state) for __ in range(mu)]
    p = Population(inds, lam, t_func, local_state)
    # p.print()
    p.select_generation(p.generate_generation())
    p.print()


