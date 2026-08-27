import sys
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    w = [next(it) for _ in range(n)]

    m = 2 * n
    INF = 4_000_000_000_000_000_000

    L = [0] * n
    R = [0] * n
    by_l = [INF] * (m + 2)
    by_r = [INF] * (m + 2)

    for i in range(n):
        l = next(it)
        r = next(it)
        L[i] = l
        R[i] = r
        if w[i] < by_l[l]:
            by_l[l] = w[i]
        if w[i] < by_r[r]:
            by_r[r] = w[i]

    # pref[x]: minimum weight among intervals with R < x.
    pref = [INF] * (m + 2)
    cur = INF
    for x in range(1, m + 1):
        pref[x] = cur
        if by_r[x] < cur:
            cur = by_r[x]

    # suff[x]: minimum weight among intervals with L > x.
    suff = [INF] * (m + 2)
    cur = INF
    for x in range(m, 0, -1):
        suff[x] = cur
        if by_l[x] < cur:
            cur = by_l[x]

    size = 1
    while size < m + 1:
        size <<= 1

    def make_tree():
        return array('q', [INF]) * (2 * size)

    # Left-oriented paths s-a-b-c-t, where a and c are left of
    # their respective endpoints and b lies to their right.
    # Trees are indexed by L_b.
    left0 = make_tree()  # W_b + 2 * pref[L_b]
    left1 = make_tree()  # W_b + pref[L_b]
    left2 = make_tree()  # W_b

    # Mirrored right-oriented paths, indexed by R_b.
    right0 = make_tree()  # W_b
    right1 = make_tree()  # W_b + suff[R_b]
    right2 = make_tree()  # W_b + 2 * suff[R_b]

    def put(tree, pos, val):
        p = size + pos
        if val < tree[p]:
            tree[p] = val

    for i in range(n):
        wi = w[i]

        x = L[i]
        put(left2, x, wi)
        if pref[x] < INF:
            put(left1, x, wi + pref[x])
            put(left0, x, wi + 2 * pref[x])

        x = R[i]
        put(right0, x, wi)
        if suff[x] < INF:
            put(right1, x, wi + suff[x])
            put(right2, x, wi + 2 * suff[x])

    for tree in (left0, left1, left2, right0, right1, right2):
        for p in range(size - 1, 0, -1):
            a = tree[p << 1]
            b = tree[p << 1 | 1]
            tree[p] = a if a < b else b

    def range_min(tree, l, r):
        if l > r:
            return INF
        l += size
        r += size
        ans = INF
        while l <= r:
            if l & 1:
                if tree[l] < ans:
                    ans = tree[l]
                l += 1
            if not (r & 1):
                if tree[r] < ans:
                    ans = tree[r]
                r -= 1
            l >>= 1
            r >>= 1
        return ans

    q = next(it)
    out = []

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        ls, rs = L[s], R[s]
        lt, rt = L[t], R[t]

        # A direct edge is always optimal when endpoint intervals are disjoint.
        if rs < lt or rt < ls:
            out.append(str(w[s] + w[t]))
            continue

        extra = INF

        # Exactly one internal vertex.
        v = pref[min(ls, lt)]
        if v < extra:
            extra = v
        v = suff[max(rs, rt)]
        if v < extra:
            extra = v

        # Exactly two internal vertices. They must be on opposite sides.
        a = pref[ls]
        b = suff[rt]
        if a < INF and b < INF:
            extra = min(extra, a + b)

        a = pref[lt]
        b = suff[rs]
        if a < INF and b < INF:
            extra = min(extra, a + b)

        # Exactly three internal vertices, with both outer internal
        # vertices on the left side.
        a_l = min(ls, lt)
        b_l = max(ls, lt)

        v = range_min(left0, 1, a_l - 1)
        if v < extra:
            extra = v

        v = range_min(left1, a_l, b_l - 1)
        if v < INF and pref[a_l] < INF:
            extra = min(extra, v + pref[a_l])

        v = range_min(left2, b_l, m)
        if v < INF and pref[ls] < INF and pref[lt] < INF:
            extra = min(extra, v + pref[ls] + pref[lt])

        # Mirrored three-internal-vertex case.
        a_r = min(rs, rt)
        b_r = max(rs, rt)

        v = range_min(right0, 1, a_r)
        if v < INF and suff[rs] < INF and suff[rt] < INF:
            extra = min(extra, v + suff[rs] + suff[rt])

        v = range_min(right1, a_r + 1, b_r)
        if v < INF and suff[b_r] < INF:
            extra = min(extra, v + suff[b_r])

        v = range_min(right2, b_r + 1, m)
        if v < extra:
            extra = v

        if extra >= INF:
            out.append("-1")
        else:
            out.append(str(w[s] + w[t] + extra))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()