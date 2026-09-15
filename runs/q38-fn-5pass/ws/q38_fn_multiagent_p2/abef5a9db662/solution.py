import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    p += 1

    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = data[p]
        R[i] = data[p + 1]
        p += 2

    Q = data[p]
    p += 1
    queries = data[p:p + Q]
    del data

    xs = sorted(set(queries))
    M = len(xs)

    size = 1
    log = 0
    while size < M:
        size <<= 1
        log += 1

    NEG = -10**18
    d = [NEG] * (2 * size)
    d[size:size + M] = xs

    for k in range(size - 1, 0, -1):
        lc = k << 1
        a = d[lc]
        b = d[lc | 1]
        d[k] = a if a >= b else b

    # Length 2*size lets push code update child lazy entries without bounds checks.
    lz = [0] * (2 * size)

    def find_first_ge(x, d=d, lz=lz, size=size, M=M):
        if d[1] < x:
            return M

        k = 1
        while k < size:
            lc = k << 1
            z = lz[k]
            if z:
                rc = lc | 1
                d[lc] += z
                lz[lc] += z
                d[rc] += z
                lz[rc] += z
                lz[k] = 0

            if d[lc] >= x:
                k = lc
            else:
                k = lc | 1

        idx = k - size
        return idx if idx < M else M

    masks = [0] * (log + 1)
    for i in range(1, log + 1):
        masks[i] = (1 << i) - 1

    down = tuple(range(log, 0, -1))
    up = tuple(range(1, log + 1))

    def range_add(l, r, d=d, lz=lz, size=size, down=down, up=up, masks=masks):
        if l >= r:
            return

        # Fast path for a full power-of-two tree.
        if l == 0 and r == size:
            d[1] += 1
            lz[1] += 1
            return

        l += size
        r += size
        l0 = l
        r0 = r

        # Push ancestors of both boundaries.
        for i in down:
            mask = masks[i]

            if l0 & mask:
                k = l0 >> i
                z = lz[k]
                if z:
                    lc = k << 1
                    rc = lc | 1
                    d[lc] += z
                    lz[lc] += z
                    d[rc] += z
                    lz[rc] += z
                    lz[k] = 0

            if r0 & mask:
                k = (r0 - 1) >> i
                z = lz[k]
                if z:
                    lc = k << 1
                    rc = lc | 1
                    d[lc] += z
                    lz[lc] += z
                    d[rc] += z
                    lz[rc] += z
                    lz[k] = 0

        # Apply +1 to covered nodes.
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

        # Recompute ancestors. The push phase guarantees these nodes have no pending tag.
        l = l0
        r = r0
        for i in up:
            mask = masks[i]

            if l & mask:
                k = l >> i
                lc = k << 1
                rc = lc | 1
                a = d[lc]
                b = d[rc]
                d[k] = a if a >= b else b

            if r & mask:
                k = (r - 1) >> i
                lc = k << 1
                rc = lc | 1
                a = d[lc]
                b = d[rc]
                d[k] = a if a >= b else b

    find = find_first_ge
    add = range_add
    Mval = M

    for i in range(N):
        li = L[i]
        root_max = d[1]

        if root_max < li:
            continue

        l = find(li)
        ri = R[i]

        if root_max <= ri:
            r = Mval
        else:
            r = find(ri + 1)

        if l < r:
            add(l, r)

    del L, R

    # Push all remaining lazy tags to leaves.
    for k in range(1, size):
        z = lz[k]
        if z:
            lc = k << 1
            rc = lc | 1
            d[lc] += z
            lz[lc] += z
            d[rc] += z
            lz[rc] += z
            lz[k] = 0

    final_map = dict(zip(xs, d[size:size + M]))
    fm = final_map
    out = [str(fm[x]) for x in queries]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()