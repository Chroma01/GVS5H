import sys
from array import array
from bisect import bisect_left, bisect_right


class DynamicPointSet2D:
    """
    Dynamic set of offline-known points (x, y).

    It supports:
      - add/remove a point
      - testing whether a closed axis-aligned rectangle contains an active point

    The outer Fenwick tree is on x. Every outer node has an offline-compressed
    Fenwick tree on y, giving O(log^2 N) per operation.
    """

    def __init__(self, n, points):
        self.n = n

        buckets = [None] * (n + 1)
        for x, y in points:
            p = x
            while p <= n:
                if buckets[p] is None:
                    buckets[p] = [y]
                else:
                    buckets[p].append(y)
                p += p & -p

        offsets = array('i', [0]) * (n + 2)
        coords = array('i')

        for p in range(1, n + 1):
            offsets[p] = len(coords)
            bucket = buckets[p]
            if bucket:
                bucket.sort()
                previous = -1
                for y in bucket:
                    if y != previous:
                        coords.append(y)
                        previous = y

        offsets[n + 1] = len(coords)

        self.offsets = offsets
        self.coords = coords
        self.bit = array('i', [0]) * len(coords)

    def add(self, x, y, delta):
        offsets = self.offsets
        coords = self.coords
        bit = self.bit

        p = x
        while p <= self.n:
            lo = offsets[p]
            hi = offsets[p + 1]
            idx = bisect_left(coords, y, lo, hi) - lo + 1
            length = hi - lo

            while idx <= length:
                bit[lo + idx - 1] += delta
                idx += idx & -idx

            p += p & -p

    def prefix_count(self, x, y):
        if x <= 0 or y <= 0:
            return 0

        offsets = self.offsets
        coords = self.coords
        bit = self.bit

        result = 0
        p = x

        while p > 0:
            lo = offsets[p]
            hi = offsets[p + 1]
            idx = bisect_right(coords, y, lo, hi) - lo

            while idx > 0:
                result += bit[lo + idx - 1]
                idx -= idx & -idx

            p -= p & -p

        return result

    def exists_rectangle(self, xl, xr, yl, yr):
        if xl > xr or yl > yr:
            return False

        count = (
            self.prefix_count(xr, yr)
            - self.prefix_count(xl - 1, yr)
            - self.prefix_count(xr, yl - 1)
            + self.prefix_count(xl - 1, yl - 1)
        )
        return count > 0

    def crosses(self, l, r):
        # Existing [a,b] with a < l < b < r.
        if self.exists_rectangle(1, l - 1, l + 1, r - 1):
            return True

        # Existing [a,b] with l < a < r < b.
        if self.exists_rectangle(l + 1, r - 1, r + 1, self.n):
            return True

        return False


def solve():
    input = sys.stdin.buffer.readline
    n, m, q = map(int, input().split())

    intervals = []
    points_by_direction = [[], []]

    for _ in range(m):
        s, t = map(int, input().split())

        if s < t:
            l, r, direction = s, t, 0
        else:
            l, r, direction = t, s, 1

        intervals.append((l, r, direction))
        points_by_direction[direction].append((l, r))

    point_sets = [
        DynamicPointSet2D(n, points_by_direction[0]),
        DynamicPointSet2D(n, points_by_direction[1]),
    ]

    # cnt_right[x]: active intervals whose geometrically left endpoint is x.
    # cnt_left[x]: active intervals whose geometrically right endpoint is x.
    cnt_right = [0] * (n + 1)
    cnt_left = [0] * (n + 1)

    def conflicts(index):
        l, r, direction = intervals[index]

        # Two intervals having the same geometrical left or right endpoint are
        # incompatible, regardless of travel directions.
        if cnt_right[l] > 0 or cnt_left[r] > 0:
            return True

        # Strict crossings are incompatible exactly for equal travel direction.
        return point_sets[direction].crosses(l, r)

    def add_interval(index):
        l, r, direction = intervals[index]
        point_sets[direction].add(l, r, 1)
        cnt_right[l] += 1
        cnt_left[r] += 1

    def remove_interval(index):
        l, r, direction = intervals[index]
        point_sets[direction].add(l, r, -1)
        cnt_right[l] -= 1
        cnt_left[r] -= 1

    # boundary[right] is the smallest left such that [left, right] is feasible.
    boundary = [0] * m
    left = 0

    for right in range(m):
        while left < right and conflicts(right):
            remove_interval(left)
            left += 1

        add_interval(right)
        boundary[right] = left

    seg_size = 1
    while seg_size < m:
        seg_size <<= 1

    seg = [0] * (seg_size * 2)
    for i, value in enumerate(boundary):
        seg[seg_size + i] = value

    for i in range(seg_size - 1, 0, -1):
        seg[i] = max(seg[i * 2], seg[i * 2 + 1])

    def range_max(l, r):
        result = -1
        l += seg_size
        r += seg_size

        while l < r:
            if l & 1:
                result = max(result, seg[l])
                l += 1
            if r & 1:
                r -= 1
                result = max(result, seg[r])

            l >>= 1
            r >>= 1

        return result

    ans = []
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1

        ans.append("Yes" if range_max(l, r + 1) <= l else "No")

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()