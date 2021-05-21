import numpy as np
import copy
import random
import codecs
from random import randint
from time import perf_counter


def get_initial_population(cromosome_len, population_size):
    population_shape = (population_size, cromosome_len)
    population = np.random.randint(2, size=population_shape).astype(int)
    return population


def fitness(population, weights, costs, capacity):
    new_population = copy.deepcopy(population)
    fitness = np.empty(new_population.shape[0])
    for i in range(new_population.shape[0]):
        current_costs = np.sum(new_population[i] * costs)
        current_weights = np.sum(new_population[i] * weights)
        while current_weights > capacity:
            indexes = np.where(new_population[i] == 1)[0]
            index = np.random.choice(indexes)
            new_population[i][index] = 0
            current_costs = np.sum(new_population[i] * costs)
            current_weights = np.sum(new_population[i] * weights)
        fitness[i] = current_costs
    return fitness.astype(int), new_population


def best_solution(population, weights, costs, capacity):
    costs = np.dot(population, costs)
    weights = np.dot(population, weights)
    indexes = np.where(weights <= capacity)[0]
    best_costs = -1
    result = None
    for index in indexes:
        if costs[index] > best_costs:
            result = (population[index], weights[index], costs[index])
            best_costs = costs[index]
    return result


def rws_selection(population, fitness, num_parents):
    fitness = list(fitness)
    survive_chances = [fit_value / sum(fitness) for fit_value in fitness]
    new_generation = random.choices(population, weights=survive_chances, k=num_parents)
    new_generation = np.asarray(new_generation)
    return new_generation


def crossover(parents, num_offsprings, crossover_rate):
    offsprings = np.empty((num_offsprings, parents.shape[1]))
    i = 0
    while i < num_offsprings:
        crossover_point = int(np.random.uniform(1, parents.shape[1]))
        is_crossover = np.random.binomial(1, crossover_rate)
        if not is_crossover:
            continue
        p1_index = i % parents.shape[0]
        p2_index = (i + 1) % parents.shape[0]
        offsprings[i, 0:crossover_point] = parents[p1_index, 0:crossover_point]
        offsprings[i, crossover_point:] = parents[p2_index, crossover_point:]
        i += 1
    return offsprings


def mutation(offsprings, mutation_rate):
    mutants = np.empty((offsprings.shape))
    for i in range(mutants.shape[0]):
        mutants[i, :] = offsprings[i, :]
        is_mutation = np.random.binomial(1, mutation_rate)
        if not is_mutation:
            continue
        int_random_value = randint(0, offsprings.shape[1] - 1)
        if mutants[i, int_random_value] == 0:
            mutants[i, int_random_value] = 1
        else:
            mutants[i, int_random_value] = 0
    return mutants


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


def solve(data, crossover_rate, mutation_rate, epochs, population_size):
    costs = data['costs']
    weights = data['weights']
    capacity = data['capacity']
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


