import sys

# Increase recursion depth to handle deep segment tree recursion if necessary
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        W = []
        for _ in range(N):
            W.append(int(next(iterator)))
            
        L = []
        R = []
        for _ in range(N):
            L.append(int(next(iterator)))
            R.append(int(next(iterator)))
            
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            s = int(next(iterator))
            t = int(next(iterator))
            queries.append((s, t))
    except StopIteration:
        return

    # Coordinate range for R is 1 to 2*N.
    # We use a safe upper bound.
    MAX_COORD = 2 * N + 5
    
    # Segment Tree for Range Minimum Query
    # tree[i] stores the min weight in the range covered by node i
    # Initialize with infinity
    tree = [float('inf')] * (4 * MAX_COORD)
    
    def update(node, start, end, idx, val):
        if start == end:
            # We want the minimum weight for a given R coordinate
            tree[node] = min(tree[node], val)
            return
        mid = (start + end) // 2
        if idx <= mid:
            update(2 * node, start, mid, idx, val)
        else:
            update(2 * node + 1, mid + 1, end, idx, val)
        tree[node] = min(tree[2 * node], tree[2 * node + 1])

    def query(node, start, end, l, r):
        if r < start or end < l:
            return float('inf')
        if l <= start and end <= r:
            return tree[node]
        mid = (start + end) // 2
        p1 = query(2 * node, start, mid, l, r)
        p2 = query(2 * node + 1, mid + 1, end, l, r)
        return min(p1, p2)

    # Populate Segment Tree
    # We use 1-based indexing for coordinates as per problem (1 to 2N)
    for i in range(N):
        update(1, 1, MAX_COORD - 1, R[i], W[i])

    results = []
    for s, t in queries:
        # Adjust to 0-based index for W, L, R arrays
        idx_s = s - 1
        idx_t = t - 1
        
        l_s, r_s = L[idx_s], R[idx_s]
        l_t, r_t = L[idx_t], R[idx_t]
        
        w_s, w_t = W[idx_s], W[idx_t]
        
        # Check direct edge: intervals are disjoint
        # Disjoint means R_s < L_t OR R_t < L_s
        if r_s < l_t or r_t < l_s:
            results.append(w_s + w_t)
        else:
            # Overlapping, need intermediate node k
            # k must be disjoint from s AND disjoint from t.
            # This implies k is either strictly to the left of both (R_k < min(L_s, L_t))
            # or strictly to the right of both (L_k > max(R_s, R_t)).
            
            min_l = min(l_s, l_t)
            max_r = max(r_s, r_t)
            
            # Query left gap: R_k < min_l => R_k in [1, min_l - 1]
            left_min = float('inf')
            if min_l - 1 >= 1:
                left_min = query(1, 1, MAX_COORD - 1, 1, min_l - 1)
            
            # Query right gap: L_k > max_r => R_k >= L_k > max_r => R_k in [max_r + 1, MAX_COORD - 1]
            right_min = float('inf')
            if max_r + 1 <= MAX_COORD - 1:
                right_min = query(1, 1, MAX_COORD - 1, max_r + 1, MAX_COORD - 1)
            
            best_k = min(left_min, right_min)
            
            if best_k == float('inf'):
                results.append(-1)
            else:
                results.append(w_s + w_t + best_k)
                
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()