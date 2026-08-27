import sys
import math

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    M = data[1]
    P = data[2:2 + n]

    # cap[i] is the smallest k such that k^2 * P[i] > M.
    caps = [math.isqrt(M // p) + 1 for p in P]

    def cost_gt(x):
        # True iff buying every unit whose marginal cost <= x costs more than M.
        s = 0
        for p, cap in zip(P, caps):
            if x >= p:
                k = (x // p + 1) // 2
                if k >= cap:
                    return True
                s += p * k * k
                if s > M:
                    return True
        return False

    def calc_le(x):
        # Exact count/cost of all units with marginal cost <= x.
        # Called only when this total cost is <= M.
        cnt = 0
        s = 0
        for p in P:
            if x >= p:
                k = (x // p + 1) // 2
                cnt += k
                s += p * k * k
        return cnt, s

    # A unit with marginal cost > M can never be bought.
    if not cost_gt(M):
        ans, _ = calc_le(M)
        print(ans)
        return

    lo, hi = 1, M
    while lo < hi:
        mid = (lo + hi) // 2
        if cost_gt(mid):
            hi = mid
        else:
            lo = mid + 1

    c = lo  # first marginal-cost level whose full inclusion exceeds M
    cnt_lt, cost_lt = calc_le(c - 1)

    eq = 0
    for p in P:
        if c % p == 0 and ((c // p) & 1):
            eq += 1

    rem = (M - cost_lt) // c
    if rem > eq:
        rem = eq
    print(cnt_lt + rem)

main()