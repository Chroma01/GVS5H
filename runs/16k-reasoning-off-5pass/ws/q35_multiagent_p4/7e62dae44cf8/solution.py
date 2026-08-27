import sys
import heapq

def solve():
    # Read all input from stdin
    data = sys.stdin.read().split()
    if not data:
        return
    
    iterator = iter(data)
    H = int(next(iterator))
    W = int(next(iterator))
    X = int(next(iterator))
    P = int(next(iterator)) - 1  # 0-indexed
    Q = int(next(iterator)) - 1  # 0-indexed
    
    S = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(next(iterator)))
        S.append(row)
    
    # Directions for adjacent cells: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    current_strength = S[P][Q]
    visited = set()
    visited.add((P, Q))
    current_pos = (P, Q)
    
    # Min-heap for adjacent slimes: (strength, r, c)
    adj_heap = []
    # Set to keep track of cells that are already in the heap
    in_heap = set()
    
    # Add initial neighbors
    for dr, dc in directions:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            if (nr, nc) not in visited:
                heapq.heappush(adj_heap, (S[nr][nc], nr, nc))
                in_heap.add((nr, nc))
    
    while adj_heap:
        s, r, c = heapq.heappop(adj_heap)
        
        # If already visited, skip
        if (r, c) in visited:
            continue
        
        # Check condition: s < current_strength / X
        # Use integer arithmetic to avoid floating point issues: s * X < current_strength
        if s * X < current_strength:
            current_strength += s
            visited.add((r, c))
            current_pos = (r, c)
            
            # Add new neighbors of the current position
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if (nr, nc) not in visited and (nr, nc) not in in_heap:
                        heapq.heappush(adj_heap, (S[nr][nc], nr, nc))
                        in_heap.add((nr, nc))
        else:
            # The weakest available slime is too strong, so no more can be absorbed
            break
    
    print(current_strength)

if __name__ == '__main__':
    solve()