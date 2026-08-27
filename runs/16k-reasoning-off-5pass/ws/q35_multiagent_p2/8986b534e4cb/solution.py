import sys

# Increase recursion depth just in case, though we try to be iterative
sys.setrecursionlimit(10**6)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    # Store intervals as (u, v) with u < v
    # People are 1-indexed in input, we'll store 0-indexed internally for arrays
    intervals = []
    for _ in range(M):
        s = int(next(iterator))
        t = int(next(iterator))
        if s < t:
            u, v = s, t
        else:
            u, v = t, s
        intervals.append((u, v))

    # Queries
    queries = []
    for _ in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r))

    # Step 1: Compute bad[i] for each person i (0-indexed)
    # bad[i] is the smallest index j > i such that interval i and j cross.
    # Two intervals i and j (with u_i < u_j) cross if u_i < u_j < v_i < v_j.
    # We iterate j from 0 to M-1. We maintain a set of active intervals.
    # An interval i is active for j if u_i < u_j and v_i >= u_j.
    # Among active intervals, we look for those with v_i < v_j.
    # If found, those intervals cross j. We set bad[i] = j and remove them from active set.
    
    bad = [M + 1] * M
    
    # We use a sorted list of (v_i, i) for active intervals.
    # Since we need to efficiently find and remove intervals with v_i < v_j,
    # and also remove those with v_i < u_j (disjoint), a balanced BST or sorted list is good.
    # In Python, we can use a list and keep it sorted, or use a heap?
    # Actually, we need to remove arbitrary elements (those with v_i < u_j) and query range [u_j, v_j-1].
    # A Segment Tree or Fenwick Tree over v coordinates (1..N) is suitable.
    # However, since we need to retrieve the index i, and potentially multiple i's share same v,
    # let's use a Segment Tree that stores the minimum v in a range, and we can traverse to find indices.
    # But simpler: Use a set of (v, i). Python's set is not ordered by value in a way that allows range queries efficiently?
    # Actually, we can use a sorted list and bisect, but removal is O(N).
    # Given M=2e5, O(M^2) is too slow.
    # Let's use a Segment Tree over the domain of v (1 to N).
    # Each leaf v stores a list of interval indices i that have v_i = v.
    # We want to find all i such that v_i in [u_j, v_j - 1].
    # And among those, we want to process them.
    # Since we remove them once processed, we can use a Segment Tree that supports:
    # 1. Point update: add i to position v_i.
    # 2. Range query: find and remove all i in range [L, R].
    
    # To implement "find and remove", we can store at each leaf a stack/list of indices.
    # And each internal node stores the minimum v present in its range? No, we query by v range.
    # We just need to know if there are any indices in [u_j, v_j - 1].
    # We can use a Segment Tree that stores the count of active intervals in each range.
    # Then we can descend to find and remove them one by one or in batches.
    
    # Let's use a simpler approach with a Segment Tree that stores the minimum index i for each v?
    # No, we need to handle multiple i's with same v.
    # Let's store a list of indices at each leaf.
    # And a boolean flag or count at each node to indicate if the range is non-empty.
    
    # Segment Tree size
    size = 1
    while size < N + 1:
        size *= 2
    
    # tree[node] will store a list of indices? No, that's too much memory if we copy lists.
    # Instead, tree[node] stores the minimum v present in the range? No, we query by v range.
    # We just need to know if there is ANY index in [u_j, v_j - 1].
    # And we need to retrieve them.
    # Let's store at each leaf a deque or list of indices.
    # Internal nodes store the sum of counts of indices in their range.
    
    count = [0] * (2 * size)
    # Leaves are at indices size to size + N
    # We'll use a list of lists for leaves, but to save memory, we can use a single list for each leaf?
    # Actually, we can just store the indices in a list at each leaf.
    leaves = [[] for _ in range(size)]
    
    def update(v, idx):
        # Add idx to leaf v
        leaves[v].append(idx)
        pos = size + v
        count[pos] += 1
        pos //= 2
        while pos > 0:
            count[pos] = count[2 * pos] + count[2 * pos + 1]
            pos //= 2

    def query_and_remove(l, r, current_j):
        # Remove all indices in v range [l, r] and set their bad to current_j
        # We need to traverse the segment tree to find leaves with count > 0 in [l, r]
        
        # Collect leaves to remove
        to_remove = []
        
        # Helper to traverse
        def traverse(node, node_l, node_r):
            if count[node] == 0:
                return
            if node_r < l or node_l > r:
                return
            if node_l == node_r:
                # Leaf node
                if l <= node_l <= r:
                    # Remove all indices at this leaf
                    while leaves[node_l]:
                        idx = leaves[node_l].pop()
                        to_remove.append(idx)
                    count[node] = 0
                return
            
            mid = (node_l + node_r) // 2
            traverse(2 * node, node_l, mid)
            traverse(2 * node + 1, mid + 1, node_r)
            count[node] = count[2 * node] + count[2 * node + 1]

        traverse(1, 1, size - 1)
        
        for idx in to_remove:
            bad[idx] = current_j

    # Process each person j
    for j in range(M):
        u_j, v_j = intervals[j]
        
        # 1. Remove intervals that are now disjoint (v_i < u_j)
        # These are intervals with v_i in [1, u_j - 1]
        # We can just query and remove them, but we don't care about their bad value anymore?
        # Actually, if they haven't been assigned a bad value, it means they never crossed anyone before.
        # And since they are now disjoint from j and any future k (u_k >= u_j > v_i), they will never cross anyone.
        # So we can just remove them.
        if u_j > 1:
            # Remove all in [1, u_j - 1]
            # We don't need to set bad for them, just remove.
            # But our query_and_remove sets bad. We can modify it or just call it.
            # Let's create a remove_only function or just call query_and_remove and ignore bad update if not needed?
            # Actually, if bad[idx] is still M+1, it means no crossing found yet.
            # If we remove it now, it will never cross anyone, so bad[idx] remains M+1, which is correct.
            # So we can just use query_and_remove.
            query_and_remove(1, u_j - 1, -1) # -1 is dummy, won't be used since we check bad later? 
            # Wait, query_and_remove sets bad[idx] = current_j. If current_j is -1, bad becomes -1.
            # We should not set bad for removed disjoint intervals.
            # Let's make a separate remove function.
            pass

        # Let's rewrite the removal logic to not set bad
        def remove_range(l, r):
            to_remove = []
            def traverse(node, node_l, node_r):
                if count[node] == 0:
                    return
                if node_r < l or node_l > r:
                    return
                if node_l == node_r:
                    if l <= node_l <= r:
                        while leaves[node_l]:
                            leaves[node_l].pop()
                        count[node] = 0
                    return
                mid = (node_l + node_r) // 2
                traverse(2 * node, node_l, mid)
                traverse(2 * node + 1, mid + 1, node_r)
                count[node] = count[2 * node] + count[2 * node + 1]
            traverse(1, 1, size - 1)

        if u_j > 1:
            remove_range(1, u_j - 1)

        # 2. Find and remove intervals in [u_j, v_j - 1]
        # These are the ones that cross j
        query_and_remove(u_j, v_j - 1, j)

        # 3. Add current interval j
        update(v_j, j)

    # Step 2: Answer queries
    # For each query [L, R] (1-indexed), check if min(bad[L-1...R-1]) <= R
    # We need RMQ on bad array.
    
    # Build Sparse Table or Segment Tree for RMQ
    # Since we need range minimum, and array is static, Sparse Table is good.
    # Or just a Segment Tree.
    
    # Using a Segment Tree for RMQ
    rmq_size = 1
    while rmq_size < M:
        rmq_size *= 2
    
    rmq_tree = [M + 1] * (2 * rmq_size)
    
    for i in range(M):
        rmq_tree[rmq_size + i] = bad[i]
        
    for i in range(rmq_size - 1, 0, -1):
        rmq_tree[i] = min(rmq_tree[2 * i], rmq_tree[2 * i + 1])
        
    def query_rmq(l, r):
        # Query min in [l, r] (0-indexed)
        l += rmq_size
        r += rmq_size
        res = M + 1
        while l <= r:
            if l % 2 == 1:
                res = min(res, rmq_tree[l])
                l += 1
            if r % 2 == 0:
                res = min(res, rmq_tree[r])
                r -= 1
            l //= 2
            r //= 2
        return res

    results = []
    for l, r in queries:
        # Convert to 0-indexed
        l0 = l - 1
        r0 = r - 1
        
        min_bad = query_rmq(l0, r0)
        
        if min_bad <= r:
            results.append("No")
        else:
            results.append("Yes")

    print('\n'.join(results))

solve()