import sys
from math import isqrt

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    M = data[1]
    P = data[2:2 + N]
    del data

    P.sort()

    pairs = []
    pairs_fp = []

    it = iter(P)
    prev = next(it)
    cnt = 1
    for x in it:
        if x == prev:
            cnt += 1
        else:
            pairs.append((prev, cnt))
            pairs_fp.append((prev, cnt * prev))
            prev = x
            cnt = 1
    pairs.append((prev, cnt))
    pairs_fp.append((prev, cnt * prev))

    min_p = P[0]
    del P

    hi = min_p * (2 * isqrt(M // min_p) + 1)
    lo = 0

    def feasible(C, pairs=pairs_fp, M=M):
        total = 0
        for p, fp in pairs:
            if p > C:
                break
            t = (C // p + 1) >> 1
            total += fp * t * t
            if total > M:
                return False
        return True

    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    C = lo

    A = 0
    B = 0
    D = 10 ** 30
    countD = 0

    for p, f in pairs:
        t = (C // p + 1) >> 1
        if t:
            A += f * t
            B += f * p * t * t

        d = p * (2 * t + 1)
        if d < D:
            D = d
            countD = f
        elif d == D:
            countD += f

    extra = (M - B) // D
    if extra > countD:
        extra = countD

    print(A + extra)

if __name__ == "__main__":
    main()