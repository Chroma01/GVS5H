import sys
import bisect

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000)

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

    # Sort bad intervals by L (input says they are sorted, but good to be safe)
    bad_intervals.sort()
    
    # Precompute Ls for binary search
    Ls = [interval[0] for interval in bad_intervals]
    
    def is_bad_optimized(x):
        # Find the first interval with L > x
        idx = bisect.bisect_right(Ls, x)
        # If idx > 0, the interval at idx-1 has L <= x.
        # We need to check if x <= R of that interval.
        if idx > 0:
            L_curr, R_curr = bad_intervals[idx-1]
            if x <= R_curr:
                return True
        return False

    # BFS Queue
    queue = [1]
    visited = {1}
    
    # To optimize finding the next bad interval, we can maintain an index
    bad_idx = 0
    
    while queue:
        u = queue.pop(0)
        
        if u == N:
            print("Yes")
            return
        
        # Find the next bad interval that starts >= u
        # Since bad_intervals is sorted, we can advance bad_idx
        while bad_idx < M and bad_intervals[bad_idx][0] < u:
            bad_idx += 1
            
        # Now bad_intervals[bad_idx] is the first interval with L >= u
        # Or bad_idx == M if no more intervals
        
        if bad_idx < M:
            L_next, R_next = bad_intervals[bad_idx]
        else:
            # No more bad intervals, effectively the rest of the line is safe
            L_next = N + 1
            R_next = N # Doesn't matter
            
        # Determine reachable squares
        # Case 1: The gap to the next bad interval is large enough (u + B < L_next)
        # In this case, we can reach any safe square up to u + B.
        # Specifically, we can reach L_next - 1 (the square just before the bad interval).
        # From L_next - 1, we can potentially jump over the bad interval.
        # We add L_next - 1 to the queue.
        
        if u + B < L_next:
            target = L_next - 1
            if target <= N and target not in visited:
                visited.add(target)
                queue.append(target)
        else:
            # Case 2: The gap is small (u + B >= L_next)
            # We must check each jump individually to see if it lands on a safe square.
            for k in range(A, B + 1):
                v = u + k
                if v > N:
                    break
                
                # Check if v is bad
                # Since we know the next bad interval starts at L_next, 
                # v is bad if L_next <= v <= R_next.
                # If v < L_next, it is safe (since no bad intervals start before L_next).
                # If v >= L_next, it might be bad.
                
                if v < L_next:
                    # Safe
                    if v not in visited:
                        visited.add(v)
                        queue.append(v)
                else:
                    # v >= L_next, check if it's in a bad interval
                    # Since intervals are sorted, we can check the current one or subsequent ones.
                    # We use the optimized check.
                    if not is_bad_optimized(v):
                        if v not in visited:
                            visited.add(v)
                            queue.append(v)
                            
    print("No")

if __name__ == '__main__':
    solve()