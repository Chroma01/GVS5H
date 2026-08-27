import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 998244353

    # Precompute Binomial Coefficients C(K, j)
    # Since K is small (<= 10), we can compute them directly or use a small table
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD

    # Prefix sums of powers of S
    # We need to maintain sums of S_l^p for p from 0 to K
    # Let power_sum[p] = sum(S_l^p) for all l processed so far (initially l=0, S_0=0)
    power_sum = [0] * (K + 1)
    
    # Initialize for S_0 = 0
    # 0^p is 0 for p > 0, and 0^0 is 1
    for p in range(K + 1):
        if p == 0:
            power_sum[p] = 1
        else:
            power_sum[p] = 0

    # Current prefix sum S_r
    current_S = 0
    
    total_ans = 0

    # Iterate r from 1 to N
    for x in A:
        current_S = (current_S + x) % MOD
        
        # We want to add sum_{l=0}^{r-1} (S_r - S_l)^K
        # Expand: sum_{j=0}^K C(K, j) * S_r^j * (-1)^(K-j) * S_l^(K-j)
        # = sum_{j=0}^K C(K, j) * S_r^j * (-1)^(K-j) * (sum_{l=0}^{r-1} S_l^(K-j))
        
        term_sum = 0
        for j in range(K + 1):
            # Calculate contribution for this j
            # Coefficient: C(K, j)
            # S_r^j
            # Sign: (-1)^(K-j)
            # Power sum: power_sum[K-j]
            
            coeff = C[K][j]
            s_r_pow = pow(current_S, j, MOD)
            
            # Sign calculation
            if (K - j) % 2 == 1:
                sign = -1
            else:
                sign = 1
            
            p_idx = K - j
            p_sum = power_sum[p_idx]
            
            term = (coeff * s_r_pow) % MOD
            term = (term * p_sum) % MOD
            
            if sign == -1:
                term = (MOD - term) % MOD
            
            term_sum = (term_sum + term) % MOD
        
        total_ans = (total_ans + term_sum) % MOD
        
        # Update power_sum to include S_r for future iterations
        # We need to update power_sum[p] += S_r^p for all p in 0..K
        for p in range(K + 1):
            if p == 0:
                # S_r^0 is always 1
                power_sum[p] = (power_sum[p] + 1) % MOD
            else:
                val = pow(current_S, p, MOD)
                power_sum[p] = (power_sum[p] + val) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()