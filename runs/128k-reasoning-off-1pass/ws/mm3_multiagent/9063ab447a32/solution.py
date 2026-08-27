import sys
import math

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]
    P.sort()  # ascending, cheapest first

    # Helper: integer square root (floor)
    def isqrt_floor(x: int) -> int:
        if x < 0:
            return 0
        return math.isqrt(x)

    # Check if we can buy total S units without exceeding cost M
    def can(S: int) -> bool:
        remaining = S
        cost = 0
        for p in P:
            if remaining == 0:
                break
            # max units we can take from this product (also 0 if p > M // remaining^2 later)
            cap = isqrt_floor(M // p) if p != 0 else 10**18
            if cap <= 0:
                # we cannot take more from this product, but maybe later products?
                # Since p is sorted ascending, if cap==0 for this p, it is 0 for all larger p too
                # because M//p decreases as p increases.
                break
            take = remaining if remaining < cap else cap
            remaining -= take
            # accumulate cost, but careful about overflow: use Python's big int, safe.
            cost += take * take * p
            if cost > M:
                return False
        return remaining == 0

    # Upper bound for answer:
    # If we used the cheapest product alone, max units = floor(sqrt(M / P_min))
    max_units = isqrt_floor(M // P[0]) if P[0] != 0 else 10**18
    # The answer cannot exceed N * max_units (we can't take more than that from cheapest product per type, but
    # actually a better bound: total units <= N * floor(sqrt(M / min(P))) (since each product i can contribute at most
    # floor(sqrt(M / P_i)) ≤ floor(sqrt(M / min(P)))).
    hi = N * max_units
    lo = 0
    # Binary search for max feasible S
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()