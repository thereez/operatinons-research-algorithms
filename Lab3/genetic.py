import codecs
from algorithms.knapsack.knapsack import *
from time import perf_counter
import pandas as pd
import numpy as np


def parse_data(file_num):
    capacity = codecs.open(f"data_knapsack/p0{file_num}_c.txt", "r", "utf_8_sig").read()
    weights = codecs.open(f"data_knapsack/p0{file_num}_w.txt", "r", "utf_8_sig").read()
    costs = codecs.open(f"data_knapsack/p0{file_num}_p.txt", "r", "utf_8_sig").read()
    optimal = codecs.open(f"data_knapsack/p0{file_num}_s.txt", "r", "utf_8_sig").read()

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
        costs = data['costs']
        weights = data['weights']
        capacity = data['capacity']
        crossover_rate = 0.8
        mutation_rate = 0.6
        epochs = 50
        population_size = 30
        best_costs = -1
        best_result = None
        start_time = perf_counter()
        population = get_initial_population(len(weights), population_size)
        num_parents = int(len(population) / 2)
        num_offsprings = len(population) - num_parents
        for i in range(epochs):
            f, p = fitness(population, weights, costs, capacity)
            new_gen = rws_selection(p, f, num_parents)
            offsprings = crossover(new_gen, num_offsprings, crossover_rate)
            mutants = mutation(offsprings, mutation_rate)
            population[0:new_gen.shape[0], :] = new_gen
            population[new_gen.shape[0]:, :] = mutants
            result = best_solution(population, weights, costs, capacity)
            if result[2] > best_costs:
                best_result = result
        f, p = fitness(population, weights, costs, capacity)
        result = best_solution(p, weights, costs, capacity)
        if result[2] > best_costs:
            best_result = result
        end_time = perf_counter()
        print('Best answer:', best_result[0])
        print('Best capacity:', best_result[1])
        print('Best costs:', best_result[2])
        print('Execution time: %.4f' % (end_time - start_time))


if __name__ == '__main__':
    main()
