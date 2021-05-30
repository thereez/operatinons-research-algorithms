import numpy as np


class LocalSearch:

    def __init__(self, flows, distances):
        self.flows = flows
        self.distances = distances
        self.n = flows.shape[0]

    def get_init_solution(self):
        init = np.arange(self.n) 
        np.random.shuffle(init)
        return init

    def calc_fitness(self, solution):
        fitness = 0
        for i in range(self.n):
            for j in range(self.n):
                fitness += self.distances[i, j] *  self.flows[solution[i], solution[j]]
        return fitness

    def calc_delta(self, ans, r, s):
        delta = 0
        for k in range(self.n):
            if k != r and k != s:
                delta += (self.flows[ans[k], ans[r]] + self.flows[ans[r], ans[k]]) * \
                         (self.distances[s, k] - self.distances[r, k]) + \
                         (self.flows[ans[k], ans[s]] + self.flows[ans[s], ans[k]]) * \
                         (self.distances[r, k] - self.distances[s, k])
        return delta
    
    def run(self, iterations_num):
        self.best_solution = self.get_init_solution()
        self.best_fitness = self.calc_fitness(self.best_solution)
        self.dont_look = [False for _ in range(self.n)]

        for n in range(iterations_num):
            updated = self.search()
            if not updated:
                print(f'Stop Local Search on iteration {n}...')
                break
        return self.best_solution, self.best_fitness

    def search(self):
        solution = np.copy(self.best_solution)
    
        for i in range(self.n - 1):
            if self.dont_look[i]:
                continue
            for j in range(i + 1, self.n):
                solution[i], solution[j] = solution[j], solution[i]
                delta = self.calc_delta(solution, i, j)
                if delta > 0:
                    self.best_fitness -= delta
                    self.best_solution = solution
                    return True
                solution[i], solution[j] = solution[j], solution[i]
                if j == self.n - 1:
                    self.dont_look[i] = True
        return False
