import numpy as np
import random

class BanditStrategy:
    
    def __init__(self, num_machines, attempts):
        self.num_machines = num_machines
        self.num_attempts = attempts
        self.success_counts = [0] * num_machines
        self.total_counts = [0] * num_machines
        self.estimated_probs_laplace = [0.5] * num_machines
        self.history = []

    def pull_once(self, attempt_number):
        if random.random() < 0.03:
            return random.randrange(0, self.num_machines)
        return np.argmax(self.estimated_probs_laplace)

    def log_result(self, attempt_number, machine_pulled, result):
        self.history.append(result)
        self.total_counts[machine_pulled] += 1
        if result:
            self.success_counts[machine_pulled] += 1
        self.estimated_probs_laplace[machine_pulled] = \
            (self.success_counts[machine_pulled]+1)/(self.total_counts[machine_pulled]+2)


