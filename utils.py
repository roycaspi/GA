import numpy as np

import Individual

class Destinations:
    cities = [] #will hold all the cities' coordinates

    def __init__(self, file): #will receive an open to read file
        i = 0
        lines = file.readlines()
        for city in lines:
            row = city.split()
            self.cities[i] = (int(row[1]), int(row[2]))
            i += 1

def fitnessFunc(individual, destinations):
    route = individual.gene.split()
    dist = 0
    for i in range(route - 1):
        dist += np.sqrt((destinations.cities[int(route[i + 1])](0) - destinations.cities[int(route[i])](0)) ** 2
                        + (destinations.cities[int(route[i + 1])](1) - destinations.cities[int(route[i])](1)) ** 2)
        # sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist
