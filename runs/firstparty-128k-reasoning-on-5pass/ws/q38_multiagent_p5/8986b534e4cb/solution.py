import sys
from bisect import bisect_right, bisect_left
from heapq import heappush, heappop


def solve():
    input = sys.stdin.buffer.readline
    N, M, Q = map(int, input().split())

    l = [0] * (M + 1)
    r = [0] * (M + 1)
    idxs = [[], []]

    for i in range(1, M + 1):
        S, T = map(int, input().split())
        if S < T:
            l[i] = S
            r[i] = T
            s = 0
        else:
            l[i] = T
            r[i] = S
            s = 1
        idxs[s].append(i)

    # p[i] = largest earlier person index that forms a bad pair with i
    p = [0] * (M + 1)

    # Bad pairs sharing the same left endpoint or the same right endpoint.
    last_l = [0] * (N + 1)
    last_r = [0] * (N + 1)
    for i in range(1, M + 1):
        li = l[i]
        ri = r[i]

        v = last_l[li]
        if v > p[i]:
            p[i] = v
        last_l[li] = i

        v = last_r[ri]
        if v > p[i]:
            p[i] = v
        last_r[ri] = i

    del last_l, last_r

    # Encode (y, index) into one integer.  Lower bits store index.
    SHIFT = (M + 1).bit_length()
    MASK = (1 << SHIFT) - 1
    N1 = N + 1

    br = bisect_right
    bl = bisect_left
    hp = heappush
    hpop = heappop

    def sweep(s, mirror):
        """
        For one direction and one crossing orientation.

        In the current coordinate system an interval is (L, R).
        For current earlier interval a, a future interval b is a bad pair of
        this orientation iff:
            L_a < L_b < R_a < R_b
        i.e. point b has x = L_b in (L_a, R_a) and y = R_b > R_a.

        We process indices backwards.  Active future intervals are stored once
        at leaf x = L_b in a segment tree over compressed L values.
        Each leaf has a max-heap by y = R_b.  Internal nodes store the maximum
        y in their subtree.  Query reports and deletes all active points in
        the rectangle x in (L_a, R_a), y > R_a.
        """
        idx_list = idxs[s]
        m = len(idx_list)
        if m < 2:
            return

        l_arr = l
        r_arr = r
        N1_local = N1

        if mirror:
            Ls = [N1_local - r_arr[i] for i in idx_list]
            Rs = [N1_local - l_arr[i] for i in idx_list]
        else:
            Ls = [l_arr[i] for i in idx_list]
            Rs = [r_arr[i] for i in idx_list]

        coords = sorted(set(Ls))
        K = len(coords)
        size = 1 << (K - 1).bit_length()

        mx = [-1] * (2 * size)
        heaps = [None] * K
        comp = {v: i for i, v in enumerate(coords)}

        p_local = p
        SHIFT_local = SHIFT
        MASK_local = MASK
        br_local = br
        bl_local = bl
        hp_local = hp
        hpop_local = hpop

        stack = []

        for pos in range(m - 1, -1, -1):
            i = idx_list[pos]
            L = Ls[pos]
            R = Rs[pos]

            # If no active point has y > R, nothing can be reported.
            if mx[1] > R:
                ql = br_local(coords, L)
                qr = bl_local(coords, R) - 1

                if ql <= qr:
                    stack.clear()
                    a = ql + size
                    b = qr + size

                    # Canonical segment-tree nodes covering [ql, qr].
                    while a <= b:
                        if a & 1:
                            if mx[a] > R:
                                stack.append(a)
                            a += 1
                        if not (b & 1):
                            if mx[b] > R:
                                stack.append(b)
                            b -= 1
                        a >>= 1
                        b >>= 1

                    while stack:
                        node = stack.pop()
                        if mx[node] <= R:
                            continue

                        if node >= size:
                            leaf = node - size
                            h = heaps[leaf]

                            if h is None:
                                mx[node] = -1
                                pos2 = node >> 1
                                while pos2:
                                    left = pos2 << 1
                                    right = left | 1
                                    new = mx[left] if mx[left] >= mx[right] else mx[right]
                                    if mx[pos2] == new:
                                        break
                                    mx[pos2] = new
                                    pos2 >>= 1
                                continue

                            while h:
                                v = -h[0]
                                y = v >> SHIFT_local
                                if y <= R:
                                    break
                                hpop_local(h)
                                idx = v & MASK_local
                                if i > p_local[idx]:
                                    p_local[idx] = i

                            new_top = (-h[0]) >> SHIFT_local if h else -1
                            if mx[node] != new_top:
                                mx[node] = new_top
                                pos2 = node >> 1
                                while pos2:
                                    left = pos2 << 1
                                    right = left | 1
                                    new = mx[left] if mx[left] >= mx[right] else mx[right]
                                    if mx[pos2] == new:
                                        break
                                    mx[pos2] = new
                                    pos2 >>= 1
                        else:
                            left = node << 1
                            right = left | 1
                            if mx[left] > R:
                                stack.append(left)
                            if mx[right] > R:
                                stack.append(right)

            # Insert current interval as a future interval for smaller indices.
            leaf = comp[L]
            h = heaps[leaf]
            val = (R << SHIFT_local) | i
            neg = -val

            if h is None:
                h = [neg]
                heaps[leaf] = h
            else:
                hp_local(h, neg)

            new_top = (-h[0]) >> SHIFT_local
            node = size + leaf
            if mx[node] != new_top:
                mx[node] = new_top
                pos2 = node >> 1
                while pos2:
                    left = pos2 << 1
                    right = left | 1
                    new = mx[left] if mx[left] >= mx[right] else mx[right]
                    if mx[pos2] == new:
                        break
                    mx[pos2] = new
                    pos2 >>= 1

    # Original coordinates handle L_a < L_b < R_a < R_b.
    # Mirrored coordinates handle the other crossing order.
    for s in (0, 1):
        sweep(s, False)
        sweep(s, True)

    # Convert p into prefix maximums in place.
    cur = 0
    for i in range(1, M + 1):
        if p[i] < cur:
            p[i] = cur
        else:
            cur = p[i]

    out = []
    append = out.append
    for _ in range(Q):
        L, R = map(int, input().split())
        if p[R] < L:
            append("Yes")
        else:
            append("No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()