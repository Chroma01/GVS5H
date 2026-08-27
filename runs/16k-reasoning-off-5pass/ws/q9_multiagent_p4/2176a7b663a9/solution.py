import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        W = [0] + [int(next(iterator)) for _ in range(N)] # 1-based indexing for W
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
    except StopIteration:
        return

    # Coordinate range for BIT
    # Coordinates are up to 2*N. Max R is 2*N.
    MAX_COORD = 2 * N + 5
    
    # Precompute min_single_left[x]: min W_k such that R_k < x
    intervals_by_R = []
    for i in range(1, N + 1):
        intervals_by_R.append((R[i], W[i], i))
    intervals_by_R.sort(key=lambda x: x[0])
    
    min_single_left = [float('inf')] * (MAX_COORD + 1)
    current_min = float('inf')
    ptr = 0
    n_intervals = len(intervals_by_R)
    
    for x in range(1, MAX_COORD + 1):
        # Add all intervals with R_i < x
        while ptr < n_intervals and intervals_by_R[ptr][0] < x:
            if intervals_by_R[ptr][1] < current_min:
                current_min = intervals_by_R[ptr][1]
            ptr += 1
        min_single_left[x] = current_min

    # Precompute min_single_right[x]: min W_k such that L_k > x
    from collections import defaultdict
    by_L = defaultdict(list)
    for i in range(1, N + 1):
        by_L[L[i]].append(W[i])
        
    current_min = float('inf')
    min_single_right = [float('inf')] * (MAX_COORD + 1)
    
    for x in range(MAX_COORD, 0, -1):
        # Intervals with L == x+1 become valid for condition L > x
        if x + 1 in by_L:
            for w in by_L[x+1]:
                if w < current_min:
                    current_min = w
        min_single_right[x] = current_min

    # Fenwick Tree for Range Minimum Query
    class FenwickTree:
        def __init__(self, size):
            self.n = size
            self.tree = [float('inf')] * (self.n + 1)
        
        def update(self, i, val):
            while i <= self.n:
                if val < self.tree[i]:
                    self.tree[i] = val
                i += i & (-i)
        
        def query(self, i):
            res = float('inf')
            while i > 0:
                if self.tree[i] < res:
                    res = self.tree[i]
                i -= i & (-i)
            return res

    # Precompute min_pair_left[x]: min W_u + W_v s.t. R_u < L_v < x
    # This means two disjoint intervals both to the left of x.
    # We iterate x and maintain the best pair found so far in the set {k | R_k < x}.
    
    # Group intervals by R
    intervals_at_R = [[] for _ in range(MAX_COORD + 1)]
    for i in range(1, N + 1):
        if R[i] <= MAX_COORD:
            intervals_at_R[R[i]].append(i)
            
    bit_left = FenwickTree(MAX_COORD)
    global_best_pair_left = float('inf')
    min_pair_left = [float('inf')] * (MAX_COORD + 1)
    
    # Iterate x from 1 to MAX_COORD
    # At x, we add intervals with R == x-1.
    # These new intervals can form pairs with existing intervals (which have R < x-1).
    # Existing intervals are already in BIT.
    # For each new interval u (R_u = x-1):
    #   cost = W[u] + bit_left.query(L_u - 1)  (Need R_v < L_u)
    #   global_best_pair_left = min(global_best_pair_left, cost)
    #   bit_left.update(R_u, W[u])
    
    for x in range(1, MAX_COORD + 1):
        # Add intervals with R == x-1
        if x - 1 >= 1:
            for u in intervals_at_R[x-1]:
                # Try to form a pair with existing intervals
                # Need R_v < L_u. Query BIT for min W with index < L_u.
                val = bit_left.query(L[u] - 1)
                if val != float('inf'):
                    cand = W[u] + val
                    if cand < global_best_pair_left:
                        global_best_pair_left = cand
                
                # Add to BIT
                bit_left.update(R[u], W[u])
        
        min_pair_left[x] = global_best_pair_left

    # Precompute min_pair_right[x]: min W_u + W_v s.t. L_u > R_v > x
    # Symmetric to left case.
    # Sort intervals by L descending.
    # Group by L
    intervals_at_L = [[] for _ in range(MAX_COORD + 1)]
    for i in range(1, N + 1):
        if L[i] <= MAX_COORD:
            intervals_at_L[L[i]].append(i)
            
    bit_right = FenwickTree(MAX_COORD)
    global_best_pair_right = float('inf')
    min_pair_right = [float('inf')] * (MAX_COORD + 1)
    
    # Iterate x from MAX_COORD down to 1
    # At x, we add intervals with L == x+1.
    # These new intervals u (L_u = x+1) can form pairs with existing v (L_v >= x+1)
    # such that L_u > R_v.
    # So we need min W_v such that R_v < L_u.
    # Query bit_right.query(L_u - 1).
    # Update global_best_pair_right.
    # Add u to BIT at R_u.
    
    for x in range(MAX_COORD, 0, -1):
        # Add intervals with L == x+1
        if x + 1 <= MAX_COORD:
            for u in intervals_at_L[x+1]:
                # Try to form a pair
                # Need R_v < L_u. Query BIT for min W with index < L_u.
                val = bit_right.query(L[u] - 1)
                if val != float('inf'):
                    cand = W[u] + val
                    if cand < global_best_pair_right:
                        global_best_pair_right = cand
                
                # Add to BIT
                bit_right.update(R[u], W[u])
        
        min_pair_right[x] = global_best_pair_right

    # Process queries
    results = []
    for s, t in queries:
        # Check direct edge
        if R[s] < L[t] or R[t] < L[s]:
            results.append(W[s] + W[t])
            continue
        
        # Overlap
        ans = float('inf')
        
        # Option 1: Common neighbor (single)
        # k disjoint from both => R_k < min(L_s, L_t) or L_k > max(R_s, R_t)
        min_L = min(L[s], L[t])
        max_R = max(R[s], R[t])
        
        c1 = min_single_left[min_L]
        if c1 != float('inf'):
            ans = min(ans, W[s] + W[t] + c1)
            
        c2 = min_single_right[max_R]
        if c2 != float('inf'):
            ans = min(ans, W[s] + W[t] + c2)
        
        # Option 2: Path length 3
        # Case A: u far left of s, v far right of t
        # u: R_u < L_s, v: L_v > R_t
        # Always disjoint since s, t overlap => L_s <= R_t
        val_A = float('inf')
        if min_single_left[L[s]] != float('inf') and min_single_right[R[t]] != float('inf'):
            val_A = W[s] + W[t] + min_single_left[L[s]] + min_single_right[R[t]]
        if val_A < ans:
            ans = val_A
            
        # Case B: u, v both far left
        # Need two disjoint in {R < min(L_s, L_t)}
        if min_pair_left[min_L] != float('inf'):
            val_B = W[s] + W[t] + min_pair_left[min_L]
            if val_B < ans:
                ans = val_B
                
        # Case C: u, v both far right
        # Need two disjoint in {L > max(R_s, R_t)}
        if min_pair_right[max_R] != float('inf'):
            val_C = W[s] + W[t] + min_pair_right[max_R]
            if val_C < ans:
                ans = val_C
        
        if ans == float('inf'):
            results.append(-1)
        else:
            results.append(ans)
            
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()