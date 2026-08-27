import sys

# Increase recursion depth just in case, though we'll use iterative segment tree
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
    except StopIteration:
        return

    # 0-indexed array A: A[0], A[1], ..., A[N-1]
    # We want to split into A[0..i], A[i+1..j], A[j+1..N-1]
    # where 0 <= i < j <= N-2.
    # Subarray 1: indices 0 to i
    # Subarray 2: indices i+1 to j
    # Subarray 3: indices j+1 to N-1
    
    # Precompute prefix distinct counts
    # pre[k] = number of distinct elements in A[0...k-1]
    # pre[0] = 0
    # pre[1] = distinct in A[0]
    # ...
    # pre[N] = distinct in A[0...N-1]
    pre = [0] * (N + 1)
    seen = set()
    for idx in range(N):
        seen.add(A[idx])
        pre[idx + 1] = len(seen)
        
    # Precompute suffix distinct counts
    # suf[k] = number of distinct elements in A[k...N-1]
    # suf[N] = 0
    # suf[N-1] = distinct in A[N-1]
    # ...
    suf = [0] * (N + 1)
    seen = set()
    for idx in range(N - 1, -1, -1):
        seen.add(A[idx])
        suf[idx] = len(seen)
        
    # Segment Tree for Range Add and Range Max Query
    # Size: N (indices 0 to N-1 correspond to possible left cut positions i)
    # We will use 1-based indexing for the segment tree internally for simplicity
    # Tree size: 2^ceil(log2(N)) * 2
    size = 1
    while size < N:
        size *= 2
    
    tree_max = [0] * (2 * size)
    tree_add = [0] * (2 * size)
    
    def push(node):
        """Push lazy values down to children."""
        if tree_add[node] != 0:
            for child in [2 * node, 2 * node + 1]:
                if child < 2 * size:
                    tree_max[child] += tree_add[node]
                    tree_add[child] += tree_add[node]
            tree_add[node] = 0

    def update_range(node, start, end, l, r, val):
        """Add val to all elements in range [l, r]."""
        if r < start or end < l:
            return
        if l <= start and end <= r:
            tree_max[node] += val
            tree_add[node] += val
            return
        
        push(node)
        mid = (start + end) // 2
        update_range(2 * node, start, mid, l, r, val)
        update_range(2 * node + 1, mid + 1, end, l, r, val)
        tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])

    def query_max(node, start, end, l, r):
        """Query max in range [l, r]."""
        if r < start or end < l:
            return -float('inf')
        if l <= start and end <= r:
            return tree_max[node]
        
        push(node)
        mid = (start + end) // 2
        left_max = query_max(2 * node, start, mid, l, r)
        right_max = query_max(2 * node + 1, mid + 1, end, l, r)
        return max(left_max, right_max)

    # Initialize the segment tree
    # We map problem index i (0 to N-2) to tree index i+1 (1 to N-1)
    # Initially, we start with j=1 (middle segment ends at index 1, 0-indexed)
    # Middle segment is A[i+1 ... 1]. i can be 0.
    # Val(0) = pre[1] + distinct(A[1...1]) = pre[1] + 1
    
    # Set initial value for i=0
    # Tree index 1 corresponds to i=0
    idx_0 = 1
    val_0 = pre[1] + 1
    # Update leaf
    pos = idx_0 + size - 1
    tree_max[pos] = val_0
    # Push up
    curr = pos // 2
    while curr >= 1:
        tree_max[curr] = max(tree_max[2 * curr], tree_max[2 * curr + 1])
        curr //= 2
        
    last_pos = {}
    ans = 0
    
    # Iterate j from 1 to N-2 (0-indexed end of middle segment)
    # j represents the end index of the middle segment A[i+1 ... j]
    # The right segment is A[j+1 ... N-1]
    # We need to compute max(pre[i+1] + distinct(A[i+1...j])) for 0 <= i <= j-1
    # Then add suf[j+1]
    
    for j in range(1, N - 1):
        # Current middle segment ends at j
        # Query max for i in [0, j-1]
        # Tree indices for i in [0, j-1] are [1, j]
        max_mid = query_max(1, 1, size, 1, j)
        
        current_total = max_mid + suf[j + 1]
        if current_total > ans:
            ans = current_total
            
        # Prepare for next iteration where middle segment ends at j+1
        # We need to update the segment tree to reflect that the middle segment now includes A[j+1]
        # Let x = A[j+1]
        if j + 1 < N:
            x = A[j + 1]
            p = last_pos.get(x, -1)
            
            # If x appeared before at index p (0-indexed),
            # then for all i such that the middle segment A[i+1...j] included p,
            # the distinct count doesn't increase.
            # The middle segment A[i+1...j] includes index p if i+1 <= p <= j, i.e., i <= p-1.
            # So for i < p, the distinct count increases by 1.
            # For i >= p, it stays the same.
            
            if p != -1:
                # Range add 1 to tree indices corresponding to i in [0, p-1]
                # Tree indices: 1 to p
                if p >= 1:
                    update_range(1, 1, size, 1, p, 1)
            
            # Update last_pos for x
            last_pos[x] = j + 1
            
            # Add new leaf for i = j
            # When middle ends at j+1, i can be j.
            # Val(j) = pre[j+1] + distinct(A[j+1...j+1]) = pre[j+1] + 1
            # Tree index for i=j is j+1
            new_i = j
            new_val = pre[new_i + 1] + 1
            pos = (new_i + 1) + size - 1
            tree_max[pos] = new_val
            # Push up
            curr = pos // 2
            while curr >= 1:
                tree_max[curr] = max(tree_max[2 * curr], tree_max[2 * curr + 1])
                curr //= 2

    print(ans)

solve()