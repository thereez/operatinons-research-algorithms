import numpy as np
from ortools.linear_solver import pywraplp
from .optimal_result import OptimalResult





class BnB:
    def __init__(self, capacity, item_weights, item_costs):
        self.capacity = capacity
        self.item_weights = item_weights
        self.item_costs = item_costs
        self.N = len(self.item_weights)
        self.indexes = np.array([i for i in range(self.N)])
        self.item_quality = np.array([cost / weight for cost, weight in zip(self.item_costs, self.item_weights)])
        self.items = list(zip(self.indexes, self.item_weights, self.item_costs, self.item_quality))
        self.lower_bound = 0
        self.result_indexes = None
        self.current_capacity = 0
        self.bounds = [[0, 1]] * self.N
        self.operations = 0

    def greedyalg(self):
        total_cost = 0
        items = sorted(self.items, key=lambda x: -x[3])
        current_capacity = 0
        for item in items:
            self.operations += 1
            if current_capacity + item[1] <= self.capacity:
                current_capacity += item[1]
                total_cost += item[2]
        self.lower_bound = total_cost

    def relaxedgreedyalgorithm(self):
        result = OptimalResult(self.N)
        items = sorted(self.items, key=lambda x: -x[3])
        current_capacity = 0
        for item in items:
            self.operations += 1
            if current_capacity + item[1] <= self.capacity:
                current_capacity += item[1]
                result.item_indexes[item[0]] = 1
                result.knapsack_weight += item[1]
                result.knapsack_cost += item[2]
            else:
                remaining_capacity = self.capacity - current_capacity
                result.item_indexes[item[0]] = remaining_capacity / item[1]
                result.knapsack_weight += remaining_capacity
                result.knapsack_cost += item[2] * result.item_indexes[item[0]]
                current_capacity += remaining_capacity
        return result

    def recursive_solution(self):
        solver = pywraplp.Solver('bnb', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        x_dict = {i: solver.NumVar(self.bounds[i][0], self.bounds[i][1], f'x_{i}') for i in range(self.N)}
        solver.Add(solver.Sum([self.item_weights[i] * x_dict[i] for i in range(self.N)]) <= self.capacity)
        solver.Maximize(solver.Sum([self.item_costs[i] * x_dict[i] for i in range(self.N)]))
        solver.Solve()
        profit = solver.Objective().Value()
        self.operations += 1  # checking lower bound
        if profit < self.lower_bound:
            return
        items = np.array([x_dict[x_d].solution_value() for x_d in x_dict])
        try:
            index = np.where(items % 1 != 0)[0][0]
        except:
            index = -1

        self.operations += 1  # checking if solution is integer
        if index == -1:
            self.lower_bound = profit
            self.result_indexes = items

        else:
            self.bounds[index] = [0, 0]
            self.recursive_solution()

            self.bounds[index] = [1, 1]
            self.current_capacity += self.item_weights[index]
            self.operations += 1  # checking if there a place for new item
            if self.current_capacity <= self.capacity:
                self.recursive_solution()

            self.bounds[index] = [0, 1]
            self.current_capacity -= self.item_weights[index]

    def boundsandbranches(self):
        first_approximation = self.relaxedgreedyalgorithm()
        items = first_approximation.item_indexes

        try:
            index = np.where(items % 1 != 0)[0][0]
        except:
            index = -1

        self.operations += 1  # checking if solution is integer
        if index == -1:
            self.lower_bound = first_approximation.knapsack_cost
            self.result_indexes = items
        else:
            self.bounds[index] = [0, 0]
            self.recursive_solution()

            self.bounds[index] = [1, 1]
            self.current_capacity += self.item_weights[index]
            self.operations += 1  # checking if there a place for new item
            if self.current_capacity <= self.capacity:
                self.recursive_solution()

            self.bounds[index] = [0, 1]
            self.current_capacity -= self.item_weights[index]

    def solve(self):
        self.greedyalg()  # determining lower bound
        self.boundsandbranches()
        result = OptimalResult(self.N)
        result.knapsack_cost = self.lower_bound
        result.knapsack_weight = np.sum(self.result_indexes * self.item_weights)
        result.item_indexes = self.result_indexes
        return result, self.operations
