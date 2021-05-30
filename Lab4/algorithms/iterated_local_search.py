import numpy as np


class LocalSearch:
    def __init__(self, flows, distances, n_iter, n_modifications):
        self.n = flows.shape[0]
        self.distances = distances
        self.flows = flows
        self.n_iter = n_iter
        self.n_modifications = n_modifications

    def init_solution(self):
        self.solution = np.arange(self.n)
        np.random.shuffle(self.solution)
        self.current_fitness = self.calc_fitness(self.solution)

    def stochastic_2_opt(self, solution=None):
        self.init_solution()
        if solution is not None:
            self.solution = solution
            self.current_fitness = self.calc_fitness(self.solution)
        improved = True
        for iteration in range(self.n_iter):
            if not improved:
                break
            best_solution = self.solution
            improved = False
            for modifications in range(self.n_modifications):
                left_index = np.random.randint(0, self.n)
                right_index = np.random.randint(left_index + 1, self.n + 1)
                tmp_solution = self.solution.copy()
                tmp_solution[left_index:right_index] = tmp_solution[left_index:right_index][::-1]
                fitness = self.calc_fitness(tmp_solution)
                if fitness < self.current_fitness:
                    improved = True
                    self.current_fitness = fitness
                    best_solution = tmp_solution
            self.solution = best_solution
        final_fitness = self.calc_fitness(self.solution)
        return self.solution, final_fitness

    def calc_fitness(self, solution):
        fitness = 0
        for i in range(self.n):
            for j in range(self.n):
                fitness += self.flows[i][j] * self.distances[solution[i]][solution[j]]
        return fitness


class IteratedLocalSearch:
    def __init__(self, flows, distances):
        self.n = flows.shape[0]
        self.distances = distances
        self.flows = flows
        self.ls = LocalSearch(self.flows, self.distances, 20, 10)

    def init_solution(self):
        self.solution = np.arange(self.n)
        np.random.shuffle(self.solution)

    def calc_fitness(self, solution):
        fitness = 0
        for i in range(self.n):
            for j in range(self.n):
                fitness += self.flows[i][j] * self.distances[solution[i]][solution[j]]
        return fitness

    def modify(self):
        k = np.random.randint(2, self.n + 1)
        indexes = np.random.choice(np.arange(self.n), k, replace=False)
        shuffled_indexes = np.random.permutation(indexes)
        modified_solution = self.solution.copy()
        modified_solution[indexes] = self.solution[shuffled_indexes]
        return modified_solution

    def acceptance_criterion(self, current_solution):
        if self.calc_fitness(self.solution) > self.calc_fitness(current_solution):
            self.solution = current_solution

    def run(self, n_iter):
        self.init_solution()
        self.solution, _ = self.ls.stochastic_2_opt(self.solution)
        for iteration in range(n_iter):
            modified_solution = self.modify()
            current_solution, _ = self.ls.stochastic_2_opt(modified_solution)
            self.acceptance_criterion(current_solution)
        final_fitness = self.calc_fitness(self.solution)
        return self.solution, final_fitness