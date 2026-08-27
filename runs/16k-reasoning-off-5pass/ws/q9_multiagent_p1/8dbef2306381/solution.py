import sys

# Increase recursion depth just in case, though we use iterative approach
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

    # Sort bad intervals by L. 
    # The problem statement guarantees R_i < L_{i+1}, so they are disjoint and sorted.
    # However, sorting ensures robustness.
    bad_intervals.sort()

    # Set of reachable squares. Initially {1}.
    # We maintain this set explicitly. Since B is small, the set size is manageable.
    reachable = {1}

    for i in range(M):
        L, R = bad_intervals[i]
        
        # We need to jump over [L, R].
        # We can only jump from squares u < L.
        # Filter reachable set to keep only u < L.
        candidates = [u for u in reachable if u < L]
        
        if not candidates:
            print("No")
            return
        
        # Calculate new reachable squares after jumping over [L, R].
        # We land on v = u + k where A <= k <= B and v > R.
        next_reachable = set()
        for u in candidates:
            # We can jump from u to [u+A, u+B]
            # We need the landing spot v > R.
            # So we need u + k > R => k > R - u.
            # Also A <= k <= B.
            # So k in [max(A, R - u + 1), B].
            start_k = max(A, R - u + 1)
            if start_k <= B:
                for k in range(start_k, B + 1):
                    v = u + k
                    next_reachable.add(v)
        
        reachable = next_reachable
        
        if not reachable:
            print("No")
            return
        
        # Check if there is a next bad interval to optimize the gap
        if i < M - 1:
            next_L, next_R = bad_intervals[i+1]
            # The gap consists of squares from R+1 to next_L-1.
            # Number of squares in gap is (next_L - 1) - (R + 1) + 1 = next_L - R - 1.
            gap_size = next_L - R - 1
            
            # If the gap is large enough (>= B), we can reach any square in [next_L - B, next_L - 1]
            # provided we can reach at least one square in the gap.
            # Since we just jumped over [L, R] and landed in the gap (v > R), 
            # and the gap is large, we can traverse the gap to reach the critical points.
            # Specifically, if gap_size >= B, we can reach [next_L - B, next_L - 1].
            
            if gap_size >= B:
                # We can reach any square in [next_L - B, next_L - 1]
                # Note: next_L - B >= R + 1 because gap_size >= B => next_L - R - 1 >= B => next_L - B >= R + 1.
                new_reachable = set()
                for k in range(1, B + 1):
                    new_reachable.add(next_L - k)
                reachable = new_reachable
            else:
                # Gap is small, keep the explicit set.
                # We don't need to prune because the set size is small.
                pass

    # Finally, check if we can reach N
    # We need u in reachable such that u + k = N for some k in [A, B]
    # i.e., u in [N - B, N - A]
    can_reach_N = False
    for u in reachable:
        if u < N:
            # Check if N is in [u+A, u+B]
            if u + A <= N <= u + B:
                can_reach_N = True
                break
    
    if can_reach_N:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()