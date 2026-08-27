import sys
import heapq
from collections import defaultdict

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
        
    # Directions for cardinal movement
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # For each block, we maintain a list of Pareto-optimal (floor, cost) pairs.
    # A state (h1, c1) dominates (h2, c2) if h1 >= h2 and c1 <= c2.
    # We store them sorted by floor. The costs will be non-increasing as floor increases?
    # Actually, for convex functions, if we sort by floor, the cost should be non-decreasing?
    # Let's think: To reach a higher floor, you generally need more stairs.
    # So if h1 < h2, then cost1 <= cost2 is typical.
    # Dominance: (h1, c1) dominates (h2, c2) if h1 >= h2 and c1 <= c2.
    # This means if you can reach a higher floor with less or equal cost, the lower floor state is useless.
    # So we want to keep states where increasing floor increases cost.
    # The non-dominated states will have strictly increasing floors and strictly increasing costs.
    
    # We use a dictionary to store the best known states for each block.
    # best[r][c] = list of (h, cost) sorted by h.
    # We will maintain the invariant that for any two states (h1, c1) and (h2, c2) in the list with h1 < h2, we have c1 < c2.
    # If we get a new state (h_new, c_new), we check if it is dominated by any existing state.
    # If not, we add it and remove any existing states that are dominated by it.
    
    # However, storing a list for each block and doing linear scans might be slow if the list grows.
    # But given the problem structure, the number of Pareto-optimal floors per block is expected to be small.
    
    # To optimize, we can use a more efficient structure, but for H,W <= 500 and Q <= 2e5, we need a fast per-query solution.
    # Running a full Dijkstra with state expansion per query might be too slow if the number of states is large.
    # Let's try to implement the Dijkstra with pruning.
    
    # Precompute neighbors for each block to avoid repeated checks
    # neighbors[r][c] = list of (nr, nc)
    neighbors = [[[] for _ in range(W)] for _ in range(H)]
    for r in range(H):
        for c in range(W):
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    neighbors[r][c].append((nr, nc))
                    
    results = []
    
    for (A, B, Y, C, D, Z) in queries:
        # Dijkstra
        # Priority queue: (cost, r, c, h)
        pq = []
        heapq.heappush(pq, (0, A, B, Y))
        
        # best[r][c] stores the list of non-dominated (h, cost)
        # We use a dictionary of lists
        best = defaultdict(list)
        
        # Helper to check if a state (h, cost) is dominated by existing states in best[r][c]
        # And to insert it while maintaining the invariant
        def is_dominated(r, c, h, cost):
            lst = best[(r, c)]
            # Check if any existing state dominates (h, cost)
            # A state (h_ex, c_ex) dominates (h, cost) if h_ex >= h and c_ex <= cost
            # Since lst is sorted by h, we can binary search or just scan if small
            for h_ex, c_ex in lst:
                if h_ex >= h and c_ex <= cost:
                    return True
            return False
        
        def add_state(r, c, h, cost):
            lst = best[(r, c)]
            # First, check if it's dominated
            if is_dominated(r, c, h, cost):
                return False
            
            # Remove states dominated by the new state
            # A state (h_ex, c_ex) is dominated by (h, cost) if h >= h_ex and cost <= c_ex
            new_lst = []
            for h_ex, c_ex in lst:
                if h >= h_ex and cost <= c_ex:
                    continue # dominated by new state
                else:
                    new_lst.append((h_ex, c_ex))
            new_lst.append((h, cost))
            # Sort by h
            new_lst.sort(key=lambda x: x[0])
            best[(r, c)] = new_lst
            return True

        # Initial state
        add_state(A, B, Y, 0)
        
        ans = float('inf')
        
        while pq:
            cost, r, c, h = heapq.heappop(pq)
            
            # If we reached the target block and floor, update answer
            if r == C and c == D and h == Z:
                ans = min(ans, cost)
                # Since Dijkstra, the first time we pop the exact target state, it's optimal?
                # Not necessarily, because we might reach (C,D,Z) with a higher cost first?
                # No, Dijkstra guarantees that the first time we pop a state, it's the minimum cost for that state.
                # But we might have multiple states for (C,D). We want the min cost for (C,D,Z).
                # So if we pop (C,D,Z), we can return immediately?
                # Yes, because all edge weights are non-negative.
                break
            
            # If this state is worse than what we already have for (r,c,h), skip
            # We can check if (h, cost) is in best[(r,c)] and if it's the best one?
            # Actually, we might have added it, but then a better one came along.
            # We can check if there's a state in best[(r,c)] that dominates (h, cost)
            # But we already filtered on insertion. However, due to multiple paths, we might have stale entries.
            # Let's check if (h, cost) is still non-dominated.
            if is_dominated(r, c, h, cost):
                continue
                
            # Try moving to adjacent blocks (walkway)
            for nr, nc in neighbors[r][c]:
                # Can move if F[nr][nc] >= h
                if F[nr][nc] >= h:
                    new_cost = cost
                    if add_state(nr, nc, h, new_cost):
                        heapq.heappush(pq, (new_cost, nr, nc, h))
                        
            # Try moving up/down stairs
            # Move up
            if h < F[r][c]:
                new_h = h + 1
                new_cost = cost + 1
                if add_state(r, c, new_h, new_cost):
                    heapq.heappush(pq, (new_cost, r, c, new_h))
                    
            # Move down
            if h > 1:
                new_h = h - 1
                new_cost = cost + 1
                if add_state(r, c, new_h, new_cost):
                    heapq.heappush(pq, (new_cost, r, c, new_h))
                    
        if ans == float('inf'):
            # This should not happen given the problem constraints
            ans = 0
            
        results.append(str(ans))
        
    print('\n'.join(results))

solve()