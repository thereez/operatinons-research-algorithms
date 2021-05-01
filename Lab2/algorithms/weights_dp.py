import numpy as np
from .optimal_result import OptimalResult


class WeightsDP:

    def __init__(self, capacity, item_weights, item_costs):
        self.capacity = capacity
        self.item_weights = np.array(item_weights)
        self.item_costs = np.array(item_costs)
        self.N = len(self.item_weights)
        self.table = np.zeros((self.N + 1, self.capacity + 1), dtype=np.uint32)
        self.operations = 0

    def get_answer(self):
        result = OptimalResult(self.N)
        knapsack_cost = self.table[self.N, self.capacity]
        self.operations += 1
        if knapsack_cost <= 0:
            return
        result.knapsack_cost = knapsack_cost
        w = self.capacity

        for i in range(self.N, -1, -1):
            self.operations += 1
            if knapsack_cost != self.table[i-1, w]:
                knapsack_cost -= self.item_costs[i-1]
                w -= self.item_weights[i-1]
                result.item_indexes[i-1] = 1
        result.knapsack_weight = np.sum(result.item_indexes * self.item_weights)
        return result, self.operations

    def solve(self):
        for i in range(1, self.N + 1):
            item_weight = self.item_weights[i-1]
            item_cost = self.item_costs[i-1]
            for w in range(self.capacity + 1):
                self.operations += 1
                if item_weight > w:
                    self.table[i, w] = self.table[i-1, w]
                else:
                    self.table[i, w] = max(self.table[i-1, w], item_cost + self.table[i-1, w-item_weight])

        return self.get_answer()
