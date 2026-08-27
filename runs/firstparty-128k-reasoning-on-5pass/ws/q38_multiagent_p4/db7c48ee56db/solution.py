import sys
from itertools import combinations


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    K = data[1]
    A = data[2:2 + N]
    del data

    total = 0
    for x in A:
        total ^= x

    nk = N - K
    m = K if K <= nk else nk

    if m == 0:
        print(total)
        return

    if m == 1:
        if K <= nk:
            ans = max(A)
        else:
            t = total
            ans = 0
            for a in A:
                v = t ^ a
                if v > ans:
                    ans = v
        print(ans)
        return

    if m == 2:
        ans = 0
        arr = A
        n = N

        if K <= nk:
            for i in range(n - 1):
                ai = arr[i]
                for j in range(i + 1, n):
                    v = ai ^ arr[j]
                    if v > ans:
                        ans = v
        else:
            t = total
            for i in range(n - 1):
                tai = t ^ arr[i]
                for j in range(i + 1, n):
                    v = tai ^ arr[j]
                    if v > ans:
                        ans = v

        print(ans)
        return

    ans = 0
    if K <= nk:
        for comb in combinations(A, m):
            x = 0
            for v in comb:
                x ^= v
            if x > ans:
                ans = x
    else:
        t = total
        for comb in combinations(A, m):
            x = 0
            for v in comb:
                x ^= v
            v = t ^ x
            if v > ans:
                ans = v

    print(ans)


if __name__ == "__main__":
    main()