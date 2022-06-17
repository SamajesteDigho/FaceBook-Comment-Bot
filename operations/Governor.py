from math import sqrt
import numpy as np

def distance(f1, f2):
    if len(f1) != len(f2):
        print('(Size 1, Size2)', (len(f1), len(f2)))
        return -1
    som = 0
    for x,y in zip(f1, f2):
        som += (x - y)**2
    return sqrt(som)


def calculate_distance_and_sort(ref, tests=[]):
    res = []
    for t in tests:
        f = t['features'].split(',')
        f = [np.float64(x) for x in f]
        dist = distance(ref, f)
        res.append((t, dist))

    # Sorting
    res.sort(key = lambda x: x[1])
    return res
