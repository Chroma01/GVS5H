import sys
import heapq

def solve():
    # Increase recursion depth just in case, though we use iterative Dijkstra
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
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
        A = int(next(iterator)) - 1
        B = int(next(iterator)) - 1
        Y = int(next(iterator))
        C = int(next(iterator)) - 1
        D = int(next(iterator)) - 1
        Z = int(next(iterator))
        queries.append((A, B, Y, C, D, Z))
        
    # Directions for cardinal adjacency
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    results = []
    
    for (A, B, Y, C, D, Z) in queries:
        # Dijkstra
        # dist[r][c] will store a list of Pareto optimal (cost, height) pairs
        # A pair (c1, h1) dominates (c2, h2) if c1 <= c2 and h1 >= h2.
        # We want to keep pairs that are not dominated.
        # Since we want to minimize cost and maximize height, the Pareto frontier
        # will have increasing cost and decreasing height.
        
        # Initialize distances
        # dist[r][c] = list of (cost, height)
        dist = [[[] for _ in range(W)] for _ in range(H)]
        
        # Priority Queue: (cost, r, c)
        pq = []
        
        # Start state
        # Cost 0, height Y at (A, B)
        # We need to add this to dist[A][B]
        # Since it's the first, we just add it.
        dist[A][B].append((0, Y))
        heapq.heappush(pq, (0, A, B))
        
        while pq:
            cost, r, c = heapq.heappop(pq)
            
            # Check if this state is still valid (not dominated by a better one already processed)
            # Since we use a PQ, the first time we pop a cell, it has the minimum cost.
            # However, there might be multiple Pareto optimal states for the same cell.
            # We need to check if the popped state is still in the dist list and not dominated.
            
            # Find the entry in dist[r][c] that matches this cost and height
            # Actually, we might have added multiple. We need to verify if this specific (cost, height)
            # is still part of the Pareto frontier or if it's been superseded.
            # A simpler way: when we pop (cost, r, c), we check if there is a better state in dist[r][c].
            # A state (c', h') is better if c' <= cost and h' >= height, and at least one strict inequality.
            # But since we process in increasing cost order, any previously processed state for (r,c)
            # has c' <= cost. If there was a state with c' <= cost and h' >= height, then (cost, height) is dominated.
            
            # Let's check if there is a state in dist[r][c] with cost <= cost and height >= height
            # Since we process in increasing cost, we only need to check if there is a state with height >= height
            # among those with cost <= cost. But since we just popped this, and we add to PQ only when we update,
            # it's possible that a better state was added later? No, PQ order ensures we process min cost first.
            # But multiple states can have same cost.
            
            # To be safe, we can check if the current (cost, height) is still "active".
            # We can mark states as processed. But let's just proceed and rely on the fact that
            # if a state is dominated, it won't generate useful neighbors.
            
            # Get the max height for this cost or better from dist[r][c]
            # Actually, let's just use the dist list to filter.
            # If there exists (c', h') in dist[r][c] such that c' <= cost and h' >= height, then skip.
            # But since we just popped this, and we add to dist when we push, it's in the list.
            # The issue is if we added a better state later. But we process in order.
            # So if there is a state with c' < cost, it was processed earlier.
            # If there is a state with c' == cost and h' >= height, it might be in the list.
            
            # Let's just check if this state is dominated by any state in dist[r][c]
            dominated = False
            for c_val, h_val in dist[r][c]:
                if c_val <= cost and h_val >= height:
                    if c_val < cost or h_val > height:
                        dominated = True
                        break
            if dominated:
                continue
                
            # If we are at the target, we don't stop because we might need to explore further
            # to find better Pareto points for the target? No, Dijkstra finds shortest path.
            # But we need all Pareto points for the target to compute the final answer.
            # So we continue until PQ is empty.
            
            # Try vertical moves: change height in current building
            # From height H, we can go to any height h <= F[r][c] with cost |H - h|.
            # This is equivalent to: for each neighbor, we can arrive at height min(H, F[neighbor]) with cost C.
            # But we can also change height in the current building before moving.
            # Instead of iterating all heights, we can just push the current state to neighbors.
            # The vertical move cost is accounted for when we arrive at the neighbor? No.
            
            # Correct logic:
            # When we are at (r,c) with cost C and height H, we can move to neighbor (nr, nc)
            # if H <= F[nr][nc]. The new cost is C, new height is H.
            # We can also change height in (r,c) to H' <= F[r][c] with cost C + |H - H'|.
            # Then move to neighbor if H' <= F[nr][nc].
            
            # To avoid iterating all heights, we can just push the current state to neighbors.
            # The vertical move within the building is handled by the fact that we can arrive at a building
            # at any height <= F[r][c] with some cost.
            
            # So, for each neighbor:
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    # Max height we can cross to (nr, nc) from (r,c) at height H
                    h_cross = min(height, F[nr][nc])
                    
                    # If we can cross at all (h_cross >= 1)
                    if h_cross >= 1:
                        new_cost = cost
                        new_height = h_cross
                        
                        # Check if this new state is dominated by existing states in dist[nr][nc]
                        # A state (c', h') dominates (new_cost, new_height) if c' <= new_cost and h' >= new_height
                        dominated_new = False
                        for c_val, h_val in dist[nr][nc]:
                            if c_val <= new_cost and h_val >= new_height:
                                if c_val < new_cost or h_val > new_height:
                                    dominated_new = True
                                    break
                        
                        if not dominated_new:
                            # Add to dist[nr][nc]
                            # Remove any states in dist[nr][nc] that are dominated by (new_cost, new_height)
                            new_dist = []
                            for c_val, h_val in dist[nr][nc]:
                                if not (new_cost <= c_val and new_height >= h_val):
                                    new_dist.append((c_val, h_val))
                            new_dist.append((new_cost, new_height))
                            dist[nr][nc] = new_dist
                            
                            heapq.heappush(pq, (new_cost, nr, nc))
                            
        # After Dijkstra, compute the answer for (C, D)
        # We have a list of (cost, height) pairs for (C, D)
        # The answer is min over all (c, h) in dist[C][D] of (c + |h - Z|)
        
        ans = float('inf')
        for c_val, h_val in dist[C][D]:
            current_ans = c_val + abs(h_val - Z)
            if current_ans < ans:
                ans = current_ans
                
        results.append(str(ans))
        
    print('\n'.join(results))

solve()