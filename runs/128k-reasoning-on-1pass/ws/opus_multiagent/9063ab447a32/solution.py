import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P_all = np.array(data[2:2 + n], dtype=np.int64)

    # compress duplicates
    P, counts = np.unique(P_all, return_counts=True)
    counts = counts.astype(np.int64)

    M64 = np.int64(M)
    MdivP = M64 // P  # elementwise floor division, each <= 1e18

    MASK = np.int64((1 << 30) - 1)
    CAP = np.int64(10 ** 9 + 1)

    def evaluate(x):
        """Return (ok, cost, units) for threshold x: buy all units with marginal cost <= x."""
        xx = np.int64(x)
        k = (xx // P + np.int64(1)) // np.int64(2)
        kk = np.minimum(k, CAP)
        t = kk * kk  # <= ~1e18, safe
        if np.any(t > MdivP):
            return (False, 0, 0)
        term = P * t  # each <= M <= 1e18, safe
        hi_part = int(np.sum((term >> np.int64(30)) * counts))
        lo_part = int(np.sum((term & MASK) * counts))
        cost = (hi_part << 30) + lo_part
        if cost > M:
            return (False, cost, 0)
        units = int(np.sum(k * counts))
        return (True, cost, units)

    lo = 0                 # always feasible (cost 0)
    hi = 200000000000000   # 2e14, guaranteed infeasible
    # sanity: ensure hi infeasible; if somehow feasible, expand (shouldn't happen)
    while evaluate(hi)[0]:
        lo = hi
        hi *= 2

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if evaluate(mid)[0]:
            lo = mid
        else:
            hi = mid

    ok, cost, units = evaluate(lo)
    price = lo + 1
    rem = M - cost
    pr = np.int64(price)
    mask_div = (pr % P == 0)
    q = pr // P
    mask_odd = (q & np.int64(1)) == np.int64(1)
    c = int(np.sum(counts[mask_div & mask_odd]))
    extra = min(c, rem // price)
    print(units + extra)

main()