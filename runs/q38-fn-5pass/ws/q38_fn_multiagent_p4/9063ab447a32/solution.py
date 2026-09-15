import sys
from math import isqrt
from bisect import bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    M = data[1]

    # Products with P_i > M can never be bought.
    P = [p for p in data[2:2 + N] if p <= M]
    del data

    if not P:
        print(0)
        return

    P.sort()
    pmin = P[0]
    last = P[-1]
    total_sum = sum(P)

    # Safe unaffordable upper bounds.
    # 1) Only the cheapest products already exceed M.
    cnt_min = bisect_right(P, pmin)
    base = pmin * cnt_min
    k = isqrt(M // base) + 1
    high = pmin * (2 * k - 1)

    # 2) All products have at least k units.
    k_all = isqrt(M // total_sum) + 1
    high_all = last * (2 * k_all - 1)
    if high_all < high:
        high = high_all

    def affordable(c, P=P, limit=M, pmin=pmin, last=last):
        if c < pmin:
            return True

        total = 0

        if c >= last:
            for p in P:
                k = (c // p + 1) >> 1
                total += p * k * k
                if total > limit:
                    return False
            return True

        for p in P:
            if p > c:
                break
            k = (c // p + 1) >> 1
            total += p * k * k
            if total > limit:
                return False
        return True

    low = 0
    while high - low > 1:
        mid = (low + high) >> 1
        if affordable(mid):
            low = mid
        else:
            high = mid

    C = low

    total = 0
    cnt = 0

    if C >= last:
        for p in P:
            k = (C // p + 1) >> 1
            total += p * k * k
            cnt += k
    else:
        for p in P:
            if p > C:
                break
            k = (C // p + 1) >> 1
            total += p * k * k
            cnt += k

    rem = M - total
    ans = cnt + rem // (C + 1)
    print(ans)


if __name__ == "__main__":
    main()