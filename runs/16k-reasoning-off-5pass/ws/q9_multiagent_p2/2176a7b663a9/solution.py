import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        W = [0] + [int(next(iterator)) for _ in range(N)] # 1-based indexing for W
        intervals = []
        for i in range(1, N + 1):
            L = int(next(iterator))
            R = int(next(iterator))
            intervals.append({'id': i, 'L': L, 'R': R, 'W': W[i]})
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            s = int(next(iterator))
            t = int(next(iterator))
            queries.append((s, t))
    except StopIteration:
        return

    # Sort intervals by R, then by L
    # This helps in efficiently finding intervals that are to the left or right
    intervals.sort(key=lambda x: (x['R'], x['L']))
    
    MAX_COORD = 2 * N + 5
    INF = float('inf')
    
    # Fenwick Tree for Range Minimum Query (Prefix Min)
    # We will update positions with R values.
    bit_min_R = [INF] * (MAX_COORD + 1)
    
    def update_bit_min(idx, val):
        while idx <= MAX_COORD:
            if val < bit_min_R[idx]:
                bit_min_R[idx] = val
            idx += idx & (-idx)
            
    def query_bit_min(idx):
        res = INF
        while idx > 0:
            if bit_min_R[idx] < res:
                res = bit_min_R[idx]
            idx -= idx & (-idx)
        return res

    # Segment Tree for Range Minimum Query (Suffix Min on L)
    MAX_L = 2 * N + 5
    seg_min_L = [INF] * (4 * MAX_L)
    
    def update_seg_min(node, start, end, idx, val):
        if start == end:
            if val < seg_min_L[node]:
                seg_min_L[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            update_seg_min(2 * node, start, mid, idx, val)
        else:
            update_seg_min(2 * node + 1, mid + 1, end, idx, val)
        seg_min_L[node] = min(seg_min_L[2 * node], seg_min_L[2 * node + 1])
        
    def query_seg_min(node, start, end, l, r):
        if r < start or end < l:
            return INF
        if l <= start and end <= r:
            return seg_min_L[node]
        mid = (start + end) // 2
        return min(query_seg_min(2 * node, start, mid, l, r),
                   query_seg_min(2 * node + 1, mid + 1, end, l, r))

    # Precompute best_left and best_right for all intervals
    best_left = [INF] * (N + 1)
    best_right = [INF] * (N + 1)
    
    # 1. Compute best_left
    # Iterate intervals sorted by R.
    # Maintain BIT of R values.
    # For current interval i (with L_i), query BIT for min W in range [1, L_i - 1].
    # Then update BIT with (R_i, W_i).
    
    # Reset BIT
    for i in range(MAX_COORD + 1):
        bit_min_R[i] = INF
        
    sorted_intervals = intervals # Already sorted by R
    
    for item in sorted_intervals:
        L, R, W_val, orig_id = item['L'], item['R'], item['W'], item['id']
        
        # Query min W for R < L
        if L > 1:
            w_min = query_bit_min(L - 1)
            if w_min != INF:
                best_left[orig_id] = w_min
        
        # Update BIT with R
        update_bit_min(R, W_val)
        
    # 2. Compute best_right
    # We need min W for L > R_i.
    # Populate Segment Tree with all intervals first.
    for item in intervals:
        update_seg_min(1, 1, MAX_L, item['L'], item['W'])
        
    for item in intervals:
        R, orig_id = item['R'], item['id']
        if R < MAX_L:
            w_min = query_seg_min(1, 1, MAX_L, R + 1, MAX_L)
            if w_min != INF:
                best_right[orig_id] = w_min
                
    results = []
    for s, t in queries:
        # Get interval data (using 0-based index for list access)
        # intervals is sorted, so we need to map back or store original.
        # We stored 'id' in intervals, but we need L, R for the specific ID.
        # Let's create a lookup array for L and R to avoid searching.
        pass

    # Re-organize intervals into arrays for O(1) access by ID
    L_arr = [0] * (N + 1)
    R_arr = [0] * (N + 1)
    for item in intervals:
        L_arr[item['id']] = item['L']
        R_arr[item['id']] = item['R']
        
    for s, t in queries:
        # Check disjoint
        # Disjoint if R_s < L_t or R_t < L_s
        if R_arr[s] < L_arr[t] or R_arr[t] < L_arr[s]:
            results.append(str(W[s] + W[t]))
            continue
        
        # Overlapping
        L_s, R_s = L_arr[s], R_arr[s]
        L_t, R_t = L_arr[t], R_arr[t]
        
        L_min = min(L_s, L_t)
        R_max = max(R_s, R_t)
        
        ans = INF
        
        # Single bridge
        # Query BIT for min W for R < L_min
        w1 = query_bit_min(L_min - 1)
        if w1 != INF:
            ans = min(ans, W[s] + W[t] + w1)
            
        # Query SegTree for min W for L > R_max
        w2 = query_seg_min(1, 1, MAX_L, R_max + 1, MAX_L)
        if w2 != INF:
            ans = min(ans, W[s] + W[t] + w2)
            
        # Two bridges
        # Option A: best_left[s] and best_right[t]
        a = best_left[s]
        b = best_right[t]
        if a != INF and b != INF:
            ans = min(ans, W[s] + W[t] + a + b)
            
        # Option B: best_right[s] and best_left[t]
        a = best_right[s]
        b = best_left[t]
        if a != INF and b != INF:
            ans = min(ans, W[s] + W[t] + a + b)
            
        if ans == INF:
            results.append("-1")
        else:
            results.append(str(ans))
            
    print('\n'.join(results))

solve()