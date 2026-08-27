import sys
from math import isqrt

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]
    prices = data[2:]

    min_price = min(prices)

    # For x units of a product with price p, the x-th marginal cost is p(2x-1).
    # Choose a threshold guaranteed to be infeasible.
    x = isqrt(m // min_price) + 1
    hi = min_price * (2 * x - 1)
    lo = 0

    def feasible(threshold):
        total = 0
        for p in prices:
            q = ((threshold // p) + 1) // 2
            total += p * q * q
            if total > m:
                return False
        return True

    # Find the largest integer threshold whose complete set of marginal units
    # costs at most m.
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    threshold = lo
    count = 0
    cost = 0

    for p in prices:
        q = ((threshold // p) + 1) // 2
        count += q
        cost += p * q * q

    # The next marginal cost is threshold + 1. Add as many tied marginals
    # as the remaining budget permits.
    next_count = 0
    for p in prices:
        q = (((threshold + 1) // p) + 1) // 2
        next_count += q

    tied = next_count - count
    extra = min(tied, (m - cost) // (threshold + 1))
    print(count + extra)

if __name__ == "__main__":
    solve()