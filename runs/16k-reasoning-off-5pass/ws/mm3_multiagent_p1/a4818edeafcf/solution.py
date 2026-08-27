import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # Compute prefix distinct counts
    pref = [0] * N
    seen = [False] * (N + 1)
    cnt = 0
    for i in range(N):
        if not seen[A[i]]:
            seen[A[i]] = True
            cnt += 1
        pref[i] = cnt
    
    # Compute suffix distinct counts
    suf = [0] * (N + 1)
    seen = [False] * (N + 1)
    cnt = 0
    for i in range(N - 1, -1, -1):
        if not seen[A[i]]:
            seen[A[i]] = True
            cnt += 1
        suf[i] = cnt
    suf[N] = 0
    
    # Segment tree with lazy propagation for range add and range max
    class SegTree:
        __slots__ = ('n', 'size', 'tree', 'lazy')
        def __init__(self, n):
            self.n = n
            self.size = 1
            while self.size < n:
                self.size <<= 1
            self.tree = [0] * (2 * self.size)
            self.lazy = [0] * (2 * self.size)
        
        def build(self, data):
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
        
        def _apply(self, idx, val):
            self.tree[idx] += val
            self.lazy[idx] += val
        
        def _push(self, idx):
            if self.lazy[idx] != 0:
                self._apply(2*idx, self.lazy[idx])
                self._apply(2*idx+1, self.lazy[idx])
                self.lazy[idx] = 0
        
        def _add(self, idx, l, r, ql, qr, val):
            if ql > r or qr < l:
                return
            if ql <= l and r <= qr:
                self._apply(idx, val)
                return
            self._push(idx)
            mid = (l + r) // 2
            self._add(2*idx, l, mid, ql, qr, val)
            self._add(2*idx+1, mid+1, r, ql, qr, val)
            self.tree[idx] = max(self.tree[2*idx], self.tree[2*idx+1])
        
        def add(self, l, r, val):
            if l > r:
                return
            self._add(1, 0, self.size - 1, l, r, val)
        
        def _query(self, idx, l, r, ql, qr):
            if ql > r or qr < l:
                return -10**9
            if ql <= l and r <= qr:
                return self.tree[idx]
            self._push(idx)
            mid = (l + r) // 2
            left = self._query(2*idx, l, mid, ql, qr)
            right = self._query(2*idx+1, mid+1, r, ql, qr)
            return max(left, right)
        
        def query(self, l, r):
            if l > r:
                return -10**9
            return self._query(1, 0, self.size - 1, l, r)
    
    seg = SegTree(N)
    seg.build(pref)
    
    last_occ = [-1] * (N + 1)
    ans = 0
    
    for m in range(1, N - 1):
        val = A[m]
        prev = last_occ[val]
        l = max(prev, 0)
        r = m - 1
        if l <= r:
            seg.add(l, r, 1)
        max_val = seg.query(0, m - 1)
        candidate = max_val + suf[m + 1]
        if candidate > ans:
            ans = candidate
        last_occ[val] = m
    
    print(ans)

if __name__ == "__main__":
    solve()