import sys
from itertools import combinations
from operator import xor
from functools import reduce


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2 + N]))

    # Enumerate the smaller side: either the chosen K elements
    # or the omitted N-K elements.
    if K <= N - K:
        best = 0
        for comb in combinations(A, K):
            x = reduce(xor, comb, 0)
            if x > best:
                best = x
        print(best)
    else:
        total = 0
        for v in A:
            total ^= v

        m = N - K  # number of omitted elements
        best = 0
        for comb in combinations(A, m):
            omitted_xor = reduce(xor, comb, 0)
            chosen_xor = total ^ omitted_xor
            if chosen_xor > best:
                best = chosen_xor
        print(best)


if __name__ == "__main__":
    main()