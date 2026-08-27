import sys

# Increase recursion depth just in case, though we will use iterative segment trees
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for k in range(K):
            x = int(next(iterator))
            y = int(next(iterator))
            queries.append((x, y, k))
    except StopIteration:
        return

    # Sort A and B
    A.sort()
    B.sort()

    # Precompute prefix sums for A to quickly get sum_A in ranges for the weighted segment tree
    # prefix_A[i] = sum(A[0]...A[i-1])
    prefix_A = [0] * (N + 1)
    for i in range(N):
        prefix_A[i+1] = prefix_A[i] + A[i]

    # Helper to get sum of A in range [l, r) (0-based indices)
    def get_sum_A(l, r):
        if l >= r:
            return 0
        return prefix_A[r] - prefix_A[l]

    # Segment Tree for Base Values (Range Add, Range Sum)
    # We need to support:
    # 1. range_add(l, r, val)
    # 2. query_sum(l, r) -> returns sum in [l, r)
    # Since we only need prefix sums for queries (sum [0, X)), we can implement a BIT or SegTree.
    # Given the constraints and Python, a BIT is very efficient and easy to implement.
    # However, we need range updates. A BIT for range updates and prefix sums is standard.
    # To support range add [l, r) with v and prefix sum at x:
    # We maintain a BIT `diff`.
    # Update(l, v), Update(r, -v).
    # Prefix sum at x is sum(diff[0]...diff[x-1]).
    # Wait, standard BIT for range add / point query is different from range add / range sum.
    # For Range Add, Range Sum:
    # We need two BITs: B1 and B2.
    # Update(l, r, v):
    #   update(B1, l, v)
    #   update(B1, r, -v)
    #   update(B2, l, v*(l-1))
    #   update(B2, r, -v*(r-1))
    # Query(x):
    #   return query(B1, x)*x - query(B2, x)
    # Note: This assumes 1-based indexing for BIT logic. Let's stick to 0-based internally but map carefully.
    
    # Let's implement a class for Range Add, Range Sum BIT (using 1-based indexing for BIT array)
    class RangeAddRangeSumBIT:
        def __init__(self, size):
            self.n = size
            self.tree1 = [0] * (self.n + 1)
            self.tree2 = [0] * (self.n + 1)

        def _update(self, idx, val, tree):
            idx += 1 # 1-based
            while idx <= self.n:
                tree[idx] += val
                idx += idx & (-idx)

        def _query(self, idx, tree):
            idx += 1 # 1-based
            s = 0
            while idx > 0:
                s += tree[idx]
                idx -= idx & (-idx)
            return s

        def update_range(self, l, r, val):
            # Add val to [l, r)
            # l, r are 0-based indices.
            # In BIT logic (1-based), range [l, r) corresponds to indices l+1 to r.
            # Update at l+1 with +val, at r+1 with -val.
            self._update(l, val, self.tree1)
            self._update(r, -val, self.tree1)
            self._update(l, val * l, self.tree2)
            self._update(r, -val * r, self.tree2)

        def query_prefix(self, idx):
            # Sum of [0, idx)
            # Formula: query(B1, idx) * idx - query(B2, idx)
            # Here idx is the number of elements (0-based count).
            # If we want sum of first k elements (indices 0 to k-1), we pass k.
            return self._query(idx, self.tree1) * idx - self._query(idx, self.tree2)

    # Segment Tree for Coefficients (Range Add, Range Weighted Sum by A)
    # We need to support:
    # 1. range_add(l, r, val) -> adds val to coeff for each i in [l, r)
    # 2. query_weighted_sum(l, r) -> returns sum(coeff[i] * A[i]) for i in [l, r)
    # Since A is static, we can precompute sum_A for any range.
    # We need a Segment Tree with Lazy Propagation.
    
    class WeightedSegTree:
        def __init__(self, A, n):
            self.n = n
            self.size = 1
            while self.size <= n:
                self.size *= 2
            # Each node stores: sum_val (sum of coeff[i]*A[i]), lazy (pending add to coeff)
            # We also need sum_A for the node to update sum_val during lazy push.
            # sum_A is static, precomputed.
            self.sum_val = [0] * (2 * self.size)
            self.lazy = [0] * (2 * self.size)
            self.sum_A = [0] * (2 * self.size)
            
            # Build sum_A
            # Leaf nodes
            for i in range(n):
                self.sum_A[self.size + i] = A[i]
            # Internal nodes
            for i in range(self.size - 1, 0, -1):
                self.sum_A[i] = self.sum_A[2*i] + self.sum_A[2*i+1]

        def _push(self, node):
            if self.lazy[node] != 0:
                val = self.lazy[node]
                # Left child
                self.lazy[2*node] += val
                self.sum_val[2*node] += val * self.sum_A[2*node]
                # Right child
                self.lazy[2*node+1] += val
                self.sum_val[2*node+1] += val * self.sum_A[2*node+1]
                self.lazy[node] = 0

        def update_range(self, l, r, val):
            # Update [l, r)
            l += self.size
            r += self.size
            while l < r:
                if l % 2 == 1:
                    self.lazy[l] += val
                    self.sum_val[l] += val * self.sum_A[l]
                    l += 1
                if r % 2 == 1:
                    r -= 1
                    self.lazy[r] += val
                    self.sum_val[r] += val * self.sum_A[r]
                l //= 2
                r //= 2

        def query_prefix(self, idx):
            # Query sum in [0, idx)
            idx += self.size
            res = 0
            while idx > 0:
                self._push(idx) # Push lazy down before accessing children? 
                # Actually for prefix sum in iterative segtree, we just accumulate from leaves up?
                # No, standard iterative query for sum requires pushing lazy from root to leaves?
                # Or we can just accumulate the values stored in the nodes covering the range.
                # But those nodes might have lazy values.
                # Correct iterative approach for range sum with lazy:
                # We need to push lazy from the path from root to the leaves involved.
                # However, the standard iterative implementation usually handles this by pushing down.
                # Let's rewrite query to be safe.
                pass
            
            # Re-implementing query properly for iterative lazy segtree
            # We need to push lazy from root down to the leaves covering [0, idx)
            # But since we only query prefix, we can just traverse the path.
            # Actually, the standard iterative update/query works if we push lazy correctly.
            # Let's use a recursive helper for query to be absolutely sure, or fix iterative.
            # Given N=10^5, recursion depth ~18 is fine.
            return self._query_recursive(0, 0, self.n, 0, idx)

        def _query_recursive(self, node, start, end, l, r):
            if r <= start or end <= l:
                return 0
            if l <= start and end <= r:
                return self.sum_val[node]
            self._push(node)
            mid = (start + end) // 2
            return self._query_recursive(2*node, start, mid, l, r) + \
                   self._query_recursive(2*node+1, mid, end, l, r)

    # Initialize structures
    bit_base = RangeAddRangeSumBIT(N)
    st_coeff = WeightedSegTree(A, N)

    # Sort queries by Y
    queries.sort(key=lambda q: q[1])
    
    results = [0] * K
    current_y = 0
    
    # Process B elements
    for x, y, k in queries:
        # We need to process B elements from current_y up to y-1
        while current_y < y:
            b_val = B[current_y]
            
            # Find split point p in A: number of elements <= b_val
            # bisect_right returns insertion point after all elements <= x
            # So A[0]...A[p-1] are <= b_val. Indices 0 to p-1.
            # In 0-based indexing: range [0, p)
            import bisect
            p = bisect.bisect_right(A, b_val)
            
            # Update Base BIT
            # For i in [0, p): add (b_val - A[i]) -> Base += b_val, Coeff -= 1
            # For i in [p, N): add (A[i] - b_val) -> Base -= b_val, Coeff += 1
            
            # Base updates
            bit_base.update_range(0, p, b_val)
            bit_base.update_range(p, N, -b_val)
            
            # Coeff updates
            st_coeff.update_range(0, p, -1)
            st_coeff.update_range(p, N, 1)
            
            current_y += 1
        
        # Answer query for X (1-based index in problem, so X elements: indices 0 to X-1)
        # Sum = sum(Base[i]) + sum(Coeff[i] * A[i]) for i in [0, X)
        base_sum = bit_base.query_prefix(x)
        coeff_sum = st_coeff.query_prefix(x)
        results[k] = base_sum + coeff_sum

    # Print results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()