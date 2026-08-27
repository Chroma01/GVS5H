import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(next(iterator))
        
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(next(iterator))
        R[i] = int(next(iterator))
        
    Q = int(next(iterator))
    queries = []
    for _ in range(Q):
        s = int(next(iterator))
        t = int(next(iterator))
        queries.append((s, t))
        
    # Step 1: Find connected components of the intersection graph G'
    # Sort intervals by L, but keep track of original indices
    sorted_intervals = sorted([(L[i], R[i], i) for i in range(1, N+1)], key=lambda x: x[0])
    
    comp = [0] * (N + 1)
    comp_id = 0
    
    if N > 0:
        comp_id = 1
        current_max_r = sorted_intervals[0][1]
        comp[sorted_intervals[0][2]] = comp_id
        
        for i in range(1, N):
            l, r, idx = sorted_intervals[i]
            if l > current_max_r:
                comp_id += 1
                current_max_r = r
            else:
                current_max_r = max(current_max_r, r)
            comp[idx] = comp_id
            
    num_components = comp_id
    
    # Precompute min weight outside each component
    # Find the two smallest weights globally and their components
    min1_w = float('inf')
    min1_comp = -1
    min2_w = float('inf')
    min2_comp = -1
    
    for i in range(1, N+1):
        w = W[i]
        c = comp[i]
        if w < min1_w:
            min2_w = min1_w
            min2_comp = min1_comp
            min1_w = w
            min1_comp = c
        elif w < min2_w:
            min2_w = w
            min2_comp = c
            
    min_out = [0] * (num_components + 1)
    for c in range(1, num_components + 1):
        if min1_comp != c:
            min_out[c] = min1_w
        else:
            min_out[c] = min2_w
            
    results = []
    
    if num_components > 1:
        for s, t in queries:
            if comp[s] != comp[t]:
                results.append(str(W[s] + W[t]))
            else:
                # Same component, need to go through a node in another component
                results.append(str(W[s] + W[t] + min_out[comp[s]]))
                
    else:
        # Single component
        # Check if all intervals pairwise intersect
        # By Helly's property for intervals, this is true iff intersection of all is non-empty
        # i.e., max(L) <= min(R)
        
        max_L = max(L[1:])
        min_R = min(R[1:])
        
        if max_L <= min_R:
            # All pairwise intersect, G has no edges
            for s, t in queries:
                results.append("-1")
        else:
            # G is connected
            # Precompute min_W_left and min_W_right
            # Coordinates up to 2N
            max_coord = 2 * N + 1
            min_W_left = [float('inf')] * (max_coord + 2)
            min_W_right = [float('inf')] * (max_coord + 2)
            
            # min_W_left[x] = min W[k] such that R[k] < x
            # min_W_right[x] = min W[k] such that L[k] > x
            
            # For min_W_left:
            min_w_for_r = [float('inf')] * (max_coord + 1)
            for i in range(1, N+1):
                r = R[i]
                if W[i] < min_w_for_r[r]:
                    min_w_for_r[r] = W[i]
                    
            running_min = float('inf')
            for x in range(1, max_coord + 2):
                # min_W_left[x] is min W for R < x, i.e., R <= x-1
                if x - 1 >= 1:
                    if min_w_for_r[x-1] < running_min:
                        running_min = min_w_for_r[x-1]
                min_W_left[x] = running_min
                
            # For min_W_right:
            min_w_for_l = [float('inf')] * (max_coord + 1)
            for i in range(1, N+1):
                l = L[i]
                if W[i] < min_w_for_l[l]:
                    min_w_for_l[l] = W[i]
                    
            running_min = float('inf')
            for x in range(max_coord, -1, -1):
                # min_W_right[x] is min W for L > x, i.e., L >= x+1
                if x + 1 <= max_coord:
                    if min_w_for_l[x+1] < running_min:
                        running_min = min_w_for_l[x+1]
                min_W_right[x] = running_min
                
            for s, t in queries:
                # Check if disjoint
                if R[s] < L[t] or R[t] < L[s]:
                    results.append(str(W[s] + W[t]))
                else:
                    # Not disjoint, need intermediate k
                    # k must be disjoint from both s and t
                    # L_min = min(L[s], L[t]), R_max = max(R[s], R[t])
                    L_min = min(L[s], L[t])
                    R_max = max(R[s], R[t])
                    
                    # k must have R[k] < L_min OR L[k] > R_max
                    w_left = min_W_left[L_min]
                    w_right = min_W_right[R_max]
                    
                    min_w_k = min(w_left, w_right)
                    
                    if min_w_k == float('inf'):
                        # Should not happen if G is connected and not complete
                        results.append("-1")
                    else:
                        results.append(str(W[s] + W[t] + min_w_k))
                        
    print('\n'.join(results))

solve()