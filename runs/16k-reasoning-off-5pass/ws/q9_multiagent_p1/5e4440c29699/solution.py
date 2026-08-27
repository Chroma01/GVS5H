import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    W = int(input_data[0])
    H = int(input_data[1])
    L = int(input_data[2])
    R = int(input_data[3])
    D = int(input_data[4])
    U = int(input_data[5])
    
    MOD = 998244353
    
    # Precompute factorials and inverse factorials for combinations
    # Max value needed is roughly W + H + 2
    MAX_N = W + H + 10
    fact = [1] * (MAX_N + 1)
    inv = [1] * (MAX_N + 1)
    
    for i in range(1, MAX_N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[MAX_N] = pow(fact[MAX_N], MOD - 2, MOD)
    for i in range(MAX_N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD
    
    # Function to calculate sum of paths in a rectangle of width w and height h
    # The number of monotonic paths from any (x1, y1) to (x2, y2) within 
    # the rectangle [0, w] x [0, h] (where 0 <= x1 <= x2 <= w and 0 <= y1 <= y2 <= h)
    # is given by the combinatorial identity: C(w + h + 2, w + 1)
    def count_paths_in_rect(w, h):
        if w < 0 or h < 0:
            return 0
        return nCr(w + h + 2, w + 1)

    # We use the Principle of Inclusion-Exclusion (PIE).
    # A path is valid if it stays in at least one of the following regions:
    # 1. y < D  (Bottom strip)
    # 2. x < L  (Left strip)
    # 3. y > U  (Top strip)
    # 4. x > R  (Right strip)
    #
    # Let P1, P2, P3, P4 be the properties corresponding to these regions.
    # We want to calculate |P1 U P2 U P3 U P4|.
    # By PIE: Sum(|Pi|) - Sum(|Pi n Pj|) + Sum(|Pi n Pj n Pk|) - |P1 n P2 n P3 n P4|
    #
    # For any subset of conditions, the valid region is the intersection of the corresponding intervals.
    # Since the intervals are contiguous, the intersection is either empty or a single rectangle.
    # If the intersection is a rectangle of width w and height h, the number of paths is C(w+h+2, w+1).

    total_valid_paths = 0
    
    # Iterate over all 16 subsets of conditions (mask from 0 to 15)
    for mask in range(16):
        # Determine the x-range and y-range for this subset
        # Start with the full grid
        curr_x_min, curr_x_max = 0, W
        curr_y_min, curr_y_max = 0, H
        
        # Apply constraints based on the mask bits
        # Bit 0 (1): y < D  => y in [0, D-1]
        # Bit 1 (2): x < L  => x in [0, L-1]
        # Bit 2 (4): y > U  => y in [U+1, H]
        # Bit 3 (8): x > R  => x in [R+1, W]
        
        if mask & 1: # Condition 1
            curr_y_max = D - 1
        if mask & 2: # Condition 2
            curr_x_max = L - 1
        if mask & 4: # Condition 3
            curr_y_min = U + 1
        if mask & 8: # Condition 4
            curr_x_min = R + 1
            
        # Check if the intersection is valid (non-empty)
        if curr_x_min > curr_x_max or curr_y_min > curr_y_max:
            term = 0
        else:
            # Width and height of the valid rectangle
            w_rect = curr_x_max - curr_x_min
            h_rect = curr_y_max - curr_y_min
            
            # Number of paths in this rectangle
            term = count_paths_in_rect(w_rect, h_rect)
        
        # Inclusion-Exclusion Principle
        # Add if even number of conditions, subtract if odd
        bits = bin(mask).count('1')
        if bits % 2 == 1:
            total_valid_paths = (total_valid_paths - term + MOD) % MOD
        else:
            total_valid_paths = (total_valid_paths + term) % MOD
            
    print(total_valid_paths)

if __name__ == '__main__':
    solve()