import sys

def solve():
    # Increase recursion depth just in case, though we try to be iterative
    sys.setrecursionlimit(300000)
    
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(next(iterator))
        
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    
    for i in range(1, N + 1):
        L[i] = int(next(iterator))
        R[i] = int(next(iterator))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        s = int(next(iterator))
        t = int(next(iterator))
        queries.append((s, t))
        
    # Step 1: Sort intervals by L_i to identify components
    # We store (L_i, R_i, original_index)
    intervals = []
    for i in range(1, N + 1):
        intervals.append((L[i], R[i], i))
        
    # Sort by L_i
    intervals.sort(key=lambda x: x[0])
    
    # Step 2: Identify connected components
    # A new component starts if current L > max_R of previous intervals
    # We assign component IDs to original indices
    comp_id = [0] * (N + 1)
    
    # To store the sorted order within each component for prefix/suffix min queries
    # comp_nodes[c] will be a list of original indices sorted by L
    comp_nodes = []
    
    current_comp = []
    max_r = -1
    
    # We'll process intervals in sorted order
    # If L[i] > max_r, then the previous group forms a component
    # and a new component starts.
    
    # However, we need to be careful: the condition for connectivity in the complement graph
    # is that the union of intervals is "connected" in the sense that there are no gaps
    # that separate the set into two disjoint sets A and B where all A < all B.
    # This is exactly captured by: if L_current > max_R_so_far, then a new component starts.
    
    comp_idx = 0
    for i in range(N):
        l_val, r_val, orig_idx = intervals[i]
        
        if i == 0:
            max_r = r_val
            current_comp.append(orig_idx)
        else:
            if l_val > max_r:
                # New component
                comp_nodes.append(current_comp)
                for idx in current_comp:
                    comp_id[idx] = comp_idx
                comp_idx += 1
                current_comp = [orig_idx]
                max_r = r_val
            else:
                current_comp.append(orig_idx)
                if r_val > max_r:
                    max_r = r_val
                    
    # Don't forget the last component
    if current_comp:
        comp_nodes.append(current_comp)
        for idx in current_comp:
            comp_id[idx] = comp_idx
            
    num_comps = comp_idx + 1 if current_comp else comp_idx
    
    # Step 3: Precompute prefix and suffix minimum weights for each component
    # For each component, we have a list of nodes sorted by L.
    # We need to quickly find the min weight node in a prefix or suffix of this list
    # that satisfies a condition on R or L.
    # Actually, the condition for being disjoint from s and t reduces to:
    # R_k < min(L_s, L_t)  OR  L_k > max(R_s, R_t)
    # Since the list is sorted by L, the condition R_k < X defines a prefix.
    # The condition L_k > Y defines a suffix.
    
    # We need to map original index to its position in the component's sorted list
    # and also store the L and R values for quick lookup.
    
    # Let's build arrays for each component:
    # comp_L[c][i] = L value of the i-th node in component c's sorted list
    # comp_R[c][i] = R value of the i-th node in component c's sorted list
    # comp_W[c][i] = W value of the i-th node in component c's sorted list
    # pref_min[c][i] = min weight in comp_W[c][0...i]
    # suff_min[c][i] = min weight in comp_W[c][i...end]
    
    comp_L = []
    comp_R = []
    comp_W = []
    pref_min = []
    suff_min = []
    
    # Also need a map from original index to (comp_id, pos_in_comp)
    # pos_map[orig_idx] = (comp_id, pos)
    pos_map = [None] * (N + 1)
    
    for c in range(num_comps):
        nodes = comp_nodes[c]
        # nodes are already sorted by L because we processed intervals in sorted order
        # But wait, we appended to current_comp in sorted order. Yes.
        
        c_L = []
        c_R = []
        c_W = []
        
        for idx in nodes:
            c_L.append(L[idx])
            c_R.append(R[idx])
            c_W.append(W[idx])
            pos_map[idx] = (c, len(c_L) - 1)
            
        comp_L.append(c_L)
        comp_R.append(c_R)
        comp_W.append(c_W)
        
        # Prefix min
        p_min = []
        curr_min = float('inf')
        for w in c_W:
            if w < curr_min:
                curr_min = w
            p_min.append(curr_min)
        pref_min.append(p_min)
        
        # Suffix min
        s_min = []
        curr_min = float('inf')
        for w in reversed(c_W):
            if w < curr_min:
                curr_min = w
            s_min.append(curr_min)
        s_min.reverse()
        suff_min.append(s_min)
        
    # Step 4: Process queries
    results = []
    
    for s, t in queries:
        # Check if same component
        if comp_id[s] != comp_id[t]:
            results.append("-1")
            continue
            
        c = comp_id[s]
        
        # Check if directly connected
        # Disjoint if R_s < L_t or R_t < L_s
        if R[s] < L[t] or R[t] < L[s]:
            results.append(str(W[s] + W[t]))
            continue
            
        # Not directly connected, so they overlap.
        # We need min weight k in component c such that:
        # (R_k < min(L_s, L_t)) OR (L_k > max(R_s, R_t))
        
        min_L_st = min(L[s], L[t])
        max_R_st = max(R[s], R[t])
        
        # Find best in prefix: R_k < min_L_st
        # In comp_R[c], find the largest index i such that comp_R[c][i] < min_L_st
        # Since comp_R is not necessarily sorted, we can't binary search directly on R.
        # BUT, we know that the nodes are sorted by L.
        # Is R monotonic? No.
        # However, we established that the set of valid k for the prefix condition
        # is NOT necessarily a prefix in the sorted-by-L array if R is not monotonic.
        
        # WAIT. Re-evaluate.
        # The condition "R_k < X" does NOT define a prefix in the L-sorted array.
        # Example: Intervals [1, 10], [2, 3], [4, 5]. Sorted by L.
        # R values: 10, 3, 5.
        # If X = 4, R_k < 4 is true for [2,3] (index 1) but false for [1,10] (index 0) and [4,5] (index 2).
        # So it's not a prefix.
        
        # This breaks the simple prefix/suffix min approach.
        # We need a different way to find the min weight node satisfying R_k < X or L_k > Y.
        
        # Alternative:
        # The number of nodes in a component can be large.
        # However, note that if a component is large, it's likely dense.
        # But we need an exact answer.
        
        # Let's use the fact that we only need the MINIMUM weight.
        # We can precompute the global minimum weight node in the component.
        # Let m be the node with min weight in component c.
        # If m satisfies the condition, we are done.
        # If not, we might need the second best, etc.
        # But checking all is O(N).
        
        # Is there a property?
        # If the component has size > 2, and s, t are not directly connected,
        # is it always possible to find a k with very small weight?
        
        # Actually, we can just check the global minimum node in the component.
        # If it works, use it.
        # If not, check the second minimum?
        # How many candidates do we need to check?
        
        # In the worst case, we might need to check many.
        # But note: The condition is R_k < min_L_st OR L_k > max_R_st.
        # This is a union of two sets.
        # Set A: {k | R_k < min_L_st}
        # Set B: {k | L_k > max_R_st}
        
        # We can precompute for each component:
        # - The minimum weight node in the entire component.
        # - The minimum weight node in the set A.
        # - The minimum weight node in the set B.
        
        # But Set A and B depend on the query (min_L_st, max_R_st).
        
        # However, min_L_st and max_R_st are determined by s and t.
        
        # Let's store for each component a list of (R_i, W_i, L_i, index) sorted by R_i.
        # Then for a query, we can binary search for R_k < min_L_st to find the min weight in that range.
        # Similarly, sort by L_i to find min weight for L_k > max_R_st.
        
        # This requires building two auxiliary structures per component.
        # Total size O(N).
        
        # Let's implement this.
        
        # We need:
        # 1. For each component, a list of nodes sorted by R, with prefix min weights.
        # 2. For each component, a list of nodes sorted by L, with suffix min weights.
        
        # We already have nodes sorted by L. Let's build the R-sorted structure.
        
        # To save memory and time, we can build these structures lazily or all at once.
        # Given N=2e5, O(N log N) is fine.
        
        # Let's rebuild the necessary structures.
        pass

    # Re-doing the precomputation with the correct approach
    
    # Reset structures
    comp_nodes_by_R = [] # List of lists, each list is (R, W, original_index) sorted by R
    comp_nodes_by_L_suffix_min = [] # List of lists, each list is (L, W, original_index) sorted by L, with suffix min
    
    # We already have comp_nodes which are sorted by L.
    # Let's build the L-suffix min structure first.
    
    # And build the R-sorted structure with prefix min.
    
    for c in range(num_comps):
        nodes = comp_nodes[c]
        
        # Structure for L-suffix min:
        # Nodes are already sorted by L.
        # We want to query: min weight among nodes with L > Y.
        # This is a suffix of the L-sorted list.
        # We already computed suff_min for L-sorted list above, but we need to map it back.
        # Let's store the L values and the suff_min array.
        
        c_L_vals = [L[idx] for idx in nodes]
        # We need the suff_min array corresponding to this order.
        # We can recompute it.
        c_W_vals = [W[idx] for idx in nodes]
        
        c_suff_min = [float('inf')] * (len(nodes) + 1)
        curr = float('inf')
        for i in range(len(nodes) - 1, -1, -1):
            if c_W_vals[i] < curr:
                curr = c_W_vals[i]
            c_suff_min[i] = curr
        c_suff_min[len(nodes)] = float('inf') # Sentinel
        
        comp_nodes_by_L_suffix_min.append((c_L_vals, c_suff_min))
        
        # Structure for R-prefix min:
        # Sort nodes by R.
        nodes_by_R = sorted(nodes, key=lambda idx: R[idx])
        c_R_vals = [R[idx] for idx in nodes_by_R]
        c_W_vals_R = [W[idx] for idx in nodes_by_R]
        
        c_pref_min = [float('inf')] * len(nodes_by_R)
        curr = float('inf')
        for i in range(len(nodes_by_R)):
            if c_W_vals_R[i] < curr:
                curr = c_W_vals_R[i]
            c_pref_min[i] = curr
            
        comp_nodes_by_R.append((c_R_vals, c_pref_min))

    # Now process queries again with these structures
    results = []
    
    for s, t in queries:
        if comp_id[s] != comp_id[t]:
            results.append("-1")
            continue
            
        c = comp_id[s]
        
        if R[s] < L[t] or R[t] < L[s]:
            results.append(str(W[s] + W[t]))
            continue
            
        min_L_st = min(L[s], L[t])
        max_R_st = max(R[s], R[t])
        
        best_w = float('inf')
        
        # Check prefix in R-sorted list: R_k < min_L_st
        c_R_vals, c_pref_min = comp_nodes_by_R[c]
        
        # Binary search for the largest index i such that c_R_vals[i] < min_L_st
        # bisect_left returns the first index where value >= min_L_st
        # So all indices before that are < min_L_st
        import bisect
        idx_r = bisect.bisect_left(c_R_vals, min_L_st)
        if idx_r > 0:
            # Min weight in c_R_vals[0...idx_r-1]
            w_cand = c_pref_min[idx_r - 1]
            if w_cand < best_w:
                best_w = w_cand
                
        # Check suffix in L-sorted list: L_k > max_R_st
        c_L_vals, c_suff_min = comp_nodes_by_L_suffix_min[c]
        
        # Binary search for the first index i such that c_L_vals[i] > max_R_st
        # bisect_right returns the first index where value > max_R_st?
        # bisect_right returns insertion point after all elements <= max_R_st.
        # So elements from idx_l to end are > max_R_st.
        idx_l = bisect.bisect_right(c_L_vals, max_R_st)
        if idx_l < len(c_L_vals):
            w_cand = c_suff_min[idx_l]
            if w_cand < best_w:
                best_w = w_cand
                
        if best_w == float('inf'):
            results.append("-1")
        else:
            results.append(str(W[s] + best_w + W[t]))
            
    print('\n'.join(results))

solve()