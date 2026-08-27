import sys
from typing import List, Tuple
import bisect

def solve() -> None:
    # Increase recursion depth just in case
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
        
    # Step 1: Identify Connected Components
    # The graph G has an edge between i and j if [L_i, R_i] and [L_j, R_j] are disjoint.
    # This is the complement of an interval graph.
    # We use a sweep-line algorithm to find connected components.
    # Sort intervals by L_i.
    # Maintain a list of components, each characterized by its maximum R.
    # When processing interval i, it connects to all components with max_R < L_i.
    # These components merge with i.
    
    intervals = []
    for i in range(1, N + 1):
        intervals.append((L[i], R[i], i))
        
    intervals.sort(key=lambda x: x[0])
    
    parent = list(range(N + 1))
    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            
    # We will maintain a list of components.
    # Each component is represented by a tuple (max_R, root).
    # We will keep this list sorted by max_R.
    components = [] # List of (max_R, root)
    
    for l, r, idx in intervals:
        # Find all components with max_R < l
        # Since components is sorted by max_R, we can use binary search.
        max_rs = [c[0] for c in components]
        
        # Find the index of the first component with max_R >= l.
        idx_split = bisect.bisect_left(max_rs, l)
        
        # All components before idx_split have max_R < l.
        to_merge_roots = []
        new_max_r = r
        
        for i in range(idx_split):
            _, root = components[i]
            to_merge_roots.append(root)
            new_max_r = max(new_max_r, components[i][0])
            
        # Merge all these components with the current interval.
        for root in to_merge_roots:
            union(idx, root)
            
        # The new component's root is the root of the merged component.
        new_root = find(idx)
        
        # Remove the merged components from the list.
        remaining = components[idx_split:]
        components = remaining
        
        # Insert the new component into the list, maintaining sorted order.
        insert_idx = bisect.bisect_left([c[0] for c in remaining], new_max_r)
        remaining.insert(insert_idx, (new_max_r, new_root))
        components = remaining
        
    # Now, parent[i] gives the root of the component of i.
    # We can map each root to a component ID.
    comp_id_map = {}
    comp_id = 0
    for i in range(1, N + 1):
        root = find(i)
        if root not in comp_id_map:
            comp_id_map[root] = comp_id
            comp_id += 1
    comp_id_arr = [comp_id_map[find(i)] for i in range(N + 1)]
    
    # Precompute global min weight in each component
    num_components = comp_id + 1
    comp_min_w = [float('inf')] * num_components
    for i in range(1, N + 1):
        cid = comp_id_arr[i]
        comp_min_w[cid] = min(comp_min_w[cid], W[i])
        
    # Step 2: Precompute minimum weights for paths of length 2
    # Sort intervals by L_i and R_i
    intervals_by_L = sorted([(L[i], R[i], i) for i in range(1, N + 1)], key=lambda x: x[0])
    intervals_by_R = sorted([(L[i], R[i], i) for i in range(1, N + 1)], key=lambda x: x[1])
    
    # Precompute prefix min for intervals_by_R (for R_k < X)
    prefix_min_R = [0] * (N + 1)
    current_min = float('inf')
    for i in range(N):
        _, _, idx = intervals_by_R[i]
        current_min = min(current_min, W[idx])
        prefix_min_R[i+1] = current_min
        
    # Precompute suffix min for intervals_by_L (for L_k > Y)
    suffix_min_L = [0] * (N + 1)
    current_min = float('inf')
    for i in range(N - 1, -1, -1):
        _, _, idx = intervals_by_L[i]
        current_min = min(current_min, W[idx])
        suffix_min_L[i] = current_min
    suffix_min_L[N] = float('inf')
    
    # Extract R values for intervals_by_R and L values for intervals_by_L for bisect.
    R_vals = [x[1] for x in intervals_by_R]
    L_vals = [x[0] for x in intervals_by_L]
    
    def get_min_weight_disjoint(s, t):
        min_L = min(L[s], L[t])
        max_R = max(R[s], R[t])
        
        # Case 1: R_k < min_L
        idx1 = bisect.bisect_left(R_vals, min_L)
        min_w1 = prefix_min_R[idx1] if idx1 > 0 else float('inf')
        
        # Case 2: L_k > max_R
        idx2 = bisect.bisect_right(L_vals, max_R)
        min_w2 = suffix_min_L[idx2] if idx2 < N else float('inf')
        
        return min(min_w1, min_w2)
    
    # For path of length 3, we need to find k disjoint from s, m disjoint from t, and k disjoint from m.
    # We can iterate over the best candidates for k and m.
    # The best k disjoint from s is either the one with min W in R_k < L_s or L_k > R_s.
    # We can get the index of this k from the bisect.
    # Then we can check if this k is disjoint from t.
    # If not, we check the next best.
    
    # To efficiently get the best k disjoint from s, we can precompute the top few candidates.
    # However, given the constraints, we can just check the best few candidates from the global lists.
    
    # Let's precompute the top 5 candidates for each interval? No, too much memory.
    # Instead, we can just check the best candidate from the left and right.
    
    # For each query, we check:
    # 1. Direct edge.
    # 2. Path of length 2.
    # 3. Path of length 3: W[s] + W[t] + min_{k disjoint from s} (W[k] + min_{m disjoint from t and k} W[m]).
    #    We can approximate this by checking the best k disjoint from s, and then the best m disjoint from t and k.
    #    If k is not disjoint from t, we check the next best k.
    
    # Let's implement a function to get the best k disjoint from s.
    def get_best_k_disjoint(s, exclude_k=None):
        min_L_s = L[s]
        max_R_s = R[s]
        
        # Best k from R_k < L_s
        idx1 = bisect.bisect_left(R_vals, min_L_s)
        candidates = []
        if idx1 > 0:
            # Get the index in intervals_by_R
            # We want the best few candidates.
            # Let's get the top 5.
            for i in range(max(0, idx1 - 5), idx1):
                _, _, k_idx = intervals_by_R[i]
                if exclude_k is None or k_idx != exclude_k:
                    candidates.append((W[k_idx], k_idx))
        
        # Best k from L_k > R_s
        idx2 = bisect.bisect_right(L_vals, max_R_s)
        for i in range(idx2, min(N, idx2 + 5)):
            _, _, k_idx = intervals_by_L[i]
            if exclude_k is None or k_idx != exclude_k:
                candidates.append((W[k_idx], k_idx))
                
        if not candidates:
            return float('inf'), -1
        
        candidates.sort()
        return candidates[0]
    
    results = []
    for s, t in queries:
        if comp_id_arr[s] != comp_id_arr[t]:
            results.append(-1)
            continue
            
        # Check direct edge
        if R[s] < L[t] or R[t] < L[s]:
            ans = W[s] + W[t]
        else:
            ans = float('inf')
            
        # Check path of length 2
        min_w = get_min_weight_disjoint(s, t)
        if min_w != float('inf'):
            ans = min(ans, W[s] + W[t] + min_w)
            
        # Check path of length 3
        # We need to find k disjoint from s, m disjoint from t, and k disjoint from m.
        # We can iterate over the best candidates for k.
        best_k_w, best_k_idx = get_best_k_disjoint(s)
        if best_k_w != float('inf'):
            # Check if best_k is disjoint from t
            if R[best_k_idx] < L[t] or R[t] < L[best_k_idx]:
                # Then m can be the best disjoint from t
                min_w_m = get_min_weight_disjoint(best_k_idx, t)
                if min_w_m != float('inf'):
                    ans = min(ans, W[s] + W[best_k_idx] + W[t] + min_w_m)
            else:
                # best_k is not disjoint from t, so we need m disjoint from t and best_k.
                # This is hard. We can try the next best k.
                # Let's get the next best k.
                _, next_k_idx = get_best_k_disjoint(s, exclude_k=best_k_idx)
                if next_k_idx != -1:
                    if R[next_k_idx] < L[t] or R[t] < L[next_k_idx]:
                        min_w_m = get_min_weight_disjoint(next_k_idx, t)
                        if min_w_m != float('inf'):
                            ans = min(ans, W[s] + W[next_k_idx] + W[t] + min_w_m)
                    else:
                        # Try next next best k
                        _, next_next_k_idx = get_best_k_disjoint(s, exclude_k=next_k_idx)
                        if next_next_k_idx != -1:
                            if R[next_next_k_idx] < L[t] or R[t] < L[next_next_k_idx]:
                                min_w_m = get_min_weight_disjoint(next_next_k_idx, t)
                                if min_w_m != float('inf'):
                                    ans = min(ans, W[s] + W[next_next_k_idx] + W[t] + min_w_m)
        
        if ans == float('inf'):
            results.append(-1)
        else:
            results.append(ans)
            
    for res in results:
        print(res)

solve()