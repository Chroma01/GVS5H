import sys
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    p = [int(x) for x in data[2:2 + n]]
    p.sort()

    max_p = p[-1]

    # Safe upper bound for the maximum feasible marginal-cost threshold.
    upper = 2 * isqrt(m * max_p) + max_p + 5

    def feasible(c, ps=p, limit=m, max_p=max_p):
        total = 0

        # If c is at least the largest price, no early break by p > c is needed.
        if c >= max_p:
            for q in ps:
                x = (c // q + 1) >> 1
                total += q * x * x
                if total > limit:
                    return False
            return True

        # Otherwise, sorted prices allow stopping once q > c.
        for q in ps:
            if q > c:
                break
            x = (c // q + 1) >> 1
            total += q * x * x
            if total > limit:
                return False
        return True

    # Binary search the largest feasible threshold C.
    lo, hi = 0, upper
    while lo < hi:
        mid = (lo + hi + 1) >> 1
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    c = lo

    # Compute exact units and cost for threshold c.
    units = 0
    cost = 0

    if c >= max_p:
        for q in p:
            x = (c // q + 1) >> 1
            units += x
            cost += q * x * x
    else:
        for q in p:
            if q > c:
                break
            x = (c // q + 1) >> 1
            units += x
            cost += q * x * x

    # Since c is maximal feasible, c + 1 is the next marginal cost.
    ans = units + (m - cost) // (c + 1)
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()