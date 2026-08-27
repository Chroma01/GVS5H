import sys
from itertools import combinations

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

    m = min(K, N - K)

    if m == 0:
        print(total)
        return

    if m == 1:
        if K == 1:
            print(max(A))
        else:
            best = 0
            for x in A:
                v = total ^ x
                if v > best:
                    best = v
            print(best)
        return

    best = 0

    if K <= N - K:
        for comb in combinations(A, m):
            x = 0
            for v in comb:
                x ^= v
            if x > best:
                best = x
    else:
        for comb in combinations(A, m):
            x = total
            for v in comb:
                x ^= v
            if x > best:
                best = x

    print(best)

if __name__ == "__main__":
    main()