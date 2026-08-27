import sys

# Increase recursion depth just in case, though we will use iterative segment tree
sys.setrecursionlimit(2000)

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

    # 1-based indexing for logic, but 0-based for array A
    # A[0] ... A[N-1]
    
    # Precompute pref[i]: distinct count in A[0...i-1] (first i elements)
    # pref[k] corresponds to subarray A[0...k-1]
    # pref[0] = 0
    # pref[1] = distinct(A[0])
    # ...
    # pref[N] = distinct(A[0...N-1])
    
    pref = [0] * (N + 1)
    seen = set()
    for i in range(N):
        seen.add(A[i])
        pref[i+1] = len(seen)
        
    # Precompute suff[i]: distinct count in A[i...N-1]
    # suff[k] corresponds to subarray A[k...N-1]
    # suff[N] = 0
    # suff[N-1] = distinct(A[N-1])
    # ...
    
    suff = [0] * (N + 1)
    seen = set()
    for i in range(N - 1, -1, -1):
        seen.add(A[i])
        suff[i] = len(seen)
        
    # Segment Tree for Range Add, Range Max Query
    # Size: N+1 to handle 1-based indices for i (cut positions)
    # We will maintain values V[i] = pref[i] + mid_distinct[i]
    # Initially mid_distinct[i] = 0, so V[i] = pref[i]
    # The segment tree will cover indices 1 to N-1 (since i can be 1 to N-2 for valid splits)
    # Actually, i ranges from 1 to N-2. But we might update ranges that go up to j-1.
    # Let's make the segment tree size N+1 for safety, indices 0 to N.
    
    size = N + 1
    tree_max = [0] * (2 * size)
    tree_add = [0] * (2 * size)
    
    # Initialize leaves with pref[i]
    # We only care about indices 1 to N-1 for queries, but let's init all.
    for i in range(size):
        tree_max[size + i] = pref[i]
        
    # Build the tree
    for i in range(size - 1, 0, -1):
        tree_max[i] = max(tree_max[2 * i], tree_max[2 * i + 1])
        
    def push(node):
        if tree_add[node] != 0:
            for child in [2 * node, 2 * node + 1]:
                tree_add[child] += tree_add[node]
                tree_max[child] += tree_add[node]
            tree_add[node] = 0
            
    def update_range(l, r, val):
        """Add val to all elements in [l, r]"""
        l += size
        r += size
        # We need to handle the lazy propagation carefully.
        # Standard iterative lazy propagation is complex. 
        # Given N=3*10^5, O(N log N) is required.
        # Let's use a recursive implementation for clarity and correctness with lazy propagation.
        pass

    # Recursive Segment Tree with Lazy Propagation
    # To avoid recursion depth issues, we can increase recursion limit or use iterative.
    # Given the constraints and Python, iterative is safer.
    # However, implementing iterative lazy segment tree is verbose.
    # Let's try recursive with increased recursion limit.
    
    sys.setrecursionlimit(1000000)
    
    tree_max = [0] * (4 * size)
    tree_add = [0] * (4 * size)
    
    def build(node, start, end):
        if start == end:
            tree_max[node] = pref[start]
        else:
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])
            
    def push(node):
        if tree_add[node] != 0:
            tree_add[2 * node] += tree_add[node]
            tree_max[2 * node] += tree_add[node]
            tree_add[2 * node + 1] += tree_add[node]
            tree_max[2 * node + 1] += tree_add[node]
            tree_add[node] = 0
            
    def update(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree_max[node] += val
            tree_add[node] += val
            return
        push(node)
        mid = (start + end) // 2
        update(2 * node, start, mid, l, r, val)
        update(2 * node + 1, mid + 1, end, l, r, val)
        tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])
        
    def query(node, start, end, l, r):
        if l > end or r < start:
            return -10**9
        if l <= start and end <= r:
            return tree_max[node]
        push(node)
        mid = (start + end) // 2
        p1 = query(2 * node, start, mid, l, r)
        p2 = query(2 * node + 1, mid + 1, end, l, r)
        return max(p1, p2)

    # Build the segment tree for range [1, N-1]
    # We only need indices 1 to N-1.
    build(1, 1, N - 1)
    
    last_pos = {}
    ans = 0
    
    # Iterate j from 2 to N-2 (1-based index for cut position)
    # j is the end of the second subarray.
    # First subarray: A[0...i-1] (cut at i)
    # Second subarray: A[i...j-1] (cut at j)
    # Third subarray: A[j...N-1]
    # i ranges from 1 to j-1.
    # j ranges from 2 to N-2.
    
    for j in range(2, N - 1):
        # Current element being added to the middle subarray is A[j-1] (0-based)
        # In 1-based indexing for cuts, the middle subarray ends at cut j.
        # The element is A[j-1].
        val = A[j-1]
        
        # Find last position of val
        p = last_pos.get(val, 0)
        
        # Update range [p, j-1] by adding 1
        # If p=0, range is [1, j-1]
        # If p >= j, no update needed (shouldn't happen as p < j)
        if p < j:
            # Range is [max(1, p), j-1]
            l_idx = p if p >= 1 else 1
            r_idx = j - 1
            if l_idx <= r_idx:
                update(1, 1, N - 1, l_idx, r_idx, 1)
        
        # Query max in [1, j-1]
        max_mid = query(1, 1, N - 1, 1, j - 1)
        
        # Add the distinct count of the third subarray
        # Third subarray is A[j...N-1] (0-based), which corresponds to suff[j]
        # Wait, suff[k] is distinct count in A[k...N-1].
        # If cut is at j (1-based), the third subarray starts at index j (0-based).
        # So it is A[j...N-1]. Its distinct count is suff[j].
        current_ans = max_mid + suff[j]
        if current_ans > ans:
            ans = current_ans
            
        # Update last position of val
        last_pos[val] = j
        
    print(ans)

solve()