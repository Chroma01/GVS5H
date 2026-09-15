import sys
from itertools import combinations
from functools import reduce
from operator import xor

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2 + N]))

    total = 0
    for x in A:
        total ^= x

    M = min(K, N - K)

    if M == 0:
        print(total)
        return

    if M == 1:
        if K <= N - K:
            print(max(A))
        else:
            best = 0
            for x in A:
                v = total ^ x
                if v > best:
                    best = v
            print(best)
        return

    if K <= N - K:
        best = 0
        for comb in combinations(A, K):
            v = reduce(xor, comb)
            if v > best:
                best = v
        print(best)
    else:
        best = 0
        for comb in combinations(A, N - K):
            v = total ^ reduce(xor, comb)
            if v > best:
                best = v
        print(best)

if __name__ == "__main__":
    main()