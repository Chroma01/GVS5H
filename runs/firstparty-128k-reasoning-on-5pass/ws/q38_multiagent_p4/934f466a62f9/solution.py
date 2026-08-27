import sys

SHIFT = 17
MASK = (1 << SHIFT) - 1
NEG = -10**30


def run(p, data, SHIFT=SHIFT, NEG=NEG):
    pshift = p << SHIFT
    d0 = 0
    d1 = d2 = d3 = d4 = d5 = d6 = d7 = NEG

    for ax, ay, az in data:
        dx = ax - pshift
        dy = ay - pshift
        dz = az - pshift

        n0 = d0
        t = d1 + dx
        if t > n0:
            n0 = t
        t = d2 + dy
        if t > n0:
            n0 = t
        t = d4 + dz
        if t > n0:
            n0 = t

        n1 = d1
        t = d0 + dx
        if t > n1:
            n1 = t
        t = d3 + dy
        if t > n1:
            n1 = t
        t = d5 + dz
        if t > n1:
            n1 = t

        n2 = d2
        t = d3 + dx
        if t > n2:
            n2 = t
        t = d0 + dy
        if t > n2:
            n2 = t
        t = d6 + dz
        if t > n2:
            n2 = t

        n3 = d3
        t = d2 + dx
        if t > n3:
            n3 = t
        t = d1 + dy
        if t > n3:
            n3 = t
        t = d7 + dz
        if t > n3:
            n3 = t

        n4 = d4
        t = d5 + dx
        if t > n4:
            n4 = t
        t = d6 + dy
        if t > n4:
            n4 = t
        t = d0 + dz
        if t > n4:
            n4 = t

        n5 = d5
        t = d4 + dx
        if t > n5:
            n5 = t
        t = d7 + dy
        if t > n5:
            n5 = t
        t = d1 + dz
        if t > n5:
            n5 = t

        n6 = d6
        t = d7 + dx
        if t > n6:
            n6 = t
        t = d4 + dy
        if t > n6:
            n6 = t
        t = d2 + dz
        if t > n6:
            n6 = t

        n7 = d7
        t = d6 + dx
        if t > n7:
            n7 = t
        t = d5 + dy
        if t > n7:
            n7 = t
        t = d3 + dz
        if t > n7:
            n7 = t

        d0 = n0
        d1 = n1
        d2 = n2
        d3 = n3
        d4 = n4
        d5 = n5
        d6 = n6
        d7 = n7

    return d0


def main():
    arr = list(map(int, sys.stdin.buffer.read().split()))
    if not arr:
        return

    idx = 0
    T = arr[idx]
    idx += 1

    out = []
    shift = SHIFT
    mask = MASK
    run_dp = run

    for _ in range(T):
        N = arr[idx]
        K = arr[idx + 1]
        idx += 2
        M = K * 2

        cakes = []
        maxd = 0

        for _ in range(N):
            x = arr[idx]
            y = arr[idx + 1]
            z = arr[idx + 2]
            idx += 3

            a = x << 1
            b = y << 1
            c = z << 1

            if a > maxd:
                maxd = a
            if b > maxd:
                maxd = b
            if c > maxd:
                maxd = c

            cakes.append(((a << shift) + 1, (b << shift) + 1, (c << shift) + 1))

        if maxd == 0:
            out.append("0")
            continue

        lo = 0
        hi = maxd + 1
        last_p = -1
        last_d0 = 0

        while lo + 1 < hi:
            mid = (lo + hi) >> 1
            d0 = run_dp(mid, cakes)
            if (d0 & mask) >= M:
                lo = mid
                last_p = mid
                last_d0 = d0
            else:
                hi = mid

        if last_p == lo:
            d0 = last_d0
        else:
            d0 = run_dp(lo, cakes)

        val2 = d0 >> shift
        out.append(str((val2 + lo * M) // 2))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()