import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    M = data[p + 1]
    Q = data[p + 2]
    p += 3

    Ls = [0] * (M + 1)
    Rs = [0] * (M + 1)
    Ts = [0] * (M + 1)  # 0: left-to-right (+), 1: right-to-left (-)

    for i in range(1, M + 1):
        S = data[p]
        T = data[p + 1]
        p += 2
        if S < T:
            Ls[i] = S
            Rs[i] = T
            Ts[i] = 0
        else:
            Ls[i] = T
            Rs[i] = S
            Ts[i] = 1

    size = 1
    while size < N + 2:
        size <<= 1

    seg0 = [0] * (2 * size)  # for type 0 (+)
    seg1 = [0] * (2 * size)  # for type 1 (-)

    left_occ = bytearray(N + 1)
    right_occ = bytearray(N + 1)

    def update(seg, pos, val):
        i = pos + size
        seg[i] = val
        i >>= 1
        while i:
            left = seg[i << 1]
            right = seg[(i << 1) | 1]
            seg[i] = left if left >= right else right
            i >>= 1

    def range_max(seg, l, r):
        # maximum on 0-indexed half-open interval [l, r)
        if l >= r:
            return 0
        l += size
        r += size
        res = 0
        while l < r:
            if l & 1:
                v = seg[l]
                if v > res:
                    res = v
                l += 1
            if r & 1:
                r -= 1
                v = seg[r]
                if v > res:
                    res = v
            l >>= 1
            r >>= 1
        return res

    def find_prefix(seg, p_len, x):
        # rightmost value > x among positions [0, p_len), or 0 if none
        if p_len <= 0:
            return 0

        i = p_len - 1 + size
        if seg[i] > x:
            return seg[i]

        while i > 1:
            if i & 1:  # i is a right child; its left sibling is fully inside prefix
                sib = i - 1
                if seg[sib] > x:
                    node = sib
                    while node < size:
                        rc = (node << 1) | 1
                        if seg[rc] > x:
                            node = rc
                        else:
                            node = node << 1
                    return seg[node]
            i >>= 1

        return 0

    def can_add(idx):
        l = Ls[idx]
        r = Rs[idx]
        t = Ts[idx]

        if left_occ[l] or right_occ[r]:
            return False

        seg = seg1 if t else seg0

        # Existing interval [a, b] with a < l.
        # Crossing iff l < b < r.
        # Among intervals containing l, the rightmost left endpoint has smallest b.
        b = find_prefix(seg, l - 1, l)
        if b and b < r:
            return False

        # Existing interval [a, b] with l < a < r.
        # Crossing iff b > r.
        if l + 1 <= r - 1:
            mx = range_max(seg, l, r - 1)
            if mx > r:
                return False

        return True

    def add(idx):
        l = Ls[idx]
        r = Rs[idx]
        t = Ts[idx]
        left_occ[l] = 1
        right_occ[r] = 1
        seg = seg1 if t else seg0
        update(seg, l - 1, r)

    def remove(idx):
        l = Ls[idx]
        r = Rs[idx]
        t = Ts[idx]
        left_occ[l] = 0
        right_occ[r] = 0
        seg = seg1 if t else seg0
        update(seg, l - 1, 0)

    maxR = [0] * (M + 2)
    R = 0

    for L in range(1, M + 1):
        if R < L - 1:
            R = L - 1

        while R + 1 <= M and can_add(R + 1):
            R += 1
            add(R)

        maxR[L] = R

        if R >= L:
            remove(L)

    out = []
    for _ in range(Q):
        Lq = data[p]
        Rq = data[p + 1]
        p += 2
        out.append("Yes" if Rq <= maxR[Lq] else "No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()