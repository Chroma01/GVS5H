import sys

class LazySegTree:
    def __init__(self, values):
        self.n = len(values)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.mx = [-10**18] * (self.size * 2)
        self.lazy = [0] * (self.size * 2)
        for i, v in enumerate(values):
            self.mx[self.size + i] = v
        for i in range(self.size - 1, 0, -1):
            self.mx[i] = max(self.mx[i << 1], self.mx[i << 1 | 1])

    def _apply(self, node, delta):
        self.mx[node] += delta
        self.lazy[node] += delta

    def _push(self, node):
        delta = self.lazy[node]
        if delta:
            self._apply(node << 1, delta)
            self._apply(node << 1 | 1, delta)
            self.lazy[node] = 0

    def add(self, left, right, delta=1):
        self._add(left, right, delta, 1, 0, self.size)

    def _add(self, left, right, delta, node, nl, nr):
        if right <= nl or nr <= left:
            return
        if left <= nl and nr <= right:
            self._apply(node, delta)
            return
        self._push(node)
        mid = (nl + nr) >> 1
        self._add(left, right, delta, node << 1, nl, mid)
        self._add(left, right, delta, node << 1 | 1, mid, nr)
        self.mx[node] = max(self.mx[node << 1], self.mx[node << 1 | 1])

    def first_at_least(self, threshold):
        if self.mx[1] < threshold:
            return self.n
        return self._first_at_least(threshold, 1, 0, self.size)

    def _first_at_least(self, threshold, node, nl, nr):
        if nr - nl == 1:
            return nl
        self._push(node)
        mid = (nl + nr) >> 1
        if self.mx[node << 1] >= threshold:
            return self._first_at_least(threshold, node << 1, nl, mid)
        return self._first_at_least(threshold, node << 1 | 1, mid, nr)

    def get(self, index):
        return self._get(index, 1, 0, self.size)

    def _get(self, index, node, nl, nr):
        if nr - nl == 1:
            return self.mx[node]
        self._push(node)
        mid = (nl + nr) >> 1
        if index < mid:
            return self._get(index, node << 1, nl, mid)
        return self._get(index, node << 1 | 1, mid, nr)


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

    distinct = sorted(set(queries))
    positions = {x: i for i, x in enumerate(distinct)}
    seg = LazySegTree(distinct)

    for l, r in contests:
        left = seg.first_at_least(l)
        right = seg.first_at_least(r + 1)
        if left < right:
            seg.add(left, right)

    final_values = {x: seg.get(i) for i, x in enumerate(distinct)}
    sys.stdout.write("\n".join(str(final_values[x]) for x in queries))


if __name__ == "__main__":
    main()