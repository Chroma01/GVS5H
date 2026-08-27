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
        
        # Adjust P and Q to 0-based indexing
        P -= 1
        Q -= 1
        
        grid = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(int(next(iterator)))
            grid.append(row)
            
    except StopIteration:
        return

    # Directions for neighbors: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Current state
    current_r, current_c = P, Q
    current_strength = grid[current_r][current_c]
    
    # 'visited' set tracks cells that are either:
    # 1. The current position of Takahashi.
    # 2. Cells that have been added to the heap (available neighbors).
    # This prevents re-adding cells and handles the dynamic grid.
    visited = set()
    visited.add((current_r, current_c))
    
    # Min-heap to store strengths of available neighbors.
    # Stores tuples: (strength, r, c)
    heap = []
    
    # Add initial neighbors to the heap
    for dr, dc in directions:
        nr, nc = current_r + dr, current_c + dc
        if 0 <= nr < H and 0 <= nc < W:
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
    
    # Greedy process
    while heap:
        strength, r, c = heapq.heappop(heap)
        
        # Check absorption condition: strictly less than 1/X times current strength
        # Equivalent to: strength * X < current_strength
        if strength * X < current_strength:
            # Absorb the slime
            current_strength += strength
            
            # The cell (r, c) is now absorbed. Its neighbors become newly adjacent.
            # We add these neighbors to the heap if they haven't been visited yet.
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        heapq.heappush(heap, (grid[nr][nc], nr, nc))
        else:
            # Cannot absorb the smallest available slime.
            # Since the heap is sorted by strength, no other slime can satisfy the condition.
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()