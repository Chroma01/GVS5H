import sys
from itertools import combinations


def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    N, K = vals[0], vals[1]
    A = vals[2:2 + N]
    del vals

    total = 0
    for v in A:
        total ^= v

    m = min(K, N - K)

    if m == 0:
        print(total)
        return

    if K <= N - K:
        ans = 0

        if m == 1:
            ans = max(A)
        elif m == 2:
            for a, b in combinations(A, 2):
                x = a ^ b
                if x > ans:
                    ans = x
        elif m == 3:
            for a, b, c in combinations(A, 3):
                x = a ^ b ^ c
                if x > ans:
                    ans = x
        elif m == 4:
            for a, b, c, d in combinations(A, 4):
                x = a ^ b ^ c ^ d
                if x > ans:
                    ans = x
        else:
            for comb in combinations(A, m):
                x = 0
                for v in comb:
                    x ^= v
                if x > ans:
                    ans = x

        print(ans)
    else:
        ans = 0
        t = total

        if m == 1:
            for a in A:
                y = t ^ a
                if y > ans:
                    ans = y
        elif m == 2:
            for a, b in combinations(A, 2):
                y = t ^ a ^ b
                if y > ans:
                    ans = y
        elif m == 3:
            for a, b, c in combinations(A, 3):
                y = t ^ a ^ b ^ c
                if y > ans:
                    ans = y
        elif m == 4:
            for a, b, c, d in combinations(A, 4):
                y = t ^ a ^ b ^ c ^ d
                if y > ans:
                    ans = y
        else:
            for comb in combinations(A, m):
                y = t
                for v in comb:
                    y ^= v
                if y > ans:
                    ans = y

        print(ans)


if __name__ == "__main__":
    main()