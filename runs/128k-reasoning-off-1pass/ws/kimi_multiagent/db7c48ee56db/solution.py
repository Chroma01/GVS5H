import sys
from itertools import combinations
from functools import reduce
from operator import xor

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))

    total = 0
    for v in a:
        total ^= v

    m = k if k <= n - k else n - k
    complement = (m != k)  # True if we enumerate excluded elements

    best = -1
    if complement:
        for comb in combinations(a, m):
            cand = total ^ reduce(xor, comb, 0)
            if cand > best:
                best = cand
    else:
        for comb in combinations(a, m):
            cand = reduce(xor, comb, 0)
            if cand > best:
                best = cand

    print(best)

solve()