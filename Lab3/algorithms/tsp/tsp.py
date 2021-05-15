import random
import numpy as np


def get_random_chromosome(chromosome_len):
    chromosome = np.arange(1, chromosome_len + 1)
    np.random.shuffle(chromosome)
    return chromosome

def get_init_population(chromosome_len, population_size):
    population = []
    for _ in range(population_size):
        population.append(get_random_chromosome(chromosome_len))
    return np.array(population)

def fitness_function(chromosome, distances):
    fitness = 0
    for i in range(1, len(chromosome)):
        prev, next = int(chromosome[i-1]), int(chromosome[i])
        fitness += distances[prev-1, next-1] # indexing starts from 0
    return fitness

def get_fitness_results(population, distances):
    fitness_results = np.zeros(len(population))
    for i, chromosome in enumerate(population):
        fitness_results[i] = fitness_function(chromosome, distances)
    return fitness_results

def rank_selection(population, distances):
    fitness_results = get_fitness_results(population, distances)
    sorted_indexes = np.argsort(fitness_results)
    probabilities = (50, 30, 15, 5) # should be changed ?
    ranked_indexes = np.array_split(sorted_indexes, 4)
    weights = []
    for rank, proba in zip(ranked_indexes, probabilities):
        weights += [proba] * len(rank)
    selection = random.choices(sorted_indexes, weights, k=len(population))        
    return population[selection]

def resolve_collision(gen, slice, links):
    while gen in set(slice):
        gen = links[gen]
    return gen

def partially_mapped_crossover(parent1, parent2, window):
    left = np.random.choice(len(parent1) // 2)
    right = left + window

    slice1, slice2 = parent1[left:right], parent2[left:right]
    links1 = {gen : slice1[i] for i, gen in enumerate(slice2)}
    links2 = {gen : slice2[i] for i, gen in enumerate(slice1)}
    parent1[left:right], parent2[left:right] = slice2, slice1

    indexes = np.arange(len(parent1))
    indexes = list(set(indexes) - set(np.arange(left, right)))
    for i in indexes:
        parent1[i] = resolve_collision(parent1[i], slice2, links1)
        parent2[i] = resolve_collision(parent2[i], slice1, links2)

    return parent1, parent2

def apply_crossover(population, p, window):
    new_population = []
    for i in range(len(population) // 2):
        idx1, idx2 = np.random.choice(len(population), 2, replace=False)
        chromo1, chromo2 = population[idx1], population[idx2]
        is_crossover = np.random.binomial(1, p)
        if is_crossover:
            chromo1, chromo2 = partially_mapped_crossover(chromo1, chromo2, window)
        new_population.append(chromo1)
        new_population.append(chromo2)
    return np.array(new_population)

def apply_mutation(population, p, window):
    # Inversion mutation + swaping two indexes
    for chromo in population:
        is_mutation = np.random.binomial(1, p)
        if is_mutation:
            # inverse
            idx = np.random.choice(len(population[0]))
            left, right = idx, idx + window
            # swap
            idx1, idx2 = np.random.choice(len(population[0]), 2, replace=False)
            chromo[idx1], chromo[idx2] = chromo[idx2], chromo[idx1]
    return population
