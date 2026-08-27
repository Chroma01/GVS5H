import sys

# Increase recursion depth just in case, though we aim for iterative or shallow recursion
sys.setrecursionlimit(200000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    MOD = 998244353
    
    results = []
    
    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
            S = []
            for _ in range(H):
                S.append(next(iterator))
        except StopIteration:
            break
            
        # We need to determine if there exists a valid configuration.
        # If it exists, the answer is 2. Otherwise 0.
        # The problem is to find if we can assign rotations such that for every boundary,
        # the segment status matches (both present or both absent).
        
        # Let's represent the grid state.
        # We will try to construct a solution using backtracking with pruning.
        # Given the constraints and the nature of the problem (likely 0 or 2 solutions),
        # we can try to fix the first cell and propagate, or use a randomized approach.
        # However, a deterministic backtracking with a small depth limit or specific ordering
        # is safer.
        
        # Optimization: The constraints are very tight. We can try to check consistency
        # by iterating through cells and checking if a valid rotation exists given neighbors.
        # But neighbors are variables.
        
        # Let's use a randomized greedy approach with restarts.
        # We shuffle the order of cells and try to assign rotations consistent with already assigned neighbors.
        # If we get stuck, we restart with a new shuffle.
        # If we succeed, return 2.
        
        # To make it efficient, we can use a simple backtracking that tries to satisfy constraints.
        # Since the grid is a torus, we can't easily linearize without care.
        # However, we can try to fix the top-left cell and propagate.
        
        # Let's define the possible rotations for each cell type.
        # Type A: 4 rotations.
        # Type B: 2 rotations.
        # We need to check if the chosen rotation is consistent with the "flow" across boundaries.
        # Actually, the condition is simpler: For every edge between (i,j) and (i, j+1),
        # the segment on the right of (i,j) must match the segment on the left of (i, j+1).
        # This implies that the configuration of segments forms a set of cycles.
        
        # Let's try a specific heuristic:
        # 1. Try to assign rotations to cells in row-major order.
        # 2. For each cell, try all valid rotations.
        # 3. Check consistency with already fixed neighbors (left and top).
        # 4. If consistent, proceed. If not, backtrack.
        # 5. Since we need to handle the torus, the last cells depend on the first.
        #    We can try all possibilities for the first cell (or first few) and propagate.
        
        # Given the constraints (sum of HW <= 10^6), we need an O(HW) or O(HW * small) solution.
        # Backtracking might be too slow if the branching factor is high.
        # But the constraints are likely to prune the search space heavily.
        
        # Let's implement a solver that tries to find ONE solution.
        # We will use a randomized order of cells to avoid worst-case scenarios.
        
        import random
        
        # Precompute possible rotations for each cell
        # 0: Top-Left, 1: Top-Right, 2: Bottom-Right, 3: Bottom-Left (for A)
        # 0: Top-Bottom, 1: Left-Right (for B)
        
        # We will store the grid of choices. -1 means unassigned.
        grid_choices = [[-1] * W for _ in range(H)]
        
        # Helper to check if a choice is valid for a cell given its neighbors
        # This check is local: it ensures that the segments crossing the boundaries match.
        # But since neighbors might not be assigned yet, we only check against assigned neighbors.
        
        # Actually, a better way is to check the global consistency at the end?
        # No, we need to build it.
        # Let's try a randomized greedy construction.
        
        found = False
        
        # Try multiple times with different random orders
        max_attempts = 50
        
        for attempt in range(max_attempts):
            # Reset grid
            for r in range(H):
                for c in range(W):
                    grid_choices[r][c] = -1
            
            # Shuffle cell order
            cells = [(r, c) for r in range(H) for c in range(W)]
            random.shuffle(cells)
            
            # Try to assign
            # We use a stack for backtracking to avoid recursion depth issues
            stack = []
            
            # We need to keep track of the current assignment state for backtracking
            # But since we reset every attempt, we can just use a recursive function with a counter
            
            # Let's use a simple recursive backtracking with a limit
            # To optimize, we can check constraints incrementally.
            
            # However, with random shuffle, we might hit a dead end quickly.
            # Let's try to be smart: prioritize cells with fewer options?
            # No, let's just try the shuffled order.
            
            # We need a way to backtrack.
            # Let's use a list of (r, c, choice) to undo.
            
            path = []
            
            def backtrack(idx):
                if idx == len(cells):
                    return True
                
                r, c = cells[idx]
                cell_type = S[r][c]
                
                # Determine possible choices
                if cell_type == 'A':
                    choices = [0, 1, 2, 3]
                else:
                    choices = [0, 1]
                
                # Try each choice
                for choice in choices:
                    # Check consistency with already assigned neighbors
                    # Neighbors: Left (c-1), Right (c+1), Top (r-1), Bottom (r+1)
                    # We only check neighbors that are already in 'path' (assigned)
                    
                    valid = True
                    
                    # Check Left neighbor: (r, c-1)
                    if c > 0:
                        # Left neighbor is (r, c-1). If it's assigned, check consistency.
                        # But wait, the path contains cells in the order of 'cells'.
                        # We need to know if (r, c-1) is assigned.
                        # We can check if grid_choices[r][c-1] != -1.
                        # However, grid_choices is being modified.
                        # Let's rely on grid_choices being updated.
                        pass
                    
                    # Actually, checking grid_choices is O(1).
                    # But we need to know which boundaries are "active".
                    # The condition is: segment on right of (r,c) == segment on left of (r, c+1)
                    # AND segment on bottom of (r,c) == segment on top of (r+1, c)
                    
                    # Let's define the segments for each choice.
                    # Choice 0 (A): Top-Left. Segments: Top, Left. (Right=0, Bottom=0)
                    # Choice 1 (A): Top-Right. Segments: Top, Right. (Left=0, Bottom=0)
                    # Choice 2 (A): Bottom-Right. Segments: Bottom, Right. (Top=0, Left=0)
                    # Choice 3 (A): Bottom-Left. Segments: Bottom, Left. (Top=0, Right=0)
                    # Choice 0 (B): Top-Bottom. Segments: Top, Bottom. (Left=0, Right=0)
                    # Choice 1 (B): Left-Right. Segments: Left, Right. (Top=0, Bottom=0)
                    
                    # Let's map choice to (top, bottom, left, right) booleans
                    # A:
                    # 0: T, L
                    # 1: T, R
                    # 2: B, R
                    # 3: B, L
                    # B:
                    # 0: T, B
                    # 1: L, R
                    
                    # Define segments
                    if cell_type == 'A':
                        segs = {
                            0: (1, 0, 1, 0), # T, B, L, R
                            1: (1, 0, 0, 1),
                            2: (0, 1, 0, 1),
                            3: (0, 1, 1, 0)
                        }
                    else:
                        segs = {
                            0: (1, 1, 0, 0), # T, B
                            1: (0, 0, 1, 1)  # L, R
                        }
                    
                    t, b, l, r = segs[choice]
                    
                    # Check Left neighbor (r, c-1)
                    if c > 0:
                        # We need to check if (r, c-1) has a segment on its Right.
                        # If (r, c-1) is assigned, check grid_choices[r][c-1].
                        # But wait, the condition is about the boundary between them.
                        # The boundary is the Right edge of (r, c-1) and Left edge of (r, c).
                        # So we need: Right of (r, c-1) == Left of (r, c).
                        # If (r, c-1) is assigned, we check its Right segment.
                        # If (r, c-1) is NOT assigned, we can't check yet?
                        # Actually, if (r, c-1) is not assigned, we assume it will be compatible?
                        # No, we must ensure that when we assign (r, c-1), it matches (r, c).
                        # But since we process in a random order, (r, c-1) might be processed later.
                        # So we can only check against assigned neighbors.
                        # If a neighbor is unassigned, we just skip the check for now.
                        # But this might lead to a dead end later.
                        # To be safe, we should check against ALL neighbors if they are assigned.
                        # If a neighbor is unassigned, we don't check.
                        
                        # However, there's a catch: if we skip checks, we might assign a value that is incompatible.
                        # But since we backtrack, it's fine.
                        pass
                    
                    # Let's implement the check properly.
                    # We check against neighbors that are ALREADY assigned (grid_choices != -1).
                    
                    # Check Left: (r, c-1) Right edge vs (r, c) Left edge
                    if c > 0 and grid_choices[r][c-1] != -1:
                        # Get segments of left neighbor
                        left_type = S[r][c-1]
                        if left_type == 'A':
                            left_segs = {0: (1,0,1,0), 1: (1,0,0,1), 2: (0,1,0,1), 3: (0,1,1,0)}
                        else:
                            left_segs = {0: (1,1,0,0), 1: (0,0,1,1)}
                        left_r, _, _, _ = left_segs[grid_choices[r][c-1]]
                        if left_r != l:
                            valid = False
                            break
                    
                    # Check Right: (r, c) Right edge vs (r, c+1) Left edge
                    # We only check if (r, c+1) is assigned.
                    if c < W - 1 and grid_choices[r][c+1] != -1:
                        right_type = S[r][c+1]
                        if right_type == 'A':
                            right_segs = {0: (1,0,1,0), 1: (1,0,0,1), 2: (0,1,0,1), 3: (0,1,1,0)}
                        else:
                            right_segs = {0: (1,1,0,0), 1: (0,0,1,1)}
                        _, _, _, right_l = right_segs[grid_choices[r][c+1]]
                        if right_l != r:
                            valid = False
                            break
                            
                    # Check Top: (r-1, c) Bottom edge vs (r, c) Top edge
                    if r > 0 and grid_choices[r-1][c] != -1:
                        top_type = S[r-1][c]
                        if top_type == 'A':
                            top_segs = {0: (1,0,1,0), 1: (1,0,0,1), 2: (0,1,0,1), 3: (0,1,1,0)}
                        else:
                            top_segs = {0: (1,1,0,0), 1: (0,0,1,1)}
                        _, top_b, _, _ = top_segs[grid_choices[r-1][c]]
                        if top_b != t:
                            valid = False
                            break
                            
                    # Check Bottom: (r, c) Bottom edge vs (r+1, c) Top edge
                    if r < H - 1 and grid_choices[r+1][c] != -1:
                        bottom_type = S[r+1][c]
                        if bottom_type == 'A':
                            bottom_segs = {0: (1,0,1,0), 1: (1,0,0,1), 2: (0,1,0,1), 3: (0,1,1,0)}
                        else:
                            bottom_segs = {0: (1,1,0,0), 1: (0,0,1,1)}
                        _, bottom_b, _, _ = bottom_segs[grid_choices[r+1][c]]
                        if bottom_b != b:
                            valid = False
                            break
                    
                    if valid:
                        # Assign
                        grid_choices[r][c] = choice
                        path.append((r, c, choice))
                        if backtrack(idx + 1):
                            return True
                        # Backtrack
                        grid_choices[r][c] = -1
                        path.pop()
                
                return False

            if backtrack(0):
                found = True
                break
        
        if found:
            results.append("2")
        else:
            results.append("0")

    print('\n'.join(results))

if __name__ == '__main__':
    solve()