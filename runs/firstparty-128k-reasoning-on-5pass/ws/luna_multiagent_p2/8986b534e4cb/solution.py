import sys
from array import array
from bisect import bisect_left


class RangeTree2D:
    def __init__(self, points, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size

        vals = [[] for _ in range(2 * size)]
        for a, b in points:
            p = a - 1 + size
            while p:
                vals[p].append(b)
                p >>= 1

        self.coords = [None] * (2 * size)
        self.seg = [None] * (2 * size)

        for p in range(1, 2 * size):
            if vals[p]:
                coord = sorted(set(vals[p]))
                self.coords[p] = coord
                s = 1
                while s < len(coord):
                    s <<= 1
                self.seg[p] = array("i", [0]) * (2 * s)

    def clear(self):
        for i in range(1, len(self.seg)):
            if self.seg[i] is not None:
                self.seg[i] = array("i", [0]) * len(self.seg[i])

    def update(self, a, b, value):
        p = a - 1 + self.size
        while p:
            coord = self.coords[p]
            if coord is not None:
                k = bisect_left(coord, b)
                seg = self.seg[p]
                base = len(seg) // 2
                q = base + k

                if seg[q] < value:
                    seg[q] = value
                    q >>= 1
                    while q:
                        nv = seg[q << 1]
                        if seg[q << 1 | 1] > nv:
                            nv = seg[q << 1 | 1]
                        if seg[q] == nv:
                            break
                        seg[q] = nv
                        q >>= 1
            p >>= 1

    def query_node(self, p, lo, hi):
        coord = self.coords[p]
        if coord is None:
            return 0

        left = bisect_left(coord, lo)
        right = bisect_left(coord, hi)
        if left >= right:
            return 0

        seg = self.seg[p]
        base = len(seg) // 2
        left += base
        right += base
        ans = 0

        while left < right:
            if left & 1:
                if seg[left] > ans:
                    ans = seg[left]
                left += 1
            if right & 1:
                right -= 1
                if seg[right] > ans:
                    ans = seg[right]
            left >>= 1
            right >>= 1

        return ans

    def query(self, left, right, lo, hi):
        if left >= right or lo >= hi:
            return 0

        left = left - 1 + self.size
        right = right - 1 + self.size
        ans = 0

        while left < right:
            if left & 1:
                v = self.query_node(left, lo, hi)
                if v > ans:
                    ans = v
                left += 1
            if right & 1:
                right -= 1
                v = self.query_node(right, lo, hi)
                if v > ans:
                    ans = v
            left >>= 1
            right >>= 1

        return ans


def main():
    input = sys.stdin.buffer.readline
    n, m, q = map(int, input().split())

    intervals = []
    directions = []

    for _ in range(m):
        s, t = map(int, input().split())
        if s < t:
            intervals.append((s, t))
            directions.append(1)
        else:
            intervals.append((t, s))
            directions.append(-1)

    queries = [tuple(map(int, input().split())) for _ in range(q)]

    bad = [0] * (m + 1)

    # Opposite directions on the same pair of endpoints are incompatible.
    last = {}
    for i, ((l, r), d) in enumerate(zip(intervals, directions), 1):
        opposite_key = (l, r, -d)
        if opposite_key in last:
            bad[i] = last[opposite_key]
        last[(l, r, d)] = i

    # Equal-direction proper crossings are incompatible.
    tree = RangeTree2D(intervals, n)

    for wanted_direction in (1, -1):
        tree.clear()

        for i, ((l, r), d) in enumerate(zip(intervals, directions), 1):
            if d != wanted_direction:
                continue

            # Earlier intervals [a,b] with a < l < b < r.
            # Starts are in [1,l), ends are in [l+1,r).
            v1 = tree.query(1, l, l + 1, r)

            # Earlier intervals [a,b] with l < a < r < b.
            # Starts are in [l+1,r), ends are in [r+1,n+1).
            v2 = tree.query(l + 1, r, r + 1, n + 1)

            if v1 > bad[i]:
                bad[i] = v1
            if v2 > bad[i]:
                bad[i] = v2

            tree.update(l, r, i)

    size = 1
    while size < m:
        size <<= 1

    seg = [0] * (2 * size)
    for i in range(1, m + 1):
        seg[size + i - 1] = bad[i]

    for i in range(size - 1, 0, -1):
        seg[i] = max(seg[i << 1], seg[i << 1 | 1])

    def range_max(left, right):
        left = left - 1 + size
        right = right + size
        ans = 0

        while left < right:
            if left & 1:
                if seg[left] > ans:
                    ans = seg[left]
                left += 1
            if right & 1:
                right -= 1
                if seg[right] > ans:
                    ans = seg[right]
            left >>= 1
            right >>= 1

        return ans

    out = []
    for left, right in queries:
        out.append("Yes\n" if range_max(left, right) < left else "No\n")

    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()