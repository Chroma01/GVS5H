import sys

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

    # If N is 1, we are already there (though constraints say N >= 2)
    if N == 1:
        print("Yes")
        return

    # Collect critical points: 1, N, and boundaries of bad intervals
    critical_points = set()
    critical_points.add(1)
    critical_points.add(N)
    
    for L, R in bad_intervals:
        critical_points.add(L)
        critical_points.add(R + 1)
        
    sorted_critical = sorted(list(critical_points))
    
    # Create a mapping from coordinate to index in sorted_critical
    coord_to_idx = {coord: i for i, coord in enumerate(sorted_critical)}
    
    # Determine which intervals between critical points are bad
    # An interval [sorted_critical[i], sorted_critical[i+1]-1] is bad if it overlaps with any bad interval
    # Since bad intervals are disjoint and sorted, we can check efficiently
    
    # First, let's mark which critical points are "bad" themselves
    # A point x is bad if it is covered by any bad interval
    # We can create a set of bad points for quick lookup, but since coordinates are large,
    # we'll use the intervals directly.
    
    # Helper function to check if a point is bad
    def is_bad(x):
        # Binary search or linear scan since M is small
        for L, R in bad_intervals:
            if L <= x <= R:
                return True
        return False

    # We will use DP. dp[i] = set of reachable squares in the interval ending at sorted_critical[i]
    # But since intervals can be large, we only track reachable squares near the boundaries.
    # Specifically, for each critical point i, we want to know if it's reachable.
    # To check if sorted_critical[i] is reachable, we look for a reachable square x such that:
    # A <= sorted_critical[i] - x <= B and the path from x to sorted_critical[i] is clear of bad squares.
    
    # Since B is small, we can maintain a set of reachable squares in a window of size B.
    # However, we need to be careful about the "clear path" condition.
    
    # Let's use a different approach:
    # Process critical points in order. For each critical point i, determine if it is reachable.
    # A critical point i is reachable if there exists a reachable critical point j < i such that:
    # 1. A <= sorted_critical[i] - sorted_critical[j] <= B
    # 2. The interval (sorted_critical[j], sorted_critical[i]) contains no bad squares.
    #    Note: sorted_critical[j] and sorted_critical[i] themselves must not be bad.
    
    # But wait, we might jump from a non-critical point. However, if we can reach a non-critical point x,
    # we can also reach any critical point y > x within distance B if the path is clear.
    # The key insight is that if a segment of good squares is long enough, we can traverse it.
    # Specifically, if we can reach any square in a good segment, we can reach any other square in the same segment
    # provided the distance is not too large? No, we can only jump A to B.
    
    # Let's stick to the critical points DP.
    # dp[i] = True if sorted_critical[i] is reachable, False otherwise.
    
    dp = [False] * len(sorted_critical)
    
    # Check if start is bad
    if is_bad(1):
        print("No")
        return
        
    dp[0] = True  # sorted_critical[0] should be 1
    
    for i in range(1, len(sorted_critical)):
        ci = sorted_critical[i]
        
        # If ci is bad, it cannot be reached
        if is_bad(ci):
            dp[i] = False
            continue
            
        # Check all previous critical points j < i
        # We only need to check j such that ci - cj <= B
        # Since B is small, we can check a few previous points
        found = False
        for j in range(i-1, -1, -1):
            cj = sorted_critical[j]
            diff = ci - cj
            
            if diff > B:
                # Since sorted_critical is sorted, further j will have even larger diff
                break
                
            if diff < A:
                continue
                
            if not dp[j]:
                continue
                
            # Check if the path from cj to ci is clear of bad squares
            # The path is clear if no square in (cj, ci) is bad.
            # Since cj and ci are critical points, the interval (cj, ci) is composed of
            # full segments between critical points. We can check if any of these segments are bad.
            # Actually, we can just check if any bad interval overlaps with (cj, ci).
            # But since cj and ci are critical points, the only way a bad interval overlaps with (cj, ci)
            # is if it is contained within (cj, ci).
            
            # We can check this by iterating over bad intervals
            path_clear = True
            for L, R in bad_intervals:
                # Check if [L, R] overlaps with (cj, ci)
                # Overlap if L < ci and R > cj
                if L < ci and R > cj:
                    # But we also need to ensure that the overlap is not just at the endpoints
                    # Since cj and ci are not bad (we checked is_bad), the overlap must be in the interior
                    # If L <= cj or R >= ci, then the bad interval is outside (cj, ci) or touches it.
                    # We need strict overlap: L > cj and R < ci? No.
                    # The condition is that no square in (cj, ci) is bad.
                    # So if there is a bad interval [L, R] such that L <= R and it overlaps with (cj, ci),
                    # then the path is not clear.
                    # Overlap with (cj, ci) means max(cj, L) < min(ci, R) + 1? No.
                    # It means there exists x such that cj < x < ci and L <= x <= R.
                    # This is equivalent to: L < ci and R > cj and not (R <= cj or L >= ci)
                    # Since we know cj < ci, and L <= R, the condition simplifies to:
                    # L < ci and R > cj and not (the bad interval is completely to the left or right)
                    # Actually, if L <= cj, then the bad interval starts before or at cj.
                    # If R >= ci, then the bad interval ends after or at ci.
                    # We need to check if the bad interval is strictly inside (cj, ci) or overlaps it.
                    # If L <= cj, then since cj is not bad, the bad interval must end after cj.
                    # If R >= ci, then since ci is not bad, the bad interval must start before ci.
                    # So if L <= cj and R >= ci, then the bad interval covers (cj, ci), so path is not clear.
                    # If L > cj and R < ci, then the bad interval is inside (cj, ci), so path is not clear.
                    # If L > cj and R >= ci, then the bad interval starts inside (cj, ci) and ends after ci, so path is not clear.
                    # If L <= cj and R < ci, then the bad interval starts before cj and ends inside (cj, ci), so path is not clear.
                    # In all cases, if L < ci and R > cj, then there is an overlap with (cj, ci).
                    # Because if L < ci and R > cj, then the interval [L, R] intersects (cj, ci).
                    # Since cj and ci are not bad, the intersection must be in the interior.
                    path_clear = False
                    break
            
            if path_clear:
                found = True
                break
                
        dp[i] = found
        
    # Check if N is reachable
    # Find the index of N in sorted_critical
    if N in coord_to_idx:
        idx = coord_to_idx[N]
        if dp[idx]:
            print("Yes")
        else:
            print("No")
    else:
        # This should not happen since we added N to critical_points
        print("No")

solve()