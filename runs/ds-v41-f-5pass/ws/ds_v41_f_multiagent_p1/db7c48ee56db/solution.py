import sys
from itertools import combinations
from functools import reduce
from operator import xor


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    N, K = data[0], data[1]
    A = data[2:]

    total_xor = 0
    for x in A:
        total_xor ^= x

    ans = 0

    if K <= N - K:
        for comb in combinations(A, K):
            v = reduce(xor, comb, 0)
            if v > ans:
                ans = v
    else:
        r = N - K
        for comb in combinations(A, r):
            excluded_xor = reduce(xor, comb, 0)
            v = total_xor ^ excluded_xor
            if v > ans:
                ans = v

    print(ans)


if __name__ == "__main__":
    main()