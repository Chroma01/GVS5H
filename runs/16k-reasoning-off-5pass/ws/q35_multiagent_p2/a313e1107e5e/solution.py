import sys

def solve():
    # Increase recursion depth just in case, though we'll use iterative segment tree
    sys.setrecursionlimit(200000)
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
        
    queries = []
    for i in range(Q):
        R = int(next(iterator))
        X = int(next(iterator))
        queries.append((R, X, i))
        
    # Coordinate compression
    # Collect all values from A and all X from queries
    values = set()
    for x in A:
        values.add(x)
    for _, X, _ in queries:
        values.add(X)
        
    sorted_values = sorted(list(values))
    comp_map = {val: i + 1 for i, val in enumerate(sorted_values)}
    M = len(sorted_values)
    
    # Segment Tree for Range Maximum Query
    # Size should be power of 2 for simplicity, or just 2*M
    size = 1
    while size < M:
        size *= 2
    
    # tree array, initialized to 0
    tree = [0] * (2 * size)
    
    def update(pos, value):
        """Update the value at pos to be max(current, value). pos is 1-based index in compressed domain."""
        idx = pos + size - 1
        if tree[idx] >= value:
            return
        tree[idx] = value
        idx //= 2
        while idx > 0:
            new_val = max(tree[2 * idx], tree[2 * idx + 1])
            if tree[idx] == new_val:
                # Optimization: if no change, stop propagating? 
                # Actually, since we only increase values, if the parent doesn't change, children won't affect it further.
                # But we must be careful. If we update a leaf, the parent might change.
                # If the new parent value is same as old, then no need to go up?
                # Yes, because max of children is non-decreasing. If it didn't change, ancestors won't change.
                break
            tree[idx] = new_val
            idx //= 1 # Wait, idx //= 2
            
    def query(l, r):
        """Query max in range [l, r] inclusive. 1-based indices."""
        if l > r:
            return 0
        # Convert to 0-based indices for the segment tree array logic if needed, 
        # but here we use the standard iterative segment tree on 0-based array of size 'size'
        # Our leaves are at size-1 + (pos-1) = size + pos - 2? 
        # Let's stick to 0-based internal indexing for the tree array.
        # pos 1 -> index size-1
        # pos M -> index size-1 + M - 1
        
        l_idx = l + size - 1
        r_idx = r + size - 1
        
        res = 0
        while l_idx <= r_idx:
            if l_idx % 2 == 1:
                res = max(res, tree[l_idx])
                l_idx += 1
            if r_idx % 2 == 0:
                res = max(res, tree[r_idx])
                r_idx -= 1
            l_idx //= 2
            r_idx //= 2
        return res

    # Group queries by R
    queries_by_r = [[] for _ in range(N + 1)]
    for R, X, idx in queries:
        queries_by_r[R].append((X, idx))
        
    answers = [0] * Q
    
    # Process array A
    for i in range(N):
        val = A[i]
        c_val = comp_map[val]
        
        # Find max LIS length ending with value < val
        # This corresponds to max in range [1, c_val - 1]
        if c_val > 1:
            max_len_prev = query(1, c_val - 1)
        else:
            max_len_prev = 0
            
        new_len = max_len_prev + 1
        
        # Update the segment tree at position c_val with new_len
        update(c_val, new_len)
        
        # Answer queries for this R = i + 1
        current_r = i + 1
        for X, q_idx in queries_by_r[current_r]:
            c_x = comp_map[X]
            # Query max in range [1, c_x]
            ans = query(1, c_x)
            answers[q_idx] = ans
            
    # Print answers
    for ans in answers:
        print(ans)

solve()