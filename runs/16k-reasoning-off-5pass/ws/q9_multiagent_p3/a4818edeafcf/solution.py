import sys

# Increase recursion depth for deep segment tree operations if necessary
sys.setrecursionlimit(300000)

class SegmentTree:
    def __init__(self, n, initial):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        # Build
        for i in range(n):
            self.tree[self.size + i] = initial[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
        
    def push(self, idx):
        if self.lazy[idx] != 0:
            self.tree[2 * idx] += self.lazy[idx]
            self.lazy[2 * idx] += self.lazy[idx]
            self.tree[2 * idx + 1] += self.lazy[idx]
            self.lazy[2 * idx + 1] += self.lazy[idx]
            self.lazy[idx] = 0

    def update(self, l, r, val, node=1, start=0, end=None):
        if end is None:
            end = self.size - 1
        
        if l > end or r < start:
            return
        
        if l <= start and end <= r:
            self.tree[node] += val
            self.lazy[node] += val
            return
        
        self.push(node)
        mid = (start + end) // 2
        self.update(l, r, val, 2 * node, start, mid)
        self.update(l, r, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, l, r, node=1, start=0, end=None):
        if end is None:
            end = self.size - 1
        
        if l > end or r < start:
            return 0
        
        if l <= start and end <= r:
            return self.tree[node]
        
        self.push(node)
        mid = (start + end) // 2
        left_max = self.query(l, r, 2 * node, start, mid)
        right_max = self.query(l, r, 2 * node + 1, mid + 1, end)
        return max(left_max, right_max)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # A is 0-indexed in Python: A[0]...A[N-1]
    # Split points i, j (1-based) correspond to:
    # Left: A[0]...A[i-1]
    # Middle: A[i]...A[j-1]
    # Right: A[j]...A[N-1]
    # Constraints: 1 <= i < j <= N-1
    # In 0-based: split indices (i, j) where 0 <= i < j <= N-2
    # Left: 0..i, Middle: i+1..j, Right: j+1..N-1
    
    # Precompute suffix distinct counts
    # suff[k] = distinct count in A[k...N-1]
    suff = [0] * (N + 1)
    seen = set()
    for k in range(N - 1, -1, -1):
        seen.add(A[k])
        suff[k] = len(seen)
    
    # Precompute next_occurrence
    # next_occ[k] = index of first occurrence of A[k] in A[k+1...N-1]
    # If not found, N
    next_occ = [N] * N
    last_pos = {}
    for k in range(N - 1, -1, -1):
        val = A[k]
        if val in last_pos:
            next_occ[k] = last_pos[val]
        else:
            next_occ[k] = N
        last_pos[val] = k

    # Precompute prefix distinct counts
    # pref[i] = distinct count in A[0...i]
    pref = [0] * N
    seen = set()
    for k in range(N):
        seen.add(A[k])
        pref[k] = len(seen)

    # Initialize Segment Tree
    # We need values for j in 0..N-2.
    # val[j] = 1 + suff[j+1]
    init_vals = [0] * (N + 1) 
    for j in range(N - 1): # 0 to N-2
        init_vals[j] = 1 + suff[j+1]
    
    st = SegmentTree(N, init_vals)
    
    ans = 0
    
    # Iterate i from N-3 down to 0
    for i in range(N - 3, -1, -1):
        # Query max(distinct(i+1, j) + suff[j+1]) for j in [i+1, N-2]
        if i + 1 <= N - 2:
            max_mid_right = st.query(i + 1, N - 2)
            current_total = pref[i] + max_mid_right
            if current_total > ans:
                ans = current_total
        
        # Update for next iteration (i-1)
        # We need to add 1 to distinct count for j where A[i] is new in A[i+1..j]
        # This is for j in [i+1, next_occ[i]-1]
        end_update = min(next_occ[i] - 1, N - 2)
        if i + 1 <= end_update:
            st.update(i + 1, end_update, 1)
            
    print(ans)

if __name__ == '__main__':
    solve()