import sys

# Set recursion depth just in case, though we aim for iterative
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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
    MAX_VAL = 2 * 10**6 + 100

    # Precompute factorials and inverse factorials
    fact = [1] * MAX_VAL
    inv_fact = [1] * MAX_VAL

    for i in range(1, MAX_VAL):
        fact[i] = (fact[i-1] * i) % MOD

    inv_fact[MAX_VAL-1] = pow(fact[MAX_VAL-1], MOD - 2, MOD)
    for i in range(MAX_VAL-2, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # Helper to compute sum_{k=1}^{M} binom(k+N, N)
    # Sum_{k=0}^{M} binom(k+N, N) = binom(M+N+1, N+1)
    # So Sum_{k=1}^{M} = binom(M+N+1, N+1) - binom(N, N) = binom(M+N+1, N+1) - 1
    def sum_binom_k_plus_N_N(M, N):
        if M < 0:
            return 0
        # Sum from k=0 to M
        total = nCr(M + N + 1, N + 1)
        # Subtract k=0 term which is binom(N, N) = 1
        return (total - 1 + MOD) % MOD

    # Helper to compute sum_{k=1}^{M} k * binom(k+N, N)
    # Using identity: k * binom(k+N, N) = (N+1) * binom(k+N+1, N+1) - N * binom(k+N, N)
    # Sum_{k=1}^{M} k * binom(k+N, N) = (N+1) * Sum_{k=1}^{M} binom(k+N+1, N+1) - N * Sum_{k=1}^{M} binom(k+N, N)
    def sum_k_binom_k_plus_N_N(M, N):
        if M < 0:
            return 0
        
        # Term 1: (N+1) * sum_{k=1}^{M} binom(k + (N+1), N+1)
        # Let N' = N+1. Sum_{k=1}^{M} binom(k+N', N') = binom(M+N'+1, N'+1) - 1
        term1_sum = sum_binom_k_plus_N_N(M, N + 1)
        term1 = ((N + 1) * term1_sum) % MOD
        
        # Term 2: N * sum_{k=1}^{M} binom(k+N, N)
        term2_sum = sum_binom_k_plus_N_N(M, N)
        term2 = (N * term2_sum) % MOD
        
        return (term1 - term2 + MOD) % MOD

    def count_paths_rect(x1, x2, y1, y2):
        # Rectangle [x1, x2] x [y1, y2]
        # Width W' = x2 - x1, Height H' = y2 - y1
        if x1 > x2 or y1 > y2:
            return 0
        
        W_prime = x2 - x1
        H_prime = y2 - y1
        
        # We need to compute:
        # Ans = (W'+1)(H'+1) T0 - (W'+1) T2 - (H'+1) T1 + T3
        # Where:
        # T0 = sum_{dx=0}^{W'} sum_{dy=0}^{H'} binom(dx+dy, dx)
        # T1 = sum_{dx=0}^{W'} sum_{dy=0}^{H'} dx * binom(dx+dy, dx)
        # T2 = sum_{dx=0}^{W'} sum_{dy=0}^{H'} dy * binom(dx+dy, dx)
        # T3 = sum_{dx=0}^{W'} sum_{dy=0}^{H'} dx * dy * binom(dx+dy, dx)

        # T0 Identity: sum_{dx=0}^{W'} sum_{dy=0}^{H'} binom(dx+dy, dx) = binom(W'+H'+2, W'+1) - 1
        T0 = (nCr(W_prime + H_prime + 2, W_prime + 1) - 1 + MOD) % MOD

        # T1: sum_{dx=0}^{W'} dx * binom(dx + H' + 1, dx + 1)
        # Let k = dx + 1. dx = k - 1. k goes from 1 to W' + 1.
        # Sum_{k=1}^{W'+1} (k-1) * binom(k + H', k)
        # = Sum_{k=1}^{W'+1} k * binom(k + H', H') - Sum_{k=1}^{W'+1} binom(k + H', H')
        
        M = W_prime + 1
        N = H_prime
        
        sum_k_binom = sum_k_binom_k_plus_N_N(M, N)
        sum_binom = sum_binom_k_plus_N_N(M, N)
        
        T1 = (sum_k_binom - sum_binom + MOD) % MOD

        # T2: By symmetry, T2(W', H') = T1(H', W')
        # Swap W' and H'
        M2 = H_prime + 1
        N2 = W_prime
        sum_k_binom_2 = sum_k_binom_k_plus_N_N(M2, N2)
        sum_binom_2 = sum_binom_k_plus_N_N(M2, N2)
        T2 = (sum_k_binom_2 - sum_binom_2 + MOD) % MOD

        # T3: sum_{dx=0}^{W'} sum_{dy=0}^{H'} dx * dy * binom(dx+dy, dx)
        # Inner sum over dy: sum_{dy=0}^{H'} dy * binom(dx+dy, dx)
        # Let j = dy. Sum_{j=0}^{H'} j * binom(dx+j, dx)
        # Identity: sum_{j=0}^{M} j * binom(j+k, k) = (k+1) * binom(M+k+2, k+2) - (M+1) * binom(M+k+1, k+1) + binom(M+k+1, k+2)? 
        # Let's derive:
        # j * binom(j+k, k) = (j+k-k) * binom(j+k, k) = (j+k) * binom(j+k, k) - k * binom(j+k, k)
        # = (k+1) * binom(j+k+1, k+1) - k * binom(j+k, k)
        # Sum_{j=0}^{H'} j * binom(j+dx, dx) = (dx+1) * Sum_{j=0}^{H'} binom(j+dx+1, dx+1) - dx * Sum_{j=0}^{H'} binom(j+dx, dx)
        
        # Sum_{j=0}^{H'} binom(j+A, A) = binom(H'+A+1, A+1)
        
        # So InnerSum(dx) = (dx+1) * binom(H'+dx+1+1, dx+1+1) - dx * binom(H'+dx+1, dx+1)
        #                 = (dx+1) * binom(H'+dx+2, dx+2) - dx * binom(H'+dx+1, dx+1)
        
        # Now sum over dx from 0 to W':
        # T3 = Sum_{dx=0}^{W'} [ (dx+1) * binom(H'+dx+2, dx+2) - dx * binom(H'+dx+1, dx+1) ]
        
        # Let's split into two parts:
        # Part A: Sum_{dx=0}^{W'} (dx+1) * binom(H'+dx+2, dx+2)
        # Let k = dx+1. k goes from 1 to W'+1.
        # Sum_{k=1}^{W'+1} k * binom(H'+k+1, k+1)
        # Note binom(N, K) = binom(N, N-K). binom(H'+k+1, k+1) = binom(H'+k+1, H')
        # So Sum_{k=1}^{W'+1} k * binom(k + (H'+1), H')
        # This is exactly the form sum_k_binom_k_plus_N_N(M, N) with M=W'+1, N=H'+1
        
        M_A = W_prime + 1
        N_A = H_prime + 1
        PartA = sum_k_binom_k_plus_N_N(M_A, N_A)
        
        # Part B: Sum_{dx=0}^{W'} dx * binom(H'+dx+1, dx+1)
        # Let k = dx. k goes from 0 to W'. But term is 0 at k=0. So sum k=1 to W'.
        # Sum_{k=1}^{W'} k * binom(k + H' + 1, k+1)
        # binom(k+H'+1, k+1) = binom(k+H'+1, H')
        # So Sum_{k=1}^{W'} k * binom(k + H', H')? No, N is H'.
        # Wait, binom(k + H' + 1, H') corresponds to N=H' in binom(k+N, N) if the first term was k+N.
        # Here we have k + H' + 1. So it's binom(k + (H'+1), H').
        # So N = H'. But the index inside binom is k + H' + 1.
        # Standard form: binom(k+N, N). Here N=H'. Then binom(k+H', H').
        # We have binom(k+H'+1, H'). This is binom((k+1)+H', H').
        # Let j = k+1. j goes from 2 to W'+1.
        # Sum_{j=2}^{W'+1} (j-1) * binom(j+H', H')
        # = Sum_{j=1}^{W'+1} (j-1) * binom(j+H', H') - (1-1)*...
        # = Sum_{j=1}^{W'+1} j * binom(j+H', H') - Sum_{j=1}^{W'+1} binom(j+H', H')
        
        M_B = W_prime + 1
        N_B = H_prime
        sum_k_binom_B = sum_k_binom_k_plus_N_N(M_B, N_B)
        sum_binom_B = sum_binom_k_plus_N_N(M_B, N_B)
        PartB = (sum_k_binom_B - sum_binom_B + MOD) % MOD
        
        T3 = (PartA - PartB + MOD) % MOD

        # Final Calculation
        term1 = ((W_prime + 1) * (H_prime + 1)) % MOD
        term1 = (term1 * T0) % MOD
        
        term2 = ((W_prime + 1) * T2) % MOD
        
        term3 = ((H_prime + 1) * T1) % MOD
        
        ans = (term1 - term2 - term3 + T3) % MOD
        ans = (ans + MOD) % MOD # Ensure positive
        
        return ans

    # Define the 4 regions for PIE
    # S_L: x < L => [0, L-1] x [0, H]
    # S_R: x > R => [R+1, W] x [0, H]
    # S_D: y < D => [0, W] x [0, D-1]
    # S_U: y > U => [0, W] x [U+1, H]
    
    regions = []
    
    # Region L
    if L > 0:
        regions.append((0, L-1, 0, H))
    
    # Region R
    if R < W:
        regions.append((R+1, W, 0, H))
        
    # Region D
    if D > 0:
        regions.append((0, W, 0, D-1))
        
    # Region U
    if U < H:
        regions.append((0, W, U+1, H))
        
    # If no regions are valid (should not happen per constraints "at least one block"), return 0
    if not regions:
        print(0)
        return

    # PIE: Iterate through all non-empty subsets of regions
    # There are at most 4 regions. 2^4 - 1 = 15 subsets.
    n_regions = len(regions)
    total_ans = 0
    
    for i in range(1, 1 << n_regions):
        # Determine intersection of regions in this subset
        x_min, x_max = 0, W
        y_min, y_max = 0, H
        
        count = 0
        valid = True
        
        for j in range(n_regions):
            if (i >> j) & 1:
                count += 1
                rx1, rx2, ry1, ry2 = regions[j]
                x_min = max(x_min, rx1)
                x_max = min(x_max, rx2)
                y_min = max(y_min, ry1)
                y_max = min(y_max, ry2)
        
        if x_min > x_max or y_min > y_max:
            continue
            
        paths = count_paths_rect(x_min, x_max, y_min, y_max)
        
        if count % 2 == 1:
            total_ans = (total_ans + paths) % MOD
        else:
            total_ans = (total_ans - paths + MOD) % MOD
            
    print(total_ans)

solve()