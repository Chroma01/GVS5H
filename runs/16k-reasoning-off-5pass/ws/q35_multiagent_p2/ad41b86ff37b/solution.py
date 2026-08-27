import sys

def solve():
    # Increase recursion depth just in case, though we won't use recursion
    sys.setrecursionlimit(10**6)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N < 3:
        # Constraints say N >= 3, but handle edge case
        print(0)
        return

    adj = [[] for _ in range(N + 1)]
    degree = [0] * (N + 1)
    
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    max_kept = 0

    # Iterate over each vertex as the potential center
    for center in range(1, N + 1):
        neighbors = adj[center]
        if not neighbors:
            continue
            
        # Collect degrees of all neighbors
        neighbor_degrees = []
        for nb in neighbors:
            neighbor_degrees.append(degree[nb])
        
        # Sort the degrees to efficiently count how many satisfy deg >= y + 1
        neighbor_degrees.sort()
        k = len(neighbor_degrees)
        
        # We want to maximize 1 + x * (y + 1)
        # For a fixed y, x is the number of neighbors with degree >= y + 1.
        # Let threshold = y + 1. We need count of d in neighbor_degrees such that d >= threshold.
        # y >= 1 implies threshold >= 2.
        
        # The maximum possible y for this center is max(neighbor_degrees) - 1.
        # The minimum possible y is 1.
        
        # Instead of iterating y from 1 to max_deg, we can iterate over the sorted degrees.
        # For a neighbor with degree d, it can support any y such that y + 1 <= d => y <= d - 1.
        # So this neighbor contributes to the count for all y in [1, d-1].
        
        # Let's iterate over possible values of y.
        # The relevant values for y are 1, 2, ..., max(neighbor_degrees) - 1.
        # For a given y, the number of valid neighbors is the count of degrees >= y + 1.
        
        # We can use binary search (bisect_left) to find the first index where degree >= y + 1.
        # Then the count is k - index.
        
        # Optimization: The max degree in neighbor_degrees is at most N.
        # But we only need to check y up to max(neighbor_degrees) - 1.
        
        max_nb_deg = neighbor_degrees[-1] if neighbor_degrees else 0
        
        # If max_nb_deg < 2, then no neighbor can have y >= 1 (since y+1 <= deg => 2 <= deg).
        # In that case, max_kept for this center is just 1 (center itself), but x must be >= 1.
        # If no neighbor can be an intermediate node, we can't form a snowflake with x>=1, y>=1.
        # However, the problem guarantees it's always possible.
        # If max_nb_deg < 2, then all neighbors have degree 1.
        # Then for y=1, we need deg >= 2. None qualify. So x=0? But x must be positive.
        # Wait, if all neighbors are leaves, we can pick x=1 neighbor, and y=0? No, y must be positive.
        # So if max_nb_deg < 2, this center cannot be the center of a valid Snowflake Tree with x>=1, y>=1.
        # But we are looking for the global maximum. Other centers might work.
        
        if max_nb_deg < 2:
            continue

        # Iterate y from 1 to max_nb_deg - 1
        # For each y, find count of neighbors with degree >= y + 1
        
        # Using bisect to find the first index where degree >= y + 1
        import bisect
        
        # Pre-calculate to avoid repeated imports or lookups if needed, but bisect is fast
        # We can iterate y. The number of y values is at most max_nb_deg.
        # Sum of max_nb_deg over all centers can be large? 
        # Worst case: Star graph. Center has degree N-1. Neighbors have degree 1.
        # max_nb_deg = 1. Loop doesn't run. Correct.
        # Worst case: Line graph. Each node has 2 neighbors (deg 2).
        # max_nb_deg = 2. y=1. Check deg >= 2. Both neighbors qualify. x=2. Kept = 1 + 2*(2) = 5.
        
        # To optimize, note that the count of valid neighbors is a step function of y.
        # It changes only when y+1 crosses a degree value.
        # We can iterate through the sorted degrees.
        
        # Let's just iterate y. The maximum degree is N.
        # In the worst case (e.g., a "broom" or specific trees), sum of max_nb_deg could be O(N^2)?
        # No. Consider a star graph with center C. Neighbors have degree 1. max_nb_deg=1.
        # Consider a graph where one node is connected to many high-degree nodes.
        # Example: Center connected to k nodes, each of degree D.
        # max_nb_deg = D. We iterate y from 1 to D-1.
        # Sum of D over all centers?
        # Each edge (u,v) contributes degree[v] to center u's list and degree[u] to center v's list.
        # Sum_{u} max_{v in adj(u)} degree[v] can be O(N^2) in worst case?
        # Yes, e.g., a "double star" or similar.
        # However, we don't need to iterate all y. We only need to check y values that are "critical".
        # The count K(y) is constant between degree values.
        # Specifically, K(y) = count(d >= y+1).
        # This value changes when y+1 equals some degree d.
        # So we only need to check y = d - 1 for each distinct degree d in neighbor_degrees.
        # Also y=1 is a candidate.
        
        unique_degrees = sorted(list(set(neighbor_degrees)))
        
        # Candidate y values:
        # 1. y = 1
        # 2. y = d - 1 for each d in unique_degrees, provided d - 1 >= 1.
        
        candidates_y = {1}
        for d in unique_degrees:
            if d - 1 >= 1:
                candidates_y.add(d - 1)
        
        for y in candidates_y:
            threshold = y + 1
            # Find first index where degree >= threshold
            idx = bisect.bisect_left(neighbor_degrees, threshold)
            count_valid = k - idx
            
            if count_valid > 0:
                # We can choose x = count_valid to maximize kept vertices for this y
                # Kept = 1 + x * (y + 1)
                kept = 1 + count_valid * (y + 1)
                if kept > max_kept:
                    max_kept = kept

    # The answer is the minimum number of deleted vertices
    # which is N - max_kept.
    print(N - max_kept)

solve()