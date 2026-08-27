import sys

# Increase recursion depth just in case, though this solution is iterative.
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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
    # We store A as a list of lists.
    # Constraints: HW <= 200,000, so this fits in memory.
    A = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(int(next(iterator)))
        A.append(row)

    # Precompute factorials and inverse factorials for nCr calculations
    MOD = 998244353
    # Max value for n in nCr is (H-1) + (W-1) = H + W - 2
    MAX_N = H + W + 5
    
    fact = [1] * MAX_N
    inv = [1] * MAX_N
    
    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Precompute the coefficient C[h][w] for each cell (0-indexed internally)
    # C[h][w] represents the number of paths passing through cell (h, w)
    # from (0,0) to (H-1, W-1).
    # Formula: C[h][w] = (paths from (0,0) to (h,w)) * (paths from (h,w) to (H-1,W-1))
    # paths to (h,w) = C(h + w, h)
    # paths from (h,w) to (H-1,W-1) = C((H-1-h) + (W-1-w), H-1-h)
    
    C = [[0] * W for _ in range(H)]
    
    for h in range(H):
        for w in range(W):
            # Paths from (0,0) to (h,w)
            # Steps: h down, w right. Total steps: h+w. Choose h downs.
            ways_to = nCr_mod(h + w, h)
            
            # Paths from (h,w) to (H-1,W-1)
            # Steps: (H-1-h) down, (W-1-w) right. Total steps: H+W-2-h-w. Choose H-1-h downs.
            ways_from = nCr_mod(H + W - 2 - h - w, H - 1 - h)
            
            C[h][w] = (ways_to * ways_from) % MOD

    # Calculate initial total sum
    # Total Sum = Sum(A[h][w] * C[h][w]) for all h, w
    total_sum = 0
    for h in range(H):
        for w in range(W):
            term = (A[h][w] * C[h][w]) % MOD
            total_sum = (total_sum + term) % MOD

    # Process queries
    try:
        Q = int(next(iterator))
        sh = int(next(iterator))
        sw = int(next(iterator))
        
        # Convert 1-based coordinates to 0-based
        current_pos_h = sh - 1
        current_pos_w = sw - 1
        
        results = []
        
        for _ in range(Q):
            d = next(iterator)
            a_val = int(next(iterator))
            
            # Update position based on direction
            if d == 'L':
                current_pos_w -= 1
            elif d == 'R':
                current_pos_w += 1
            elif d == 'U':
                current_pos_h -= 1
            elif d == 'D':
                current_pos_h += 1
            
            # The problem states: "Move one cell... Then set A_{h,w} to a_i".
            # So the update happens at the new position.
            h, w = current_pos_h, current_pos_w
            
            # Get old value
            old_val = A[h][w]
            
            # Calculate change in total sum
            # New contribution: a_val * C[h][w]
            # Old contribution: old_val * C[h][w]
            # Delta = (a_val - old_val) * C[h][w]
            
            diff = (a_val - old_val) % MOD
            term_change = (diff * C[h][w]) % MOD
            
            total_sum = (total_sum + term_change) % MOD
            
            # Update grid
            A[h][w] = a_val
            
            results.append(str(total_sum))
            
        print('\n'.join(results))
        
    except StopIteration:
        pass

if __name__ == '__main__':
    solve()