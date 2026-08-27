import sys
from math import isqrt
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2+N]]
    P.sort()
    if P[0] > M:
        print(0)
        return

    # Products whose first unit already costs more than M can never be bought.
    idx = bisect_right(P, M)
    if idx < N:
        P = P[:idx]

    p = P[0]
    s = isqrt(M // p)
    hi = 2 * p * s + p + 1

    # Products with first unit above hi never appear in the searched range.
    idx = bisect_right(P, hi)
    if idx < len(P):
        P = P[:idx]

    def ok(x, P=P, M=M):
        total = 0
        for p_i in P:
            if p_i > x:
                break
            c = (x // p_i + 1) >> 1
            total += c * c * p_i
            if total > M:
                return False
        return True

    lo = 0
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if ok(mid):
            lo = mid
        else:
            hi = mid

    X = lo
    f = 0
    g = 0
    for p_i in P:
        if p_i > X:
            break
        c = (X // p_i + 1) >> 1
        f += c
        g += c * c * p_i

    ans = f + (M - g) // (X + 1)
    print(ans)

if __name__ == "__main__":
    main()