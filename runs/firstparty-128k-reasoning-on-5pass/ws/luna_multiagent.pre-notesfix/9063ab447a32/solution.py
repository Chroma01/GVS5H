import sys
import math


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    p = list(map(int, input().split()))

    pmin = min(p)
    qmax = math.isqrt(m // pmin) + 1
    hi = (2 * qmax - 1) * pmin
    lo = 0

    def cost_at(t):
        total = 0
        for x in p:
            q = (t // x + 1) // 2
            total += q * q * x
            if total > m:
                return total
        return total

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost_at(mid) <= m:
            lo = mid
        else:
            hi = mid

    total_cost = 0
    total_units = 0
    next_cost = None

    for x in p:
        q = (lo // x + 1) // 2
        total_units += q
        total_cost += q * q * x
        candidate = (2 * q + 1) * x
        if next_cost is None or candidate < next_cost:
            next_cost = candidate

    remaining = m - total_cost
    total_units += remaining // next_cost

    print(total_units)


if __name__ == "__main__":
    solve()