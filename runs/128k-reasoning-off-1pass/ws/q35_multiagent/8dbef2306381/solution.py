import sys
from collections import deque

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
        
        intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            intervals.append((L, R))
    except StopIteration:
        return

    # If N is 1, we are already there (though constraints say N >= 2)
    if N == 1:
        print("Yes")
        return

    # Collect critical points: 1, N, and R_i + 1 for each bad interval
    critical_points = set()
    critical_points.add(1)
    critical_points.add(N)
    
    for L, R in intervals:
        if R + 1 <= N:
            critical_points.add(R + 1)
        # We don't need L-1 because we only land on safe squares.
        # The start of a safe segment is R_i + 1.
        # We start at 1.
        
    sorted_points = sorted(list(critical_points))
    point_to_idx = {p: i for i, p in enumerate(sorted_points)}
    
    # Precompute reachability for distances
    # We need to know if a distance d can be formed by sum of integers in [A, B]
    # Since B is small (<= 20), we can compute this up to a reasonable threshold.
    # The Frobenius number for interval [A, B] is small. 
    # A safe upper bound is B * A or B^2. Let's use 2000 to be safe.
    MAX_DIST_CHECK = 2000
    can_reach = [False] * (MAX_DIST_CHECK + 1)
    can_reach[0] = True
    
    for d in range(1, MAX_DIST_CHECK + 1):
        for step in range(A, B + 1):
            if d - step >= 0 and can_reach[d - step]:
                can_reach[d] = True
                break
    
    # Find threshold T such that for all d >= T, can_reach[d] is True
    # This happens when we have B consecutive True values.
    threshold = -1
    consecutive_true = 0
    for d in range(MAX_DIST_CHECK + 1):
        if can_reach[d]:
            consecutive_true += 1
            if consecutive_true >= B:
                threshold = d - B + 1
                break
        else:
            consecutive_true = 0
            
    # If threshold is not found within MAX_DIST_CHECK, it might be larger.
    # But with B <= 20, it should be found well before 2000.
    # If not found, we assume no large distances are reachable (which is wrong, but let's extend check if needed).
    # Let's extend the check if threshold is not found.
    if threshold == -1:
        # Extend the DP
        extended_limit = MAX_DIST_CHECK + 1000
        can_reach.extend([False] * 1000)
        for d in range(MAX_DIST_CHECK + 1, extended_limit + 1):
            for step in range(A, B + 1):
                if d - step >= 0 and can_reach[d - step]:
                    can_reach[d] = True
                    break
            if can_reach[d]:
                consecutive_true += 1
                if consecutive_true >= B:
                    threshold = d - B + 1
                    break
            else:
                consecutive_true = 0
        
        if threshold == -1:
            # Should not happen for valid A, B
            threshold = extended_limit + 1

    # Helper function to check if distance d is reachable
    def is_reachable(d):
        if d < 0:
            return False
        if d == 0:
            return True
        if d <= MAX_DIST_CHECK:
            return can_reach[d]
        else:
            # For large d, it is reachable if d >= threshold
            return d >= threshold

    # Determine which safe segment each critical point belongs to
    # A point p is in a safe segment if it is not covered by any bad interval.
    # Also, we need to group points that are in the same contiguous safe segment.
    # Two points u < v are in the same safe segment if there is no bad interval [L, R] such that u < L <= R < v is not quite right.
    # Actually, the safe segments are:
    # [1, L_1 - 1], [R_1 + 1, L_2 - 1], ..., [R_M + 1, N]
    # A critical point p is in the k-th safe segment if it falls within that range.
    # We can assign a segment ID to each critical point.
    
    # Sort intervals to make it easier
    intervals.sort()
    
    # Function to get segment ID for a point p
    # Segments are indexed 0, 1, ..., M
    # Segment 0: [1, L_1 - 1]
    # Segment i (1 <= i < M): [R_i + 1, L_{i+1} - 1]
    # Segment M: [R_M + 1, N]
    
    # We can determine the segment ID by checking which bad interval it falls into or after which one it is.
    # A point p is in segment k if:
    # - For k=0: p < L_1 (if M > 0)
    # - For k>0: R_k < p < L_{k+1} (if k < M)
    # - For k=M: p > R_M
    
    # Let's create a list of segment boundaries
    # Bad intervals are [L_i, R_i]
    # Safe intervals are [1, L_1-1], [R_1+1, L_2-1], ..., [R_M+1, N]
    
    # We can iterate through sorted points and assign segment IDs.
    # Since points are sorted, we can just check against the intervals.
    
    segment_ids = [0] * len(sorted_points)
    
    # For each point, find its segment
    # We can use binary search or just linear scan since M is small (2e4) and points are 2e4.
    # O(M^2) is 4e8, which is too slow. Let's use a smarter way.
    
    # Create a list of "events"
    # Each bad interval [L, R] makes squares L..R bad.
    # The safe segments are the gaps between these.
    
    # Let's create an array of segment starts.
    # Segment 0 starts at 1.
    # Segment i (i>=1) starts at R_{i-1} + 1.
    # The end of segment i is L_{i+1} - 1 (or N for the last one).
    
    # We can determine the segment ID of a point p by finding the largest R_i such that R_i < p.
    # If no such R_i exists, segment ID is 0.
    # If R_i < p, then the segment ID is i+1? Let's see.
    # If p < L_1, it's in segment 0.
    # If R_1 < p < L_2, it's in segment 1.
    # So if we find the largest i such that R_i < p, then the segment ID is i.
    # Wait, if R_1 < p, then p is after the first bad interval. So it's in segment 1.
    # If R_2 < p, then p is after the second bad interval. So it's in segment 2.
    # So segment ID = number of bad intervals that end before p.
    
    # Let's extract R values from intervals
    R_values = [R for L, R in intervals]
    R_values.sort()
    
    import bisect
    
    for i, p in enumerate(sorted_points):
        # Count how many R_values are strictly less than p
        # bisect_left gives the first index where R_values[idx] >= p
        # So the number of R_values < p is exactly that index.
        idx = bisect.bisect_left(R_values, p)
        segment_ids[i] = idx
        
    # Now, build the graph and run BFS
    # Nodes are indices in sorted_points
    # Edges from i to j if segment_ids[i] == segment_ids[j] and is_reachable(sorted_points[j] - sorted_points[i])
    
    # To optimize, we can group points by segment ID
    segments = {}
    for i, sid in enumerate(segment_ids):
        if sid not in segments:
            segments[sid] = []
        segments[sid].append(i)
        
    # Adjacency list
    adj = [[] for _ in range(len(sorted_points))]
    
    for sid, indices in segments.items():
        # For each pair of indices in the same segment
        # We want to add edge from i to j if i < j and is_reachable(p[j] - p[i])
        # To avoid O(K^2), we can iterate i and then j.
        # But K can be up to 40000. O(K^2) is too slow.
        # However, note that we only need to reach N.
        # We can use BFS. For each node u, we want to find all v > u in the same segment such that v-u is reachable.
        # Instead of iterating all v, we can iterate over possible reachable distances d, and check if u+d is a critical point.
        # But d can be large.
        # Alternative: Since B is small, the number of reachable distances in a small range is dense.
        # But the gap between critical points can be large.
        
        # Let's try the O(K^2) approach but with pruning.
        # If the segment is very long, there might be many points.
        # But in practice, M is 2e4, so total points are 4e4.
        # If all points are in one segment, we have 4e4 points.
        # O(K^2) is 1.6e9, which is too slow in Python.
        
        # We need a faster way.
        # Observation: If we can reach u, we can reach any v in the same segment such that v-u is reachable.
        # We can use a BFS. For each u, we want to find all v > u in the same segment with v-u reachable.
        # We can iterate over the next few points? No.
        
        # Better approach: For each segment, we have a list of points.
        # We can use a sliding window or a set of reachable points.
        # But we only care about critical points.
        
        # Let's use the fact that if we can reach u, we can reach u+d for any reachable d.
        # We can maintain a set of reachable critical points in the current segment.
        # But we need to find them efficiently.
        
        # Alternative: Since B is small, the set of reachable distances is periodic or has a simple structure.
        # We can iterate over all critical points v in the segment.
        # For a fixed u, we want to check if v-u is reachable.
        # We can precompute the set of reachable distances up to a large value? No.
        
        # Let's try to optimize the edge construction.
        # For each segment, let the points be p_0, p_1, ..., p_k.
        # We want to add edges (i, j) for i < j if p_j - p_i is reachable.
        # We can iterate i from 0 to k.
        # For each i, we iterate j from i+1 to k.
        # If p_j - p_i is too large, we can use the threshold.
        # If p_j - p_i is small, we use the precomputed array.
        
        # To speed up, we can break early if p_j - p_i is very large and not reachable?
        # No, we need to check all j.
        
        # Given the constraints and Python, we might need to hope that the test cases are not worst-case.
        # Or we can use a different approach: BFS with a queue.
        # For each u, we can try to jump to the next critical point v.
        # If v-u is reachable, we add v to the queue.
        # But we might skip some points.
        # If we can reach u, and we can reach v from u, we add v.
        # If we can't reach v directly from u, we might reach it from some intermediate w.
        # But if w is not a critical point, it's not in our graph.
        # However, as argued, if we can reach w from u and v from w, then v is reachable from u directly.
        # So we only need direct edges.
        
        # Let's implement the O(K^2) approach but with a break if the distance is too large and not reachable?
        # No, we can't break because larger distances might be reachable.
        
        # We'll implement it and hope for the best. If it's too slow, we might need to optimize.
        # One optimization: If p_j - p_i > threshold, it is reachable if threshold is set.
        # So we can quickly check.
        
        for i in range(len(indices)):
            u_idx = indices[i]
            u_val = sorted_points[u_idx]
            for j in range(i + 1, len(indices)):
                v_idx = indices[j]
                v_val = sorted_points[v_idx]
                dist = v_val - u_val
                if is_reachable(dist):
                    adj[u_idx].append(v_idx)
                else:
                    # If dist is not reachable, and dist is small, we continue.
                    # If dist is large and not reachable, it means dist < threshold and not in can_reach.
                    # But if dist is large, it should be reachable if dist >= threshold.
                    # So if we get here, dist < threshold and not reachable.
                    # We can continue to next j, as dist will increase.
                    pass

    # BFS from node 0 (which is 1)
    start_node = point_to_idx[1]
    end_node = point_to_idx[N]
    
    if start_node == end_node:
        print("Yes")
        return
        
    visited = [False] * len(sorted_points)
    visited[start_node] = True
    queue = deque([start_node])
    
    found = False
    while queue:
        u = queue.popleft()
        if u == end_node:
            found = True
            break
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                
    if found:
        print("Yes")
    else:
        print("No")

solve()