import sys

# Increase recursion depth just in case, though we use iterative approach
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

    # Grid A is 0-indexed internally
    # We read H rows, each with W integers
    A = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(iterator)))
        A.append(row)
    
    MOD = 998244353
    
    # Read Q, sh, sw
    Q = int(next(iterator))
    sh = int(next(iterator)) - 1 # 0-indexed
    sw = int(next(iterator)) - 1 # 0-indexed
    
    # Read queries
    queries = []
    for _ in range(Q):
        d = next(iterator)
        a = int(next(iterator))
        queries.append((d, a))
        
    # DP Arrays
    # dp1[h][w]: sum of products from (0,0) to (h,w)
    # dp2[h][w]: sum of products from (h,w) to (H-1, W-1)
    
    # Initialize dp1
    dp1 = [[0] * W for _ in range(H)]
    dp1[0][0] = A[0][0]
    for i in range(H):
        for j in range(W):
            if i == 0 and j == 0:
                continue
            val = A[i][j]
            up = dp1[i-1][j] if i > 0 else 0
            left = dp1[i][j-1] if j > 0 else 0
            dp1[i][j] = val * (up + left) % MOD
            
    # Initialize dp2
    dp2 = [[0] * W for _ in range(H)]
    dp2[H-1][W-1] = A[H-1][W-1]
    for i in range(H-1, -1, -1):
        for j in range(W-1, -1, -1):
            if i == H-1 and j == W-1:
                continue
            val = A[i][j]
            down = dp2[i+1][j] if i < H-1 else 0
            right = dp2[i][j+1] if j < W-1 else 0
            dp2[i][j] = val * (down + right) % MOD
            
    # Process queries
    # We maintain the current total sum as dp1[H-1][W-1]
    # For each query, we update A[sh][sw], then update dp1 and dp2 tables
    # The update takes O(H+W) in the worst case (propagating along rows/cols)
    # However, since HW <= 200,000, the number of cells in the affected cone is at most 200,000.
    
    output = []
    
    for d, a in queries:
        # Determine direction and update coordinates
        # d is 'L', 'R', 'U', 'D'
        # But the problem says "Move one cell in the direction d_i... Then set A_{h,w} to a_i"
        # So we need to find the NEW (sh, sw) based on the move from the CURRENT (sh, sw).
        
        # Current position is (sh, sw)
        # Move direction d
        # New position (nsh, nsw)
        
        if d == 'L':
            nsh, nsw = sh, sw - 1
        elif d == 'R':
            nsh, nsw = sh, sw + 1
        elif d == 'U':
            nsh, nsw = sh - 1, sw
        elif d == 'D':
            nsh, nsw = sh + 1, sw
            
        # Update A[nsh][nsw]
        old_val = A[nsh][nsw]
        new_val = a
        A[nsh][nsw] = new_val
        
        # Calculate the change in the total sum
        # The total sum is dp1[H-1][W-1].
        # The contribution of paths passing through (nsh, nsw) is:
        # (dp1[nsh-1][nsw] + dp1[nsh][nsw-1]) * old_val * (dp2[nsh+1][nsw] + dp2[nsh][nsw+1])
        # Let L = dp1[nsh-1][nsw] + dp1[nsh][nsw-1]
        # Let R = dp2[nsh+1][nsw] + dp2[nsh][nsw+1]
        # Old contribution = L * old_val * R
        # New contribution = L * new_val * R
        # Change = L * (new_val - old_val) * R
        
        # Note: We must use the OLD dp1 and dp2 values to calculate L and R.
        # Because L depends on cells before (nsh, nsw) which are NOT affected by A[nsh][nsw] change.
        # And R depends on cells after (nsh, nsw) which are NOT affected by A[nsh][nsw] change.
        
        L = 0
        if nsh > 0:
            L = (L + dp1[nsh-1][nsw]) % MOD
        if nsw > 0:
            L = (L + dp1[nsh][nsw-1]) % MOD
            
        R = 0
        if nsh < H-1:
            R = (R + dp2[nsh+1][nsw]) % MOD
        if nsw < W-1:
            R = (R + dp2[nsh][nsw+1]) % MOD
            
        delta = (new_val - old_val) % MOD
        change = (L * delta) % MOD * R % MOD
        
        # Update total sum
        dp1[H-1][W-1] = (dp1[H-1][W-1] + change) % MOD
        
        # Now update dp1 table for the cone (nsh, nsw) to (H-1, W-1)
        # We iterate i from nsh to H-1, j from nsw to W-1
        # But we must be careful: dp1[i][j] depends on dp1[i-1][j] and dp1[i][j-1].
        # If i == nsh and j == nsw, we use the new A[nsh][nsw].
        # If i > nsh or j > nsw, we use the updated values from the current iteration.
        
        # Optimization: If H is large and W is small, or vice versa, we can optimize the loops.
        # But the constraints HW <= 200,000 ensure that the number of iterations is at most 200,000.
        
        # Update dp1
        for i in range(nsh, H):
            for j in range(nsw, W):
                if i == nsh and j == nsw:
                    # First cell in the cone, use new A
                    val = new_val
                else:
                    val = A[i][j]
                
                up = dp1[i-1][j] if i > 0 else 0
                left = dp1[i][j-1] if j > 0 else 0
                dp1[i][j] = val * (up + left) % MOD
                
        # Update dp2 table for the cone (nsh, nsw) to (0, 0)
        # We iterate i from nsh down to 0, j from nsw down to 0
        # dp2[i][j] depends on dp2[i+1][j] and dp2[i][j+1].
        
        for i in range(nsh, -1, -1):
            for j in range(nsw, -1, -1):
                if i == nsh and j == nsw:
                    val = new_val
                else:
                    val = A[i][j]
                
                down = dp2[i+1][j] if i < H-1 else 0
                right = dp2[i][j+1] if j < W-1 else 0
                dp2[i][j] = val * (down + right) % MOD

        output.append(str(dp1[H-1][W-1]))
        
    print('\n'.join(output))

if __name__ == '__main__':
    solve()