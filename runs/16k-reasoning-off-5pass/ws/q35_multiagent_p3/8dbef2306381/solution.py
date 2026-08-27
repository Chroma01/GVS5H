import sys
from bisect import bisect_left, bisect_right

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
    except StopIteration:
        return

    intervals = []
    for _ in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        intervals.append((L, R))
    
    # If N is bad, we cannot reach it
    # Check if N is in any interval
    # Since intervals are sorted and disjoint, we can use binary search
    # But let's just check directly since M is small
    
    def is_bad(x):
        # Check if x is in any interval [L, R]
        # Use binary search to find the interval that might contain x
        # We have a list of intervals sorted by L
        # Find the rightmost interval with L <= x
        # Then check if x <= R for that interval
        if not intervals:
            return False
        
        # intervals are sorted by L
        # Find the index of the last interval with L <= x
        # We can use bisect_right on the list of L's
        Ls = [iv[0] for iv in intervals]
        idx = bisect_right(Ls, x) - 1
        if idx < 0:
            return False
        L, R = intervals[idx]
        return L <= x <= R

    if is_bad(N):
        print("No")
        return

    # Collect critical points
    critical_points = set()
    critical_points.add(1)
    critical_points.add(N)
    
    for L, R in intervals:
        if L - 1 >= 1:
            critical_points.add(L - 1)
        if R + 1 <= N:
            critical_points.add(R + 1)
            
    # Filter out bad points
    safe_critical_points = []
    for p in critical_points:
        if not is_bad(p):
            safe_critical_points.append(p)
            
    safe_critical_points.sort()
    
    # Map point to index
    point_to_idx = {p: i for i, p in enumerate(safe_critical_points)}
    
    # If 1 or N is not in safe_critical_points, then it's not reachable (but 1 should be there, and we checked N is safe)
    if 1 not in point_to_idx or N not in point_to_idx:
        print("No")
        return
        
    start_idx = point_to_idx[1]
    end_idx = point_to_idx[N]
    
    # Build graph: for each point, find all points in [p+A, p+B]
    # Since the list is sorted, we can use binary search to find the range
    n_points = len(safe_critical_points)
    adj = [[] for _ in range(n_points)]
    
    for i in range(n_points):
        u = safe_critical_points[i]
        low = u + A
        high = u + B
        
        # Find the first index j such that safe_critical_points[j] >= low
        j_start = bisect_left(safe_critical_points, low)
        # Find the first index j such that safe_critical_points[j] > high
        j_end = bisect_left(safe_critical_points, high + 1)
        
        for j in range(j_start, j_end):
            v = safe_critical_points[j]
            if v > u: # Should be true since low > u
                adj[i].append(j)
                
    # BFS from start_idx
    from collections import deque
    visited = [False] * n_points
    queue = deque()
    queue.append(start_idx)
    visited[start_idx] = True
    
    while queue:
        curr = queue.popleft()
        if curr == end_idx:
            print("Yes")
            return
            
        for nxt in adj[curr]:
            if not visited[nxt]:
                visited[nxt] = True
                queue.append(nxt)
                
    print("No")

solve()