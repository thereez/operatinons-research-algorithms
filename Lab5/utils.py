import os
import numpy as np


class Params:
    def __init__(self, iterations, ants_num, alpha, beta, rho):
        self.iterations = iterations
        self.ants_num = ants_num
        self.alpha = alpha
        self.beta = beta
        self.rho = rho # evaporation rate


def compute_distance_matrix(coords):
    N = len(coords)
    distances = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            distance = np.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)
            if distance == 0:
                distance = 0.001
            distances[i, j] = distances[j, i] = distance
    np.fill_diagonal(distances, 100000)
    return distances


def parse_file(filename):
    data = {}
    with open(os.getcwd() + '/data/benchmarks/' + filename, 'r') as file:
        lines = [str(elem) for elem in file.read().split()]
        file_it = iter(lines)

        while 1:
            token = next(file_it)
            if token == "NAME":
                next(file_it)
                data['name'] = next(file_it)
            elif token == "trucks:":
                data['n_trucks'] = int(next(file_it)[:-1])
            elif token == "value:":
                data['opt_value'] = int(next(file_it)[:-1])
            elif token == "DIMENSION":
                next(file_it)
                data['dimension'] = int(next(file_it))
            elif token == "CAPACITY":
                next(file_it)
                data['capacity'] = int(next(file_it))
            elif token == "NODE_COORD_SECTION":
                break

        coords = []
        for i in range(data['dimension']):
            next(file_it)
            coords.append((int(next(file_it)), int(next(file_it))))
        data['coords'] = np.array(coords)
        demand = []
        next(file_it)
        for i in range(data['dimension']):
            next(file_it)
            demand.append(int(next(file_it)))
        data['demand'] = np.array(demand)

        data['distances'] = compute_distance_matrix(coords)

        return data
