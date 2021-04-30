import numpy as np
from .optimal_result import OptimalResult


class CostsDP:

    def __init__(self, capacity, item_weights, item_costs):
        self.capacity = capacity
        self.item_weights = np.array(item_weights)
        self.item_costs = np.array(item_costs)
        self.N = len(self.item_weights)
        self.cost_sum = np.sum(self.item_costs)

        self.table = np.zeros((self.N + 1, self.cost_sum + 1), dtype=np.uint32)
        self.table[0, 1:] += (self.capacity + 1)

    def get_indexes(self, result, N, cost):
        if self.table[N, cost] == 0:
            return
        if self.table[N-1, cost] == self.table[N, cost]:
            self.get_indexes(result, N - 1, cost)
        else:
            self.get_indexes(result, N - 1, cost - self.item_costs[N - 1])
            result.item_indexes[N - 1] = 1

    def get_answer(self):
        result = OptimalResult(self.N)
        # Look at last row, find first value that < self.capacity + 1
        for idx, weight in enumerate(self.table[-1][::-1]):
            if weight < self.capacity + 1:
                result.knapsack_weight = weight
                knapsack_cost = self.cost_sum - idx
                break
        self.get_indexes(result, self.N, knapsack_cost)
        result.knapsack_cost = np.sum(self.item_costs * result.item_indexes)
        return result

    def solve(self):
        for i in range(1, self.N + 1):
            item_weight = self.item_weights[i-1]
            item_cost = self.item_costs[i-1]
            for c in range(self.cost_sum + 1):
                if item_cost > c:
                    self.table[i, c] = self.table[i-1, c]
                else:
                    self.table[i, c] = min(self.table[i-1, c], item_weight + self.table[i-1, c-item_cost])

        return self.get_answer()
