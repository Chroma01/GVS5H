import sys

# Increase recursion depth just in case, though we try to avoid deep recursion
sys.setrecursionlimit(10**6)

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
    # A[i] corresponds to A_{i+1} in problem statement
    
    # Precompute first occurrence and previous occurrence for each index
    # first_occ[v] stores the first index (0-based) where value v appears
    first_occ = {}
    prev_occ = [-1] * N
    
    for i in range(N):
        val = A[i]
        if val not in first_occ:
            first_occ[val] = i
        else:
            prev_occ[i] = first_occ[val]
            # Update first_occ? No, we want the absolute first occurrence in the whole array
            # But for the interval logic within A[L..R], the "first" is relative to L.
            # However, the interval for a value v in A[L..R] is [first_in_subarray, last_in_subarray].
            # first_in_subarray is max(L, first_occ[v]).
            # last_in_subarray is the current R if v is present.
            # The "prev_occ" logic helps track the immediate previous occurrence.
            
    # We need to track components. A component is a set of indices that are connected.
    # In terms of intervals, a component corresponds to a merged interval [L_comp, R_comp].
    # We maintain a list of disjoint intervals representing the current components for the current R.
    # Since we iterate R, we can maintain these intervals.
    
    # However, we need to answer for all L.
    # We use a Segment Tree to maintain the values f(L, R) for all L.
    # The segment tree supports:
    # 1. Range Add: Add v to all elements in [l, r]
    # 2. Range Sum: Sum of all elements in [1, N] (or [0, N-1])
    
    # Segment Tree Implementation
    # Size N
    size = N
    tree_sum = [0] * (4 * size)
    tree_lazy = [0] * (4 * size)

    def push(node, l, r):
        if tree_lazy[node] != 0:
            mid = (l + r) // 2
            left_node = 2 * node
            right_node = 2 * node + 1
            
            tree_lazy[left_node] += tree_lazy[node]
            tree_sum[left_node] += tree_lazy[node] * (mid - l + 1)
            
            tree_lazy[right_node] += tree_lazy[node]
            tree_sum[right_node] += tree_lazy[node] * (r - mid)
            
            tree_lazy[node] = 0

    def update_range(node, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            tree_sum[node] += val * (r - l + 1)
            tree_lazy[node] += val
            return
        
        push(node, l, r)
        mid = (l + r) // 2
        update_range(2 * node, l, mid, ql, qr, val)
        update_range(2 * node + 1, mid + 1, r, ql, qr, val)
        tree_sum[node] = tree_sum[2 * node] + tree_sum[2 * node + 1]

    def get_total_sum():
        return tree_sum[1]

    # To manage components efficiently:
    # We maintain a list of disjoint intervals [start, end] for the current R.
    # These intervals represent the merged intervals of values.
    # When we move from R-1 to R:
    # Case 1: A[R] is new.
    #   - Add 1 to f(L, R) for all L in [0, R-1] (0-based index for L, corresponding to 1..R in 1-based).
    #     Actually, L ranges from 0 to R-1 (indices of A). The subarray is A[L..R].
    #     In 0-based indexing, L goes from 0 to R.
    #     Wait, f(L,R) is defined for 1 <= L <= R <= N.
    #     In 0-based: 0 <= L <= R < N.
    #     When we are at R (0-based), we consider all L from 0 to R.
    #     If A[R] is new, it starts a new interval [R, R].
    #     This new interval is disjoint from all previous intervals [s, e] where e <= R-1.
    #     So it adds 1 component for all L <= R.
    #     So we add 1 to tree for range [0, R].
    #     Add interval [R, R] to our list of components.
    #
    # Case 2: A[R] is old, last seen at p = prev_occ[R].
    #   - The interval for A[R] was [first_occ[A[R]], R-1] (conceptually, for L <= first_occ[A[R]]).
    #     Actually, the component containing first_occ[A[R]] had some end E_prev.
    #     Now it extends to R.
    #     This might merge with other components that overlap with [first_occ[A[R]], R].
    #     Let S = first_occ[A[R]].
    #     Find the component containing S. Let it be [S_comp, E_comp].
    #     Extend E_comp to R.
    #     Check for other components [s_j, e_j] such that they overlap with [S_comp, R].
    #     Overlap condition: s_j <= R and e_j >= S_comp.
    #     Since components are disjoint and sorted, and we just extended the right end,
    #     we only need to check components to the right of [S_comp, E_comp] that start <= R.
    #     Actually, any component with s_j <= R and e_j >= S_comp will merge.
    #     Since e_j <= R-1 (from previous step), the condition is e_j >= S_comp.
    #     Also s_j must be > E_comp (since disjoint).
    #     So we look for components with s_j > E_comp and s_j <= R and e_j >= S_comp.
    #     Wait, if s_j > E_comp, then the interval [s_j, e_j] is to the right.
    #     It overlaps [S_comp, R] if s_j <= R. (Since e_j >= s_j > E_comp >= S_comp, the lower bound is satisfied).
    #     So we merge all components with s_j in (E_comp, R].
    #     For each such component [s_j, e_j], we subtract 1 from f(L, R) for all L <= s_j.
    #     Why L <= s_j? Because the component [s_j, e_j] exists in A[L..R] only if L <= s_j.
    #     And the component [S_comp, E_comp] exists if L <= S_comp.
    #     Since S_comp <= s_j (as S_comp is the start of the left component), the condition for both to exist is L <= S_comp.
    #     Wait. If L > S_comp, the interval for the left component changes.
    #     The logic "subtract 1 for L <= min(s1, s2)" applies when the merge happens for the specific subarray.
    #     The merge happens if both components are "active" and their intervals overlap.
    #     The interval for the left component in A[L..R] is [max(L, S_comp), R].
    #     The interval for the right component is [s_j, e_j] (assuming L <= s_j).
    #     They overlap if max(L, S_comp) <= e_j.
    #     Since e_j >= S_comp, this is always true if L <= S_comp? No.
    #     If L > S_comp, the left interval starts at L. Overlap if L <= e_j.
    #     This is getting complex.
    #     
    #     Standard trick:
    #     f(L,R) = number of components.
    #     When we merge two components C1 and C2, the number of components decreases by 1.
    #     This decrease is valid for all L such that both C1 and C2 are present in A[L..R] AND their intervals overlap.
    #     C1 is present if L <= start(C1).
    #     C2 is present if L <= start(C2).
    #     So L <= min(start(C1), start(C2)).
    #     Do they overlap?
    #     Interval C1: [max(L, start(C1)), end(C1)].
    #     Interval C2: [start(C2), end(C2)].
    #     Overlap if max(L, start(C1)) <= end(C2).
    #     Since start(C1) <= start(C2) and end(C1) < start(C2) (disjoint),
    #     and we are merging because the new extension makes them overlap.
    #     The new end of C1 is R.
    #     So they overlap if max(L, start(C1)) <= end(C2).
    #     Since end(C2) >= start(C2) > start(C1), if L <= start(C1), then max(L, start(C1)) = start(C1) <= end(C2). True.
    #     If start(C1) < L <= end(C2), then max(L, start(C1)) = L <= end(C2). True.
    #     If L > end(C2), then L > end(C2). False.
    #     So the merge is valid for L <= end(C2).
    #     Also we need C2 to be present: L <= start(C2).
    #     So L <= min(end(C2), start(C2)) = start(C2).
    #     So we subtract 1 for L in [0, start(C2)-1] (0-based indices).
    #     Wait, if L = start(C2), C2 is present. Interval is [start(C2), end(C2)].
    #     C1 interval is [max(start(C2), start(C1)), R] = [start(C2), R].
    #     Overlap? [start(C2), end(C2)] and [start(C2), R]. Yes, they share start(C2).
    #     So L = start(C2) is included.
    #     So range is [0, start(C2)].
    #     In 0-based indexing, indices 0 to start(C2).
    
    # Data structure for components:
    # We can use a list of intervals, but we need to find and merge efficiently.
    # Since we only add intervals and merge, and intervals are always disjoint,
    # we can use a sorted list or a balanced BST. In Python, we can use a list and keep it sorted,
    # but merging might be O(K). Total K can be O(N).
    # However, each merge reduces the number of components.
    # Total merges is O(N).
    # We can use a dictionary or list to store components by their start index.
    
    # Let's store components as a list of [start, end].
    # We will keep this list sorted by start.
    components = [] # List of [start, end]
    
    # To quickly find the component containing a specific index or the component to the right,
    # we can use binary search or just iterate since we merge adjacent ones.
    # Actually, we can maintain a pointer or use bisect.
    
    from bisect import bisect_left, bisect_right
    
    # We also need to quickly find the component that contains 'S' (first_occ[A[R]]).
    # Since components are disjoint, we can search for the component with start <= S and end >= S.
    
    total_ans = 0
    
    for R in range(N):
        val = A[R]
        p = prev_occ[R]
        
        if p == -1:
            # New value
            # Add 1 to f(L, R) for all L in [0, R]
            update_range(1, 0, N - 1, 0, R, 1)
            # Add new component [R, R]
            components.append([R, R])
        else:
            # Old value
            S = first_occ[val]
            
            # Find the component containing S
            # Since components are sorted by start, and disjoint,
            # we can find the component with start <= S.
            # The component containing S must have start <= S <= end.
            
            # Find index in components
            # We can search for the rightmost component with start <= S
            starts = [c[0] for c in components]
            idx = bisect_right(starts, S) - 1
            
            if idx < 0:
                # Should not happen if S is in a component
                # But if S is not in any component?
                # S is first_occ, so it must be in a component if val appeared before.
                # Wait, if val appeared before, it was added to a component.
                pass
            else:
                comp = components[idx]
                S_comp, E_comp = comp
                
                # Extend this component to R
                # But first, check for merges with components to the right
                # Components to the right have start > E_comp.
                # They merge if their start <= R.
                
                # We will collect components to merge
                to_merge = []
                i = idx + 1
                while i < len(components):
                    c_start, c_end = components[i]
                    if c_start <= R:
                        to_merge.append(components[i])
                        i += 1
                    else:
                        break
                
                # For each component to merge, subtract 1 from f(L, R) for L in [0, c_start]
                for c_start, c_end in to_merge:
                    # Subtract 1 for L in [0, c_start]
                    update_range(1, 0, N - 1, 0, c_start, -1)
                
                # Remove merged components and update the main component
                # Remove from idx+1 to idx+len(to_merge)
                if to_merge:
                    del components[idx+1 : idx+1+len(to_merge)]
                    # Update the main component
                    components[idx][1] = R
                else:
                    # No merge, just extend
                    components[idx][1] = R
        
        # Add current total sum to answer
        total_ans += get_total_sum()
        
    print(total_ans)

solve()