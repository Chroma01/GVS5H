import sys

# Set recursion limit just in case, though we use iterative DP
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    H = int(next(iterator))
    W = int(next(iterator))
    
    # Read the grid A
    # A is 1-indexed in problem, we'll use 0-indexed internally
    # A[h][w] corresponds to row h, column w (0-indexed)
    A = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(next(iterator)))
        A.append(row)
        
    Q = int(next(iterator))
    sh = int(next(iterator)) - 1  # Convert to 0-indexed
    sw = int(next(iterator)) - 1  # Convert to 0-indexed
    
    # Current position of Takahashi
    curr_h, curr_w = sh, sw
    
    MOD = 998244353
    
    # Initialize DP table
    # dp[h][w] = sum of products of all paths from (0,0) to (h,w)
    # dp[0][0] = A[0][0]
    # dp[h][w] = A[h][w] * (dp[h-1][w] + dp[h][w-1]) if h>0 and w>0
    #            = A[h][w] * dp[h-1][w] if h>0 and w==0
    #            = A[h][w] * dp[h][w-1] if h==0 and w>0
    
    dp = [[0] * W for _ in range(H)]
    
    # Base case
    dp[0][0] = A[0][0] % MOD
    
    # Fill first row
    for j in range(1, W):
        dp[0][j] = (dp[0][j-1] * A[0][j]) % MOD
        
    # Fill first column
    for i in range(1, H):
        dp[i][0] = (dp[i-1][0] * A[i][0]) % MOD
        
    # Fill the rest of the DP table
    for i in range(1, H):
        for j in range(1, W):
            dp[i][j] = (A[i][j] * (dp[i-1][j] + dp[i][j-1])) % MOD
            
    # Process queries
    output = []
    
    for _ in range(Q):
        d = next(iterator)
        a_val = int(next(iterator))
        
        # Move Takahashi
        if d == 'L':
            curr_w -= 1
        elif d == 'R':
            curr_w += 1
        elif d == 'U':
            curr_h -= 1
        elif d == 'D':
            curr_h += 1
            
        # Update the grid value
        old_val = A[curr_h][curr_w]
        A[curr_h][curr_w] = a_val
        
        # If the updated cell is (0,0), we need to recompute everything
        # But generally, we only need to recompute the affected subgrid
        # Affected cells are those (i,j) such that i >= curr_h and j >= curr_w
        
        # Recompute dp[curr_h][curr_w] first
        # It depends on dp[curr_h-1][curr_w] and dp[curr_h][curr_w-1]
        # These are not affected if we process in topological order
        
        # Compute new dp[curr_h][curr_w]
        val = 0
        if curr_h > 0:
            val = (val + dp[curr_h-1][curr_w]) % MOD
        if curr_w > 0:
            val = (val + dp[curr_h][curr_w-1]) % MOD
        dp[curr_h][curr_w] = (A[curr_h][curr_w] * val) % MOD
        
        # Now propagate changes to all descendants
        # We iterate over i from curr_h to H-1, and j from curr_w to W-1
        # But we must skip (curr_h, curr_w) itself as it's already updated
        # And we must process in topological order (row by row, then column by column)
        
        for i in range(curr_h, H):
            for j in range(curr_w, W):
                if i == curr_h and j == curr_w:
                    continue
                    
                val = 0
                if i > 0:
                    val = (val + dp[i-1][j]) % MOD
                if j > 0:
                    val = (val + dp[i][j-1]) % MOD
                dp[i][j] = (A[i][j] * val) % MOD
                
        output.append(str(dp[H-1][W-1]))
        
    print('\n'.join(output))

solve()