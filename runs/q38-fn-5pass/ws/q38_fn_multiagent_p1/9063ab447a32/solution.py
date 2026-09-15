import sys
from math import isqrt


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    m = data[1]
    p = data[2:2 + n]

    if not p:
        print(0)
        return

    p.sort()
    sum_p = sum(p)
    min_p = p[0]
    max_p = p[-1]

    # Safe infeasible upper bound from the cheapest product alone.
    k = isqrt(m // min_p) + 1
    high = (2 * k - 1) * min_p

    # Safe infeasible upper bound from all products together.
    k = isqrt(m // sum_p) + 1
    high_all = (2 * k - 1) * max_p
    if high_all < high:
        high = high_all

    low = 0
    ps = p
    mm = m
    mp = max_p

    # Binary search the largest marginal-cost cutoff X with total cost <= M.
    while high - low > 1:
        mid = (low + high) // 2
        total = 0

        if mid >= mp:
            for pi in ps:
                t = (mid // pi + 1) >> 1
                total += pi * t * t
                if total > mm:
                    break
        else:
            for pi in ps:
                if pi > mid:
                    break
                t = (mid // pi + 1) >> 1
                total += pi * t * t
                if total > mm:
                    break

        if total <= mm:
            low = mid
        else:
            high = mid

    x = low

    total = 0
    count = 0

    if x >= mp:
        for pi in ps:
            t = (x // pi + 1) >> 1
            total += pi * t * t
            count += t
    else:
        for pi in ps:
            if pi > x:
                break
            t = (x // pi + 1) >> 1
            total += pi * t * t
            count += t

    # Since x is the largest feasible integer, x + 1 is the next marginal cost.
    ans = count + (mm - total) // (x + 1)
    print(ans)


if __name__ == "__main__":
    solve()