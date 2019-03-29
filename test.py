import math
import numpy as np

test1 = {"a": 0, "b": 10, "c": 3, "d": 1, "e": 5}
test = {"a": 0}

n_neighbours = len(test.keys())

sims = np.ones(n_neighbours)

for i, (key, item) in enumerate(test.items()):

    sims[i-1] = item+1/n_neighbours

y = lambda x: (1/x)

inverse = y(sims)

min_sim = np.min(inverse)
max_sim = np.max(inverse)

if min_sim == max_sim:

    difference = 1

else:
    
    difference = max_sim-min_sim

f = lambda x: (x - min_sim)/difference

normalized = f(inverse)

print(inverse.tolist())
print(list(normalized))