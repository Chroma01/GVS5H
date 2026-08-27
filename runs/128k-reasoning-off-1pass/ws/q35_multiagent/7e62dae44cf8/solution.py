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
        
        S = []
        for i in range(H):
            row = []
            for j in range(W):
                row.append(int(next(iterator)))
            S.append(row)
    except StopIteration:
        return

    # Convert 1-based P, Q to 0-based
    start_r = P - 1
    start_c = Q - 1

    current_strength = S[start_r][start_c]
    visited = [[False] * W for _ in range(H)]
    visited[start_r][start_c] = True

    # Min-heap to store (strength, r, c) of adjacent unvisited cells
    pq = []

    # Directions for adjacent cells: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Add initial neighbors of the starting cell
    for dr, dc in directions:
        nr, nc = start_r + dr, start_c + dc
        if 0 <= nr < H and 0 <= nc < W:
            if not visited[nr][nc]:
                heapq.heappush(pq, (S[nr][nc], nr, nc))

    while pq:
        s, r, c = heapq.heappop(pq)
        
        # Check if we can absorb this slime
        # Condition: s < current_strength / X
        # Using integer arithmetic: s * X < current_strength
        if s * X < current_strength:
            current_strength += s
            visited[r][c] = True
            
            # Add unvisited neighbors of the absorbed cell to the heap
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if not visited[nr][nc]:
                        heapq.heappush(pq, (S[nr][nc], nr, nc))
        else:
            # Since this is the smallest strength in the heap, and it can't be absorbed,
            # no other slime in the heap can be absorbed either.
            break

    print(current_strength)

if __name__ == '__main__':
    solve()