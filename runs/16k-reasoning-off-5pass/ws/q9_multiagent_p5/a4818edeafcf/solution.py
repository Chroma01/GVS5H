import sys

# Increase recursion depth to handle deep recursion in Segment Tree if necessary
sys.setrecursionlimit(300000)

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        # Initialize leaves
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        # Build tree
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
    
    def _push(self, node):
        if self.lazy[node] != 0:
            self.tree[2 * node] += self.lazy[node]
            self.lazy[2 * node] += self.lazy[node]
            self.tree[2 * node + 1] += self.lazy[node]
            self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0

    def _update(self, node, start, end, l, r, val):
        if r <= start or end <= l:
            return
        if l <= start and end <= r:
            self.tree[node] += val
            self.lazy[node] += val
            return
        self._push(node)
        mid = (start + end) // 2
        self._update(2 * node, start, mid, l, r, val)
        self._update(2 * node + 1, mid, end, l, r, val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * i + 1])

    def update_range(self, l, r, val):
        if l >= r:
            return
        self._update(1, 0, self.size, l, r, val)

    def _query(self, node, start, end, l, r):
        if r <= start or end <= l:
            return -float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        self._push(node)
        mid = (start + end) // 2
        v1 = self._query(2 * node, start, mid, l, r)
        v2 = self._query(2 * node + 1, mid, end, l, r)
        return max(v1, v2)

    def query_range(self, l, r):
        if l >= r:
            return -float('inf')
        return self._query(1, 0, self.size, l, r)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    if N < 3:
        print(0)
        return

    # Precompute next_occurrence
    # next_occ[i] = index of the next occurrence of A[i] after i
    # If no next occurrence, set to N
    next_occ = [N] * N
    last_pos = {}
    for i in range(N - 1, -1, -1):
        val = A[i]
        if val in last_pos:
            next_occ[i] = last_pos[val]
        last_pos[val] = i

    # Precompute suffix distinct counts
    # S[k] = distinct count in A[k...N-1]
    S = [0] * (N + 1)
    seen = set()
    for i in range(N - 1, -1, -1):
        seen.add(A[i])
        S[i] = len(seen)

    # Precompute prefix distinct counts
    # Pre[i] = distinct count in A[0...i]
    Pre = [0] * N
    seen = set()
    for i in range(N):
        seen.add(A[i])
        Pre[i] = len(seen)

    # Initialize Segment Tree
    # We need to maintain values for j in range [1, N-2] (0-based indices of A)
    # The value at index j (in our logic) corresponds to distinct(A[i+1...j]) + S[j+1]
    # In the Segment Tree, we map j to index j-1.
    # So the tree covers indices 0 to N-3.
    # Size of tree = N-2.
    
    if N - 2 <= 0:
        print(0)
        return

    initial_vals = []
    seen = set()
    # Calculate initial values for i=0 (middle part starts at index 1)
    # j ranges from 1 to N-2
    for j in range(1, N - 1):
        seen.add(A[j])
        d_mid = len(seen)
        val = d_mid + S[j+1]
        initial_vals.append(val)

    st = SegmentTree(initial_vals)
    
    ans = 0
    
    # Iterate i from 0 to N-3
    # i is the end index of the first subarray (0-based)
    # 1st part: A[0...i]
    # 2nd part: A[i+1...j]
    # 3rd part: A[j+1...N-1]
    # We need to maximize Pre[i] + (distinct(i+1...j) + S[j+1])
    # The term in parenthesis is stored in the Segment Tree at index j-1.
    
    for i in range(N - 2):
        # Query max for j in [i+1, N-2]
        # Tree indices correspond to j-1, so range is [i, N-3]
        # In SegmentTree query_range(l, r), r is exclusive.
        # So we query [i, N-2)
        
        q = st.query_range(i, N - 2)
        if q != -float('inf'):
            current_val = Pre[i] + q
            if current_val > ans:
                ans = current_val
        
        # Prepare for next iteration (i -> i+1)
        # We need to update the tree to reflect the removal of A[i+1] from the start of the middle segment.
        # The middle segment changes from A[i+1...j] to A[i+2...j].
        # If A[i+1] was the unique occurrence in A[i+1...j], the distinct count decreases by 1.
        # This happens if the next occurrence of A[i+1] is > j.
        # Let next_idx = next_occ[i+1].
        # We need to subtract 1 for all j such that i+1 <= j < next_idx.
        # In tree indices (j-1), this corresponds to range [i, next_idx - 2].
        # So update range [i, next_idx - 1) in the tree.
        
        if i < N - 3:
            val_to_remove = A[i+1]
            next_idx = next_occ[i+1]
            
            # Determine the right bound for the update
            # We want to update j up to next_idx - 1.
            # Tree index for j is j-1.
            # Max tree index to update is (next_idx - 1) - 1 = next_idx - 2.
            # So range is [i, next_idx - 1).
            # Also, j cannot exceed N-2, so tree index cannot exceed N-3.
            # Thus, r_update = min(next_idx - 1, N - 2).
            
            r_update = min(next_idx - 1, N - 2)
            if r_update > i:
                st.update_range(i, r_update, -1)

    print(ans)

if __name__ == '__main__':
    solve()