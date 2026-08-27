import sys
from collections import defaultdict
import bisect

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
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
        
    intervals = []
    for i in range(1, N + 1):
        L = int(next(iterator))
        R = int(next(iterator))
        intervals.append((L, R, i))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        s = int(next(iterator))
        t = int(next(iterator))
        queries.append((s, t))
        
    # Sort intervals by L_i, then by R_i
    intervals.sort(key=lambda x: (x[0], x[1]))
    
    # DSU implementation
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    # Extract L and R values for binary search
    L_vals = [iv[0] for iv in intervals]
    R_vals = [iv[1] for iv in intervals]
    
    # Create a list of intervals sorted by R for finding left disjoint intervals
    intervals_by_R = sorted(intervals, key=lambda x: x[1])
    R_vals_by_R = [iv[1] for iv in intervals_by_R]
    
    # Map from original index to position in sorted intervals
    pos_in_sorted = [0] * (N + 1)
    for idx, (L, R, orig_idx) in enumerate(intervals):
        pos_in_sorted[orig_idx] = idx
        
    # For each interval, union with nearest disjoint on left and right
    for idx in range(N):
        L_i, R_i, orig_i = intervals[idx]
        
        # Find left disjoint: largest R < L_i
        # In intervals_by_R, find the rightmost interval with R < L_i
        pos = bisect.bisect_left(R_vals_by_R, L_i)
        if pos > 0:
            # The interval at pos-1 has R < L_i
            orig_j = intervals_by_R[pos-1][2]
            union(orig_i, orig_j)
            
        # Find right disjoint: smallest L > R_i
        # In intervals (sorted by L), find the leftmost interval with L > R_i
        pos_right = bisect.bisect_right(L_vals, R_i)
        if pos_right < N:
            orig_k = intervals[pos_right][2]
            union(orig_i, orig_k)
            
    # Precompute min and second min weight in each component
    comp_min_W = defaultdict(lambda: float('inf'))
    comp_second_min_W = defaultdict(lambda: float('inf'))
    
    for i in range(1, N + 1):
        root = find(i)
        w = W[i]
        if w < comp_min_W[root]:
            comp_second_min_W[root] = comp_min_W[root]
            comp_min_W[root] = w
        elif w < comp_second_min_W[root]:
            comp_second_min_W[root] = w
            
    # For each query, check connectivity and compute min path weight
    results = []
    for s, t in queries:
        root_s = find(s)
        root_t = find(t)
        
        if root_s != root_t:
            results.append("-1")
            continue
            
        # Same component
        # Check if direct edge exists
        L_s, R_s, _ = intervals[pos_in_sorted[s]]
        L_t, R_t, _ = intervals[pos_in_sorted[t]]
        
        direct = False
        if R_s < L_t or R_t < L_s:
            direct = True
            
        min_w = comp_min_W[root_s]
        second_min_w = comp_second_min_W[root_s]
        
        # Find min weight in component excluding s and t
        min_hub = float('inf')
        if W[s] != min_w:
            min_hub = min_w
        else:
            # min_w is W[s], so we need the min of second_min_w and W[t] if W[t] != min_w
            if W[t] != min_w:
                min_hub = min(second_min_w, W[t])
            else:
                min_hub = second_min_w
                
        if direct:
            ans = W[s] + W[t]
        else:
            if min_hub == float('inf'):
                # No hub available, and no direct edge.
                # This means they are not connected?
                ans = -1
            else:
                ans = W[s] + W[t] + min_hub
                
        results.append(str(ans))
        
    print('\n'.join(results))

solve()