import sys

# Increase recursion depth to handle deep trees if necessary
sys.setrecursionlimit(3000000)

class SegmentTree:
    def __init__(self, size):
        # Size needs to be a power of 2 for easier iterative implementation
        # or we can handle arbitrary sizes. Let's use a standard array size.
        # Max value is 500000. Let's use 500005.
        self.n = size
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        
        # tree stores the values (min and max are the same since array is sorted)
        # Actually, we need to store min and max to prune the search.
        # Since the array is always sorted, min is at left child, max at right child?
        # No, min is the value at index 0 of the range, max is value at index (end) of range.
        # But with lazy propagation, we need to track min and max of the range covered by the node.
        self.tree_min = [0] * (2 * self.size)
        self.tree_max = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        
        # Initialize leaves
        # Indices 0 to n-1 correspond to initial ratings 0 to n-1
        # Value at index i is i.
        for i in range(self.n):
            self.tree_min[self.size + i] = i
            self.tree_max[self.size + i] = i
        # Fill the rest with infinity/-infinity if needed, but we only query up to n
        # For safety in min/max logic, fill with appropriate bounds
        for i in range(self.n, self.size):
            self.tree_min[self.size + i] = float('inf')
            self.tree_max[self.size + i] = float('-inf')
            
        # Build the tree
        for i in range(self.size - 1, 0, -1):
            self.tree_min[i] = min(self.tree_min[2 * i], self.tree_min[2 * i + 1])
            self.tree_max[i] = max(self.tree_max[2 * i], self.tree_max[2 * i + 1])

    def push(self, node):
        if self.lazy[node] != 0:
            val = self.lazy[node]
            self.lazy[2 * node] += val
            self.tree_min[2 * node] += val
            self.tree_max[2 * node] += val
            
            self.lazy[2 * node + 1] += val
            self.tree_min[2 * node + 1] += val
            self.tree_max[2 * node + 1] += val
            
            self.lazy[node] = 0

    def update_range(self, l, r, val):
        # Update range [l, r) (0-indexed)
        if l >= r:
            return
        
        self._update_recursive(1, 0, self.size, l, r, val)

    def _update_recursive(self, node, node_l, node_r, l, r, val):
        if node_l >= r or node_r <= l:
            return
        
        if node_l >= l and node_r <= r:
            self.lazy[node] += val
            self.tree_min[node] += val
            self.tree_max[node] += val
            return
        
        self.push(node)
        mid = (node_l + node_r) // 2
        self._update_recursive(2 * node, node_l, mid, l, r, val)
        self._update_recursive(2 * node + 1, mid, node_r, l, r, val)
        
        self.tree_min[node] = min(self.tree_min[2 * node], self.tree_min[2 * node + 1])
        self.tree_max[node] = max(self.tree_max[2 * node], self.tree_max[2 * node + 1])

    def find_first_ge(self, val):
        # Find smallest index i such that A[i] >= val
        # We need to push down laziness as we traverse
        return self._find_first_recursive(1, 0, self.size, val)

    def _find_first_recursive(self, node, node_l, node_r, val):
        # If the max value in this range is less than val, no element here satisfies condition
        if self.tree_max[node] < val:
            return -1
        
        # If leaf
        if node_l == node_r:
            return node_l
        
        self.push(node)
        mid = (node_l + node_r) // 2
        
        # Try left child first
        res = self._find_first_recursive(2 * node, node_l, mid, val)
        if res != -1:
            return res
        
        # Try right child
        return self._find_first_recursive(2 * node + 1, mid, node_r, val)

    def find_last_le(self, val):
        # Find largest index i such that A[i] <= val
        if self.tree_min[1] > val:
            return -1
            
        return self._find_last_recursive(1, 0, self.size, val)

    def _find_last_recursive(self, node, node_l, node_r, val):
        # If the min value in this range is greater than val, no element here satisfies condition
        if self.tree_min[node] > val:
            return -1
        
        if node_l == node_r:
            return node_l
        
        self.push(node)
        mid = (node_l + node_r) // 2
        
        # Try right child first
        res = self._find_last_recursive(2 * node + 1, mid, node_r, val)
        if res != -1:
            return res
        
        # Try left child
        return self._find_last_recursive(2 * node, node_l, mid, val)

    def get_value(self, idx):
        # Push down to leaf
        idx += self.size
        while idx > 1:
            idx //= 2
            self.push(idx)
        return self.tree_min[idx]

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Read N contests
    contests = []
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        contests.append((L, R))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    # Max possible rating is 500000. We need to cover up to 500000.
    # The array indices will be 0 to 500000. Size = 500001.
    MAX_VAL = 500005
    st = SegmentTree(MAX_VAL)
    
    # Process contests
    for L, R in contests:
        # We need to find range [l, r] of indices such that st.get_value(i) is in [L, R]
        # Since the array is sorted, we find first index with value >= L
        # and last index with value <= R.
        
        l_idx = st.find_first_ge(L)
        r_idx = st.find_last_le(R)
        
        if l_idx != -1 and r_idx != -1 and l_idx <= r_idx:
            st.update_range(l_idx, r_idx + 1, 1)
            
    # Process queries
    results = []
    for _ in range(Q):
        X = int(next(iterator))
        # Ensure X is within bounds
        if X >= MAX_VAL:
            # If X is larger than our tracked range, it won't have been incremented
            # because all intervals are <= 500000.
            # However, if X was incremented, it could exceed 500000.
            # But we only track up to 500000. 
            # If initial X > 500000, it never enters any interval [L, R] where R <= 500000.
            # So result is X.
            results.append(str(X))
        else:
            results.append(str(st.get_value(X)))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()