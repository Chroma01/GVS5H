import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]
    # Sort descending so the running cost blows up early (early break helps).
    P.sort(reverse=True)

    def eval_T(T):
        # Returns (total_units, total_cost) for buying every marginal <= T.
        # Cost may exceed M (we break early).
        s = 0
        c = 0
        for p in P:
            k = (T // p + 1) // 2
            if k:
                s += k
                c += k * k * p
                if c > M:
                    return s, c
        return s, c

    lo = 0                  # C(lo) <= M always (k_i(0) = 0)
    hi = 3 * 10**14         # C(hi) > M always (proved in notes)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        _, c = eval_T(mid)
        if c <= M:
            lo = mid
        else:
            hi = mid

    # Recompute exact stats at lo.
    ks = [(lo // p + 1) // 2 for p in P]
    S = sum(ks)
    C = sum(k * k * p for k, p in zip(ks, P))

    # Cheapest remaining marginal unit.
    T_next = min((2 * k + 1) * p for k, p in zip(ks, P))
    cnt_next = sum(1 for k, p in zip(ks, P) if (2 * k + 1) * p == T_next)

    extra = (M - C) // T_next
    if extra > cnt_next:
        extra = cnt_next  # cannot trigger if lo is truly maximal; safety cap

    print(S + extra)

solve()