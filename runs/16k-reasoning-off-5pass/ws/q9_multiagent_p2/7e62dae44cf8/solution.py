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
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Current strength of Takahashi
    current_strength = grid[P][Q]
    
    # Mark the starting cell as visited (absorbed conceptually, though he stays there)
    # Actually, the problem says he absorbs the slime and moves into the cell.
    # So the cell he is in is effectively "occupied" by him.
    # We need to track which cells are currently adjacent to him.
    
    # We will use a set to keep track of cells that have been added to the priority queue
    # to avoid duplicates.
    pq_cells = set()
    
    # Priority Queue stores (strength, r, c)
    pq = []
    
    # Initial neighbors
    for dr, dc in dirs:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            heapq.heappush(pq, (grid[nr][nc], nr, nc))
            pq_cells.add((nr, nc))
            
    # We need to track which cells have been absorbed (removed from grid)
    # Since we modify the grid in place, we can just check if a cell is still valid.
    # However, to avoid re-adding a cell that was already absorbed, we need a visited set for absorbed cells.
    # Actually, the logic is:
    # 1. Pop smallest neighbor.
    # 2. If absorbable: add strength, mark cell as absorbed, find new neighbors.
    # 3. If not absorbable: stop.
    
    # To prevent adding the same cell multiple times to the PQ:
    # We maintain `pq_cells` set. If a cell is in `pq_cells`, it's either in PQ or processed.
    # But wait, if we process a cell (absorb it), we remove it from `pq_cells`? 
    # No, once a cell is absorbed, it's gone. We shouldn't add it again.
    # So `pq_cells` tracks cells that are currently adjacent or have been added to PQ.
    # When we absorb a cell, we remove it from `pq_cells` so it's not added again as a neighbor?
    # Actually, the standard way is:
    # `visited` set for cells that have been added to PQ.
    # When we pop (s, r, c):
    #   If (r, c) is already absorbed (we can track this separately), skip? 
    #   But we only push each cell once.
    
    # Let's refine:
    # `added_to_pq` set: stores (r, c) of cells that are currently in the PQ or have been processed.
    # When we generate new neighbors, if a neighbor is not in `added_to_pq`, we add it.
    # When we absorb a cell, we remove it from `added_to_pq`? No, it's gone.
    # But we need to know if a cell is currently adjacent.
    # The PQ contains the adjacent cells.
    # If we pop a cell, we absorb it. It is no longer adjacent.
    # We need to add its neighbors.
    # We must ensure we don't add a cell to PQ if it's already in PQ or already absorbed.
    # Since we only absorb once, we can use a `visited` set for cells that have been added to PQ.
    # If a cell is in `visited`, it's either in PQ or already absorbed.
    # If it's in PQ, we don't add it again. If it's absorbed, we definitely don't add it.
    # So `visited` is sufficient.
    
    visited = set()
    visited.add((P, Q)) # Starting cell is "visited" (occupied)
    
    # Add initial neighbors to PQ and visited
    for dr, dc in dirs:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            heapq.heappush(pq, (grid[nr][nc], nr, nc))
            visited.add((nr, nc))
            
    while pq:
        s, r, c = heapq.heappop(pq)
        
        # Check if this cell is still valid (not absorbed yet)
        # Since we only push each cell once, if it's in PQ, it hasn't been absorbed.
        # However, we might have added it, then absorbed it? No, we only absorb when popping.
        # Wait, could we have added the same cell twice? No, `visited` prevents that.
        # So if we pop it, it's a valid adjacent cell.
        
        # Condition: s * X < current_strength
        if s * X < current_strength:
            # Absorb
            current_strength += s
            # Mark as absorbed (remove from visited? No, just don't add back)
            # Actually, we can just leave it in visited, it won't be added again.
            # But we need to add its neighbors.
            
            # Find neighbors of (r, c)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if (nr, nc) not in visited:
                        heapq.heappush(pq, (grid[nr][nc], nr, nc))
                        visited.add((nr, nc))
        else:
            # Cannot absorb the smallest neighbor.
            # Since PQ is sorted, no other neighbor can be absorbed.
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()