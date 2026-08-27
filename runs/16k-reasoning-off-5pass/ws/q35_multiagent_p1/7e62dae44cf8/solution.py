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

    # Current strength of Takahashi
    current_strength = S[P][Q]
    
    # Visited set to track absorbed cells
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    
    # Min-heap for adjacent slimes: (strength, r, c)
    heap = []
    
    # Directions for adjacent cells
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Add initial adjacent cells to the heap
    for dr, dc in directions:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            heapq.heappush(heap, (S[nr][nc], nr, nc))
    
    # To avoid adding the same cell to the heap multiple times,
    # we can use a set for cells currently in the heap or just check visited.
    # However, a cell might be added multiple times if we're not careful.
    # Let's use a separate set to track cells that are in the heap.
    in_heap = set()
    in_heap.add((P, Q)) # Mark start as processed/in_heap conceptually, though not in heap
    
    # Re-initialize in_heap properly for neighbors
    in_heap = set()
    in_heap.add((P, Q))
    
    # Clear heap and rebuild with proper in_heap tracking
    heap = []
    in_heap = set()
    in_heap.add((P, Q))
    
    for dr, dc in directions:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            if (nr, nc) not in in_heap:
                heapq.heappush(heap, (S[nr][nc], nr, nc))
                in_heap.add((nr, nc))
    
    while heap:
        strength, r, c = heapq.heappop(heap)
        
        # Check if this cell is already visited (shouldn't happen if we manage in_heap correctly, but safe to check)
        if visited[r][c]:
            continue
            
        # Check if we can absorb this slime
        # Condition: strength < current_strength / X
        # Equivalent to: strength * X < current_strength
        if strength * X < current_strength:
            # Absorb the slime
            current_strength += strength
            visited[r][c] = True
            
            # Add neighbors of the absorbed cell to the heap
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if not visited[nr][nc] and (nr, nc) not in in_heap:
                        heapq.heappush(heap, (S[nr][nc], nr, nc))
                        in_heap.add((nr, nc))
        else:
            # Since the heap is a min-heap, if the smallest strength slime cannot be absorbed,
            # no other slime in the heap can be absorbed.
            break
            
    print(current_strength)

solve()