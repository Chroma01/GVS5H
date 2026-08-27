import sys
from bisect import bisect_left, bisect_right
from array import array


def process_crossings(items, n, bad):
    """
    items: list of (a, b, index), all having the same direction.
    Finds prior intervals strictly crossing each current interval.
    """
    if not items:
        return

    base = 1
    while base <= n:
        base <<= 1

    buckets = [None] * (base << 1)

    # Register each possible point in all ancestors of its x coordinate.
    for a, b, _ in items:
        p = base + a
        while p:
            v = buckets[p]
            if v is None:
                buckets[p] = [b]
            else:
                v.append(b)
            p >>= 1

    # Convert coordinate lists to static inner maximum segment trees.
    for p, v in enumerate(buckets):
        if v is not None:
            coords = array('i', sorted(set(v)))
            sz = 1
            while sz < len(coords):
                sz <<= 1
            vals = array('i', [0]) * (sz << 1)
            buckets[p] = (coords, vals, sz)

    def inner_query(data, yl, yr):
        # An outer tree node may belong to the queried x range while no
        # interval of this direction was registered in that node.
        if data is None or yl > yr:
            return 0

        coords, vals, sz = data
        l = bisect_left(coords, yl)
        r = bisect_right(coords, yr)
        if l >= r:
            return 0

        l += sz
        r += sz
        ans = 0
        while l < r:
            if l & 1:
                x = vals[l]
                if x > ans:
                    ans = x
                l += 1
            if r & 1:
                r -= 1
                x = vals[r]
                if x > ans:
                    ans = x
            l >>= 1
            r >>= 1
        return ans

    def rectangle_query(xl, xr, yl, yr):
        if xl > xr or yl > yr:
            return 0
        if xl < 1:
            xl = 1
        if xr > n:
            xr = n
        if xl > xr:
            return 0

        l = base + xl
        r = base + xr + 1
        ans = 0

        while l < r:
            if l & 1:
                x = inner_query(buckets[l], yl, yr)
                if x > ans:
                    ans = x
                l += 1
            if r & 1:
                r -= 1
                x = inner_query(buckets[r], yl, yr)
                if x > ans:
                    ans = x
            l >>= 1
            r >>= 1

        return ans

    def update(x, y, idx):
        p = base + x
        while p:
            coords, vals, sz = buckets[p]
            q = bisect_left(coords, y) + sz

            # Insertions are in increasing person-index order. Therefore the
            # newest inserted index is the maximum in every affected node.
            vals[q] = idx
            q >>= 1
            while q:
                vals[q] = idx
                q >>= 1

            p >>= 1

    for a, b, idx in items:
        # Earlier [c,d] such that c < a < d < b.
        v1 = rectangle_query(1, a - 1, a + 1, b - 1)

        # Earlier [c,d] such that a < c < b < d.
        v2 = rectangle_query(a + 1, b - 1, b + 1, n)

        if v1 > bad[idx]:
            bad[idx] = v1
        if v2 > bad[idx]:
            bad[idx] = v2

        update(a, b, idx)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    q = next(it)

    left = [0] * (m + 1)
    right = [0] * (m + 1)
    orient = bytearray(m + 1)  # 1 if S<T, 0 if S>T

    forward_items = []
    backward_items = []

    for i in range(1, m + 1):
        s = next(it)
        t = next(it)

        if s < t:
            a, b = s, t
            orient[i] = 1
            forward_items.append((a, b, i))
        else:
            a, b = t, s
            backward_items.append((a, b, i))

        left[i] = a
        right[i] = b

    bad = [0] * (m + 1)

    # Equal undirected intervals conflict only for opposite directions.
    equal_forward = {}
    equal_backward = {}

    # For each town, retain the latest previous interval incident to it
    # whose opposite endpoint lies on the indicated side.
    other_on_left = [0] * (n + 1)
    other_on_right = [0] * (n + 1)

    key_base = n + 1

    for i in range(1, m + 1):
        a = left[i]
        b = right[i]
        key = a * key_base + b

        if orient[i]:
            v = equal_backward.get(key, 0)
            if v > bad[i]:
                bad[i] = v
            equal_forward[key] = i
        else:
            v = equal_forward.get(key, 0)
            if v > bad[i]:
                bad[i] = v
            equal_backward[key] = i

        # At endpoint a, the other endpoint is to its right.
        v = other_on_right[a]
        if v > bad[i]:
            bad[i] = v

        # At endpoint b, the other endpoint is to its left.
        v = other_on_left[b]
        if v > bad[i]:
            bad[i] = v

        other_on_right[a] = i
        other_on_left[b] = i

    # Strictly crossing intervals conflict only when directions match.
    process_crossings(forward_items, n, bad)
    process_crossings(backward_items, n, bad)

    # Static maximum segment tree over bad[] for query ranges.
    size = 1
    while size < m:
        size <<= 1

    seg = array('i', [0]) * (size << 1)

    for i in range(1, m + 1):
        seg[size + i - 1] = bad[i]

    for p in range(size - 1, 0, -1):
        x = seg[p << 1]
        y = seg[p << 1 | 1]
        seg[p] = x if x >= y else y

    out = []

    for _ in range(q):
        l = next(it)
        r = next(it)

        x = size + l - 1
        y = size + r
        mx = 0

        while x < y:
            if x & 1:
                if seg[x] > mx:
                    mx = seg[x]
                x += 1
            if y & 1:
                y -= 1
                if seg[y] > mx:
                    mx = seg[y]
            x >>= 1
            y >>= 1

        out.append("Yes" if mx < l else "No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()