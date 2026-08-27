import sys

def solve():
    # Increase recursion depth just in case, though we try to be iterative
    sys.setrecursionlimit(2000000)
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    people = []
    for _ in range(M):
        s = int(next(iterator))
        t = int(next(iterator))
        if s > t:
            s, t = t, s
        people.append((s, t))

    queries = []
    for _ in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r))

    # Precompute conflict indices
    # conflict_idx[j] will store the index i < j that crosses j, if any.
    # Specifically, we look for i < j such that L_i < L_j < R_i < R_j.
    # We use a segment tree to maintain max R_i for intervals with L_i < current L_j.
    
    # Coordinate compression for L and R values is not strictly necessary if we use a segment tree over the town indices (1 to N).
    # Town indices are up to 4*10^5.
    
    max_town = N + 2
    # Segment tree to store max R_i for a given L_i range?
    # Actually, we need to query: max R_i among all processed i such that L_i < L_j.
    # We can maintain a Fenwick tree or Segment Tree over the domain of L values (1..N).
    # When processing person j with (L_j, R_j):
    # 1. Query max R_i for L_i in [1, L_j - 1]. Let this be max_R.
    # 2. Find the index i that achieved this max_R.
    # 3. If max_R > L_j and max_R < R_j, then person i crosses person j.
    #    Set conflict_idx[j] = i.
    # 4. Update the data structure at position L_j with value R_j (and index j).
    
    # We need a Segment Tree that supports:
    # - Point update: set value at pos L_j to (R_j, j). We want to maximize R_j.
    # - Range query: max R in [1, L_j - 1].
    
    # Since we only add intervals, and we want the max R, we can use a simple Segment Tree.
    # Size of segment tree: 4 * N.
    
    seg_tree_max_r = [0] * (4 * max_town)
    seg_tree_idx = [-1] * (4 * max_town)
    
    def update(node, start, end, pos, val_r, val_idx):
        if start == end:
            if val_r > seg_tree_max_r[node]:
                seg_tree_max_r[node] = val_r
                seg_tree_idx[node] = val_idx
            return
        
        mid = (start + end) // 2
        if pos <= mid:
            update(2 * node, start, mid, pos, val_r, val_idx)
        else:
            update(2 * node + 1, mid + 1, end, pos, val_r, val_idx)
            
        if seg_tree_max_r[2 * node] >= seg_tree_max_r[2 * node + 1]:
            seg_tree_max_r[node] = seg_tree_max_r[2 * node]
            seg_tree_idx[node] = seg_tree_idx[2 * node]
        else:
            seg_tree_max_r[node] = seg_tree_max_r[2 * node + 1]
            seg_tree_idx[node] = seg_tree_idx[2 * node + 1]

    def query(node, start, end, l, r):
        if r < start or end < l:
            return 0, -1
        
        if l <= start and end <= r:
            return seg_tree_max_r[node], seg_tree_idx[node]
        
        mid = (start + end) // 2
        max_r1, idx1 = query(2 * node, start, mid, l, r)
        max_r2, idx2 = query(2 * node + 1, mid + 1, end, l, r)
        
        if max_r1 >= max_r2:
            return max_r1, idx1
        else:
            return max_r2, idx2

    conflict_idx = [-1] * M
    
    # Process each person
    for j in range(M):
        L_j, R_j = people[j]
        
        # Query max R_i for i < j with L_i < L_j
        # Range [1, L_j - 1]
        if L_j > 1:
            max_r, idx = query(1, 1, N, 1, L_j - 1)
        else:
            max_r, idx = 0, -1
            
        # Check for crossing: L_i < L_j < R_i < R_j
        # We have L_i < L_j from query range.
        # We need L_j < R_i < R_j.
        if max_r > L_j and max_r < R_j:
            conflict_idx[j] = idx
        else:
            conflict_idx[j] = -1
            
        # Update with current person's interval
        update(1, 1, N, L_j, R_j, j + 1) # Store 1-based index for conflict_idx to match query logic later? 
        # Let's store 0-based index in conflict_idx array, but segment tree can store anything.
        # Let's store j (0-based) in seg_tree_idx.
        # But wait, update function uses val_idx. Let's fix it to store j.
        # Re-define update call:
        # We need to overwrite the value at L_j. The segment tree stores max R.
        # If multiple intervals start at same L, we keep the one with largest R.
        # The update above does: if val_r > current, update. This is correct for max.
        
    # Now we have conflict_idx array where conflict_idx[j] is the index i < j that crosses j, or -1.
    # A query [L, R] (1-based) is valid if for all j in [L-1, R-1] (0-based), conflict_idx[j] < L-1.
    # i.e., max(conflict_idx[L-1...R-1]) < L-1.
    
    # Build a Sparse Table or Segment Tree for Range Maximum Query on conflict_idx.
    # Since queries are offline or online, Sparse Table is good for static RMQ.
    # M up to 2*10^5.
    
    # RMQ on conflict_idx
    # conflict_idx values are -1 or indices 0..M-1.
    
    # Using a Segment Tree for RMQ on conflict_idx
    rmq_size = 1
    while rmq_size < M:
        rmq_size *= 2
    
    rmq_tree = [-1] * (2 * rmq_size)
    
    for i in range(M):
        rmq_tree[rmq_size + i] = conflict_idx[i]
        
    for i in range(rmq_size - 1, 0, -1):
        rmq_tree[i] = max(rmq_tree[2 * i], rmq_tree[2 * i + 1])
        
    def rmq_query(l, r):
        # Query max in [l, r] inclusive, 0-based
        l += rmq_size
        r += rmq_size
        res = -1
        while l <= r:
            if l % 2 == 1:
                res = max(res, rmq_tree[l])
                l += 1
            if r % 2 == 0:
                res = max(res, rmq_tree[r])
                r -= 1
            l //= 2
            r //= 2
        return res

    results = []
    for l, r in queries:
        # Query range [l, r] 1-based -> indices [l-1, r-1] 0-based
        l_idx = l - 1
        r_idx = r - 1
        
        max_conflict = rmq_query(l_idx, r_idx)
        
        if max_conflict < l_idx:
            results.append("Yes")
        else:
            results.append("No")
            
    print('\n'.join(results))

solve()