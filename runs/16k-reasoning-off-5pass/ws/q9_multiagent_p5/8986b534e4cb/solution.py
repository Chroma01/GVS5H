import sys

# Increase recursion depth to handle deep recursion in CDQ
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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

    # 1-based indexing for paths
    S = [0] * (M + 1)
    T = [0] * (M + 1)
    
    for i in range(1, M + 1):
        S[i] = int(next(iterator))
        T[i] = int(next(iterator))
    
    # Queries: L, R, original_index
    queries = []
    for i in range(Q):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r, i))
    
    # Result array: True if valid (No crossing), False if invalid (Crossing found)
    ans = [True] * Q
    
    # Fenwick Tree (Binary Indexed Tree) for range sum queries on T coordinates
    # Size N+2 to handle 1-based indexing comfortably
    bit = [0] * (N + 2)
    
    def update(idx, val):
        while idx <= N:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
    
    def query_range(l, r):
        if l > r:
            return 0
        return query(r) - query(l - 1)

    # CDQ Divide and Conquer
    # We process the array of intervals from index 1 to M.
    # We want to detect if there exists a pair (i, j) such that L <= i, j <= R
    # and S[i] < S[j] < T[i] < T[j].
    # This condition implies a "crossing" of intervals which makes the problem unsolvable.
    
    def cdq(l, r, qs):
        if l == r:
            return
        
        mid = (l + r) // 2
        
        # Filter queries that cover the current range [l, r]
        # A query [L, R] covers [l, r] if L <= l and R >= r.
        # If a crossing pair is found in [l, r], it satisfies L <= i < j <= R,
        # so the query is invalid.
        
        qs_curr = []
        for q in qs:
            L, R, idx = q
            if L <= l and R >= r:
                qs_curr.append(q)
        
        if not qs_curr:
            return
            
        # Prepare left and right parts
        left_intervals = []
        for i in range(l, mid + 1):
            left_intervals.append((S[i], T[i]))
        
        right_intervals = []
        for j in range(mid + 1, r + 1):
            right_intervals.append((S[j], T[j]))
            
        # Sort by S to enable the sweep-line approach
        left_intervals.sort(key=lambda x: x[0])
        right_intervals.sort(key=lambda x: x[0])
        
        ptr = 0
        n_left = len(left_intervals)
        n_right = len(right_intervals)
        
        found_crossing = False
        clear_indices = []
        
        # Iterate through right intervals and add left intervals to BIT
        # We look for pairs (i, j) with i in left, j in right such that:
        # S[i] < S[j] < T[i] < T[j]
        for s_j, t_j in right_intervals:
            # Add all left intervals with S[i] < S[j] to the BIT
            while ptr < n_left and left_intervals[ptr][0] < s_j:
                t_i = left_intervals[ptr][1]
                if 1 <= t_i <= N:
                    update(t_i, 1)
                    clear_indices.append(t_i)
                ptr += 1
            
            # Check if there is any T[i] in (s_j, t_j)
            # We need T[i] > S[j] and T[i] < T[j]
            # So we query the range [S[j] + 1, T[j] - 1]
            if s_j + 1 <= t_j - 1:
                if query_range(s_j + 1, t_j - 1) > 0:
                    found_crossing = True
                    break
        
        # Clear BIT to restore state for other recursive calls
        for t_i in clear_indices:
            update(t_i, -1)
            
        # Mark queries as invalid if a crossing was found
        if found_crossing:
            for q in qs_curr:
                ans[q[2]] = False

    # Initial call with all queries
    all_queries = queries
    cdq(1, M, all_queries)
    
    # Output results
    output = []
    for i in range(Q):
        if ans[i]:
            output.append("Yes")
        else:
            output.append("No")
            
    print('\n'.join(output))

if __name__ == '__main__':
    solve()