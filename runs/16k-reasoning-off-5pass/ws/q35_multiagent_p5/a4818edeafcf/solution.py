import sys

# Increase recursion depth just in case, though we will use iterative segment tree
sys.setrecursionlimit(2000000)

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

    # Precompute prefix distinct counts: pre[k] = distinct in A[0...k-1]
    # pre[0] = 0
    # pre[1] = distinct(A[0])
    # ...
    # pre[N] = distinct(A[0...N-1])
    pre = [0] * (N + 1)
    seen = set()
    for k in range(N):
        seen.add(A[k])
        pre[k + 1] = len(seen)

    # Precompute suffix distinct counts: suf[k] = distinct in A[k...N-1]
    # suf[N] = 0
    # suf[N-1] = distinct(A[N-1])
    # ...
    suf = [0] * (N + 1)
    seen = set()
    for k in range(N - 1, -1, -1):
        seen.add(A[k])
        suf[k] = len(seen)

    # Precompute previous occurrence for each element
    # prev_occ[k] is the index of the previous occurrence of A[k]
    # If no previous occurrence, it is -1
    prev_occ = [-1] * N
    last_pos = {}
    for k in range(N):
        val = A[k]
        if val in last_pos:
            prev_occ[k] = last_pos[val]
        last_pos[val] = k

    # Segment Tree for Range Add and Range Max Query
    # We need to maintain values for i in [1, N-2]
    # The segment tree will cover indices 1 to N-1 (to be safe, up to N-1)
    # Size of segment tree array: 4 * N is sufficient
    size = N + 1
    tree_max = [0] * (4 * size)
    tree_lazy = [0] * (4 * size)

    def build(node, start, end, initial_vals):
        if start == end:
            tree_max[node] = initial_vals[start]
        else:
            mid = (start + end) // 2
            build(2 * node, start, mid, initial_vals)
            build(2 * node + 1, mid + 1, end, initial_vals)
            tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])

    def push(node):
        if tree_lazy[node] != 0:
            lazy_val = tree_lazy[node]
            tree_max[2 * node] += lazy_val
            tree_lazy[2 * node] += lazy_val
            tree_max[2 * node + 1] += lazy_val
            tree_lazy[2 * node + 1] += lazy_val
            tree_lazy[node] = 0

    def update(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree_max[node] += val
            tree_lazy[node] += val
            return
        push(node)
        mid = (start + end) // 2
        update(2 * node, start, mid, l, r, val)
        update(2 * node + 1, mid + 1, end, l, r, val)
        tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])

    def query(node, start, end, l, r):
        if l > end or r < start:
            return -10**18
        if l <= start and end <= r:
            return tree_max[node]
        push(node)
        mid = (start + end) // 2
        left_val = query(2 * node, start, mid, l, r)
        right_val = query(2 * node + 1, mid + 1, end, l, r)
        return max(left_val, right_val)

    # Initialize segment tree with pre[i] for i in [1, N-1]
    # We only care about i in [1, N-2] for the final answer, but we can build for [1, N-1]
    # initial_vals[i] = pre[i]
    initial_vals = [0] * (size)
    for i in range(1, N):
        initial_vals[i] = pre[i]
    
    # Build the tree for range [1, N-1]
    if N >= 2:
        build(1, 1, N - 1, initial_vals)
    else:
        # Should not happen given constraints N >= 3
        pass

    ans = 0

    # Iterate j from 2 to N-1 (0-based index for the start of the 3rd part)
    # In 0-based indexing:
    # Split points are i and j where 1 <= i < j <= N-1.
    # Part 1: A[0...i-1]
    # Part 2: A[i...j-1]
    # Part 3: A[j...N-1]
    # We iterate j from 2 to N-1.
    # For each j, we update the segment tree to reflect that A[j-1] is now part of the middle section for relevant i's.
    # Wait, the loop variable j in the plan was the start of the 3rd part.
    # Let's stick to the plan's variable naming but map to 0-based.
    # Plan: j goes from 2 to N-1. This j is the start index of the 3rd part (0-based).
    # So the 3rd part is A[j...N-1].
    # The middle part is A[i...j-1].
    # The 1st part is A[0...i-1].
    # i ranges from 1 to j-1.
    
    # When we move to a new j, we are effectively adding A[j-1] to the middle part for all i <= j-1.
    # The element being added is A[j-1].
    # Let current element index be k = j-1.
    # We need to update D[i] for i in (prev_occ[k], k].
    # prev_occ[k] is the previous occurrence of A[k].
    
    for j in range(2, N):
        k = j - 1  # The index of the element being added to the middle part
        val = A[k]
        p = prev_occ[k]
        
        # Update range [max(1, p+1), k] with +1
        # The segment tree covers indices 1 to N-1.
        # We update indices i such that p+1 <= i <= k.
        # Since we query for i in [1, j-1] = [1, k], this update affects the query range.
        
        left_idx = p + 1
        if left_idx < 1:
            left_idx = 1
        right_idx = k
        
        if left_idx <= right_idx:
            # Ensure right_idx is within the built range [1, N-1]
            if right_idx > N - 1:
                right_idx = N - 1
            
            if left_idx <= right_idx:
                update(1, 1, N - 1, left_idx, right_idx, 1)
        
        # Query max in [1, j-1] = [1, k]
        # Since i must be <= j-1 = k.
        # And i >= 1.
        max_val = query(1, 1, N - 1, 1, k)
        
        if max_val != -10**18:
            current_ans = max_val + suf[j]
            if current_ans > ans:
                ans = current_ans

    print(ans)

solve()