import codecs
from time import perf_counter
import pandas as pd
import numpy as np

from algorithms.fptas import FPTAS
from algorithms.weights_dp import WeightsDP
from algorithms.costs_dp import CostsDP
from algorithms.two_approx import TwoApprox
from algorithms.branches_and_bounds import BnB


def parse_data(file_num):  # TODO: add base dir
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


results = pd.DataFrame(
    columns=['Benchmark_№', 'Algorithm', 'Average_time', 'Number_of_operations', 'Cost', 'Weight'])

algo_dict = {TwoApprox: 'TwoApprox', BnB: 'Branches and bounds', WeightsDP: 'WeightsDP', CostsDP: 'CostsDP',
             FPTAS: 'FPTAS'}


def measure_time(algorithm, benchmark, capacity, weights, costs, iterations=1):
    global results
    total_time = 0
    for i in range(iterations):
        start_time = perf_counter()
        algo = algorithm(capacity, weights, costs)
        result, operations = algo.solve()
        end_time = perf_counter()
        total_time += end_time - start_time
    total_time /= iterations
    print(algo_dict[algorithm], ':\n', result)
    print('Number of operations:', operations)
    print('Average execution time:', total_time, '\n')
    results = results.append(
        {'Benchmark_№': benchmark, 'Algorithm': algo_dict[algorithm], 'Number_of_operations': operations,
         'Cost': result.knapsack_cost, 'Weight': result.knapsack_weight}, ignore_index = True)


def main():
    for i in range(1, 8):
        data = parse_data(i)
        print(f'Optimal result for {i} example:', data['optimal'])
        print('Optimal cost:', np.sum(np.array(data['optimal']) * np.array(data['costs'])))
        print('Optimal weight:', np.sum(np.array(data['optimal']) * np.array(data['weights'])), '\n')
        for a in [TwoApprox, BnB, WeightsDP, CostsDP, FPTAS]:
            measure_time(a, i, data['capacity'], data['weights'], data['costs'])
        print('\n\n')


if __name__ == '__main__':
    main()
