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
    
    # Precompute binomial coefficients C(K, j) for j in 0..K
    # Since K is small (<= 10), we can compute them directly
    C = [0] * (K + 1)
    C[0] = 1
    for i in range(1, K + 1):
        C[i] = C[i-1] * (K - i + 1) // i
        
    # Compute prefix sums S[0..N]
    # S[0] = 0, S[i] = A[0] + ... + A[i-1]
    S = [0] * (N + 1)
    for i in range(1, N + 1):
        S[i] = (S[i-1] + A[i-1]) % MOD
        
    # We need to compute sum_{0 <= l < r <= N} (S[r] - S[l])^K
    # Expand using binomial theorem:
    # (S[r] - S[l])^K = sum_{j=0}^K C(K, j) * S[r]^j * (-S[l])^(K-j)
    #                 = sum_{j=0}^K C(K, j) * S[r]^j * (-1)^(K-j) * S[l]^(K-j)
    
    # Swap summations:
    # Total = sum_{j=0}^K C(K, j) * (-1)^(K-j) * sum_{0 <= l < r <= N} S[r]^j * S[l]^(K-j)
    
    # For each j, let p = K - j. We need sum_{r=1}^N S[r]^j * (sum_{l=0}^{r-1} S[l]^p)
    # We can maintain running sums of S[l]^p as we iterate r from 1 to N.
    
    # Precompute powers of each prefix sum S[i] for exponents 0 to K
    # powers[i][e] = S[i]^e mod MOD
    powers = [[0] * (K + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        val = S[i]
        powers[i][0] = 1  # val^0 = 1
        for e in range(1, K + 1):
            powers[i][e] = (powers[i][e-1] * val) % MOD
            
    # Initialize running sums for each exponent
    # running_sum[e] stores sum_{l=0}^{r-1} S[l]^e
    running_sum = [0] * (K + 1)
    
    total = 0
    
    # Iterate r from 1 to N
    for r in range(1, N + 1):
        # Before processing r, running_sum[e] contains sum_{l=0}^{r-1} S[l]^e
        # For each j from 0 to K, p = K - j
        # Contribution for this r and j: C(K, j) * (-1)^(K-j) * S[r]^j * running_sum[K-j]
        
        for j in range(K + 1):
            p = K - j
            term = (C[j] * powers[r][j]) % MOD
            term = (term * running_sum[p]) % MOD
            
            if p % 2 == 1:
                # (-1)^p = -1
                term = (-term) % MOD
                
            total = (total + term) % MOD
            
        # Now add S[r]^e to running_sum[e] for all e, so it's available for future r's
        for e in range(K + 1):
            running_sum[e] = (running_sum[e] + powers[r][e]) % MOD
            
    # Ensure the result is non-negative
    total = total % MOD
    
    print(total)

solve()