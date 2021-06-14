import numpy as np


class ACO:

    def __init__(self, n_trucks, dimension, capacity, demands, distances, params):
        self.params = params
        self.n_trucks = n_trucks
        self.dimension = dimension
        self.capacity = capacity
        self.demands = demands
        self.distances = distances
        self.init_pheromone =  1 / self.dimension

        self.distances_sum = distances.sum()
        self.final_cost = self.distances_sum

        self.attractiveness = 1 / self.distances
        self.create_pheromones()

    def create_pheromones(self):
        self.pheromones = np.full((self.dimension, self.dimension), fill_value=self.init_pheromone)
        np.fill_diagonal(self.pheromones, 0)

    def get_transition(self, i, j):
        return pow(self.pheromones[i, j], self.params.alpha) * pow(self.attractiveness[i, j], self.params.beta)

    def get_next_node(self, i):
        forbidden = np.copy(self.visited)
        for j in range(self.dimension):
            if not self.visited[j] and self.demands[j] > self.capacity_left:
                forbidden[j] = True

        if sum(forbidden) == self.dimension:
            return 0

        prob_list = np.array([0 if forbidden[j] else self.get_transition(i, j) for j in range(self.dimension)])
        prob_list /= prob_list.sum()
        return np.random.choice(np.arange(self.dimension), p=prob_list)

    def local_pheromone_update(self, i, j):
        self.pheromones[i, j] += self.init_pheromone / self.distances[i, j]
        self.pheromones[j, i] = self.pheromones[i, j]

    def global_pheromone_update(self, best_solution, best_cost):
        for path in best_solution:
            for index, _ in enumerate(path[:-1]):
                i, j = path[index], path[index + 1]
                self.pheromones[i, j] += self.capacity / best_cost
                self.pheromones[j, i] = self.pheromones[i, j]

    def get_cost(self, solution):
        total_cost = 0
        for i, _ in enumerate(solution[:-1]):
            total_cost += self.distances[solution[i], solution[i + 1]]
        return total_cost

    def get_routes_by_ant(self):
        new_route = True
        solution = []
        self.visited = [False] * self.dimension
        self.visited[0] = True

        while sum(self.visited) < self.dimension:
            if new_route:
                curr_node = 0
                path = [curr_node]
                self.capacity_left = self.capacity
                new_route = False

            next_node = self.get_next_node(curr_node)
            path.append(next_node)

            if next_node == 0:
                solution.append(path)
                new_route = True
            else:
                self.capacity_left -= self.demands[next_node]
                self.local_pheromone_update(curr_node, next_node)
                curr_node = next_node
                self.visited[curr_node] = True

        solution.append(path + [0])
        cost = sum([self.get_cost(path) for path in solution])
        return cost, solution

    def solve(self, verbose=False):
        for iteration in range(self.params.iterations):
            best_solution = None
            best_cost = self.distances_sum

            for ant in range(self.params.ants_num):
                cost, solution = self.get_routes_by_ant()
                if cost < best_cost:
                    best_solution = solution
                    best_cost = cost

            self.global_pheromone_update(best_solution, best_cost)
            # Испарение феромонов
            self.pheromones = (self.pheromones * self.params.rho).astype(np.float64)

            if best_cost < self.final_cost:
                self.final_cost = best_cost
                self.final_sol = best_solution

            if verbose:
                print(f'Iteration: {iteration}, Final cost: {self.final_cost}')

        return [list(np.array(x) + 1) for x in self.final_sol], self.final_cost
