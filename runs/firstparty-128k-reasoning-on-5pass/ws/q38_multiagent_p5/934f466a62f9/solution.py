import sys

SHIFT = 17
BASE = 1 << SHIFT
MASK = BASE - 1
SHIFT2 = SHIFT + 1
NEG = -10**30


def calc(p, items, NEG=NEG, MASK=MASK, SHIFT=SHIFT):
    """
    For a fixed per-pair penalty p, run the 8-parity DP.

    Returns:
      adjusted_value: maximum sum of (2*coordinate - p) over selected cakes
      pair_count:     selected_count // 2 among optimal solutions
                      (ties are broken by larger selected_count)
    """
    pB = p << SHIFT
    d0 = 0
    d1 = d2 = d3 = d4 = d5 = d6 = d7 = NEG

    for ax, ay, az in items:
        a = ax - pB
        b = ay - pB
        c = az - pB

        n0 = d0
        t = d1 + a
        if t > n0:
            n0 = t
        t = d2 + b
        if t > n0:
            n0 = t
        t = d4 + c
        if t > n0:
            n0 = t

        n1 = d1
        t = d0 + a
        if t > n1:
            n1 = t
        t = d3 + b
        if t > n1:
            n1 = t
        t = d5 + c
        if t > n1:
            n1 = t

        n2 = d2
        t = d3 + a
        if t > n2:
            n2 = t
        t = d0 + b
        if t > n2:
            n2 = t
        t = d6 + c
        if t > n2:
            n2 = t

        n3 = d3
        t = d2 + a
        if t > n3:
            n3 = t
        t = d1 + b
        if t > n3:
            n3 = t
        t = d7 + c
        if t > n3:
            n3 = t

        n4 = d4
        t = d5 + a
        if t > n4:
            n4 = t
        t = d6 + b
        if t > n4:
            n4 = t
        t = d0 + c
        if t > n4:
            n4 = t

        n5 = d5
        t = d4 + a
        if t > n5:
            n5 = t
        t = d7 + b
        if t > n5:
            n5 = t
        t = d1 + c
        if t > n5:
            n5 = t

        n6 = d6
        t = d7 + a
        if t > n6:
            n6 = t
        t = d4 + b
        if t > n6:
            n6 = t
        t = d2 + c
        if t > n6:
            n6 = t

        n7 = d7
        t = d6 + a
        if t > n7:
            n7 = t
        t = d5 + b
        if t > n7:
            n7 = t
        t = d3 + c
        if t > n7:
            n7 = t

        d0, d1, d2, d3, d4, d5, d6, d7 = n0, n1, n2, n3, n4, n5, n6, n7

    return d0 >> SHIFT, (d0 & MASK) >> 1


def main():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    T = next(it)
    out = []
    calc_local = calc

    for _ in range(T):
        N = next(it)
        K = next(it)

        tx1 = tx2 = ty1 = ty2 = tz1 = tz2 = 0

        if K == 1:
            for _ in range(N):
                x = next(it)
                y = next(it)
                z = next(it)

                if x > tx1:
                    tx2 = tx1
                    tx1 = x
                elif x > tx2:
                    tx2 = x

                if y > ty1:
                    ty2 = ty1
                    ty1 = y
                elif y > ty2:
                    ty2 = y

                if z > tz1:
                    tz2 = tz1
                    tz1 = z
                elif z > tz2:
                    tz2 = z

            ans = max(tx1 + tx2, ty1 + ty2, tz1 + tz2)
            out.append(str(ans))
            continue

        items = []
        append = items.append

        for _ in range(N):
            x = next(it)
            y = next(it)
            z = next(it)

            append(((x << SHIFT2) + 1, (y << SHIFT2) + 1, (z << SHIFT2) + 1))

            if x > tx1:
                tx2 = tx1
                tx1 = x
            elif x > tx2:
                tx2 = x

            if y > ty1:
                ty2 = ty1
                ty1 = y
            elif y > ty2:
                ty2 = y

            if z > tz1:
                tz2 = tz1
                tz1 = z
            elif z > tz2:
                tz2 = z

        pmax = max(tx1 + tx2, ty1 + ty2, tz1 + tz2)

        if pmax == 0:
            out.append("0")
            continue

        # If we must take the maximum possible number of pairs, penalty 0
        # already forces the maximum feasible even count, and tie-breaking
        # by count gives the exact optimum.
        if K == N // 2:
            D, _ = calc_local(0, items)
            out.append(str(D >> 1))
            continue

        lo = 0
        hi = pmax + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            _, cnt = calc_local(mid, items)
            if cnt >= K:
                lo = mid
            else:
                hi = mid

        p = lo
        D, _ = calc_local(p, items)
        ans = (D + 2 * p * K) >> 1
        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()