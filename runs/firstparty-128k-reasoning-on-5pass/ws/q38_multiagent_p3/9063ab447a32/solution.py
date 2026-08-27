import sys
from math import isqrt

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    M = data[1]
    P = data[2:2 + N]
    del data

    P.sort()
    pmin = P[0]

    # Valid upper bound: marginal cost of the (isqrt(M // pmin) + 1)-th
    # unit of a cheapest product. Its cumulative cost alone exceeds M.
    hi = 2 * pmin * isqrt(M // pmin) + pmin
    limit = M + 1

    def cost_leq(x, P=P, limit=limit):
        total = 0
        for p in P:
            if p > x:
                break
            c = (x + p) // (p + p)
            total += p * c * c
            if total >= limit:
                return limit
        return total

    lo = 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost_leq(mid) >= limit:
            hi = mid
        else:
            lo = mid

    T = hi
    x = lo  # T - 1

    cnt = 0
    total = 0
    for p in P:
        if p > x:
            break
        c = (x + p) // (p + p)
        cnt += c
        total += p * c * c

    ans = cnt + (M - total) // T
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    solve()