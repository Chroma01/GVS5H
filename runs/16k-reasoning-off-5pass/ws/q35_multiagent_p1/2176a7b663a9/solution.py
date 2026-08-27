import sys

def solve():
    # Increase recursion depth just in case, though we don't use recursion
    sys.setrecursionlimit(200005)
    
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
        
    # Precompute min weight for nodes with R_k < X
    # Sort nodes by R_i
    nodes_by_R = sorted(range(1, N + 1), key=lambda i: R[i])
    
    # min_left_weight[i] stores the minimum weight among the first i+1 nodes in nodes_by_R
    # i.e., nodes with the smallest R values.
    # We want to query: min weight among all k such that R[k] < X.
    # This corresponds to a prefix of nodes_by_R.
    
    # Create an array of weights in the order of nodes_by_R
    weights_by_R = [W[i] for i in nodes_by_R]
    
    # Precompute prefix minimums
    # prefix_min[i] = min(weights_by_R[0]...weights_by_R[i])
    prefix_min = [0] * N
    if N > 0:
        current_min = weights_by_R[0]
        for i in range(N):
            if weights_by_R[i] < current_min:
                current_min = weights_by_R[i]
            prefix_min[i] = current_min
            
    # To find min weight with R[k] < X, we find the largest index idx such that R[nodes_by_R[idx]] < X.
    # Then the answer is prefix_min[idx]. If no such idx, then infinity.
    
    # We can use bisect to find the position.
    # R_values_sorted is the list of R values for nodes in nodes_by_R order.
    R_values_sorted = [R[i] for i in nodes_by_R]
    
    import bisect
    
    def get_min_left(X):
        # Find rightmost index where R < X
        # bisect_left returns the first index where R >= X
        idx = bisect.bisect_left(R_values_sorted, X)
        if idx == 0:
            return float('inf')
        return prefix_min[idx - 1]
        
    # Precompute min weight for nodes with L_k > Y
    # Sort nodes by L_i
    nodes_by_L = sorted(range(1, N + 1), key=lambda i: L[i])
    
    weights_by_L = [W[i] for i in nodes_by_L]
    
    # Precompute suffix minimums
    # suffix_min[i] = min(weights_by_L[i]...weights_by_L[N-1])
    suffix_min = [0] * N
    if N > 0:
        current_min = weights_by_L[N - 1]
        for i in range(N - 1, -1, -1):
            if weights_by_L[i] < current_min:
                current_min = weights_by_L[i]
            suffix_min[i] = current_min
            
    L_values_sorted = [L[i] for i in nodes_by_L]
    
    def get_min_right(Y):
        # Find leftmost index where L > Y
        # bisect_right returns the first index where L > Y? 
        # bisect_right returns insertion point after all elements <= Y.
        # So elements from idx onwards are > Y.
        idx = bisect.bisect_right(L_values_sorted, Y)
        if idx == N:
            return float('inf')
        return suffix_min[idx]
        
    results = []
    
    for s, t in queries:
        # Check direct edge
        # Edge exists if intervals are disjoint: R_s < L_t or R_t < L_s
        direct_weight = float('inf')
        if R[s] < L[t] or R[t] < L[s]:
            direct_weight = W[s] + W[t]
            
        # If direct edge exists, it's a candidate.
        # But we also check 2-hop paths.
        # If s and t are not directly connected, they must overlap.
        # If they overlap, any k disjoint from both must be:
        # 1. To the left of both: R_k < min(L_s, L_t)
        # 2. To the right of both: L_k > max(R_s, R_t)
        
        # Note: If they are directly connected, we still might find a cheaper 2-hop path?
        # No, because weights are positive. W_s + W_t < W_s + W_k + W_t for any W_k > 0.
        # So if direct edge exists, it is always the shortest path.
        
        if direct_weight != float('inf'):
            results.append(str(direct_weight))
            continue
            
        # If no direct edge, they overlap.
        # Calculate bounds for k
        L_min = min(L[s], L[t])
        R_max = max(R[s], R[t])
        
        min_k_left = get_min_left(L_min)
        min_k_right = get_min_right(R_max)
        
        min_k = min(min_k_left, min_k_right)
        
        if min_k == float('inf'):
            results.append("-1")
        else:
            ans = W[s] + W[t] + min_k
            results.append(str(ans))
            
    print('\n'.join(results))

solve()