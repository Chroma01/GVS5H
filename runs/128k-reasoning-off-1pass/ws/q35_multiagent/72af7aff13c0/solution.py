import sys

def solve():
    # Increase recursion depth just in case, though we use iterative DP
    sys.setrecursionlimit(300000)
    
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read the grid A
    # A is 1-indexed in problem, we'll use 0-indexed internally
    # A[h][w] corresponds to row h, col w
    A = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(int(next(iterator)))
        A.append(row)
        
    try:
        Q = int(next(iterator))
        sh = int(next(iterator))
        sw = int(next(iterator))
    except StopIteration:
        Q = 0
        sh = 1
        sw = 1
        
    # Ensure H <= W for better performance in updates
    # If H > W, we transpose the grid
    transposed = False
    if H > W:
        H, W = W, H
        new_A = [[0] * H for _ in range(W)]
        for r in range(H):
            for c in range(W):
                new_A[c][r] = A[r][c]
        A = new_A
        transposed = True
        
    # Current position of Takahashi (1-indexed in input)
    # Convert to 0-indexed
    curr_r = sh - 1
    curr_c = sw - 1
    
    MOD = 998244353
    
    # Precompute DP table
    # DP[r][c] = sum of products of paths from (0,0) to (r,c)
    # DP[r][c] = A[r][c] * (DP[r-1][c] + DP[r][c-1])
    
    # Initialize DP table
    DP = [[0] * W for _ in range(H)]
    
    # Base case
    DP[0][0] = A[0][0] % MOD
    
    # Fill first row
    for c in range(1, W):
        DP[0][c] = (DP[0][c-1] * A[0][c]) % MOD
        
    # Fill first column
    for r in range(1, H):
        DP[r][0] = (DP[r-1][0] * A[r][0]) % MOD
        
    # Fill rest of the table
    for r in range(1, H):
        for c in range(1, W):
            DP[r][c] = (A[r][c] * (DP[r-1][c] + DP[r][c-1])) % MOD
            
    # Process queries
    results = []
    
    for _ in range(Q):
        d = next(iterator)
        a_val = int(next(iterator))
        
        # Determine new position
        nr, nc = curr_r, curr_c
        if d == 'L':
            nc -= 1
        elif d == 'R':
            nc += 1
        elif d == 'U':
            nr -= 1
        elif d == 'D':
            nr += 1
            
        # Update position
        curr_r, curr_c = nr, nc
        
        # Update A[nr][nc] to a_val
        old_val = A[nr][nc]
        A[nr][nc] = a_val
        
        # Recompute the affected rectangle: rows nr to H-1, cols nc to W-1
        # We iterate in topological order (row by row, then column by column)
        
        # For row nr, start from col nc
        # For rows > nr, start from col nc
        
        # We can optimize by noting that for row nr, if nc > 0, DP[nr][nc-1] is unchanged.
        # If nc == 0, then DP[nr][0] depends only on DP[nr-1][0] which is unchanged (since nr > 0 or if nr=0, handled below).
        
        # Let's just recompute the entire affected rectangle from scratch.
        # This is O((H-nr)*(W-nc)) which is at most O(HW).
        # Given H <= sqrt(200000) ~ 450, this is often fast enough.
        
        for r in range(nr, H):
            for c in range(nc, W):
                if r == 0 and c == 0:
                    DP[0][0] = A[0][0] % MOD
                elif r == 0:
                    DP[0][c] = (DP[0][c-1] * A[0][c]) % MOD
                elif c == 0:
                    DP[r][0] = (DP[r-1][0] * A[r][0]) % MOD
                else:
                    DP[r][c] = (A[r][c] * (DP[r-1][c] + DP[r][c-1])) % MOD
                    
        # The answer is DP[H-1][W-1]
        results.append(str(DP[H-1][W-1]))
        
    print('\n'.join(results))

solve()