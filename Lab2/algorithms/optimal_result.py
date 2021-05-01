import numpy as np


class OptimalResult:

    def __init__(self, N):
        self.knapsack_cost = 0
        self.knapsack_weight = 0
        self.item_indexes = np.zeros(N, dtype=np.float32)
    
    def __repr__(self):
        return f"Cost of knapsack: {self.knapsack_cost} \nWeight of knapsack: {self.knapsack_weight}\nIncluded items: {self.item_indexes}"
