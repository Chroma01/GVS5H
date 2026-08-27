import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N = data[idx]
    idx += 1

    MAXX = 500000
    SIZE = 1 << (MAXX - 1).bit_length()

    # d[k] = max of segment, including lazy[k] but not ancestors' lazy
    d = [0] * (2 * SIZE)
    d[SIZE:SIZE + MAXX] = range(1, MAXX + 1)

    for i in range(SIZE - 1, 0, -1):
        a = d[i << 1]
        b = d[i << 1 | 1]
        d[i] = a if a >= b else b

    # lz is allocated for leaves too; leaf lazy values are harmless and avoid bounds checks.
    lz = [0] * (2 * SIZE)

    def lower_bound(v, d=d, lz=lz, SIZE=SIZE, MAXX=MAXX):
        """First index i with A[i] >= v, or MAXX if none."""
        if d[1] < v:
            return MAXX

        k = 1
        acc = 0  # accumulated lazy from ancestors
        while k < SIZE:
            z = lz[k]
            lc = k << 1
            # actual max of left child = d[lc] + ancestor lazy + lazy[k]
            if d[lc] + acc + z >= v:
                k = lc
            else:
                k = lc | 1
            acc += z

        i = k - SIZE
        return i if i < MAXX else MAXX

    def range_add(l, r, d=d, lz=lz, SIZE=SIZE):
        """Add 1 to A[l:r]."""
        l += SIZE
        r += SIZE
        l0 = l
        r0 = r

        while l < r:
            if l & 1:
                d[l] += 1
                lz[l] += 1
                l += 1
            if r & 1:
                r -= 1
                d[r] += 1
                lz[r] += 1
            l >>= 1
            r >>= 1

        # Pull boundary ancestors bottom-up.
        l = l0 >> 1
        r = (r0 - 1) >> 1
        while l:
            lc = l << 1
            a = d[lc]
            b = d[lc | 1]
            d[l] = (a if a >= b else b) + lz[l]

            if r != l:
                lc = r << 1
                a = d[lc]
                b = d[lc | 1]
                d[r] = (a if a >= b else b) + lz[r]

            l >>= 1
            r >>= 1

    for _ in range(N):
        L = data[idx]
        R = data[idx + 1]
        idx += 2

        if L == 1:
            l = 0
        else:
            l = lower_bound(L)
            if l == MAXX:
                continue

        r = lower_bound(R + 1)
        if l < r:
            range_add(l, r)

    # Push all lazy values down to leaves.
    for k in range(1, SIZE):
        z = lz[k]
        if z:
            lc = k << 1
            rc = lc | 1
            d[lc] += z
            d[rc] += z
            lz[lc] += z
            lz[rc] += z
            lz[k] = 0

    Q = data[idx]
    idx += 1

    out = []
    append = out.append
    base = SIZE
    for _ in range(Q):
        x = data[idx]
        idx += 1
        append(str(d[base + x - 1]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()