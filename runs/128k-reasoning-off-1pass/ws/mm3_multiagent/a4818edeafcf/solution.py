import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))
    
    # prefix distinct counts
    pref = [0] * (N + 1)
    seen = [False] * (N + 1)
    for i in range(1, N + 1):
        if not seen[A[i]]:
            seen[A[i]] = True
            pref[i] = pref[i - 1] + 1
        else:
            pref[i] = pref[i - 1]
    
    # suffix distinct counts
    suff = [0] * (N + 2)
    seen = [False] * (N + 1)
    for i in range(N, 0, -1):
        if not seen[A[i]]:
            seen[A[i]] = True
            suff[i] = suff[i + 1] + 1
        else:
            suff[i] = suff[i + 1]
    suff[N + 1] = 0
    
    # segment tree for range add and range max
    class SegTree:
        __slots__ = ('n', 'size', 'tree', 'lazy')
        def __init__(self, n):
            self.n = n
            self.size = 1
            while self.size < n:
                self.size <<= 1
            self.tree = [0] * (2 * self.size)
            self.lazy = [0] * (2 * self.size)
        
        def _push(self, node):
            if self.lazy[node]:
                self.tree[node * 2] += self.lazy[node]
                self.lazy[node * 2] += self.lazy[node]
                self.tree[node * 2 + 1] += self.lazy[node]
                self.lazy[node * 2 + 1] += self.lazy[node]
                self.lazy[node] = 0
        
        def _range_add(self, l, r, val, node, node_l, node_r):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                self.tree[node] += val
                self.lazy[node] += val
                return
            self._push(node)
            mid = (node_l + node_r) // 2
            self._range_add(l, r, val, node * 2, node_l, mid)
            self._range_add(l, r, val, node * 2 + 1, mid + 1, node_r)
            self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])
        
        def range_add(self, l, r, val):
            if l > r:
                return
            self._range_add(l, r, val, 1, 1, self.n)
        
        def _range_max(self, l, r, node, node_l, node_r):
            if r < node_l or node_r < l:
                return -10**9
            if l <= node_l and node_r <= r:
                return self.tree[node]
            self._push(node)
            mid = (node_l + node_r) // 2
            return max(self._range_max(l, r, node * 2, node_l, mid),
                       self._range_max(l, r, node * 2 + 1, mid + 1, node_r))
        
        def range_max(self, l, r):
            return self._range_max(l, r, 1, 1, self.n)
    
    seg = SegTree(N)
    last = [0] * (N + 1)
    last[A[1]] = 1
    ans = 0
    
    for j in range(2, N):
        v = A[j]
        last_v = last[v]
        if last_v > 0:
            seg.range_add(last_v, j - 1, 1)
        max_common = seg.range_max(1, j - 1)
        candidate = pref[j] + suff[j + 1] + max_common
        if candidate > ans:
            ans = candidate
        last[v] = j
    
    print(ans)

if __name__ == "__main__":
    solve()