import sys

# Set recursion depth just in case
sys.setrecursionlimit(2000)

MOD = 998244353
MAX_N = 2000005  # Sufficient for W+H+2 where W, H <= 10^6

fact = [1] * MAX_N
inv = [1] * MAX_N
invFact = [1] * MAX_N

def precompute():
    for i in range(2, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
    
    inv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, -1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD
        
    for i in range(MAX_N):
        invFact[i] = inv[i]

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    num = fact[n]
    den = (invFact[r] * invFact[n-r]) % MOD
    return (num * den) % MOD

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    W = int(input_data[0])
    H = int(input_data[1])
    L = int(input_data[2])
    R = int(input_data[3])
    D = int(input_data[4])
    U = int(input_data[5])
    
    precompute()
    
    # Helper for Sum_{i=a}^b nCr(i+k, k)
    def sum_nCr_k(k, a, b):
        if a > b: return 0
        # Sum_{i=a}^b nCr(i+k, k) = nCr(b+k+1, k+1) - nCr(a-1+k+1, k+1)
        return (nCr(b+k+1, k+1) - nCr(a-1+k+1, k+1)) % MOD
    
    # Helper for Sum_{i=a}^b nCr(i+k, i+1) = nCr(i+k, k-1)
    def sum_nCr_i1(k, a, b):
        if a > b: return 0
        # Sum_{i=a}^b nCr(i+k, k-1) = nCr(b+k, k) - nCr(a-1+k, k)
        return (nCr(b+k, k) - nCr(a-1+k, k)) % MOD
        
    def sum_nCr(dx_min, dx_max, dy_min, dy_max):
        # Sum_{dx=dx_min}^{dx_max} Sum_{dy=dy_min}^{dy_max} nCr(dx+dy, dx)
        # = Sum_{dx} (nCr(dx+dy_max+1, dx+1) - nCr(dx+dy_min, dx+1))
        # = Sum_{dx} nCr(dx+dy_max+1, dy_max) - Sum_{dx} nCr(dx+dy_min, dy_min)
        # Note: nCr(dx+K, dx+1) = nCr(dx+K, K-1)
        
        term1 = sum_nCr_i1(dy_max, dx_min, dx_max)
        term2 = sum_nCr_i1(dy_min, dx_min, dx_max)
        return (term1 - term2) % MOD

    def sum_paths_avoiding_rect(dx_min, dx_max, dy_min, dy_max, L, R, D, U):
        # Sum over dx in [dx_min, dx_max], dy in [dy_min, dy_max] of paths_avoiding(dx, dy, L, R, D, U)
        # paths_avoiding(dx, dy) = nCr(dx+dy, dx) - A - B + C
        
        # Sum nCr(dx+dy, dx)
        sum_total = sum_nCr(dx_min, dx_max, dy_min, dy_max)
        
        # Sum A: Sum_{dx, dy} (nCr(R+dy+1, dy+1) - nCr(L-1+dy, dy))
        # = (dx_max - dx_min + 1) * [ Sum_{dy=dy_min}^{dy_max} (nCr(R+dy+1, dy+1) - nCr(L-1+dy, dy)) ]
        # nCr(R+dy+1, dy+1) = nCr(R+dy+1, R)
        # nCr(L-1+dy, dy) = nCr(L-1+dy, L-1)
        
        count_dx = dx_max - dx_min + 1
        if count_dx <= 0: return 0
        
        # Sum_{dy} nCr(R+dy+1, R)
        # = nCr(dy_max+R+1, R+1) - nCr(dy_min-1+R+1, R+1)
        # Note: nCr(n, k) with n < k is 0.
        term_A1 = (nCr(dy_max+R+1, R+1) - nCr(dy_min+R, R+1)) % MOD
        
        # Sum_{dy} nCr(L-1+dy, L-1)
        # = nCr(dy_max+L, L) - nCr(dy_min+L-1, L)
        term_A2 = (nCr(dy_max+L, L) - nCr(dy_min+L-1, L)) % MOD
        
        sum_A = (count_dx * ((term_A1 - term_A2) % MOD)) % MOD
        
        # Sum B: Sum_{dx, dy} (nCr(dx+U+1, dx+1) - nCr(dx+D-1, dx))
        # = (dy_max - dy_min + 1) * [ Sum_{dx=dx_min}^{dx_max} (nCr(dx+U+1, dx+1) - nCr(dx+D-1, dx)) ]
        # nCr(dx+U+1, dx+1) = nCr(dx+U+1, U)
        # nCr(dx+D-1, dx) = nCr(dx+D-1, D-1)
        
        count_dy = dy_max - dy_min + 1
        if count_dy <= 0: return 0
        
        # Sum_{dx} nCr(dx+U+1, U)
        term_B1 = (nCr(dx_max+U+1, U+1) - nCr(dx_min+U, U+1)) % MOD
        
        # Sum_{dx} nCr(dx+D-1, D-1)
        term_B2 = (nCr(dx_max+D, D) - nCr(dx_min+D-1, D)) % MOD
        
        sum_B = (count_dy * ((term_B1 - term_B2) % MOD)) % MOD
        
        # Sum C: Sum_{dx, dy} nCr(L+D, L) * nCr(dx-L+dy-D, dx-L)
        # This term is non-zero only if dx >= L and dy >= D.
        # So we clamp the range to [max(dx_min, L), dx_max] and [max(dy_min, D), dy_max].
        
        eff_dx_min = max(dx_min, L)
        eff_dx_max = dx_max
        eff_dy_min = max(dy_min, D)
        eff_dy_max = dy_max
        
        if eff_dx_min > eff_dx_max or eff_dy_min > eff_dy_max:
            sum_C = 0
        else:
            # Sum nCr(dx-L+dy-D, dx-L)
            # Let dx' = dx-L, dy' = dy-D.
            # Sum_{dx'=eff_dx_min-L}^{eff_dx_max-L} Sum_{dy'=eff_dy_min-D}^{eff_dy_max-D} nCr(dx'+dy', dx')
            # = sum_nCr(eff_dx_min-L, eff_dx_max-L, eff_dy_min-D, eff_dy_max-D)
            # Arguments are non-negative because eff_dx_min >= L and eff_dy_min >= D.
            sum_C = nCr(L+D, L) * sum_nCr(eff_dx_min-L, eff_dx_max-L, eff_dy_min-D, eff_dy_max-D)
            sum_C %= MOD
        
        total = (sum_total - sum_A - sum_B + sum_C) % MOD
        return total

    # Define regions
    # R1: 0<=x<=W, 0<=y<=D-1 (Below)
    # R2: 0<=x<=L-1, D<=y<=H (Left)
    # R3: R+1<=x<=W, D<=y<=H (Right)
    # R4: L<=x<=R, U+1<=y<=H (Top)
    
    regions = [
        (0, W, 0, D-1),   # R1
        (0, L-1, D, H),   # R2
        (R+1, W, D, H),   # R3
        (L, R, U+1, H)    # R4
    ]
    
    # Filter out empty regions
    valid_regions = []
    for r in regions:
        if r[0] <= r[1] and r[2] <= r[3]:
            valid_regions.append(r)
    
    total_valid = 0
    
    for i in range(len(valid_regions)):
        for j in range(len(valid_regions)):
            x1, x2, y1, y2 = valid_regions[i]
            x3, x4, y3, y4 = valid_regions[j]
            
            # We need to sum paths from (x, y) in R_i to (x', y') in R_j avoiding the hole.
            # dx = x' - x, dy = y' - y.
            # dx ranges from x3-x2 to x4-x1.
            # dy ranges from y3-y2 to y4-y1.
            
            dx_min = x3 - x2
            dx_max = x4 - x1
            dy_min = y3 - y2
            dy_max = y4 - y1
            
            if dx_min > dx_max or dy_min > dy_max:
                continue
            
            dx_min = max(0, dx_min)
            dy_min = max(0, dy_min)
            
            if dx_min > dx_max or dy_min > dy_max:
                continue
            
            # Add the sum of valid paths
            term = sum_paths_avoiding_rect(dx_min, dx_max, dy_min, dy_max, L, R, D, U)
            total_valid = (total_valid + term) % MOD
            
    print(total_valid)

solve()