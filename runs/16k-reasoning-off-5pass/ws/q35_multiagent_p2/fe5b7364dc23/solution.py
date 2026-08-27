import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    N = int(input_data[0])
    K = int(input_data[1])
    
    A = []
    for i in range(N):
        A.append(int(input_data[2 + i]))
    
    MOD = 998244353
    
    # Compute prefix sums S_0, S_1, ..., S_N
    # S[0] = 0, S[i] = A[0] + ... + A[i-1]
    S = [0] * (N + 1)
    for i in range(1, N + 1):
        S[i] = (S[i-1] + A[i-1]) % MOD
    
    # Precompute binomial coefficients C(K, k) for k in 0..K
    # Since K is small (<= 10), we can compute them directly
    def nCr_mod(n, r, mod):
        if r < 0 or r > n:
            return 0
        if r == 0 or r == n:
            return 1
        if r > n // 2:
            r = n - r
        
        res = 1
        for i in range(r):
            res = res * (n - i) % mod
            # Modular inverse of i+1
            inv = pow(i + 1, mod - 2, mod)
            res = res * inv % mod
        return res
    
    binom_coeffs = []
    for k in range(K + 1):
        binom_coeffs.append(nCr_mod(K, k, MOD))
    
    total_ans = 0
    
    # For each k from 0 to K, compute:
    # binom(K, k) * (-1)^k * sum_{r=1}^{N} S[r]^(K-k) * (sum_{j=0}^{r-1} S[j]^k)
    
    for k in range(K + 1):
        # Compute the inner sum: sum_{r=1}^{N} S[r]^(K-k) * (sum_{j=0}^{r-1} S[j]^k)
        current_sum_Sk = 0  # This will store sum_{j=0}^{r-1} S[j]^k
        inner_sum = 0
        
        # We need S[r]^(K-k) and S[r]^k for each r
        # Let exp_high = K - k, exp_low = k
        
        exp_high = K - k
        exp_low = k
        
        for r in range(1, N + 1):
            # Add S[r]^exp_high * current_sum_Sk to inner_sum
            term = pow(S[r], exp_high, MOD) * current_sum_Sk % MOD
            inner_sum = (inner_sum + term) % MOD
            
            # Update current_sum_Sk by adding S[r]^exp_low
            current_sum_Sk = (current_sum_Sk + pow(S[r], exp_low, MOD)) % MOD
        
        # Multiply by binom(K, k) * (-1)^k
        sign = 1 if k % 2 == 0 else -1
        term_total = binom_coeffs[k] * inner_sum % MOD
        if sign == -1:
            total_ans = (total_ans - term_total) % MOD
        else:
            total_ans = (total_ans + term_total) % MOD
    
    # Ensure the result is non-negative
    total_ans = total_ans % MOD
    print(total_ans)

if __name__ == '__main__':
    solve()