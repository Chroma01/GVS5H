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
    P -= 1
    Q -= 1

    S = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(next(iterator)))
        S.append(row)

    # Current strength starts with the slime at (P, Q)
    current_strength = S[P][Q]
    
    # Visited set to keep track of absorbed cells
    visited = [[False for _ in range(W)] for _ in range(H)]
    visited[P][Q] = True
    
    # Min-priority queue for adjacent slimes: (strength, r, c)
    pq = []
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Add initial neighbors
    for dr, dc in directions:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
            heapq.heappush(pq, (S[nr][nc], nr, nc))
            visited[nr][nc] = True  # Mark as added to PQ to avoid duplicates
    
    while pq:
        s, r, c = heapq.heappop(pq)
        
        # Check if we can absorb this slime
        # Condition: s < current_strength / X
        # Equivalent to: s * X < current_strength (using integer arithmetic to avoid precision issues)
        if s * X < current_strength:
            current_strength += s
            
            # Add unvisited neighbors of the newly absorbed cell
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                    heapq.heappush(pq, (S[nr][nc], nr, nc))
                    visited[nr][nc] = True
        else:
            # Since we process in increasing order of strength, if the smallest
            # cannot be absorbed, no other can be absorbed either.
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()