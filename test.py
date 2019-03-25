import math
import numpy as np

test = {"a": 0, "b": 10, "c": 3, "d": 1, "e": 5}

n_neighbours = len(test.keys())

sims = np.ones(n_neighbours)

eps = np.finfo(1.0).eps

for i, (key, item) in enumerate(test.items()):

   sims[i-1] = item+1/n_neighbours

#z = lambda x: (x+np.finfo(1.0).eps)

#xeps = z(sims)

y = lambda x: (1/x)

inverse = y(sims)

min_sim = np.min(inverse)
max_sim = np.max(inverse)

difference = max_sim-min_sim

f = lambda x: (x - min_sim)/difference

normalized = f(inverse)

print(inverse.tolist())
print(list(normalized))