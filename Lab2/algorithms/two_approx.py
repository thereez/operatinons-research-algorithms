import numpy as np
from .optimal_result import OptimalResult


class TwoApprox:

    def __init__(self, capacity, item_weights, item_costs):
        self.capacity = capacity
        self.item_weights = np.array(item_weights)
        self.item_costs = np.array(item_costs)
        self.N = len(self.item_weights)
        self.indexes = np.array([i for i in range(self.N)])
        self.item_quality = np.array([cost / weight for cost, weight in zip(self.item_costs, self.item_weights)])
        self.items = list(zip(self.indexes, self.item_weights, self.item_costs, self.item_quality))
        self.operations = 0

    def greedyalgorithm(self):
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
        return result

    def maxgreed(self):
        result = OptimalResult(self.N)
        items = sorted(self.items, key=lambda x: -x[2])
        current_capacity = 0
        for item in items:
            self.operations += 1
            if current_capacity + item[1] <= self.capacity:
                current_capacity += item[1]
                result.item_indexes[item[0]] = 1
                result.knapsack_weight += item[1]
                result.knapsack_cost += item[2]
        return result

    def solve(self):
        greedy_result = self.greedyalgorithm()
        maxgreed_result = self.maxgreed()
        self.operations += 1
        if greedy_result.knapsack_cost >= maxgreed_result.knapsack_cost:
            return greedy_result, self.operations
        else:
            return maxgreed_result, self.operations
