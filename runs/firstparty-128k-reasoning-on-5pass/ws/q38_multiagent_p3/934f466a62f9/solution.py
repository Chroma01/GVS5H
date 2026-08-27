import sys

SHIFT = 17
MASK = (1 << SHIFT) - 1
NEG = -1 << 70


def calc(p, items, SHIFT=SHIFT, NEG=NEG):
    # Encoded state: value * 2**SHIFT + count.
    # For penalty p, a cake with doubled value 2v contributes (2v - p)*2**SHIFT + 1.
    # Items store 2v * 2**SHIFT, and ps = p*2**SHIFT - 1.
    ps = (p << SHIFT) - 1

    d0 = 0
    d1 = d2 = d3 = d4 = d5 = d6 = d7 = NEG

    for xe, ye, ze in items:
        A = xe - ps
        B = ye - ps
        C = ze - ps

        n0 = d0
        t = d1 + A
        if t > n0: n0 = t
        t = d2 + B
        if t > n0: n0 = t
        t = d4 + C
        if t > n0: n0 = t

        n1 = d1
        t = d0 + A
        if t > n1: n1 = t
        t = d3 + B
        if t > n1: n1 = t
        t = d5 + C
        if t > n1: n1 = t

        n2 = d2
        t = d3 + A
        if t > n2: n2 = t
        t = d0 + B
        if t > n2: n2 = t
        t = d6 + C
        if t > n2: n2 = t

        n3 = d3
        t = d2 + A
        if t > n3: n3 = t
        t = d1 + B
        if t > n3: n3 = t
        t = d7 + C
        if t > n3: n3 = t

        n4 = d4
        t = d5 + A
        if t > n4: n4 = t
        t = d6 + B
        if t > n4: n4 = t
        t = d0 + C
        if t > n4: n4 = t

        n5 = d5
        t = d4 + A
        if t > n5: n5 = t
        t = d7 + B
        if t > n5: n5 = t
        t = d1 + C
        if t > n5: n5 = t

        n6 = d6
        t = d7 + A
        if t > n6: n6 = t
        t = d4 + B
        if t > n6: n6 = t
        t = d2 + C
        if t > n6: n6 = t

        n7 = d7
        t = d6 + A
        if t > n7: n7 = t
        t = d5 + B
        if t > n7: n7 = t
        t = d3 + C
        if t > n7: n7 = t

        d0 = n0
        d1 = n1
        d2 = n2
        d3 = n3
        d4 = n4
        d5 = n5
        d6 = n6
        d7 = n7

    return d0


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    idx = 0
    T = data[idx]
    idx += 1

    out = []
    append_out = out.append
    mask = MASK
    shift = SHIFT
    calc_func = calc

    for _ in range(T):
        N = data[idx]
        K = data[idx + 1]
        idx += 2

        tx1 = tx2 = ty1 = ty2 = tz1 = tz2 = 0

        # For K = 1, the answer is simply max_d (top1_d + top2_d).
        if K == 1:
            for i in range(N):
                x = data[idx]
                y = data[idx + 1]
                z = data[idx + 2]
                idx += 3

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

            B = max(tx1 + tx2, ty1 + ty2, tz1 + tz2)
            append_out(str(B))
            continue

        items = [None] * N
        for i in range(N):
            x = data[idx]
            y = data[idx + 1]
            z = data[idx + 2]
            idx += 3

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

            # x << 18 = 2*x * 2**17
            items[i] = (x << 18, y << 18, z << 18)

        B = max(tx1 + tx2, ty1 + ty2, tz1 + tz2)
        if B == 0:
            append_out("0")
            continue

        target = K << 1
        lo = 0
        hi = B + 1

        while lo + 1 < hi:
            mid = (lo + hi) >> 1
            enc = calc_func(mid, items)
            if (enc & mask) >= target:
                lo = mid
            else:
                hi = mid

        enc = calc_func(lo, items)
        val = enc >> shift
        ans = (val + lo * target) // 2
        append_out(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()