import argparse
from time import perf_counter

import utils
from ant_colony import ACO


def solve(input_file, params):
    data = utils.parse_file(input_file)
    start = perf_counter()
    algo = ACO(data['n_trucks'], data['dimension'], data['capacity'], data['demand'], data['distances'], params)
    result = algo.solve()
    end = perf_counter()
    print(result)
    print('Total time:', end - start)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-benchmark', required=True, type=str)
    parser.add_argument('-iterations', type=int, default=100)
    parser.add_argument('-ants_num', type=int, default=18)
    parser.add_argument('-alpha', type=float, default=0.9)
    parser.add_argument('-beta', type=float, default=2.1)
    parser.add_argument('-rho', type=float, default=0.7)
  
    args = parser.parse_args()
    params = utils.Params(iterations=args.iterations, ants_num=args.ants_num,
                          alpha=args.alpha, beta=args.beta, rho=args.rho)
    solve(args.benchmark, params)
