import sys
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    P = list(map(int, data[2:2 + n]))

    pmin = min(P)
    # Valid upper bound on the threshold: force the cheapest product to
    # have k units with pmin*k^2 > m.  k = isqrt(m//pmin)+1, marginal = (2k-1)*pmin.
    hi = (2 * (isqrt(m // pmin) + 1) - 1) * pmin
    lo = 0

    # smallest X such that C(X) = sum_i P_i * k_i(X)^2 > m,
    # where k_i(X) = number of units of product i whose marginal cost
    # P_i*(2k-1) is <= X  =>  k = (X//P_i + 1)//2
    while lo < hi:
        mid = (lo + hi) >> 1
        c = 0
        for p in P:
            k = (mid // p + 1) >> 1
            c += p * k * k
            if c > m:
                break
        if c > m:
            hi = mid
        else:
            lo = mid + 1

    X = lo
    if X == 0:
        print(0)
        return
    xm = X - 1

    # buy all units with marginal cost < X  (i.e. <= X-1)
    cb = 0   # their total cost  = C(X-1)
    cn = 0   # their count
    ca = 0   # units with marginal cost exactly X
    for p in P:
        km = (xm // p + 1) >> 1
        cb += p * km * km
        cn += km
        ca += ((X // p + 1) >> 1) - km

    extra = (m - cb) // X     # affordable extra units at marginal X
    if extra > ca:            # cap by availability (never actually binds)
        extra = ca

    print(cn + extra)


main()