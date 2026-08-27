import sys
from math import isqrt
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    M = int(data[1])
    plist = list(map(int, data[2:2 + N]))
    P = np.array(plist, dtype=np.int64)

    # Cap on units per product: any k > isqrt(M//p) costs more than M by itself,
    # so capping at isqrt(M//p)+1 never removes an economically relevant unit.
    # With this cap, k*k*p <= M + (2*isqrt(M//p)+1)*p <= ~1.001e18 < 2^63, so
    # per-element int64 arithmetic is overflow-safe.
    Kcap = np.array([isqrt(M // p) + 1 for p in plist], dtype=np.int64)

    # Float64 precheck margin: pairwise-summation relative error is ~1e-15,
    # so when the float sum <= M + 1e8 the true sum is <= ~1.0002e18 and an
    # exact int64 sum cannot overflow; when it is > M + 1e8 the true sum is
    # certainly > M.
    FLIMIT = M + 100_000_000

    def cost_le_M(T):
        """Return exact total cost of all units with marginal cost <= T if it
        is <= M, else None."""
        k = (T // P + 1) // 2
        np.minimum(k, Kcap, out=k)
        c = k * k
        c *= P
        if c.sum(dtype=np.float64) > FLIMIT:
            return None
        s = int(c.sum(dtype=np.int64))
        return s if s <= M else None

    # Largest threshold T in [0, M] with cost(T) <= M.
    lo, hi = 0, M + 1  # invariant: cost(lo) <= M; hi exclusive
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if cost_le_M(mid) is not None:
            lo = mid
        else:
            hi = mid

    # Final answer: all units with marginal cost <= lo, plus as many units at
    # the cheapest remaining marginal cost L as the leftover budget allows.
    k = (lo // P + 1) // 2
    np.minimum(k, Kcap, out=k)
    cnt = int(k.sum(dtype=np.int64))
    cost = int((k * k * P).sum(dtype=np.int64))  # <= M, no overflow
    R = M - cost
    L = int(((2 * k + 1) * P).min())  # cheapest unit not yet bought
    print(cnt + R // L)


main()