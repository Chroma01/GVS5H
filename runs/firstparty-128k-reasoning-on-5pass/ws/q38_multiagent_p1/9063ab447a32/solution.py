import sys
from math import isqrt
from bisect import bisect_left


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    M = data[1]
    P = data[2:2 + N]
    del data

    if not P:
        print(0)
        return

    pmin = min(P)
    if pmin > M:
        print(0)
        return

    P.sort()

    q = isqrt(M // pmin) + 1
    hi = pmin * (2 * q - 1)

    # For every feasible T we have T < hi, so products with p >= hi never contribute.
    idx = bisect_left(P, hi)
    if idx < len(P):
        P = P[:idx]

    # Compress equal P values when it is likely to help.
    use_comp = False
    vals = weights = counts = None
    if len(P) > 1:
        vals = []
        weights = []
        counts = []
        prev = P[0]
        cnt = 1
        for p in P[1:]:
            if p == prev:
                cnt += 1
            else:
                vals.append(prev)
                counts.append(cnt)
                weights.append(prev * cnt)
                prev = p
                cnt = 1
        vals.append(prev)
        counts.append(cnt)
        weights.append(prev * cnt)

        if len(vals) * 2 <= len(P):
            use_comp = True
        else:
            vals = weights = counts = None

    M_local = M

    if use_comp:
        vals_local = vals
        weights_local = weights
        counts_local = counts

        def ok(T, M=M_local, vals=vals_local, weights=weights_local, zip_=zip):
            s = 0
            for p, w in zip_(vals, weights):
                if p > T:
                    break
                c = (T // p + 1) >> 1
                s += w * c * c
                if s > M:
                    return False
            return True
    else:
        P_local = P

        def ok(T, M=M_local, P=P_local):
            s = 0
            for p in P:
                if p > T:
                    break
                c = (T // p + 1) >> 1
                s += p * c * c
                if s > M:
                    return False
            return True

    # T = pmin - 1 is always feasible: no marginal cost is <= pmin - 1.
    lo = pmin - 1
    while lo + 1 < hi:
        mid = (lo + hi) >> 1
        if ok(mid):
            lo = mid
        else:
            hi = mid

    T = lo

    if use_comp:
        C = 0
        S = 0
        for p, w, cnt in zip(vals_local, weights_local, counts_local):
            if p > T:
                break
            c = (T // p + 1) >> 1
            C += cnt * c
            S += w * c * c
    else:
        C = 0
        S = 0
        for p in P_local:
            if p > T:
                break
            c = (T // p + 1) >> 1
            C += c
            S += p * c * c

    ans = C + (M - S) // (T + 1)
    print(ans)


if __name__ == "__main__":
    main()