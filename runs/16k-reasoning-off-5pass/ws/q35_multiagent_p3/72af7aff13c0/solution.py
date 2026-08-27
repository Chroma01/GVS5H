import sys

# Set recursion limit just in case, though we will use iterative DP
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read the grid
    # We will store the grid as a 1D list or 2D list.
    # Given HW <= 200,000, we can use a 2D list if one dimension is small.
    # To optimize, we ensure H <= W by transposing if necessary.
    # This way, H is at most sqrt(200,000) ~ 447.
    
    grid = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(int(next(iterator)))
        grid.append(row)

    try:
        Q = int(next(iterator))
        sh = int(next(iterator))
        sw = int(next(iterator))
    except StopIteration:
        Q = 0
        sh = 1
        sw = 1

    # Check if we need to transpose
    # We want H to be the smaller dimension for efficient DP updates
    # If H > W, transpose the grid
    transposed = False
    if H > W:
        # Transpose the grid
        new_grid = [[0] * H for _ in range(W)]
        for r in range(H):
            for c in range(W):
                new_grid[c][r] = grid[r][c]
        grid = new_grid
        H, W = W, H
        # Adjust starting position
        sh, sw = sw, sh
        transposed = True

    # Now H <= W and H * W <= 200,000
    # H is small (<= 447)
    
    MOD = 998244353

    # dp[r][c] will store the sum of products of paths from (0,0) to (r,c)
    # We use 0-indexed internally.
    # dp[r][c] = grid[r][c] * (dp[r-1][c] + dp[r][c-1])
    
    # Initialize DP table
    dp = [[0] * W for _ in range(H)]
    
    # Base case
    dp[0][0] = grid[0][0] % MOD
    
    # Fill the first row
    for c in range(1, W):
        dp[0][c] = (dp[0][c-1] * grid[0][c]) % MOD
        
    # Fill the first column
    for r in range(1, H):
        dp[r][0] = (dp[r-1][0] * grid[r][0]) % MOD
        
    # Fill the rest of the DP table
    for r in range(1, H):
        for c in range(1, W):
            dp[r][c] = (grid[r][c] * (dp[r-1][c] + dp[r][c-1])) % MOD

    # Function to update the DP table after a change in grid[r][c]
    # Since H is small, we can recompute the affected part of the DP table.
    # The affected part is from (r,c) to (H-1, W-1).
    # However, recomputing the entire subgrid might still be O(HW) in worst case.
    # But since H is small, we can optimize by processing row by row.
    
    # Actually, if we change grid[r][c], we need to update dp[r][c] and then propagate.
    # The propagation is:
    # dp[r][c] depends on dp[r-1][c] and dp[r][c-1].
    # dp[r][c+1] depends on dp[r-1][c+1] and dp[r][c].
    # dp[r+1][c] depends on dp[r][c] and dp[r+1][c-1].
    
    # We can recompute the DP table starting from (r,c).
    # But we must be careful: if we recompute row by row, we need to ensure that
    # when we compute dp[i][j], dp[i-1][j] and dp[i][j-1] are already up-to-date.
    
    # Since we only changed one cell, we can recompute the DP table from (r,c) onwards.
    # But this is still O(HW) in the worst case.
    
    # However, note that H is small. So O(HW) is acceptable if we do it efficiently.
    # But Q is up to 200,000, so O(Q * HW) is too slow.
    
    # We need a faster update.
    # Let's think about it differently.
    # The DP is linear. The change in dp[H-1][W-1] can be computed by considering
    # the change in grid[r][c] and its effect on the paths.
    
    # But this is complex.
    
    # Alternative: Since H is small, we can maintain the DP table and update it efficiently.
    # When grid[r][c] changes, we update dp[r][c] and then propagate the change to the right and down.
    # The propagation can be done in O(H * W) in the worst case, but we can optimize by only
    # recomputing the affected cells.
    
    # Actually, if we change grid[r][c], the new dp[r][c] is:
    # new_dp[r][c] = new_grid[r][c] * (dp[r-1][c] + dp[r][c-1])
    # Then, for each cell (i,j) with i>=r and j>=c, we can update dp[i][j] if it depends on the changed values.
    
    # But this is still O(HW) in the worst case.
    
    # Let's try to implement the O(HW) per query solution and see if it passes in Python.
    # If not, we need a more efficient method.
    
    # Given the constraints and the fact that H is small, we can try to optimize the update.
    # We can recompute the DP table row by row starting from row r.
    # For row r, we recompute from column c to W-1.
    # For rows i > r, we recompute the entire row.
    
    # This is O(H * W) in the worst case.
    
    # But wait, if H is small, say H=447, and W=447, then HW=200,000.
    # Q=200,000, so total operations are 4e10, which is too slow for Python.
    
    # We need a better approach.
    
    # Let's use the fact that the DP is linear and the change propagates.
    # We can compute the change in dp[H-1][W-1] by considering the change in grid[r][c].
    # The change in dp[r][c] is delta = (new_grid[r][c] - old_grid[r][c]) * (dp[r-1][c] + dp[r][c-1])
    # Then, this change propagates to the right and down.
    
    # The propagation to the right:
    # dp[r][c+1] changes by delta * grid[r][c+1]
    # dp[r][c+2] changes by delta * grid[r][c+1] * grid[r][c+2]
    # ...
    
    # The propagation down:
    # dp[r+1][c] changes by delta * grid[r+1][c]
    # dp[r+2][c] changes by delta * grid[r+1][c] * grid[r+2][c]
    # ...
    
    # But the propagation is 2D, so it's more complex.
    
    # Actually, we can use a BFS to compute the changes.
    # But this is still O(HW) in the worst case.
    
    # Given the time constraints, let's implement the O(HW) per query solution with optimizations.
    # We will recompute the DP table from (r,c) onwards.
    
    # To speed up, we can use a 1D array for the current row and update it.
    
    # Let's implement the update function.
    
    def update_dp(r, c, new_val):
        nonlocal dp, grid
        grid[r][c] = new_val
        
        # Recompute dp[r][c]
        prev = 0
        if r > 0:
            prev += dp[r-1][c]
        if c > 0:
            prev += dp[r][c-1]
        dp[r][c] = (new_val * prev) % MOD
        
        # Propagate to the right in the same row
        for j in range(c+1, W):
            prev = dp[r][j-1]
            if r > 0:
                prev += dp[r-1][j]
            dp[r][j] = (grid[r][j] * prev) % MOD
            
        # Propagate to the subsequent rows
        for i in range(r+1, H):
            # Recompute the entire row i
            # First element of the row
            prev = dp[i-1][0]
            if i > 1:
                # dp[i][0] depends on dp[i-1][0] and dp[i][0-1] which is 0
                # So dp[i][0] = grid[i][0] * dp[i-1][0]
                pass
            dp[i][0] = (grid[i][0] * dp[i-1][0]) % MOD
            
            for j in range(1, W):
                prev = dp[i-1][j] + dp[i][j-1]
                dp[i][j] = (grid[i][j] * prev) % MOD

    # Process queries
    results = []
    
    for _ in range(Q):
        try:
            d = next(iterator)
            a = int(next(iterator))
        except StopIteration:
            break
            
        # Move Takahashi
        if d == 'L':
            sw -= 1
        elif d == 'R':
            sw += 1
        elif d == 'U':
            sh -= 1
        elif d == 'D':
            sh += 1
            
        # Convert to 0-indexed
        r, c = sh - 1, sw - 1
        
        # Update the grid and DP table
        update_dp(r, c, a)
        
        # The answer is dp[H-1][W-1]
        results.append(str(dp[H-1][W-1]))
        
    print('\n'.join(results))

solve()