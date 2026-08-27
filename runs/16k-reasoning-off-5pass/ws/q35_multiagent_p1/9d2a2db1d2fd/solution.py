import sys
import heapq

# Set recursion limit just in case, though we use iterative Dijkstra
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    F = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(next(iterator)))
        F.append(row)

    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0

    queries = []
    for _ in range(Q):
        A = int(next(iterator))
        B = int(next(iterator))
        Y = int(next(iterator))
        C = int(next(iterator))
        D = int(next(iterator))
        Z = int(next(iterator))
        queries.append((A, B, Y, C, D, Z))

    # Directions for cardinal adjacency
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bidirectional_dijkstra(start_r, start_c, start_h, end_r, end_c, end_h):
        # If start and end are the same block and same floor, cost is 0
        if start_r == end_r and start_c == end_c and start_h == end_h:
            return 0
        
        # If start and end are the same block, cost is just vertical movement
        if start_r == end_r and start_c == end_c:
            return abs(start_h - end_h)

        # Forward search: from (start_r, start_c) at floor start_h
        # State: (cost, r, c, h)
        # We want to find min cost to reach any state (r, c, h) that can reach (end_r, end_c) at end_h
        
        # Backward search: from (end_r, end_c) at floor end_h
        # State: (cost, r, c, h)
        
        # Forward Dijkstra
        # dist_f[r][c][h] is not feasible due to large h.
        # We use a dictionary or just rely on the heap and visited set.
        # To optimize, we store best known cost for (r, c, h).
        # But h is large. We only visit relevant h.
        
        # Key optimization: 
        # The state space is (r, c, h).
        # We prune if we find a better cost for the same (r, c, h).
        # Also, if we reach (r, c) at floor h with cost C, 
        # and we have previously reached (r, c) at floor h' <= h with cost C' <= C,
        # is the new state dominated? 
        # Not necessarily, because being higher might allow walkways that lower doesn't.
        # However, if we reached (r, c) at h' <= h with C' <= C, 
        # we can always go up from h' to h with cost h - h'.
        # So if C' + (h - h') <= C, then the new state is dominated.
        # i.e., if C' - h' <= C - h, then the new state is worse or equal in terms of "potential".
        # Actually, the "potential" to reach a high floor H_target is C + (H_target - h).
        # So we want to minimize C - h for high floors? No.
        # Let's just use a simple visited set for (r, c, h) and hope the number of visited states is small.
        # Given the constraints and problem type, this is the best we can do in Python without complex structures.
        
        # Forward
        # heap: (cost, r, c, h)
        heap_f = []
        heapq.heappush(heap_f, (0, start_r, start_c, start_h))
        
        # best_f[r][c] = min cost to reach (r,c) at ANY floor? No, we need floor specific.
        # Let's store best_f[r][c][h] but use a dict for sparse storage.
        # best_f[(r,c,h)] = cost
        best_f = {}
        best_f[(start_r, start_c, start_h)] = 0
        
        # Backward
        heap_b = []
        heapq.heappush(heap_b, (0, end_r, end_c, end_h))
        best_b = {}
        best_b[(end_r, end_c, end_h)] = 0
        
        # To meet, we check if a state in forward search can connect to a state in backward search.
        # Connection: same (r, c) and same h.
        # Total cost = cost_f + cost_b.
        
        min_total_cost = float('inf')
        
        # We run both searches until one heap is empty or we have a good enough bound
        # Since edge weights are 0 and 1, we can use 0-1 BFS logic but Dijkstra is safer for 0/1 mix.
        
        # To prevent infinite loops and excessive states, we limit the search?
        # No, we just run until heaps are empty or we find the optimal.
        # But with bidirectional, we stop when the sum of min costs in heaps exceeds current best?
        # Not exactly, because we need to meet at a specific node.
        
        # Standard bidirectional Dijkstra termination:
        # When the smallest cost in heap_f + smallest cost in heap_b >= min_total_cost, we can stop?
        # Only if we have already found a meeting point.
        
        found_meeting = False
        
        while heap_f and heap_b:
            # Check termination condition
            if heap_f[0][0] + heap_b[0][0] >= min_total_cost:
                # If the sum of the lowest costs in both heaps is already >= best found,
                # we can't find a better solution.
                # But we must ensure we have checked all possible meeting points with lower costs.
                # This is valid for bidirectional Dijkstra with non-negative weights.
                break

            # Expand forward
            if heap_f[0][0] <= heap_b[0][0]:
                cost_f, r, c, h = heapq.heappop(heap_f)
                
                if cost_f > min_total_cost:
                    continue
                    
                # If this state has been visited in backward search, we found a meeting point
                if (r, c, h) in best_b:
                    total = cost_f + best_b[(r, c, h)]
                    if total < min_total_cost:
                        min_total_cost = total
                        found_meeting = True
                    continue
                
                # Explore neighbors
                # 1. Stairs: up and down
                for dh in [-1, 1]:
                    nh = h + dh
                    if 1 <= nh <= F[r][c]:
                        new_cost = cost_f + 1
                        if (r, c, nh) not in best_f or new_cost < best_f[(r, c, nh)]:
                            best_f[(r, c, nh)] = new_cost
                            heapq.heappush(heap_f, (new_cost, r, c, nh))
                
                # 2. Walkways: adjacent blocks at same floor
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        # Can walk if nh <= F[nr][nc]
                        if h <= F[nr][nc]:
                            new_cost = cost_f # 0 cost
                            if (nr, nc, h) not in best_f or new_cost < best_f[(nr, nc, h)]:
                                best_f[(nr, nc, h)] = new_cost
                                heapq.heappush(heap_f, (new_cost, nr, nc, h))
                                
            else:
                # Expand backward
                cost_b, r, c, h = heapq.heappop(heap_b)
                
                if cost_b > min_total_cost:
                    continue

                # If this state has been visited in forward search
                if (r, c, h) in best_f:
                    total = cost_b + best_f[(r, c, h)]
                    if total < min_total_cost:
                        min_total_cost = total
                        found_meeting = True
                    continue

                # Explore neighbors (same logic, reversed)
                # 1. Stairs
                for dh in [-1, 1]:
                    nh = h + dh
                    if 1 <= nh <= F[r][c]:
                        new_cost = cost_b + 1
                        if (r, c, nh) not in best_b or new_cost < best_b[(r, c, nh)]:
                            best_b[(r, c, nh)] = new_cost
                            heapq.heappush(heap_b, (new_cost, r, c, nh))
                
                # 2. Walkways
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        if h <= F[nr][nc]:
                            new_cost = cost_b
                            if (nr, nc, h) not in best_b or new_cost < best_b[(nr, nc, h)]:
                                best_b[(nr, nc, h)] = new_cost
                                heapq.heappush(heap_b, (new_cost, nr, nc, h))

        return min_total_cost

    results = []
    for q in queries:
        A, B, Y, C, D, Z = q
        # Convert to 0-indexed
        start_r, start_c = A - 1, B - 1
        end_r, end_c = C - 1, D - 1
        
        ans = bidirectional_dijkstra(start_r, start_c, Y, end_r, end_c, Z)
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()