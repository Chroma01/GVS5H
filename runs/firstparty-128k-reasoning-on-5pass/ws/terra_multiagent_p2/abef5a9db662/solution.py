import sys


class LazySegmentTree:
    def __init__(self, values):
        self.n = len(values)
        size = 4 * self.n + 5
        self.mx = [0] * size
        self.lazy = [0] * size
        self._build(1, 0, self.n, values)

    def _build(self, node, left, right, values):
        if right - left == 1:
            self.mx[node] = values[left]
            return
        mid = (left + right) // 2
        self._build(node * 2, left, mid, values)
        self._build(node * 2 + 1, mid, right, values)
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def _apply(self, node, add):
        self.mx[node] += add
        self.lazy[node] += add

    def _push(self, node):
        add = self.lazy[node]
        if add:
            self._apply(node * 2, add)
            self._apply(node * 2 + 1, add)
            self.lazy[node] = 0

    def range_add(self, ql, qr, add=1):
        self._range_add(1, 0, self.n, ql, qr, add)

    def _range_add(self, node, left, right, ql, qr, add):
        if qr <= left or right <= ql:
            return
        if ql <= left and right <= qr:
            self._apply(node, add)
            return
        self._push(node)
        mid = (left + right) // 2
        self._range_add(node * 2, left, mid, ql, qr, add)
        self._range_add(node * 2 + 1, mid, right, ql, qr, add)
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def first_at_least(self, value):
        if self.mx[1] < value:
            return self.n
        return self._first_at_least(1, 0, self.n, value)

    def _first_at_least(self, node, left, right, value):
        if right - left == 1:
            return left
        self._push(node)
        mid = (left + right) // 2
        if self.mx[node * 2] >= value:
            return self._first_at_least(node * 2, left, mid, value)
        return self._first_at_least(node * 2 + 1, mid, right, value)

    def first_greater_than(self, value):
        if self.mx[1] <= value:
            return self.n
        return self._first_greater_than(1, 0, self.n, value)

    def _first_greater_than(self, node, left, right, value):
        if right - left == 1:
            return left
        self._push(node)
        mid = (left + right) // 2
        if self.mx[node * 2] > value:
            return self._first_greater_than(node * 2, left, mid, value)
        return self._first_greater_than(node * 2 + 1, mid, right, value)

    def point_get(self, index):
        return self._point_get(1, 0, self.n, index)

    def _point_get(self, node, left, right, index):
        if right - left == 1:
            return self.mx[node]
        self._push(node)
        mid = (left + right) // 2
        if index < mid:
            return self._point_get(node * 2, left, mid, index)
        return self._point_get(node * 2 + 1, mid, right, index)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    ptr = 0

    n = data[ptr]
    ptr += 1
    contests = []
    for _ in range(n):
        l = data[ptr]
        r = data[ptr + 1]
        ptr += 2
        contests.append((l, r))

    q = data[ptr]
    ptr += 1
    queries = data[ptr:ptr + q]

    unique_values = sorted(set(queries))
    seg = LazySegmentTree(unique_values)

    for l, r in contests:
        left = seg.first_at_least(l)
        right = seg.first_greater_than(r)
        if left < right:
            seg.range_add(left, right)

    final_by_initial = {
        x: seg.point_get(i)
        for i, x in enumerate(unique_values)
    }

    sys.stdout.write("\n".join(str(final_by_initial[x]) for x in queries))


if __name__ == "__main__":
    main()