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

    if N < 3:
        # Constraints say N >= 3, but handle gracefully
        print(0)
        return

    # Precompute prefix distinct counts
    # pre[i] = number of distinct elements in A[0...i]
    pre = [0] * N
    seen = set()
    count = 0
    for i in range(N):
        if A[i] not in seen:
            seen.add(A[i])
            count += 1
        pre[i] = count

    # Precompute suffix distinct counts
    # suf[i] = number of distinct elements in A[i...N-1]
    suf = [0] * N
    seen = set()
    count = 0
    for i in range(N - 1, -1, -1):
        if A[i] not in seen:
            seen.add(A[i])
            count += 1
        suf[i] = count

    # Segment Tree for Range Add and Range Max Query
    # Size needs to cover indices 0 to N-2 for split points i
    # We'll use a size of N for simplicity
    size = N
    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)

    def push(node):
        """Push lazy values to children."""
        if lazy[node] != 0:
            for child in [2 * node, 2 * node + 1]:
                if child < 2 * size:
                    tree[child] += lazy[node]
                    lazy[child] += lazy[node]
            lazy[node] = 0

    def update_range(node, start, end, l, r, val):
        """Add val to all elements in range [l, r]."""
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree[node] += val
            lazy[node] += val
            return
        
        push(node)
        mid = (start + end) // 2
        update_range(2 * node, start, mid, l, r, val)
        update_range(2 * node + 1, mid + 1, end, l, r, val)
        tree[node] = max(tree[2 * node], tree[2 * node + 1])

    def query_max(node, start, end, l, r):
        """Query max in range [l, r]."""
        if l > end or r < start:
            return -float('inf')
        if l <= start and end <= r:
            return tree[node]
        
        push(node)
        mid = (start + end) // 2
        left_max = query_max(2 * node, start, mid, l, r)
        right_max = query_max(2 * node + 1, mid + 1, end, l, r)
        return max(left_max, right_max)

    # Initialize segment tree with -infinity
    # We will set specific values as we go.
    # To initialize properly, we can just set leaves to a very small number initially
    # But since we only access valid indices, we can just build it or set leaves.
    # Let's set all leaves to -10**9 initially.
    for i in range(size):
        tree[size + i] = -10**9
    
    # Build the initial tree (max of children)
    for i in range(size - 1, 0, -1):
        tree[i] = max(tree[2 * i], tree[2 * i + 1])

    # Helper to update a single position (point update)
    def set_val(pos, val):
        idx = size + pos
        tree[idx] = val
        idx //= 2
        while idx >= 1:
            tree[idx] = max(tree[2 * idx], tree[2 * idx + 1])
            idx //= 2

    # last_pos array to store the last seen index of each value
    last_pos = {}

    # We iterate j from 1 to N-2.
    # For each j, we want max(pre[i] + D(A[i+1...j])) for 0 <= i <= j-1.
    # Let V_i(j) = pre[i] + D(A[i+1...j]).
    
    # Base case: j = 1
    # Middle segment is A[1...1].
    # i can only be 0.
    # V_0(1) = pre[0] + D(A[1...1]) = pre[0] + 1.
    
    # Initialize for j=1
    # Set V_0(1)
    val_i0 = pre[0] + 1
    set_val(0, val_i0)
    
    # Query max for i in [0, 0]
    current_max_mid = query_max(1, 0, size - 1, 0, 0)
    
    # Answer candidate for j=1
    # Last subarray is A[2...N-1], distinct count is suf[2]
    ans = current_max_mid + suf[2]

    # Loop j from 1 to N-3 to prepare for j+1
    # In each iteration, we move from middle ending at j to middle ending at j+1.
    # The element added is A[j+1].
    for j in range(1, N - 2):
        # We are currently at state where tree has V_i(j) for i in 0..j-1
        # We want to transition to state V_i(j+1) for i in 0..j
        
        # Element to add to middle segment is A[j+1]
        val = A[j+1]
        
        # Find last position of val before j+1
        if val in last_pos:
            L = last_pos[val]
        else:
            L = -1
        
        # Update range [L, j] by adding 1
        # If L < 0, update [0, j]
        if L < 0:
            update_range(1, 0, size - 1, 0, j, 1)
        else:
            # L is an index in A. The condition for increase is i >= L.
            # So we update indices i in [L, j].
            # Note: L is the last occurrence index.
            # If L >= j, then no i in [0, j-1] satisfies i >= L? 
            # Actually L < j+1 always. If L == j, then i >= j means i=j.
            # But we are updating existing i's which are <= j-1.
            # So if L >= j, the range [L, j] might be empty or just {j}.
            # Since we only have valid values for i <= j-1 currently,
            # updating [L, j] where L >= j will only affect index j (which we will set next)
            # or nothing if L > j.
            # Let's just call update_range, it handles bounds.
            update_range(1, 0, size - 1, L, j, 1)
        
        # Now update last_pos for val
        last_pos[val] = j + 1
        
        # Now we need to set V_j(j+1) = pre[j] + D(A[j+1...j+1]) = pre[j] + 1
        # This is a new candidate for i=j.
        new_val = pre[j] + 1
        set_val(j, new_val)
        
        # Now query max for i in [0, j]
        current_max_mid = query_max(1, 0, size - 1, 0, j)
        
        # Candidate answer for split at j+1
        # Last subarray is A[j+2...N-1], distinct count is suf[j+2]
        ans = max(ans, current_max_mid + suf[j+2])

    print(ans)

solve()