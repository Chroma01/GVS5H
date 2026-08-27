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
    except StopIteration:
        return

    # Adjust P, Q to 0-indexed
    r0 = P - 1
    c0 = Q - 1

    S = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(next(iterator)))
        S.append(row)

    # Initial strength
    current_strength = S[r0][c0]
    
    # Visited set to track absorbed cells
    visited = [[False] * W for _ in range(H)]
    visited[r0][c0] = True
    
    # Min-priority queue for frontier slimes: (strength, r, c)
    pq = []
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Add initial neighbors to the priority queue
    for dr, dc in directions:
        nr, nc = r0 + dr, c0 + dc
        if 0 <= nr < H and 0 <= nc < W:
            heapq.heappush(pq, (S[nr][nc], nr, nc))
    
    while pq:
        s, r, c = heapq.heappop(pq)
        
        # If already visited, skip
        if visited[r][c]:
            continue
        
        # Check condition: s < current_strength / X
        # Equivalent to: s * X < current_strength
        if s * X < current_strength:
            # Absorb the slime
            current_strength += s
            visited[r][c] = True
            
            # Add unvisited neighbors to the priority queue
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                    heapq.heappush(pq, (S[nr][nc], nr, nc))
        else:
            # The smallest strength slime in the frontier cannot be absorbed.
            # Since all other slimes in the PQ have strength >= s,
            # none of them can be absorbed either.
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()