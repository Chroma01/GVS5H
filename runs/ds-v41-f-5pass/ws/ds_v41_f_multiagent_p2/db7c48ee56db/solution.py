import sys
from itertools import combinations
from functools import reduce
from operator import xor

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))

    if k <= n - k:
        best = 0
        for comb in combinations(a, k):
            v = reduce(xor, comb, 0)
            if v > best:
                best = v
        print(best)
    else:
        total = reduce(xor, a, 0)
        rem = n - k
        if rem == 0:
            print(total)
            return
        best = 0
        for comb in combinations(a, rem):
            v = total ^ reduce(xor, comb, 0)
            if v > best:
                best = v
        print(best)

main()