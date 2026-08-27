import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    MOD = 998244353

    # Precompute factorials and inverse factorials
    MAX_N = N + 5
    fact = [1] * MAX_N
    finv = [1] * MAX_N
    
    for i in range(2, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    finv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, 1, -1):
        finv[i] = (finv[i+1] * (i+1)) % MOD
        
    # Precompute modular inverse for numbers 1..N using linear sieve method
    inv = [1] * MAX_N
    for i in range(2, MAX_N):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # Helper for nCr
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (finv[r] * finv[n-r]) % MOD
        return (num * den) % MOD

    # Calculate digit counts and sums for each length
    # Lengths can be up to 6 (since 2*10^5 has 6 digits)
    cnt = [0] * 7
    sum_len = [0] * 7
    
    for i in range(1, N + 1):
        l = len(str(i))
        cnt[l] += 1
        sum_len[l] = (sum_len[l] + i) % MOD

    # Helper to compute DP table for a given set of counts
    # dp[j] = sum of 10^(total_length) for subsets of size j
    def compute_dp(counts):
        # counts is a list of counts for lengths 1..6
        dp = [0] * (N + 1)
        dp[0] = 1
        
        current_len = 1
        for c in counts:
            if c == 0:
                continue
            # We are adding 'c' items of length 'current_len'
            # new_dp[j] = sum_{k=0 to min(c, j)} (C(c, k) * 10^(k*current_len) * dp[j-k])
            new_dp = [0] * (N + 1)
            
            # Precompute powers of 10 for this length
            # 10^(k * current_len)
            # We can compute iteratively
            
            # Optimization: iterate j downwards or use temp array. 
            # Using temp array is safer for combination logic.
            
            for j in range(N + 1):
                if dp[j] == 0:
                    continue
                
                # Determine max k
                max_k = c
                if j + max_k > N:
                    max_k = N - j
                
                term_10 = 1
                # C(c, k) = fact[c] * finv[k] * finv[c-k]
                # We can factor out fact[c]
                fact_c = fact[c]
                
                for k in range(max_k + 1):
                    ways = (finv[k] * finv[c-k]) % MOD
                    term = (ways * term_10) % MOD
                    new_dp[j+k] = (new_dp[j+k] + term * dp[j]) % MOD
                    term_10 = (term_10 * pow(10, current_len, MOD)) % MOD
            
            dp = new_dp
            current_len += 1
        return dp

    # Precompute powers of 10
    pow10 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow10[i] = (pow10[i-1] * 10) % MOD

    # Precompute 10^L for L in 1..6
    pow10_len = [pow10[l] for l in range(7)]

    # 1. Compute TotalA_M using all counts
    all_counts = cnt[1:] # indices 1 to 6
    total_A = compute_dp(all_counts)
    
    ans = 0
    
    # Precompute inv_C[M] = 1 / C(N-1, M) for M in 0..N-1
    # C(N-1, M) = fact[N-1] * finv[M] * finv[N-1-M]
    # inv_C[M] = inv(fact[N-1]) * inv(finv[M]) * inv(finv[N-1-M])? No.
    # inv_C[M] = pow(C, MOD-2, MOD)
    
    inv_C = [0] * N
    if N > 1:
        fact_n_minus_1 = fact[N-1]
        for M in range(N):
            if M > N-1:
                inv_C[M] = 0
            else:
                C = (fact_n_minus_1 * finv[M] % MOD * finv[N-1-M]) % MOD
                inv_C[M] = pow(C, MOD - 2, MOD)
    else:
        # N=1 case handled separately or loop range(1) works
        pass

    # Precompute inv[N]
    inv_N = inv[N] if N > 0 else 1

    for L in range(1, 7):
        if cnt[L] == 0:
            continue
            
        # Create counts for dp_minus_L
        counts_minus = list(cnt[1:])
        counts_minus[L-1] -= 1 
        
        # Compute DP for this modified set
        dp_minus = compute_dp(counts_minus)
        
        coeff_sum = 0
        
        # Calculate Coeff_L
        # Coeff_L = sum_{M=0}^{N-1} (1 / (N * C(N-1, M))) * (TotalA_M - 10^L * dp_minus[M-1])
        
        for M in range(N): # M from 0 to N-1
            # Term from TotalA
            val = total_A[M]
            
            # Subtract term from dp_minus
            if M > 0:
                # dp_minus[M-1] corresponds to choosing M-1 items from the rest
                sub = (pow10_len[L] * dp_minus[M-1]) % MOD
                val = (val - sub + MOD) % MOD
            
            # Coeff = inv[N] * inv_C[M]
            coeff = (inv_N * inv_C[M]) % MOD
            term = (val * coeff) % MOD
            coeff_sum = (coeff_sum + term) % MOD
            
        # Add to answer: SumLen[L] * coeff_sum
        term_ans = (sum_len[L] * coeff_sum) % MOD
        ans = (ans + term_ans) % MOD

    print(ans)

if __name__ == '__main__':
    solve()