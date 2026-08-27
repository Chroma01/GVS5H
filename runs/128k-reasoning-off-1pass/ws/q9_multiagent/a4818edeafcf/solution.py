import sys

# Increase recursion depth just in case, though iterative segment tree is used
sys.setrecursionlimit(200000)

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)

    def _push(self, x):
        if self.lazy[x] != 0:
            self.tree[2 * x] += self.lazy[x]
            self.lazy[2 * x] += self.lazy[x]
            self.tree[2 * x + 1] += self.lazy[x]
            self.lazy[2 * x + 1] += self.lazy[x]
            self.lazy[x] = 0

    def update(self, l, r, val):
        # Range [l, r)
        l += self.size
        r += self.size
        while l < r:
            if l % 2 == 1:
                self.tree[l] += val
                self.lazy[l] += val
                l += 1
            if r % 2 == 1:
                r -= 1
                self.tree[r] += val
                self.lazy[r] += val
            l //= 2
            r //= 2
            if l < r:
                self._push(l)
                self._push(r)

    def query(self, l, r):
        # Range [l, r)
        l += self.size
        r += self.size
        res = -float('inf')
        while l < r:
            if l % 2 == 1:
                res = max(res, self.tree[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res = max(res, self.tree[r])
            l //= 2
            r //= 2
            if l < r:
                self._push(l)
                self._push(r)
        return res

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    A = [int(x) for x in data[1:]]
    
    # Precompute prefix distinct counts
    # pref[i] = distinct count in A[0...i-1] (length i)
    pref = [0] * (N + 1)
    seen = set()
    cnt = 0
    for i in range(N):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        pref[i+1] = cnt
        
    # Precompute suffix distinct counts
    # suff[i] = distinct count in A[i...N-1]
    suff = [0] * (N + 1)
    seen = set()
    cnt = 0
    for i in range(N-1, -1, -1):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        suff[i] = cnt
        
    # Segment Tree to maintain max of (pref[i+1] + distinct(i+1, j))
    st = SegmentTree(N)
    
    # last_pos maps value -> last seen index (0-based)
    last_pos = {}
    
    # Initialize last_pos with A[0] at index 0
    if N >= 1:
        last_pos[A[0]] = 0
    
    # If N >= 2, we also need A[1] in last_pos for the logic to work correctly when j=1
    # because when we process j=1, we look for A[2] and check against history up to A[1].
    if N >= 2:
        last_pos[A[1]] = 1
        
    # Initial setup for j = 1 (second split point, 0-based)
    # We need to consider i = 0.
    # distinct(1, 1) is distinct count of A[1...1] which is 1.
    # Value at i=0: pref[1] + 1
    
    if N >= 2:
        st.update(0, 1, pref[1] + 1)
    else:
        # If N < 2, we can't split into 3 non-empty parts, but constraints say N >= 3.
        # Just in case, handle gracefully.
        return

    ans = 0
    
    # Iterate j from 1 to N-2
    for j in range(1, N - 1):
        # Query max for i in [0, j-1]
        # st.query(0, j) covers [0, j)
        current_max = st.query(0, j)
        if current_max != -float('inf'):
            total = current_max + suff[j+1]
            if total > ans:
                ans = total
        
        # Prepare for j+1
        x = A[j+1]
        p = last_pos.get(x, -1)
        
        if p != -1:
            # Update range [p, j)
            if p < j:
                st.update(p, j, 1)
        else:
            # Update range [0, j)
            st.update(0, j, 1)
            
        # Add new i = j
        # val[j] = pref[j+1] + 1
        val_j = pref[j+1] + 1
        st.update(j, j+1, val_j)
        
        # Update last_pos
        last_pos[x] = j+1
        
    print(ans)

if __name__ == '__main__':
    solve()