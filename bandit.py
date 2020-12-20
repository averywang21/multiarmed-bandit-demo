import numpy as np
import random 
from bandit_strategy import BanditStrategy

scores = []
machines = [0.4, 0.6, 0.3, 0.5]
attempts = 100
iterations = 10000


for j in range(iterations):
    score = 0
    strategy = BanditStrategy(num_machines=len(machines), attempts=attempts)
    for i in range(attempts):
        decision = strategy.pull_once(i)
        if random.random() < machines[decision]:
            strategy.log_result(i, decision, 1)
            score += 1
        else:
            strategy.log_result(i, decision, 0)
    scores.append(score)

print(np.round(np.mean(scores), 3))
print(np.round(np.std(scores)/np.sqrt(len(scores)), 3))