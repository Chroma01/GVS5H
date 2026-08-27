import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
        X = int(next(iterator))
        P = int(next(iterator))
        Q = int(next(iterator))
        
        # Grid is 1-indexed in problem, we will use 0-indexed internally
        S = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(int(next(iterator)))
            S.append(row)
    except StopIteration:
        return

    # Convert 1-based P, Q to 0-based
    start_r, start_c = P - 1, Q - 1
    
    # Takahashi's current strength
    current_strength = S[start_r][start_c]
    
    # Visited array to keep track of slimes that have been either absorbed 
    # or added to the priority queue.
    visited = [[False for _ in range(W)] for _ in range(H)]
    
    # Priority queue stores tuples (strength, r, c)
    pq = []
    
    # Directions for neighbors: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Initialize: Add all initial neighbors of (start_r, start_c) to the PQ
    for dr, dc in directions:
        nr, nc = start_r + dr, start_c + dc
        if 0 <= nr < H and 0 <= nc < W:
            if not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(pq, (S[nr][nc], nr, nc))
    
    # Greedy simulation
    while pq:
        s_val, r, c = heapq.heappop(pq)
        
        # Check if the slime can be absorbed
        # Condition: s_val < current_strength / X
        # Equivalent to: s_val * X < current_strength (using integer arithmetic)
        if s_val * X < current_strength:
            current_strength += s_val
            
            # The slime at (r, c) is absorbed. Takahashi moves to (r, c).
            # New neighbors are the neighbors of (r, c).
            # We add unvisited neighbors to the PQ.
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if not visited[nr][nc]:
                        visited[nr][nc] = True
                        heapq.heappush(pq, (S[nr][nc], nr, nc))
        else:
            # Since the PQ is a min-heap, if the smallest available slime cannot be absorbed,
            # no other slime can be absorbed either (as they are all >= s_val).
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()