import sys
import gc


def main():
    gc.disable()

    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    contest_start = 1
    q_index = contest_start + 2 * N
    Q = data[q_index]
    query_start = q_index + 1

    # Only initial ratings that appear in queries are needed.
    max_x = 0
    for i in range(Q):
        x = data[query_start + i]
        if x > max_x:
            max_x = x

    present = bytearray(max_x + 1)
    for i in range(Q):
        present[data[query_start + i]] = 1

    pos = [0] * (max_x + 1)
    vals = []
    append_val = vals.append
    idx = 0
    for x in range(1, max_x + 1):
        if present[x]:
            pos[x] = idx
            append_val(x)
            idx += 1
    del present

    U = idx
    if U == 0:
        return

    size = 1
    while size < U:
        size <<= 1
    log = size.bit_length() - 1

    masks = [0] * (log + 1)
    for i in range(1, log + 1):
        masks[i] = (1 << i) - 1

    # Segment tree over the sorted unique query values.
    # d[k] = max value in node k excluding lazy values of ancestors.
    # lazy[k] = pending addition included in d[k] but not in children.
    d = [0] * (2 * size)
    d[size:size + U] = vals
    del vals

    for i in range(size - 1, 0, -1):
        left = i << 1
        a = d[left]
        b = d[left | 1]
        d[i] = a if a >= b else b

    lazy = [0] * (2 * size)

    def first_ge(t, d=d, lazy=lazy, size=size, U=U):
        # Assumes t <= current maximum. Returns first index with value >= t,
        # or U if it falls into padding.
        k = 1
        acc = 0
        while k < size:
            z = lazy[k]
            ca = acc + z
            left = k << 1
            if d[left] + ca >= t:
                k = left
            else:
                k = left | 1
            acc = ca
        idx = k - size
        if idx >= U:
            return U
        return idx

    def range_add(l, r, d=d, lazy=lazy, size=size, log=log, masks=masks):
        if l >= r:
            return

        l += size
        r += size
        l0 = l
        r0 = r

        while l < r:
            if l & 1:
                d[l] += 1
                lazy[l] += 1
                l += 1
            if r & 1:
                r -= 1
                d[r] += 1
                lazy[r] += 1
            l >>= 1
            r >>= 1

        # Rebuild only ancestors that are not fully covered.
        for i in range(1, log + 1):
            mask = masks[i]
            if l0 & mask:
                k = l0 >> i
                left = k << 1
                a = d[left]
                b = d[left | 1]
                d[k] = lazy[k] + (a if a >= b else b)
            if r0 & mask:
                k = (r0 - 1) >> i
                left = k << 1
                a = d[left]
                b = d[left | 1]
                d[k] = lazy[k] + (a if a >= b else b)

    fg = first_ge
    ra = range_add

    p = contest_start
    for _ in range(N):
        L = data[p]
        R = data[p + 1]
        p += 2

        maxv = d[1]
        if maxv < L:
            continue

        if L == 1:
            a = 0
        else:
            a = fg(L)

        if maxv <= R:
            b = U
        else:
            b = fg(R + 1)

        if a < b:
            ra(a, b)

    # Push all lazy values to leaves once.
    d_local = d
    lazy_local = lazy
    for k in range(1, size):
        z = lazy_local[k]
        if z:
            left = k << 1
            d_local[left] += z
            d_local[left | 1] += z
            lazy_local[left] += z
            lazy_local[left | 1] += z

    out = []
    append_out = out.append
    base = size
    pos_local = pos

    for i in range(Q):
        x = data[query_start + i]
        append_out(str(d_local[base + pos_local[x]]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()