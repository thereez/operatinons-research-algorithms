from time import perf_counter
import numpy as np
import argparse

from algorithms.local_search import LocalSearch


def parse_file(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        n = int(lines[0])
        flows, distances = [], []
        for i in range(1, n + 1):
            distances.append([int(x) for x in lines[i].split()])
        for i in range(n + 2, len(lines)):
            flows.append([int(x) for x in lines[i].split()])
    return np.array(flows, dtype=np.int32), np.array(distances, dtype=np.int32)

def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-benchmark', required=True, type=str,
                        choices=('20', '40', '60', '80', '100'),
                        help='Required. Input benchmark filename.')
    parser.add_argument('-algorithm', required=True, type=str,
                        choices=('LocalSearch', 'IteratedSearch'),
                        help='Required. Algorithm type.')
    parser.add_argument('-iterations_num', type=int, default=50,
                        help='Optional. Input number of iterations.')
    return parser

def main():
    args = build_argparser().parse_args()
    filename = f'data/tai{args.benchmark}a'
    iterations_num = args.iterations_num
    if args.algorithm == 'LocalSearch':
        algo = LocalSearch(*parse_file(filename))
        
    start = perf_counter()
    best_solution, best_fitness = algo.run(iterations_num)
    end = perf_counter()
    print('Total time:', end - start)
    print('Solution:', best_solution)
    print('Fitness:', best_fitness, '\n')


if __name__ == '__main__':
    main()
