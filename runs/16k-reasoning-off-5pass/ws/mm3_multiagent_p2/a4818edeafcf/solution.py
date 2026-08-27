import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    
    # Compute prefix distinct counts
    pref = [0] * (N + 1)
    last_occ = [0] * (N + 1)  # since 1 <= A_i <= N
    distinct_count = 0
    for i in range(1, N + 1):
        if last_occ[A[i]] == 0:
            distinct_count += 1
        last_occ[A[i]] = i
        pref[i] = distinct_count
    
    # Compute suffix distinct counts
    suf = [0] * (N + 2)  # suf[i] for i=1..N
    last_occ = [N + 1] * (N + 1)
    distinct_count = 0
    for i in range(N, 0, -1):
        if last_occ[A[i]] == N + 1:
            distinct_count += 1
        last_occ[A[i]] = i
        suf[i] = distinct_count
    
    # C[i] = suf[i+1] for i=1..N-1
    C = [0] * (N + 1)
    for i in range(1, N):
        C[i] = suf[i + 1]
    
    # Compute next occurrence array
    nxt = [N + 1] * (N + 2)  # nxt[i] for i=1..N
    next_pos = [N + 1] * (N + 1)
    for i in range(N, 0, -1):
        nxt[i] = next_pos[A[i]]
        next_pos[A[i]] = i
    
    # Segment tree for range add and range max over indices 1..N-1
    class SegTree:
        __slots__ = ('n', 'size', 'tree', 'lazy')
        def __init__(self, n):
            self.n = n
            size = 1
            while size < n:
                size <<= 1
            self.size = size
            self.tree = [0] * (2 * size)
            self.lazy = [0] * (2 * size)
        
        def _apply(self, idx, val):
            self.tree[idx] += val
            self.lazy[idx] += val
        
        def _push(self, idx):
            if self.lazy[idx] != 0:
                self._apply(idx << 1, self.lazy[idx])
                self._apply(idx << 1 | 1, self.lazy[idx])
                self.lazy[idx] = 0
        
        def _add(self, l, r, val, idx, left, right):
            if l > right or r < left:
                return
            if l <= left and right <= r:
                self._apply(idx, val)
                return
            self._push(idx)
            mid = (left + right) >> 1
            self._add(l, r, val, idx << 1, left, mid)
            self._add(l, r, val, idx << 1 | 1, mid + 1, right)
            self.tree[idx] = self.tree[idx << 1] if self.tree[idx << 1] > self.tree[idx << 1 | 1] else self.tree[idx << 1 | 1]
        
        def range_add(self, l, r, val):
            if l > r:
                return
            self._add(l, r, val, 1, 1, self.size)
        
        def _max(self, l, r, idx, left, right):
            if l > right or r < left:
                return -10**9
            if l <= left and right <= r:
                return self.tree[idx]
            self._push(idx)
            mid = (left + right) >> 1
            left_max = self._max(l, r, idx << 1, left, mid)
            right_max = self._max(l, r, idx << 1 | 1, mid + 1, right)
            return left_max if left_max > right_max else right_max
        
        def range_max(self, l, r):
            if l > r:
                return -10**9
            return self._max(l, r, 1, 1, self.size)
    
    seg = SegTree(N - 1)
    G = [0] * (N + 1)
    # Process s from N-1 down to 1
    for s in range(N - 1, 0, -1):
        # Set total[s] = 1 + C[s]
        seg.range_add(s, s, 1 + C[s])
        # Add 1 to range [s+1, nxt[s]-1] intersected with [1, N-1]
        r = nxt[s] - 1
        if r > N - 1:
            r = N - 1
        if s + 1 <= r:
            seg.range_add(s + 1, r, 1)
        # G[s] is the maximum over indices >= s
        G[s] = seg.range_max(s, N - 1)
    
    # Compute the answer: max over s=2..N-1 of (pref[s-1] + G[s])
    ans = 0
    for s in range(2, N):
        val = pref[s - 1] + G[s]
        if val > ans:
            ans = val
    print(ans)

if __name__ == "__main__":
    solve()