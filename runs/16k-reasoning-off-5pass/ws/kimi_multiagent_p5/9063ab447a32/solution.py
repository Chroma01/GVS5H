import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = list(map(int, data[2:2 + n]))

    # Marginal cost of the j-th unit (1-indexed) of product i is (2j-1)*P_i.
    # For a threshold T, product i contributes k_i = max j with (2j-1)*P_i <= T,
    # i.e. k_i = (T // P_i + 1) // 2, costing k_i^2 * P_i.

    def cost_leq(T, limit):
        # total cost of buying all units with marginal cost <= T; early exit > limit
        total = 0
        for p in P:
            k = (T // p + 1) // 2
            if k:
                total += k * k * p
                if total > limit:
                    return total
        return total

    # Binary search the largest T with S(T) <= M.
    # Upper bound: worst case P_i = 1, all budget on one product -> ~sqrt(M) units,
    # marginal ~ 2*sqrt(M) * maxP. 4e18 is a safe loose bound.
    lo, hi = 0, 4 * 10**18
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost_leq(mid, M) <= M:
            lo = mid
        else:
            hi = mid - 1
    T = lo

    # Recompute count and cost at T exactly.
    count = 0
    cost = 0
    for p in P:
        k = (T // p + 1) // 2
        if k:
            count += k
            cost += k * k * p

    # Remaining budget buys extra units; each costs at least T+1, and there are
    # strictly more products offering marginal exactly T+1 than we can afford
    # (otherwise S(T+1) <= M, contradicting maximality of T).
    answer = count + (M - cost) // (T + 1)
    print(answer)

solve()