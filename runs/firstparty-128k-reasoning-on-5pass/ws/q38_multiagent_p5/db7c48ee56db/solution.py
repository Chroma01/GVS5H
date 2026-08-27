import sys
from itertools import combinations

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    total = 0
    for v in A:
        total ^= v

    if K == N:
        print(total)
        return

    if K == 1:
        print(max(A))
        return

    if N - K == 1:
        best = 0
        for v in A:
            val = total ^ v
            if val > best:
                best = val
        print(best)
        return

    if K <= N - K:
        best = 0
        for c in combinations(A, K):
            x = 0
            for v in c:
                x ^= v
            if x > best:
                best = x
    else:
        best = 0
        r = N - K
        for c in combinations(A, r):
            x = 0
            for v in c:
                x ^= v
            x ^= total
            if x > best:
                best = x

    print(best)

if __name__ == "__main__":
    main()