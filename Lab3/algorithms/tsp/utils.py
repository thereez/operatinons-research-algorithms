import re
import numpy as np


# a280, ch150, fl417
def parse_euc_file(filename):
    with open(filename, 'r') as file:
        cities = [] 
        for line in file:
            line = line.split()
            if not line[0].isdigit():
                continue
            x = float(line[1])
            y = float(line[2])
            cities.append((x, y))

        N = len(cities)
        distances = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == j:
                    distances[i, j] = np.inf
                else:
                    distances[i, j] = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
        return distances


def pseudo_euclidean_distance(city1, city2):
    xd = city1[0] - city2[0]
    yd = city1[1] - city2[1]
    rij = np.sqrt((xd*xd + yd*yd) / 10)
    tij = int(rij + 0.5)
    if tij < rij:
        return tij + 1
    return tij
 
# att48
def parse_att_file(filename):
    with open(filename, 'r') as file:
        cities = [] 
        for line in file:
            line = line.split()
            if not line[0].isdigit():
                continue
            x = float(line[1])
            y = float(line[2])
            cities.append((x, y))

        N = len(cities)
        distances = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == j:
                    distances[i, j] = np.inf
                else:
                    distances[i, j] = pseudo_euclidean_distance(cities[i], cities[j])
        return distances

# bays29, gr17
def parse_matrix_file(filename, dimension):
    with open(filename, 'r') as file:
        start = 0
        distances = np.zeros((dimension, dimension))
        for line in file:
            if start == dimension:
                break
            line = line.split()
            if not line[0].isdigit():
                continue
            values = np.array([float(v) for v in line])
            distances[start, :] = values
            start += 1
        return distances


def get_distances(filename):
    if filename in ('bays29', 'gr17'):
        dimension = int(re.findall('[0-9]+', filename)[0])
        return parse_matrix_file('data/' + filename + '.tsp', dimension)
    if filename == 'att48':
        return parse_att_file('data/' + filename + '.tsp')
    if filename in ('a280', 'ch150', 'fl417'):
        return parse_euc_file('data/' + filename + '.tsp')
