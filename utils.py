import numpy as np

from Individual import *


class Destinations:

    def __init__(self, file):  # will receive an open to read file
        self.cities = [0]  # city number 1 wil be placed in index 1
        lines = file.readlines()
        for city in lines:
            row = city.split()
            self.cities.append((float(row[1]), float(row[2])))


def fitnessFunc(gene, destinations):
    dist = 0
    for i in range(len(gene) - 1):
        dist += np.sqrt((destinations.cities[gene[i + 1]][0] - destinations.cities[gene[i]][0]) ** 2
                        + (destinations.cities[gene[i + 1]][1] - destinations.cities[gene[i]][1]) ** 2)
        # sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    dist += np.sqrt((destinations.cities[gene[0]][0] - destinations.cities[gene[len(gene) - 1]][0]) ** 2
                    + (destinations.cities[gene[0]][1] - destinations.cities[gene[i]][1]) ** 2) #return to first city calculation
    return dist


if __name__ == "__main__":
    f = open("tokyo.dat")
    map = Destinations(f)
    local_state = np.random.RandomState(None)
    adam = Individual(np.random.permutation(8) + 1, 5, fitnessFunc, local_state, map)
    eve = Individual(np.random.permutation(8) + 1, 5, fitnessFunc, local_state, map)
    print(adam.orderCrossover(eve))
