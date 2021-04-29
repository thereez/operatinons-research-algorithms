import numpy as np
from optimal_result import OptimalResult


class CostsDP:

    def __init__(self, capacity, item_weights, item_costs):
        self.capacity = capacity
        self.item_weights = np.array(item_weights)
        self.item_costs = np.array(item_costs)
        self.N = len(self.item_weights)
        self.cost_sum = np.sum(self.item_costs)

        self.table = np.zeros((self.N + 1, self.cost_sum + 1), dtype=np.uint32)
        self.table[0, 1:] += (self.capacity + 1)

    def get_answer(self):
        result = OptimalResult(self.N)
        # Look at last row, find first value that < self.capacity + 1
        for idx, weight in enumerate(self.table[-1][::-1]):
            if weight < self.capacity + 1:
                result.knapsack_weight = weight
                result.knapsack_cost = self.cost_sum - idx
                break

        w = result.knapsack_weight
        knapsack_cost = result.knapsack_cost
        for i in range(self.N, 0, -1):
            cost_diff = knapsack_cost - self.item_costs[i-1]
            weight_diff = w - self.item_weights[i-1]
            if self.table[-1][cost_diff] == weight_diff:
                knapsack_cost = cost_diff
                w = weight_diff
                result.item_indexes[i-1] = 1
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
