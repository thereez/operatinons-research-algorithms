import utils as utils
import argparse


def solve(input_file):
    data = utils.parse_file(input_file)
    print(data)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-benchmark', required=True, type=str)
    args = parser.parse_args()

    solve(args.benchmark)
