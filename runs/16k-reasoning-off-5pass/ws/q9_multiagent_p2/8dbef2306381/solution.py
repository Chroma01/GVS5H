import sys
from collections import deque
import bisect

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
        
        bad_intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            bad_intervals.append((L, R))
    except StopIteration:
        return

    # Critical points: 1, N, L_i, R_i+1, L_i-1
    # We include L_i-1 to ensure we can check the point just before a bad interval
    # We include R_i+1 to ensure we can check the point just after a bad interval
    # This set of points is sufficient because the jump range [A, B] is small (<= 20).
    # Any valid jump landing in a safe region will either land on a critical point
    # or allow us to reach a critical point that enables jumping over the next bad interval.
    critical_points = set()
    critical_points.add(1)
    critical_points.add(N)
    
    for L, R in bad_intervals:
        critical_points.add(L)
        critical_points.add(R + 1)
        critical_points.add(L - 1)
        
    # Sort and remove duplicates
    P = sorted(list(critical_points))
    
    # Precompute bad status for each critical point
    # A point x is bad if L <= x <= R for some interval.
    # Since intervals are disjoint and sorted, x can belong to at most one interval.
    # We use binary search to find the interval.
    
    intervals = bad_intervals # Already sorted by L per constraints
    
    # Function to check if x is bad
    def is_bad(x):
        # Find first interval where L > x
        idx = bisect.bisect_right(intervals, (x, float('inf')))
        # Check the interval immediately before (if any)
        if idx > 0:
            L, R = intervals[idx-1]
            if L <= x <= R:
                return True
        return False

    # BFS initialization
    # reachable[i] is True if P[i] is reachable
    reachable = [False] * len(P)
    reachable[0] = True # P[0] is always 1
    
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        x = P[u]
        
        # We can jump to any y in [x+A, x+B]
        # We only care about critical points in this range
        
        lower_bound = x + A
        upper_bound = x + B
        
        # Find first index k such that P[k] >= lower_bound
        k_start = bisect.bisect_left(P, lower_bound)
        
        # Find first index k such that P[k] > upper_bound
        k_end = bisect.bisect_right(P, upper_bound)
        
        # Iterate through critical points in range
        for k in range(k_start, k_end):
            y = P[k]
            if is_bad(y):
                continue
            
            if not reachable[k]:
                reachable[k] = True
                queue.append(k)
    
    # Check if N is reachable
    # Find index of N in P
    idx_N = bisect.bisect_left(P, N)
    if idx_N < len(P) and P[idx_N] == N and reachable[idx_N]:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()