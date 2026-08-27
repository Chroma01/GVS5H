import sys

# Increase recursion depth just in case
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        W = [0] + [int(next(iterator)) for _ in range(N)]
        L = [0] + [int(next(iterator)) for _ in range(N)]
        R = [0] + [int(next(iterator)) for _ in range(N)]
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            s = int(next(iterator))
            t = int(next(iterator))
            queries.append((s, t))
    except StopIteration:
        return

    # Constants
    MAX_COORD = 2 * N + 5
    INF = 10**18
    
    # Binary Indexed Tree for Range Minimum Query
    # bit[i] stores the minimum weight for R-coordinates in the range covered by i
    bit = [INF] * (MAX_COORD + 1)
    
    def update(idx, val):
        while idx <= MAX_COORD:
            if val < bit[idx]:
                bit[idx] = val
            idx += idx & -idx
            
    def query(idx):
        res = INF
        while idx > 0:
            if bit[idx] < res:
                res = bit[idx]
            idx -= idx & -idx
        return res

    # Prepare points for sweep-line
    # Each point is (L_i, R_i, W_i)
    points = []
    for i in range(1, N + 1):
        points.append((L[i], R[i], W[i]))
    
    # Initialize answers
    ans = [INF] * Q
    
    # Prepare sub-queries for the sweep-line
    # We need to find min W_k such that:
    # 1. R_k < min(L_s, L_t)
    # 2. L_k > R_t AND R_k < L_s
    # 3. L_k > R_s AND R_k < L_t
    # 4. L_k > max(R_s, R_t)
    #
    # We will process these offline.
    # Event format for queries: (A, B, query_index)
    # We want min W_k where L_k > A and R_k < B.
    # We sort points by L descending and queries by A descending.
    
    sub_queries = []
    
    for i in range(Q):
        s, t = queries[i]
        
        # Check for direct edge (length 1 path)
        # Edge exists if [L_s, R_s] and [L_t, R_t] are disjoint
        if R[s] < L[t] or R[t] < L[s]:
            ans[i] = W[s] + W[t]
        else:
            # If no direct edge, we look for a path of length 2 via some k.
            # k must be disjoint from s AND disjoint from t.
            # Disjoint from s: R_k < L_s OR L_k > R_s
            # Disjoint from t: R_k < L_t OR L_k > R_t
            # Intersection of these conditions gives 4 cases.
            
            # Case 1: R_k < L_s AND R_k < L_t  => R_k < min(L_s, L_t)
            # Constraint on L_k is none (effectively L_k > -inf).
            # We set A = 0 (since L_k >= 1)
            b1 = min(L[s], L[t])
            if b1 > 0:
                sub_queries.append((0, b1, i))
            
            # Case 2: R_k < L_s AND L_k > R_t
            sub_queries.append((R[t], L[s], i))
            
            # Case 3: R_k < L_t AND L_k > R_s
            sub_queries.append((R[s], L[t], i))
            
            # Case 4: L_k > R_s AND L_k > R_t => L_k > max(R_s, R_t)
            # Constraint on R_k is none (effectively R_k < inf).
            # We set B = 2*N + 2 (since max R is 2N)
            a4 = max(R[s], R[t])
            sub_queries.append((a4, 2 * N + 2, i))

    # Sort points by L descending
    points.sort(key=lambda x: x[0], reverse=True)
    
    # Sort queries by A descending
    sub_queries.sort(key=lambda x: x[0], reverse=True)
    
    # Sweep-line processing
    p_idx = 0
    n_points = len(points)
    
    for a, b, q_idx in sub_queries:
        # Add all points with L_k > a into the BIT
        # Since both lists are sorted descending, we advance p_idx while points[p_idx].L > a
        while p_idx < n_points and points[p_idx][0] > a:
            l, r, w = points[p_idx]
            update(r, w)
            p_idx += 1
        
        # Query min weight where R_k < b => range [1, b-1]
        if b > 1:
            res = query(b - 1)
            if res < ans[q_idx]:
                ans[q_idx] = res

    # Output results
    for i in range(Q):
        if ans[i] == INF:
            print("-1")
        else:
            print(ans[i])

if __name__ == '__main__':
    solve()