import numpy as np

from Population import *


class Destinations:

    def __init__(self, file):  # will receive an open to read file
        self.cities = [0]  # city number 1 wil be placed in index 1
        lines = file.readlines()
        for city in lines:
            row = city.split()
            self.cities.append((float(row[1]), float(row[2])))

    def fitnessFunc(self, gene):
        dist = 0
        for i in range(len(gene) - 1):
            dist += np.sqrt((self.cities[gene[i + 1]][0] - self.cities[gene[i]][0]) ** 2
                            + (self.cities[gene[i + 1]][1] - self.cities[gene[i]][1]) ** 2)
            # sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        dist += np.sqrt((self.cities[gene[0]][0] - self.cities[gene[len(gene) - 1]][0]) ** 2
                        + (self.cities[gene[0]][1] - self.cities[gene[len(gene) - 1]][1]) ** 2)
        # return to first city calculation
        return dist


if __name__ == "__main__":
    f = open("tokyo.dat")
    d = Destinations(f)
    local_state = np.random.RandomState(None)
    adam = Individual(np.random.permutation(8) + 1, 5, d.fitnessFunc, local_state)
    eve = Individual(np.random.permutation(8) + 1, 5, d.fitnessFunc, local_state)
    print(adam.orderCrossover(eve))
    print(adam.fitness)
