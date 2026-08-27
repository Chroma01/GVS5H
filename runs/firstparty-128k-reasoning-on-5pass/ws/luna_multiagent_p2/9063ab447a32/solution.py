import sys
import math


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]
    p = data[2:]

    p_min = min(p)
    s = math.isqrt(m // p_min)
    hi = 2 * p_min * (s + 2)
    lo = 0

    def cost_at(t):
        total = 0
        for v in p:
            count = (t // v + 1) // 2
            total += v * count * count
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

    for v in p:
        count = (lo // v + 1) // 2
        total_units += count
        total_cost += v * count * count
        marginal = v * (2 * count + 1)
        if next_cost is None or marginal < next_cost:
            next_cost = marginal

    total_units += (m - total_cost) // next_cost
    print(total_units)


if __name__ == "__main__":
    solve()