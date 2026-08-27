import sys

MOD = 998244353

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    H = int(input_data[idx]); idx += 1
    W = int(input_data[idx]); idx += 1
    
    # Read grid values into a flat list for O(1) access
    grid = [0] * (H * W)
    for i in range(H * W):
        grid[i] = int(input_data[idx]); idx += 1
    
    Q = int(input_data[idx]); idx += 1
    sh = int(input_data[idx]); idx += 1
    sw = int(input_data[idx]); idx += 1
    
    # Precompute factorials up to H+W
    N = H + W + 5
    fact = [1] * N
    for i in range(1, N):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * N
    inv_fact[N-1] = pow(fact[N-1], MOD-2, MOD)
    for i in range(N-2, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
    
    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD
    
    # Precompute weights for all cells using 0-indexed positions
    weights = [0] * (H * W)
    for h in range(H):
        for w in range(W):
            # number of ways from (1,1) to (h+1, w+1) is C(h+w, h)
            # number of ways from (h+1, w+1) to (H,W) is C((H-1-h)+(W-1-w), H-1-h)
            a = C(h + w, h)
            b = C((H - 1 - h) + (W - 1 - w), H - 1 - h)
            weights[h * W + w] = a * b % MOD
    
    # Compute initial total sum
    total = 0
    for i in range(H * W):
        total = (total + grid[i] * weights[i]) % MOD
    
    # Current position (0-indexed)
    cur_h = sh - 1
    cur_w = sw - 1
    
    out = []
    for _ in range(Q):
        d = input_data[idx]; idx += 1
        a = int(input_data[idx]); idx += 1
        
        # Move in the given direction
        if d == 'L':
            cur_w -= 1
        elif d == 'R':
            cur_w += 1
        elif d == 'U':
            cur_h -= 1
        elif d == 'D':
            cur_h += 1
        
        # Update the cell value
        pos = cur_h * W + cur_w
        w_val = weights[pos]
        old_val = grid[pos]
        # Subtract old contribution, add new contribution
        total = (total - old_val * w_val) % MOD
        total = (total + a * w_val) % MOD
        # Update grid
        grid[pos] = a
        
        out.append(str(total % MOD))
    
    print('\n'.join(out))

if __name__ == "__main__":
    main()