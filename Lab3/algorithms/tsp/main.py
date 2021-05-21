import argparse
from time import perf_counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import get_distances
from tsp import get_init_population, rank_selection, apply_crossover, apply_mutation, get_fitness_results


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-benchmark', required=True, type=str,
                        choices=('a280', 'ch150', 'fl417', 'att48', 'bays29', 'gr17'),
                        help='Required. Input benchmark filename.')
    parser.add_argument('-population_size', required=True, type=int,
                        help='Required. Input population size.')
    parser.add_argument('-generations_num', required=True, type=int,
                        help='Required. Input number of generations (iterations).')
    parser.add_argument('-crossover_chance', type=float, default=0.8,
                        help='Optional. Input probability of crossover. Default: 0.8.')
    parser.add_argument('-crossover_window', type=int, default=10,
                        help='Optional. Input size of window used in partially mapped crossover. Default: 10.')
    parser.add_argument('-mutation_chance', type=float, default=0.01,
                        help='Optional. Input probability of mutation. Default: 0.01.')
    parser.add_argument('-mutation_window', type=int, default=10,
                        help='Optional. Input size of window, which will be inversed during mutation. Default: 10.')
    parser.add_argument('-verbose', default=False, action='store_true',
                        help='Optional. Print best result for every generation. Default: False.')
    return parser

def plot_results(costs, num):
    plt.figure(figsize = (15,10))
    plt.title('GA convergence')
    plt.xlabel('Generation num')
    plt.ylabel('Best result')
    plt.plot(np.arange(num), costs)
    plt.legend()
    plt.show()

def main():
    args = build_argparser().parse_args()

    distances = get_distances(args.benchmark)
    best_result = np.inf
    answer = None

    start_time = perf_counter()
    population = get_init_population(len(distances), args.population_size)
    costs = []

    for i in range(args.generations_num):
        population = rank_selection(population, distances)
        population = apply_crossover(population, args.crossover_chance, args.crossover_window)
        population = apply_mutation(population, args.mutation_chance, args.mutation_window)
        
        fitness = get_fitness_results(population, distances)
        generation_result = sorted(fitness)[0]
        costs.append(generation_result)
        if generation_result < best_result:
            best_result = generation_result
            answer = population[np.argsort(fitness)[0]]
            assert len(answer) == len(set(answer)) # check if all cities are unique
        if args.verbose:
            print(f'Generation {i+1} is created.')
            print('The minimal distance:', generation_result, '\n')

    end_time = perf_counter()
    print('Best result by Genetic Algorithm:', best_result)
    print('Total time:', end_time - start_time)
    print('Route:', answer)
    plot_results(costs, args.generations_num)


if __name__ == '__main__':
    main()
