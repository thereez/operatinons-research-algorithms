import numpy as np
from .costs_dp import CostsDP
from .two_approx import TwoApprox


class FPTAS:

    def __init__(self, capacity, item_weights, item_costs, eps=0.1):
        self.item_costs = np.array(item_costs)
        self.N = len(item_weights)
        c_2a = TwoApprox(capacity, item_weights, item_costs).solve()[0].knapsack_cost
        self.alpha = (c_2a * eps) / self.N
        self.new_costs = np.floor(self.item_costs / self.alpha).astype(np.uint32)
        self.dp = CostsDP(capacity, np.array(item_weights), self.new_costs)
        self.operations = 0

    def solve(self):
        result, self.operations = self.dp.solve()
        result.knapsack_cost = np.sum(self.item_costs * result.item_indexes)
        return result, self.operations
