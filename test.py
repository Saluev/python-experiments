import experiments
from math import exp


def f(x, y, z):
    # this is an experiment
    result = 0.0
    tmp = 1.0
    for q in range(1, x):
        result += 1.0 / tmp
        tmp *= q
    return abs(result - exp(1.0)) #result ** (x + y + z) - exp(x + y + z)

r = experiments.start(f, iterations=100, cores=4, x = range(10), y = 1, z = (1, 2))
print "Results:\n", "\n".join(map(str, r))