import sys
from bisect import bisect_left, bisect_right
from array import array


class RangeTreeMax:
    """
    Static 2D coordinate structure supporting:
      - point update (outer, inner) with a maximum value
      - rectangle maximum query:
          outer in [lo, hi], inner < threshold  if suffix=False
          outer in [lo, hi], inner > threshold  if suffix=True
    """

    def __init__(self, n_outer, outer_values, inner_values, indices, suffix):
        base = 1
        while base < n_outer:
            base <<= 1

        self.base = base
        self.suffix = suffix

        coords = {}

        for idx in indices:
            p = base + outer_values[idx] - 1
            x = inner_values[idx]
            while p:
                if p in coords:
                    coords[p].append(x)
                else:
                    coords[p] = [x]
                p >>= 1

        bits = {}
        for node, lst in coords.items():
            lst.sort()

            unique_count = 0
            previous = None
            for x in lst:
                if x != previous:
                    lst[unique_count] = x
                    unique_count += 1
                    previous = x
            del lst[unique_count:]

            bits[node] = array('i', [0]) * (unique_count + 1)

        self.coords = coords
        self.bits = bits

    def update(self, outer, inner, value):
        p = self.base + outer - 1

        while p:
            lst = self.coords[p]
            bit = self.bits[p]
            n = len(lst)

            if self.suffix:
                # Reversed coordinate: larger original values become smaller.
                pos = n - bisect_left(lst, inner)
            else:
                pos = bisect_left(lst, inner) + 1

            while pos <= n:
                if value > bit[pos]:
                    bit[pos] = value
                pos += pos & -pos

            p >>= 1

    def _node_query(self, node, threshold):
        lst = self.coords.get(node)
        if lst is None:
            return 0

        bit = self.bits[node]

        if self.suffix:
            # Original coordinate strictly greater than threshold.
            pos = len(lst) - bisect_right(lst, threshold)
        else:
            # Original coordinate strictly less than threshold.
            pos = bisect_left(lst, threshold)

        result = 0
        while pos:
            if bit[pos] > result:
                result = bit[pos]
            pos -= pos & -pos

        return result

    def query(self, lo, hi, threshold):
        if lo > hi:
            return 0

        l = self.base + lo - 1
        r = self.base + hi - 1
        result = 0

        while l <= r:
            if l & 1:
                value = self._node_query(l, threshold)
                if value > result:
                    result = value
                l += 1

            if not (r & 1):
                value = self._node_query(r, threshold)
                if value > result:
                    result = value
                r -= 1

            l >>= 1
            r >>= 1

        return result


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    ptr = 0

    n = data[ptr]
    m = data[ptr + 1]
    q = data[ptr + 2]
    ptr += 3

    left = [0] * m
    right = [0] * m
    orientation = [0] * m

    for i in range(m):
        s = data[ptr]
        t = data[ptr + 1]
        ptr += 2

        if s < t:
            left[i] = s
            right[i] = t
        else:
            left[i] = t
            right[i] = s
            orientation[i] = 1

    queries = []
    for _ in range(q):
        l = data[ptr]
        r = data[ptr + 1]
        ptr += 2
        queries.append((l, r))

    # bad[i] is the largest 1-based earlier index conflicting with i.
    bad = [0] * m

    # Equal normalized left endpoints or equal normalized right endpoints.
    latest_left = [0] * (n + 1)
    latest_right = [0] * (n + 1)

    for i in range(m):
        l = left[i]
        r = right[i]

        value = latest_left[l]
        if latest_right[r] > value:
            value = latest_right[r]
        bad[i] = value

        latest_left[l] = i + 1
        latest_right[r] = i + 1

    # Earlier interval: l' < l < r' < r.
    # This is a conflict only when both directions are equal.
    for typ in (0, 1):
        indices = [i for i in range(m) if orientation[i] == typ]
        if not indices:
            continue

        # Point for an earlier interval: (r', l').
        # Need r' in (l, r), l' < l.
        tree = RangeTreeMax(n, right, left, indices, suffix=False)

        for i in indices:
            l = left[i]
            r = right[i]

            value = tree.query(l + 1, r - 1, l)
            if value > bad[i]:
                bad[i] = value

            tree.update(r, l, i + 1)

        del tree

    # Earlier interval: l < l' < r < r'.
    # Again this is a conflict only for equal directions.
    for typ in (0, 1):
        indices = [i for i in range(m) if orientation[i] == typ]
        if not indices:
            continue

        # Point for an earlier interval: (l', r').
        # Need l' in (l, r), r' > r.
        tree = RangeTreeMax(n, left, right, indices, suffix=True)

        for i in indices:
            l = left[i]
            r = right[i]

            value = tree.query(l + 1, r - 1, r)
            if value > bad[i]:
                bad[i] = value

            tree.update(l, r, i + 1)

        del tree

    # Segment tree for range maxima of bad.
    size = 1
    while size < m:
        size <<= 1

    seg = [0] * (size << 1)
    seg[size:size + m] = bad

    for i in range(size - 1, 0, -1):
        a = seg[i << 1]
        b = seg[i << 1 | 1]
        seg[i] = a if a >= b else b

    answer = []

    for l, r in queries:
        a = size + l - 1
        b = size + r
        maximum = 0

        while a < b:
            if a & 1:
                if seg[a] > maximum:
                    maximum = seg[a]
                a += 1

            if b & 1:
                b -= 1
                if seg[b] > maximum:
                    maximum = seg[b]

            a >>= 1
            b >>= 1

        answer.append("Yes" if maximum < l else "No")

    sys.stdout.write("\n".join(answer))


if __name__ == "__main__":
    main()