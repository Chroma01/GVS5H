import sys
from array import array
from bisect import bisect_left, bisect_right


class Dynamic2DRangeMax:
    """
    Points are inserted online as (x, y, value), with increasing values.
    Supports maximum value in an inclusive rectangle.
    Outer segment tree is over x; every outer node has a static compressed
    inner segment tree over y values.
    """

    def __init__(self, n, points):
        self.n = n
        size = 1
        while size < n:
            size <<= 1
        self.size = size

        buckets = [None] * (size << 1)

        for x, y in points:
            p = x + size - 1
            while p:
                b = buckets[p]
                if b is None:
                    buckets[p] = [y]
                else:
                    b.append(y)
                p >>= 1

        offsets = array('i', [0]) * (size << 1)
        lengths = array('i', [0]) * (size << 1)
        bases = array('i', [0]) * (size << 1)

        coords = array('i')
        total_tree_size = 0

        for node in range(1, size << 1):
            b = buckets[node]
            if b is None:
                continue

            b.sort()
            offsets[node] = len(coords)

            last = -1
            cnt = 0
            for v in b:
                if v != last:
                    coords.append(v)
                    last = v
                    cnt += 1

            lengths[node] = cnt
            base = 1
            while base < cnt:
                base <<= 1
            bases[node] = base
            total_tree_size += base << 1
            buckets[node] = None

        tree_offsets = array('i', [0]) * (size << 1)
        cur = 0
        for node in range(1, size << 1):
            tree_offsets[node] = cur
            if bases[node]:
                cur += bases[node] << 1

        self.coords = coords
        self.offsets = offsets
        self.lengths = lengths
        self.bases = bases
        self.tree_offsets = tree_offsets
        self.seg = array('i', [0]) * total_tree_size

    def add(self, x, y, value):
        p = x + self.size - 1
        coords = self.coords
        offsets = self.offsets
        lengths = self.lengths
        bases = self.bases
        tree_offsets = self.tree_offsets
        seg = self.seg

        while p:
            coord_pos = bisect_left(
                coords, y, offsets[p], offsets[p] + lengths[p]
            ) - offsets[p]

            start = tree_offsets[p]
            local = bases[p] + coord_pos
            seg[start + local] = value

            while local > 1:
                local >>= 1
                left_child = local << 1
                a = seg[start + left_child]
                b = seg[start + (left_child | 1)]
                seg[start + local] = a if a >= b else b

            p >>= 1

    def _query_node(self, node, yl, yr):
        if yl > yr or self.lengths[node] == 0:
            return 0

        coord_start = self.offsets[node]
        coord_end = coord_start + self.lengths[node]
        lo = bisect_left(self.coords, yl, coord_start, coord_end) - coord_start
        hi = bisect_right(self.coords, yr, coord_start, coord_end) - coord_start

        if lo >= hi:
            return 0

        base = self.bases[node]
        start = self.tree_offsets[node]
        l = base + lo
        r = base + hi

        ans = 0
        seg = self.seg
        while l < r:
            if l & 1:
                v = seg[start + l]
                if v > ans:
                    ans = v
                l += 1
            if r & 1:
                r -= 1
                v = seg[start + r]
                if v > ans:
                    ans = v
            l >>= 1
            r >>= 1
        return ans

    def query(self, xl, xr, yl, yr):
        if xl > xr or yl > yr:
            return 0

        l = xl + self.size - 1
        r = xr + self.size
        ans = 0

        while l < r:
            if l & 1:
                v = self._query_node(l, yl, yr)
                if v > ans:
                    ans = v
                l += 1
            if r & 1:
                r -= 1
                v = self._query_node(r, yl, yr)
                if v > ans:
                    ans = v
            l >>= 1
            r >>= 1

        return ans


def solve():
    input = sys.stdin.buffer.readline
    N, M, Q = map(int, input().split())

    left = [0] * M
    right = [0] * M
    sign = [0] * M
    original_s = [0] * M
    original_t = [0] * M

    points_by_sign = [[], []]

    for i in range(M):
        s, t = map(int, input().split())
        original_s[i] = s
        original_t[i] = t

        if s < t:
            l, r, sg = s, t, 1
        else:
            l, r, sg = t, s, 0

        left[i] = l
        right[i] = r
        sign[i] = sg
        points_by_sign[sg].append((l, r))

    structures = [
        Dynamic2DRangeMax(N, points_by_sign[0]),
        Dynamic2DRangeMax(N, points_by_sign[1]),
    ]

    prev = [0] * M
    latest_left = {}
    latest_right = {}
    latest_directed = {}

    for i in range(M):
        l = left[i]
        r = right[i]
        sg = sign[i]
        idx = i + 1
        best = 0

        v = latest_left.get(l, 0)
        if v > best:
            best = v

        v = latest_right.get(r, 0)
        if v > best:
            best = v

        v = latest_directed.get((original_t[i], original_s[i]), 0)
        if v > best:
            best = v

        st = structures[sg]

        # Earlier [a,b] satisfying a < l < b < r.
        if l > 1:
            v = st.query(1, l - 1, l + 1, r - 1)
            if v > best:
                best = v

        # Earlier [a,b] satisfying l < a < r < b.
        if r < N:
            v = st.query(l + 1, r - 1, r + 1, N)
            if v > best:
                best = v

        prev[i] = best

        latest_left[l] = idx
        latest_right[r] = idx
        latest_directed[(original_s[i], original_t[i])] = idx
        st.add(l, r, idx)

    size = 1
    while size < M:
        size <<= 1

    rmq = [0] * (size << 1)
    for i, v in enumerate(prev):
        rmq[size + i] = v
    for i in range(size - 1, 0, -1):
        a = rmq[i << 1]
        b = rmq[i << 1 | 1]
        rmq[i] = a if a >= b else b

    out = []
    for _ in range(Q):
        L, R = map(int, input().split())
        l = size + L - 1
        r = size + R
        mx = 0

        while l < r:
            if l & 1:
                if rmq[l] > mx:
                    mx = rmq[l]
                l += 1
            if r & 1:
                r -= 1
                if rmq[r] > mx:
                    mx = rmq[r]
            l >>= 1
            r >>= 1

        out.append("Yes" if mx < L else "No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()