import sys

# Increase recursion depth to handle deep trees if necessary
sys.setrecursionlimit(3000000)

class SegmentTree:
    def __init__(self, n, max_val):
        """
        Initialize Segment Tree.
        n: number of leaves (initial ratings 1 to n)
        max_val: maximum possible value in the tree (current rating)
        """
        self.n = n
        self.max_val = max_val
        # Size of tree array: 4 * n is safe
        self.size = 1
        while self.size < n:
            self.size *= 2
        
        # Arrays: min_val, max_val, lazy_add
        # Using lists for simplicity. Index 1 is root.
        self.min_val = [0] * (4 * self.size)
        self.max_val = [0] * (4 * self.size)
        self.lazy = [0] * (4 * self.size)

        # Build the tree
        # Leaf i (0-indexed) corresponds to initial rating i+1
        # Initially, current rating = initial rating
        self._build(1, 0, self.size - 1)

    def _build(self, node, start, end):
        if start == end:
            # Leaf node: initial rating is start + 1
            val = start + 1
            self.min_val[node] = val
            self.max_val[node] = val
            self.lazy[node] = 0
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self.min_val[node] = min(self.min_val[2 * node], self.min_val[2 * node + 1])
            self.max_val[node] = max(self.max_val[2 * node], self.max_val[2 * node + 1])
            self.lazy[node] = 0

    def _push(self, node):
        if self.lazy[node] != 0:
            val = self.lazy[node]
            # Apply to left child
            self.min_val[2 * node] += val
            self.max_val[2 * node] += val
            self.lazy[2 * node] += val
            
            # Apply to right child
            self.min_val[2 * node + 1] += val
            self.max_val[2 * node + 1] += val
            self.lazy[2 * node + 1] += val
            
            # Reset current node
            self.lazy[node] = 0

    def update(self, l, r):
        """
        Add 1 to all leaves in range [l, r] (0-indexed).
        This function implements the pruning logic:
        - If max_val < l or min_val > r, skip.
        - If min_val >= l and max_val <= r, apply lazy and update min/max.
        - Otherwise, recurse.
        """
        self._update(1, 0, self.size - 1, l, r)

    def _update(self, node, start, end, l, r):
        # Pruning: if the range of current ratings in this node is completely outside [l, r]
        if self.max_val[node] < l or self.min_val[node] > r:
            return
        
        # If the range is completely inside [l, r]
        if self.min_val[node] >= l and self.max_val[node] <= r:
            self.min_val[node] += 1
            self.max_val[node] += 1
            self.lazy[node] += 1
            return

        # Push lazy before going down
        self._push(node)
        
        mid = (start + end) // 2
        
        # Recurse
        if start <= r:
            self._update(2 * node, start, mid, l, r)
        if end >= l:
            self._update(2 * node + 1, mid + 1, end, l, r)
            
        # Update current node from children
        self.min_val[node] = min(self.min_val[2 * node], self.min_val[2 * node + 1])
        self.max_val[node] = max(self.max_val[2 * node], self.max_val[2 * node + 1])

    def get_final_rating(self, x):
        """
        Get the final rating for initial rating x (1-indexed).
        x is 1-based, so we look at leaf index x-1.
        """
        if x < 1 or x > self.n:
            return 0
        # We need to query the specific leaf. 
        # Since we only did range updates, we can just traverse down or maintain a separate array.
        # However, to keep it simple and consistent with the tree structure, 
        # we can just query the leaf value. But wait, the tree stores min/max.
        # We need the exact value. Let's add a point query or just reconstruct.
        # Actually, since we only add 1, the value at leaf i is (i+1) + total_adds.
        # But total_adds depends on the path.
        # Let's implement a point query that sums up lazy values on the path.
        return self._query_point(1, 0, self.size - 1, x - 1)

    def _query_point(self, node, start, end, idx):
        if start == end:
            return self.min_val[node]
        
        self._push(node)
        mid = (start + end) // 2
        if idx <= mid:
            return self._query_point(2 * node, start, mid, idx)
        else:
            return self._query_point(2 * node + 1, mid + 1, end, idx)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        contests = []
        for _ in range(N):
            L = int(next(iterator))
            R = int(next(iterator))
            contests.append((L, R))
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            X = int(next(iterator))
            queries.append(X)
    except StopIteration:
        return

    # Max possible initial rating is 500,000
    MAX_RATING = 500000
    
    # Build Segment Tree
    # Leaves 0 to MAX_RATING-1 correspond to initial ratings 1 to MAX_RATING
    # The max possible rating can be 500000 + 200000 = 700000.
    # We set max_val to a safe upper bound.
    st = SegmentTree(MAX_RATING, MAX_RATING + N) 
    
    # Process contests
    for L, R in contests:
        # We need to update leaves corresponding to initial ratings X such that
        # current_rating(X) is in [L, R].
        # current_rating(X) is stored in the tree.
        # We update the range [L, R] on the tree values.
        # The tree leaves are indexed 0..MAX_RATING-1.
        # The update function handles the logic based on min/max values.
        st.update(L, R)
        
    # Answer queries
    results = []
    for X in queries:
        if X > MAX_RATING:
            # If X is larger than our tree size, it never enters any [L, R] since max R is 500,000
            # and L >= 1. So rating stays X.
            results.append(str(X))
        else:
            res = st.get_final_rating(X)
            results.append(str(res))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()