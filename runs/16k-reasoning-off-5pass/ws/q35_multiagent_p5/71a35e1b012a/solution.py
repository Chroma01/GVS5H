import sys

def solve():
    # Increase recursion depth just in case, though we try to be iterative
    sys.setrecursionlimit(2000000)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    ops = []
    for _ in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        ops.append((L, R))

    # Separate Op 1 and Op 2 candidates
    # Op 1: [L, R]
    # Op 2: covers [1, L-1] and [R+1, N]
    
    op1_intervals = []
    op2_candidates = [] # Store (L, R)
    
    for L, R in ops:
        op1_intervals.append((L, R))
        op2_candidates.append((L, R))

    # --- Precompute Op 1 Coverage Structure ---
    # We need to answer: min number of Op 1 intervals to cover [l, r]
    # Let reach[i] = max R such that there exists an Op 1 [L, R] with L <= i
    # If no such interval, reach[i] = i (or i-1 to indicate no progress)
    
    reach = [0] * (N + 2)
    for L, R in op1_intervals:
        if R > reach[L]:
            reach[L] = R
            
    # Propagate reach: reach[i] should be max reach for any start <= i
    # Actually, for greedy covering starting at l, we want the interval starting <= l that goes furthest.
    # So we compute max_reach[i] = max(reach[j] for j <= i)
    max_reach = [0] * (N + 2)
    current_max = 0
    for i in range(1, N + 2):
        if reach[i] > current_max:
            current_max = reach[i]
        max_reach[i] = current_max
        
    # Precompute binary lifting table for greedy jumps
    # up[k][i] = the position we reach after 2^k jumps starting from i
    # Jump from i: next_pos = max_reach[i] + 1
    # If max_reach[i] < i, we can't move forward.
    
    LOG = 20
    up = [[0] * (N + 2) for _ in range(LOG)]
    
    for i in range(1, N + 2):
        nxt = max_reach[i] + 1
        if nxt > N + 1:
            nxt = N + 1
        up[0][i] = nxt
        
    for k in range(1, LOG):
        for i in range(1, N + 2):
            up[k][i] = up[k-1][up[k-1][i]]
            
    def count_op1(l, r):
        """Min Op 1s to cover [l, r]. Returns infinity if impossible."""
        if l > r:
            return 0
        if max_reach[l] < l:
            return float('inf')
        
        # We need to cover [l, r].
        # Start at curr = l.
        # We want to find min steps to reach > r.
        curr = l
        count = 0
        for k in range(LOG - 1, -1, -1):
            if up[k][curr] <= r:
                curr = up[k][curr]
                count += (1 << k)
        
        # One more jump to cover up to r
        if curr <= r:
            count += 1
            curr = up[0][curr]
            
        if curr > r:
            return count
        else:
            return float('inf')

    # --- Precompute Op 2 Information ---
    # min_R_for_prefix[P] = min(R_i + 1) for all Op 2 with L_i - 1 >= P
    # has_prefix[P] = True if exists Op 2 with L_i - 1 >= P
    # has_suffix[S] = True if exists Op 2 with R_i + 1 <= S
    
    min_R_for_prefix = [float('inf')] * (N + 2)
    has_prefix = [False] * (N + 2)
    has_suffix = [False] * (N + 2)
    
    # Initialize with infinity
    for i in range(N + 2):
        min_R_for_prefix[i] = float('inf')
        
    for L, R in op2_candidates:
        p_val = L - 1
        s_val = R + 1
        
        if p_val >= 1:
            has_prefix[p_val] = True
            if s_val < min_R_for_prefix[p_val]:
                min_R_for_prefix[p_val] = s_val
                
        if s_val <= N:
            has_suffix[s_val] = True
            
    # Propagate has_prefix: if we can cover prefix P, we can cover P-1
    # But min_R_for_prefix needs to be the min R for ANY op that covers >= P.
    # Let's compute min_R_for_prefix[P] properly.
    # min_R_for_prefix[P] = min(min_R_for_prefix[P], min_R_for_prefix[P+1])?
    # No. min_R_for_prefix[P] is min(R+1) among ops with L-1 >= P.
    # If an op has L-1 >= P+1, it also has L-1 >= P.
    # So the set of ops for P is a superset of ops for P+1.
    # Thus min_R_for_prefix[P] <= min_R_for_prefix[P+1].
    
    for P in range(N, 0, -1):
        if min_R_for_prefix[P+1] < min_R_for_prefix[P]:
            min_R_for_prefix[P] = min_R_for_prefix[P+1]
        if has_prefix[P+1]:
            has_prefix[P] = True
            
    # Propagate has_suffix: if we can cover suffix S, we can cover S+1?
    # has_suffix[S] = exists op with R+1 <= S.
    # If exists op with R+1 <= S-1, then R+1 <= S.
    # So has_suffix[S] is true if has_suffix[S-1] is true?
    # No. has_suffix[S] means we cover [S, N].
    # If we have an op covering [S-1, N] (i.e. R+1 <= S-1), it also covers [S, N].
    # So if has_suffix[S-1] is true, has_suffix[S] is true.
    # Wait, let's check definition.
    # Op 2 covers [R+1, N]. So if R+1 <= S, it covers [S, N].
    # If R+1 <= S-1, then R+1 <= S.
    # So yes, has_suffix is monotonic: if S is coverable, S+1 is coverable.
    # But we want to know if there is an op that covers AT LEAST up to S.
    # Actually, has_suffix[S] should be true if min(R+1) <= S.
    # Let min_R_suffix[S] = min(R+1) for all ops.
    # Then has_suffix[S] is true if min_R_suffix <= S.
    
    # Let's recompute has_suffix correctly.
    # We want: exists Op 2 with R+1 <= S.
    # Let global_min_R_suffix = min(R+1) for all Op 2s.
    global_min_R_suffix = float('inf')
    for L, R in op2_candidates:
        s_val = R + 1
        if s_val < global_min_R_suffix:
            global_min_R_suffix = s_val
            
    for S in range(1, N + 2):
        if global_min_R_suffix <= S:
            has_suffix[S] = True
            
    # --- Find Minimum Cost ---
    best_total_cost = float('inf')
    best_P = -1
    best_S = -1
    best_op2_indices = []
    best_op1_indices = []
    
    # We iterate P from 0 to N.
    # P is the end of the prefix covered by Op 2s.
    # S is the start of the suffix covered by Op 2s.
    # Uncovered middle: [P+1, S-1].
    
    # Precompute min suffix start > P that is valid
    # min_valid_suffix_start[P] = min { S > P | has_suffix[S] }
    # This can be precomputed.
    
    min_valid_suffix_start = [float('inf')] * (N + 2)
    current_min = float('inf')
    for S in range(N + 1, 0, -1):
        if has_suffix[S]:
            current_min = S
        min_valid_suffix_start[S-1] = current_min # For P=S-1, min valid S is current_min
        
    # Actually, min_valid_suffix_start[P] should be min S > P.
    # Let's do it forward.
    min_valid_suffix_start = [float('inf')] * (N + 2)
    first_valid_S = float('inf')
    for S in range(1, N + 2):
        if has_suffix[S]:
            first_valid_S = S
        min_valid_suffix_start[S] = first_valid_S # This is min valid S >= S. We want > P.
        
    # Let's just iterate P and find best S.
    
    for P in range(0, N + 1):
        # Case 1: Use 1 Op 2 to cover prefix >= P and suffix >= S
        # This requires an Op 2 with L-1 >= P and R+1 <= S.
        # Min such S is min_R_for_prefix[P].
        M_R = min_R_for_prefix[P]
        
        if M_R != float('inf'):
            # We can choose S = M_R.
            # Cost = 1 + Op1Cost(P+1, M_R-1)
            # Note: If M_R-1 < P+1, the middle is empty, cost 0.
            mid_l = P + 1
            mid_r = M_R - 1
            c1 = 1 + count_op1(mid_l, mid_r)
            if c1 < best_total_cost:
                best_total_cost = c1
                best_P = P
                best_S = M_R
                best_op2_indices = [] # Will reconstruct
                best_op1_indices = []
                
        # Case 2: Use 2 Op 2s.
        # One for prefix >= P, one for suffix <= S.
        # Requires has_prefix[P] and has_suffix[S].
        # We want to minimize 2 + Op1Cost(P+1, S-1).
        # Best S is the smallest valid S > P.
        
        if has_prefix[P]:
            S_min = min_valid_suffix_start[P+1] # Smallest S > P
            if S_min != float('inf') and S_min < M_R: # Only if Case 1 didn't cover this S with cost 1
                # Check if S_min is valid
                if has_suffix[S_min]:
                    mid_l = P + 1
                    mid_r = S_min - 1
                    c2 = 2 + count_op1(mid_l, mid_r)
                    if c2 < best_total_cost:
                        best_total_cost = c2
                        best_P = P
                        best_S = S_min
                        best_op2_indices = []
                        best_op1_indices = []

    if best_total_cost == float('inf'):
        print("-1")
        return

    # --- Reconstruct Solution ---
    # We need to select specific Op 2s and Op 1s.
    
    selected_ops = [0] * M # 0, 1, or 2
    
    # Find Op 2 for prefix P
    # We need an Op 2 with L-1 >= P.
    # If best_S == min_R_for_prefix[best_P], we need ONE Op 2 that satisfies both.
    # Else, we need TWO Op 2s.
    
    op2_indices = []
    
    if best_S == min_R_for_prefix[best_P]:
        # Find one Op 2 with L-1 >= best_P and R+1 <= best_S
        found = False
        for idx, (L, R) in enumerate(ops):
            if (L - 1 >= best_P) and (R + 1 <= best_S):
                selected_ops[idx] = 2
                op2_indices.append(idx)
                found = True
                break
        if not found:
            # Should not happen if logic is correct
            pass
    else:
        # Find Op 2 for prefix
        for idx, (L, R) in enumerate(ops):
            if (L - 1 >= best_P):
                selected_ops[idx] = 2
                op2_indices.append(idx)
                break
        # Find Op 2 for suffix
        for idx, (L, R) in enumerate(ops):
            if (R + 1 <= best_S):
                selected_ops[idx] = 2
                op2_indices.append(idx)
                break
                
    # Find Op 1s to cover [best_P+1, best_S-1]
    mid_l = best_P + 1
    mid_r = best_S - 1
    
    if mid_l <= mid_r:
        curr = mid_l
        while curr <= mid_r:
            # Find best Op 1 covering curr
            # We need an Op 1 with L <= curr and max R.
            # We can precompute this or search.
            # Since we have max_reach, we know the max R is max_reach[curr].
            # But we need the index.
            
            # Let's precompute best_op1_index[i] = index of Op 1 that starts <= i and has max R.
            pass
            
    # Re-implement Op 1 selection with indices
    # Precompute best_op1_idx[i]
    best_op1_idx = [-1] * (N + 2)
    max_r_val = -1
    best_idx = -1
    for i in range(1, N + 1):
        # Check all ops starting at i? No, too slow.
        # Instead, iterate ops and update.
        pass
        
    # Let's do it during input reading
    # Re-read ops to store indices
    ops_with_idx = []
    for idx, (L, R) in enumerate(ops):
        ops_with_idx.append((L, R, idx))
        
    # Recompute max_reach with index
    reach_idx = [-1] * (N + 2)
    reach_val = [0] * (N + 2)
    
    for L, R, idx in ops_with_idx:
        if R > reach_val[L]:
            reach_val[L] = R
            reach_idx[L] = idx
            
    max_reach_val = [0] * (N + 2)
    max_reach_idx = [-1] * (N + 2)
    curr_max = 0
    curr_idx = -1
    for i in range(1, N + 2):
        if reach_val[i] > curr_max:
            curr_max = reach_val[i]
            curr_idx = reach_idx[i]
        max_reach_val[i] = curr_max
        max_reach_idx[i] = curr_idx
        
    # Re-select Op 1s
    if mid_l <= mid_r:
        curr = mid_l
        while curr <= mid_r:
            idx = max_reach_idx[curr]
            if idx == -1:
                # Should not happen if solution exists
                break
            selected_ops[idx] = 1
            curr = ops[idx][1] + 1 # ops is list of (L, R)
            
    # Output
    print(best_total_cost)
    print(" ".join(map(str, selected_ops)))

solve()