import sys
from bisect import bisect_left, bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    pref = [0] * (n + 1)
    for i, x in enumerate(a):
        pref[i + 1] = pref[i] + x

    # Segment tree for range maximum queries.
    size = 1
    while size < n:
        size <<= 1

    seg = [0] * (2 * size)
    seg[size:size + n] = a
    for i in range(size - 1, 0, -1):
        seg[i] = max(seg[i << 1], seg[i << 1 | 1])

    def range_max(l, r):
        """Maximum of A[l:r]. Assumes l < r."""
        l += size
        r += size
        res = 0
        while l < r:
            if l & 1:
                if seg[l] > res:
                    res = seg[l]
                l += 1
            if r & 1:
                r -= 1
                if seg[r] > res:
                    res = seg[r]
            l >>= 1
            r >>= 1
        return res

    # All occurrences of each value, used to split a component at all maxima.
    positions = {}
    for i, x in enumerate(a):
        positions.setdefault(x, []).append(i)

    # A component is an interval after removing all occurrences of its maximum.
    # Its children are the non-empty gaps between those maxima.
    comp_l = []
    comp_r = []
    comp_max = []
    comp_sum = []
    comp_parent = []

    # Each original position belongs to exactly one maximum group/component.
    owner = [-1] * n

    stack = [(0, n, -1)]
    while stack:
        l, r, par = stack.pop()

        m = range_max(l, r)
        loc = positions[m]
        lo = bisect_left(loc, l)
        hi = bisect_right(loc, r - 1)
        maxima = loc[lo:hi]

        cid = len(comp_l)
        comp_l.append(l)
        comp_r.append(r)
        comp_max.append(m)
        comp_sum.append(pref[r] - pref[l])
        comp_parent.append(par)

        for p in maxima:
            owner[p] = cid

        prev = l
        for p in maxima:
            if prev < p:
                stack.append((prev, p, cid))
            prev = p + 1
        if prev < r:
            stack.append((prev, r, cid))

    cnum = len(comp_l)

    # A slime at a maximum of component c consumes all of c iff it has
    # an immediately adjacent strictly smaller slime within that component.
    full_base = [False] * n
    for i in range(n):
        c = owner[i]
        m = comp_max[c]
        l = comp_l[c]
        r = comp_r[c]
        if (i > l and a[i - 1] < m) or (i + 1 < r and a[i + 1] < m):
            full_base[i] = True

    # Binary lifting on the component tree.
    # good[k][v] means that after consuming component v completely, one can
    # also consume exactly 2^k ancestor-components.
    log = max(1, cnum.bit_length())
    up = [comp_parent]
    good = [bytearray(cnum)]

    for v in range(cnum):
        p = comp_parent[v]
        if p != -1 and comp_sum[v] > comp_max[p]:
            good[0][v] = 1

    for k in range(1, log):
        prev_up = up[-1]
        prev_good = good[-1]
        cur_up = [-1] * cnum
        cur_good = bytearray(cnum)

        for v in range(cnum):
            mid = prev_up[v]
            if mid != -1:
                cur_up[v] = prev_up[mid]
                if prev_good[v] and prev_good[mid]:
                    cur_good[v] = 1

        up.append(cur_up)
        good.append(cur_good)

    ans = [0] * n

    for i in range(n):
        c = owner[i]

        if not full_base[i]:
            # It cannot absorb any equal maximum neighbor, and its parent
            # component has a strictly larger maximum.
            ans[i] = a[i]
            continue

        # First consume this component, then greedily climb as far as possible.
        for k in range(log - 1, -1, -1):
            if good[k][c]:
                c = up[k][c]

        ans[i] = comp_sum[c]

    print(*ans)


if __name__ == "__main__":
    solve()