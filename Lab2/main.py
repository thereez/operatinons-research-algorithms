import codecs
from time import perf_counter

import numpy as np

from algorithms.fptas import FPTAS
from algorithms.weights_dp import WeightsDP
from algorithms.costs_dp import CostsDP


def parse_data(file_num): #TODO: add base dir
    capacity = codecs.open(f"data/p0{file_num}_c.txt", "r", "utf_8_sig").read()
    weights = codecs.open(f"data/p0{file_num}_w.txt", "r", "utf_8_sig").read()
    costs = codecs.open(f"data/p0{file_num}_p.txt", "r", "utf_8_sig").read()
    optimal = codecs.open(f"data/p0{file_num}_s.txt", "r", "utf_8_sig").read()

    data = {
        'capacity': int(capacity.strip()),
        'weights': [int(w.strip()) for w in weights.splitlines()],
        'costs': [int(c.strip()) for c in costs.splitlines()],
        'optimal': [int(i.strip()) for i in optimal.splitlines()],
    }
    return data


def main():
    for i in range(1, 8):
        data = parse_data(i)
        print(f'Optimal result for {i} example:', data['optimal'])
        print('Optimal cost:', np.sum(np.array(data['optimal']) * np.array(data['costs'])))
        print('Optimal weight:', np.sum(np.array(data['optimal']) * np.array(data['weights'])), '\n')

        algo = WeightsDP(data['capacity'], data['weights'], data['costs'])
        print('DP weights:\n', algo.solve(), '\n')

        algo = CostsDP(data['capacity'], data['weights'], data['costs'])
        print('DP costs:\n', algo.solve(), '\n')

        algo = FPTAS(data['capacity'], data['weights'], data['costs'])
        print('FPTAS:\n', algo.solve(), '\n')

        print('\n\n')


if __name__ == '__main__':
    main()
