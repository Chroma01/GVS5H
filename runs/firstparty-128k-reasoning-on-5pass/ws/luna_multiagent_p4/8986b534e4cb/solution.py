import sys
from bisect import bisect_left
from array import array


class TwoDimensionalMax:
    """Supports:
       add(key, value, index)
       query(key_l, key_r, value < threshold):
           maximum index
    """

    __slots__ = ("size", "coords", "bits")

    def __init__(self, points, key_limit):
        size = 1
        while size < key_limit:
            size <<= 1
        self.size = size

        coords = [[] for _ in range(2 * size)]
        for key, value in points:
            node = size + key
            while node:
                coords[node].append(value)
                node >>= 1

        bits = [None] * (2 * size)
        for i in range(1, 2 * size):
            if coords[i]:
                values = sorted(set(coords[i]))
                coords[i] = values
                bits[i] = array("i", [0]) * (len(values) + 1)
            else:
                coords[i] = None

        self.coords = coords
        self.bits = bits

    def add(self, key, value, index):
        node = self.size + key
        while node:
            values = self.coords[node]
            pos = bisect_left(values, value) + 1
            bit = self.bits[node]

            while pos < len(bit):
                if bit[pos] < index:
                    bit[pos] = index
                pos += pos & -pos

            node >>= 1

    def _prefix(self, node, value):
        values = self.coords[node]
        if values is None:
            return 0

        pos = bisect_left(values, value)
        bit = self.bits[node]
        result = 0

        while pos:
            if result < bit[pos]:
                result = bit[pos]
            pos -= pos & -pos

        return result

    def query(self, left, right, value):
        if left > right:
            return 0

        left += self.size
        right += self.size + 1
        result = 0

        while left < right:
            if left & 1:
                result = max(result, self._prefix(left, value))
                left += 1
            if right & 1:
                right -= 1
                result = max(result, self._prefix(right, value))

            left >>= 1
            right >>= 1

        return result


def compute_crossing_conflicts(intervals, m, n):
    previous = [0] * (m + 1)

    # Earlier interval: a < current l < b < current r.
    # Both strict inequalities are needed to exclude endpoint touching.
    for direction in (0, 1):
        ids = [
            i for i in range(1, m + 1)
            if intervals[i][2] == direction
        ]

        points = [(intervals[i][1], intervals[i][0]) for i in ids]
        ds = TwoDimensionalMax(points, n + 1)

        for i in ids:
            l, r, _ = intervals[i]
            previous[i] = max(
                previous[i],
                ds.query(l + 1, r - 1, l)
            )
            ds.add(r, l, i)

    # Current interval: current l < earlier a < current r < earlier b.
    # Again, strict ranges exclude endpoint touching.
    for direction in (0, 1):
        ids = [
            i for i in range(1, m + 1)
            if intervals[i][2] == direction
        ]

        points = [(intervals[i][0], -intervals[i][1]) for i in ids]
        ds = TwoDimensionalMax(points, n + 1)

        for i in ids:
            l, r, _ = intervals[i]
            previous[i] = max(
                previous[i],
                ds.query(l + 1, r - 1, -r)
            )
            ds.add(l, -r, i)

    return previous


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    q = next(it)

    intervals = [(0, 0, 0)] * (m + 1)

    for i in range(1, m + 1):
        s = next(it)
        t = next(it)

        if s < t:
            intervals[i] = (s, t, 0)
        else:
            intervals[i] = (t, s, 1)

    previous = compute_crossing_conflicts(intervals, m, n)

    # Sharing an endpoint is contradictory only for opposite directions.
    latest_left = [{}, {}]
    latest_right = [{}, {}]

    for i in range(1, m + 1):
        l, r, direction = intervals[i]
        opposite = 1 - direction

        previous[i] = max(
            previous[i],
            latest_left[opposite].get(l, 0),
            latest_right[opposite].get(r, 0),
        )

        latest_left[direction][l] = i
        latest_right[direction][r] = i

    size = 1
    while size < m:
        size <<= 1

    seg = [0] * (2 * size)

    for i in range(1, m + 1):
        seg[size + i - 1] = previous[i]

    for i in range(size - 1, 0, -1):
        seg[i] = max(seg[i << 1], seg[i << 1 | 1])

    answers = []

    for _ in range(q):
        left = next(it)
        right = next(it)

        x = size + left - 1
        y = size + right
        best = 0

        while x < y:
            if x & 1:
                best = max(best, seg[x])
                x += 1
            if y & 1:
                y -= 1
                best = max(best, seg[y])

            x >>= 1
            y >>= 1

        answers.append("Yes" if best < left else "No")

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()