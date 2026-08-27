import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    A = list(map(int, data[1:]))
    del data

    M = N - 1
    size = 1 << (M - 1).bit_length()
    LOG = size.bit_length() - 1
    NEG = -10**9

    next_pos = [N] * N
    diff = [0] * N
    last = [-1] * (N + 1)
    seen = bytearray(N + 1)
    total_distinct = 0

    for i in range(N - 1, -1, -1):
        a = A[i]
        b = last[a]
        if b != -1:
            next_pos[i] = b
            diff[i] += 1
            diff[b] -= 1
        last[a] = i
        if not seen[a]:
            seen[a] = 1
            total_distinct += 1

    del A, last, seen

    d = [NEG] * (2 * size)
    cur = 0
    base = size
    for c in range(M):
        cur += diff[c]
        d[base + c] = cur
    cover_i = diff[0]

    for p in range(size - 1, 0, -1):
        lc = p << 1
        x = d[lc]
        y = d[lc + 1]
        d[p] = x if x >= y else y

    lazy = [0] * size
    masks = [1 << b for b in range(LOG - 1, -1, -1)]

    ans = 0
    for i in range(N - 2):
        b = next_pos[i]
        if b != N:
            l_up = i + 1
            r_up = b
            if l_up < r_up:
                l2 = l_up + size
                r2 = r_up + size
                l0 = l2
                r0 = r2
                while l2 < r2:
                    if l2 & 1:
                        d[l2] -= 1
                        if l2 < size:
                            lazy[l2] -= 1
                        l2 += 1
                    if r2 & 1:
                        r2 -= 1
                        d[r2] -= 1
                        if r2 < size:
                            lazy[r2] -= 1
                    l2 >>= 1
                    r2 >>= 1

                l0 >>= 1
                r0 = (r0 - 1) >> 1
                while l0:
                    lc = l0 << 1
                    x = d[lc]
                    y = d[lc + 1]
                    d[l0] = (x if x >= y else y) + lazy[l0]
                    if r0 != l0:
                        lc = r0 << 1
                        x = d[lc]
                        y = d[lc + 1]
                        d[r0] = (x if x >= y else y) + lazy[r0]
                    l0 >>= 1
                    r0 >>= 1

        l = i + 1
        p = 1
        carry = 0
        best = NEG
        for mask in masks:
            carry += lazy[p]
            if l & mask:
                p = (p << 1) | 1
            else:
                p <<= 1
                v = d[p | 1] + carry
                if v > best:
                    best = v
        v = d[p] + carry
        if v > best:
            best = v

        cand = total_distinct + cover_i + best
        if cand > ans:
            ans = cand

        if i < N - 3:
            cover_i += diff[i + 1]

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()