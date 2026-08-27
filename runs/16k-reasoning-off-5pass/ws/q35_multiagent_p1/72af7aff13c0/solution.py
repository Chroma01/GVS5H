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

    # Read the grid A
    # A is 1-indexed in problem, we'll use 0-indexed internally for storage
    # but keep logic clear. Let's use 0-indexed arrays of size H x W.
    # A[h][w] corresponds to row h+1, col w+1.
    
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

    # Directions mapping
    dir_map = {
        'L': (0, -1),
        'R': (0, 1),
        'U': (-1, 0),
        'D': (1, 0)
    }
    
    # Current position of Takahashi (1-indexed)
    curr_r = sh
    curr_c = sw
    
    MOD = 998244353
    
    # Precompute Down DP table
    # Down[h][w] = sum of products of paths from (0,0) to (h,w)
    # Down[h][w] = A[h][w] * (Down[h-1][w] + Down[h][w-1])
    Down = [[0] * W for _ in range(H)]
    
    # Initialize (0,0)
    Down[0][0] = A[0][0] % MOD
    
    for r in range(H):
        for c in range(W):
            if r == 0 and c == 0:
                continue
            
            val = 0
            if r > 0:
                val = (val + Down[r-1][c]) % MOD
            if c > 0:
                val = (val + Down[r][c-1]) % MOD
            
            Down[r][c] = (val * A[r][c]) % MOD

    # Precompute Up DP table
    # Up[h][w] = sum of products of paths from (h,w) to (H-1, W-1)
    # Up[h][w] = A[h][w] * (Up[h+1][w] + Up[h][w+1])
    Up = [[0] * W for _ in range(H)]
    
    # Initialize (H-1, W-1)
    Up[H-1][W-1] = A[H-1][W-1] % MOD
    
    for r in range(H-1, -1, -1):
        for c in range(W-1, -1, -1):
            if r == H-1 and c == W-1:
                continue
            
            val = 0
            if r < H-1:
                val = (val + Up[r+1][c]) % MOD
            if c < W-1:
                val = (val + Up[r][c+1]) % MOD
            
            Up[r][c] = (val * A[r][c]) % MOD

    # Precompute Pre and Suf tables
    # Pre[r][c] = Down[r-1][c] + Down[r][c-1]
    # Suf[r][c] = Up[r+1][c] + Up[r][c+1]
    
    Pre = [[0] * W for _ in range(H)]
    Suf = [[0] * W for _ in range(H)]
    
    for r in range(H):
        for c in range(W):
            p_val = 0
            if r > 0:
                p_val = (p_val + Down[r-1][c]) % MOD
            if c > 0:
                p_val = (p_val + Down[r][c-1]) % MOD
            Pre[r][c] = p_val
            
            s_val = 0
            if r < H-1:
                s_val = (s_val + Up[r+1][c]) % MOD
            if c < W-1:
                s_val = (s_val + Up[r][c+1]) % MOD
            Suf[r][c] = s_val

    # Compute initial total sum
    # Total = sum(Pre[r][c] * A[r][c] * Suf[r][c]) for all r, c
    total_sum = 0
    for r in range(H):
        for c in range(W):
            term = (Pre[r][c] * A[r][c]) % MOD
            term = (term * Suf[r][c]) % MOD
            total_sum = (total_sum + term) % MOD

    results = []
    
    for _ in range(Q):
        d = next(iterator)
        a_new = int(next(iterator))
        
        # Move Takahashi
        dr, dc = dir_map[d]
        curr_r += dr
        curr_c += dc
        
        # Convert to 0-indexed for array access
        r_idx = curr_r - 1
        c_idx = curr_c - 1
        
        a_old = A[r_idx][c_idx]
        
        # Update total sum
        # Change in A is (a_new - a_old)
        # Contribution change is (a_new - a_old) * Pre[r][c] * Suf[r][c]
        
        diff = (a_new - a_old) % MOD
        change = (diff * Pre[r_idx][c_idx]) % MOD
        change = (change * Suf[r_idx][c_idx]) % MOD
        
        total_sum = (total_sum + change) % MOD
        
        # Update A
        A[r_idx][c_idx] = a_new
        
        results.append(str(total_sum))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()