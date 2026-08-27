import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = list(map(int, data[2:2 + n]))

    def count_cost(T):
        # units with marginal cost (2j-1)*P_i <= T
        total_units = 0
        total_cost = 0
        for p in P:
            k = (T // p + 1) // 2
            total_units += k
            total_cost += k * k * p
            if total_cost > M:
                # early exit; still return units (not used when infeasible)
                return total_units, total_cost
        return total_units, total_cost

    # Find hi with cost(hi) > M by doubling
    lo = 0
    hi = 1
    while True:
        _, c = count_cost(hi)
        if c > M:
            break
        hi *= 2

    # Binary search largest T in [lo, hi) with cost(T) <= M
    # invariant: cost(lo) <= M, cost(hi) > M
    while hi - lo > 1:
        mid = (lo + hi) // 2
        _, c = count_cost(mid)
        if c <= M:
            lo = mid
        else:
            hi = mid

    units, cost = count_cost(lo)
    # Next cheapest units have marginal cost exactly hi = lo + 1
    # (since cost(hi) > M >= cost(lo), at least one unit has marginal hi,
    #  and there are more such units than the remaining budget can afford)
    ans = units + (M - cost) // hi
    print(ans)

solve()