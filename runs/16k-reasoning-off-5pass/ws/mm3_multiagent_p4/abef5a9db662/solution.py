import sys

class SegTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        # Initialize leaves for indices 1..n with their own index
        for i in range(n):
            self.tree[self.size + i] = i + 1
        # Remaining leaves keep 0 (safe because queries have L >= 1)
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

    def _push(self, node, l, r):
        if self.lazy[node] != 0:
            if l != r:
                left = 2 * node
                right = left + 1
                self.tree[left] += self.lazy[node]
                self.lazy[left] += self.lazy[node]
                self.tree[right] += self.lazy[node]
                self.lazy[right] += self.lazy[node]
            self.lazy[node] = 0

    def _range_add(self, node, nl, nr, l, r, val):
        if r < nl or nr < l:
            return
        if l <= nl and nr <= r:
            self.tree[node] += val
            self.lazy[node] += val
            return
        self._push(node, nl, nr)
        mid = (nl + nr) // 2
        self._range_add(2 * node, nl, mid, l, r, val)
        self._range_add(2 * node + 1, mid + 1, nr, l, r, val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def range_add(self, l, r, val):
        if l > r:
            return
        self._range_add(1, 1, self.size, l, r, val)

    def find_first_ge(self, x):
        if self.tree[1] < x:
            return None
        node = 1
        nl = 1
        nr = self.size
        while nl != nr:
            self._push(node, nl, nr)
            mid = (nl + nr) // 2
            if self.tree[2 * node] >= x:
                node = 2 * node
                nr = mid
            else:
                node = 2 * node + 1
                nl = mid + 1
        return nl

    def point_query(self, idx):
        node = 1
        nl = 1
        nr = self.size
        while nl != nr:
            self._push(node, nl, nr)
            mid = (nl + nr) // 2
            if idx <= mid:
                node = 2 * node
                nr = mid
            else:
                node = 2 * node + 1
                nl = mid + 1
        return self.tree[node]

def main():
    import sys
    input = sys.stdin.readline
    N = int(input())
    intervals = []
    for _ in range(N):
        L, R = map(int, input().split())
        intervals.append((L, R))
    Q = int(input())
    queries = [int(input()) for _ in range(Q)]

    max_initial = max(queries) if queries else 0
    max_R = max((R for _, R in intervals), default=0)
    max_possible = max(max_initial, max_R) + N + 1
    n = max_possible
    if n < 1:
        n = 1

    seg = SegTree(n)

    for L, R in intervals:
        a = seg.find_first_ge(L)
        if a is None:
            continue
        b_idx = seg.find_first_ge(R + 1)
        if b_idx is None:
            b = n
        else:
            b = b_idx - 1
        if a <= b:
            seg.range_add(a, b, 1)

    out = []
    for X in queries:
        out.append(str(seg.point_query(X)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()