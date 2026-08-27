import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]
    p = data[2:]

    def affordable(x):
        total = 0
        for price in p:
            count = (x // price + 1) // 2
            total += count * count * price
            if total > m:
                return False
        return True

    lo, hi = 0, m
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if affordable(mid):
            lo = mid
        else:
            hi = mid - 1

    threshold = lo
    total_cost = 0
    total_units = 0
    next_cost = None

    for price in p:
        count = (threshold // price + 1) // 2
        total_units += count
        total_cost += count * count * price

        marginal = (2 * count + 1) * price
        if next_cost is None or marginal < next_cost:
            next_cost = marginal

    remaining = m - total_cost
    total_units += remaining // next_cost

    print(total_units)

if __name__ == "__main__":
    solve()