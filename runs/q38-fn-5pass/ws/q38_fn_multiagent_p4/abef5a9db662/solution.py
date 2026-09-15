import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    intervals_start = 1
    q_pos = 1 + 2 * N
    Q = data[q_pos]
    queries_start = q_pos + 1

    vals = sorted(set(data[queries_start:queries_start + Q]))
    M = len(vals)

    size = 1 << (M - 1).bit_length()
    log = size.bit_length() - 1

    NEG = -10**9
    mx = [NEG] * (2 * size)

    base = size
    for i, v in enumerate(vals):
        mx[base + i] = v

    for k in range(size - 1, 0, -1):
        left = k << 1
        a = mx[left]
        b = mx[left + 1]
        if b > a:
            a = b
        mx[k] = a

    lazy = [0] * size
    levels = list(range(1, log + 1))

    def first_ge(x, mx=mx, lazy=lazy, size=size, M=M):
        if mx[1] < x:
            return M

        k = 1
        need = x

        while k < size:
            lz = lazy[k]
            left = k << 1

            if mx[left] + lz >= need:
                k = left
            else:
                k = left + 1

            need -= lz

        idx = k - size
        if idx >= M:
            return M
        return idx

    def range_add(l, r, mx=mx, lazy=lazy, size=size, levels=levels):
        if l > r:
            return

        l += size
        r += size + 1
        l0 = l
        r0 = r - 1

        while l < r:
            if l & 1:
                mx[l] += 1
                if l < size:
                    lazy[l] += 1
                l += 1

            if r & 1:
                r -= 1
                mx[r] += 1
                if r < size:
                    lazy[r] += 1

            l >>= 1
            r >>= 1

        for i in levels:
            k = l0 >> i
            left = k << 1
            a = mx[left]
            b = mx[left + 1]
            if b > a:
                a = b
            mx[k] = a + lazy[k]

            k2 = r0 >> i
            if k2 != k:
                left = k2 << 1
                a = mx[left]
                b = mx[left + 1]
                if b > a:
                    a = b
                mx[k2] = a + lazy[k2]

    fg = first_ge
    ra = range_add
    p = intervals_start
    end = intervals_start + 2 * N
    d = data
    m = M

    while p < end:
        L = d[p]
        R = d[p + 1]
        p += 2

        l = fg(L)
        if l == m:
            continue

        r = fg(R + 1) - 1
        if l <= r:
            ra(l, r)

    queries = data[queries_start:queries_start + Q]
    del data, d

    for k in range(1, size):
        z = lazy[k]
        if z:
            left = k << 1
            right = left + 1

            mx[left] += z
            if left < size:
                lazy[left] += z

            mx[right] += z
            if right < size:
                lazy[right] += z

            lazy[k] = 0

    pos = {v: i for i, v in enumerate(vals)}
    del vals

    out = [None] * Q
    get = pos.__getitem__
    mx_local = mx
    base = size

    for i, x in enumerate(queries):
        out[i] = str(mx_local[base + get(x)])

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()