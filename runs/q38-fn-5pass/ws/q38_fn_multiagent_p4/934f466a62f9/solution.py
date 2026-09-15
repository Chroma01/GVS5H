import sys

# BASE must be larger than the maximum possible selected-cake count (<= 1e5).
SHIFT = 17
BASE = 1 << SHIFT
MASK = BASE - 1
NEG = -(1 << 80)


def calc(C, cakes, _SHIFT=SHIFT, _NEG=NEG):
    """
    Returns packed key for penalty C per pair.

    key = adjusted_doubled_value * BASE + selected_count
    adjusted_doubled_value = 2 * assigned_sum - 2 * C * pairs
    """
    CB = C << _SHIFT

    o0 = 0
    o1 = o2 = o3 = o4 = o5 = o6 = o7 = _NEG

    for xB1, yB1, zB1 in cakes:
        ax = xB1 - CB
        ay = yB1 - CB
        az = zB1 - CB

        # mask 0: sources 1(X), 2(Y), 4(Z)
        n0 = o0
        v = o1 + ax
        if v > n0:
            n0 = v
        v = o2 + ay
        if v > n0:
            n0 = v
        v = o4 + az
        if v > n0:
            n0 = v

        # mask 1: sources 0(X), 3(Y), 5(Z)
        n1 = o1
        v = o0 + ax
        if v > n1:
            n1 = v
        v = o3 + ay
        if v > n1:
            n1 = v
        v = o5 + az
        if v > n1:
            n1 = v

        # mask 2: sources 3(X), 0(Y), 6(Z)
        n2 = o2
        v = o3 + ax
        if v > n2:
            n2 = v
        v = o0 + ay
        if v > n2:
            n2 = v
        v = o6 + az
        if v > n2:
            n2 = v

        # mask 3: sources 2(X), 1(Y), 7(Z)
        n3 = o3
        v = o2 + ax
        if v > n3:
            n3 = v
        v = o1 + ay
        if v > n3:
            n3 = v
        v = o7 + az
        if v > n3:
            n3 = v

        # mask 4: sources 5(X), 6(Y), 0(Z)
        n4 = o4
        v = o5 + ax
        if v > n4:
            n4 = v
        v = o6 + ay
        if v > n4:
            n4 = v
        v = o0 + az
        if v > n4:
            n4 = v

        # mask 5: sources 4(X), 7(Y), 1(Z)
        n5 = o5
        v = o4 + ax
        if v > n5:
            n5 = v
        v = o7 + ay
        if v > n5:
            n5 = v
        v = o1 + az
        if v > n5:
            n5 = v

        # mask 6: sources 7(X), 4(Y), 2(Z)
        n6 = o6
        v = o7 + ax
        if v > n6:
            n6 = v
        v = o4 + ay
        if v > n6:
            n6 = v
        v = o2 + az
        if v > n6:
            n6 = v

        # mask 7: sources 6(X), 5(Y), 3(Z)
        n7 = o7
        v = o6 + ax
        if v > n7:
            n7 = v
        v = o5 + ay
        if v > n7:
            n7 = v
        v = o3 + az
        if v > n7:
            n7 = v

        o0 = n0
        o1 = n1
        o2 = n2
        o3 = n3
        o4 = n4
        o5 = n5
        o6 = n6
        o7 = n7

    return o0


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    T = data[p]
    p += 1

    out = []
    shift = SHIFT
    mask = MASK

    for _ in range(T):
        N = data[p]
        K = data[p + 1]
        p += 2

        cakes = []
        max2 = 0

        for _ in range(N):
            x = data[p]
            y = data[p + 1]
            z = data[p + 2]
            p += 3

            xx = x + x
            yy = y + y
            zz = z + z

            if xx > max2:
                max2 = xx
            if yy > max2:
                max2 = yy
            if zz > max2:
                max2 = zz

            # Precompute (2*attr)*BASE + 1.
            cakes.append(((xx << shift) + 1, (yy << shift) + 1, (zz << shift) + 1))

        if K == 0:
            out.append("0")
            continue

        target = K << 1

        # C is the penalty per pair.
        # hi is exclusive and false: C > max doubled attribute makes every pair negative.
        lo = 0
        hi = max2 + 1

        while hi - lo > 1:
            mid = (lo + hi) >> 1
            key = calc(mid, cakes)
            cnt = key & mask
            if cnt >= target:
                lo = mid
            else:
                hi = mid

        key = calc(lo, cakes)
        val2 = key >> shift
        ans = (val2 + 2 * lo * K) // 2
        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()