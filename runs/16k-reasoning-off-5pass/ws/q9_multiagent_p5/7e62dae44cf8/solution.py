import sys

# Increase recursion depth just in case, though we use iterative approach
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
        X = int(next(iterator))
        P = int(next(iterator))
        Q = int(next(iterator))
        
        grid = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(int(next(iterator)))
            grid.append(row)
    except StopIteration:
        return

    # Convert to 0-indexed
    r, c = P - 1, Q - 1
    
    # Current strength
    current_strength = grid[r][c]
    
    # Track occupied cells to avoid re-absorbing or moving back into an empty spot
    # Initially, only (r,c) is occupied by Takahashi.
    occupied = set()
    occupied.add((r, c))
    
    # Directions for 8-connectivity (King's moves)
    # Based on Sample 1 explanation, diagonal moves are implied by "newly adjacent" logic
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    while True:
        # Find the best neighbor to absorb
        # We want the smallest strength among valid neighbors
        best_val = float('inf')
        best_r, best_c = -1, -1
        
        # Check all 8 neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                # Check if not occupied
                if (nr, nc) not in occupied:
                    val = grid[nr][nc]
                    # Check condition: strictly less than current_strength / X
                    # To avoid float issues, use: val * X < current_strength
                    if val * X < current_strength:
                        if val < best_val:
                            best_val = val
                            best_r, best_c = nr, nc
        
        # If no valid move found, break
        if best_r == -1:
            break
        
        # Perform the move
        # 1. Add strength
        current_strength += best_val
        
        # 2. Update occupied set
        # The current cell (r, c) becomes empty (remove from occupied)
        # The new cell (best_r, best_c) becomes occupied (add to occupied)
        occupied.remove((r, c))
        occupied.add((best_r, best_c))
        
        # 3. Move
        r, c = best_r, best_c
        
    print(current_strength)

if __name__ == '__main__':
    solve()