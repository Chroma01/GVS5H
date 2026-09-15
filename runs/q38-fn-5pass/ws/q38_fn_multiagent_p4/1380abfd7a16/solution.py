import sys


def main():
    it = map(int, sys.stdin.buffer.read().split())
    try:
        n = next(it)
    except StopIteration:
        return

    p = [0]
    p.extend(it)
    del it

    # Power-of-two size >= n.
    sz = 1 << (n - 1).bit_length()

    # Fenwick tree over final positions: 1 = empty, 0 = filled.
    bit = [0] * (sz + 1)
    bit[1:n + 1] = [1] * n

    # Precompute Fenwick ancestors for updates.
    # The root at index sz is never queried, so updates stop before it.
    up = [0] * (sz + 1)
    b = bit
    u = up
    for i in range(1, sz):
        j = i + (i & -i)
        u[i] = j
        if j < sz:
            b[j] += b[i]

    # Binary-lifting steps for kth-one search.
    steps = []
    s = sz >> 1
    while s:
        steps.append(s)
        s >>= 1
    steps = tuple(steps)

    ans = [0] * n
    a = ans
    pp = p
    st = steps
    sz_local = sz

    # Place values N, N-1, ..., 1 into the P_i-th empty final position.
    for i in range(n, 0, -1):
        k = pp[i]
        idx = 0

        for s in st:
            nxt = idx + s
            val = b[nxt]
            if val < k:
                idx = nxt
                k -= val

        pos = idx + 1
        a[pos - 1] = i

        j = pos
        while j < sz_local:
            b[j] -= 1
            j = u[j]

    sys.stdout.write(' '.join(map(str, a)))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()