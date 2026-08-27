import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    K = int(input_data[1])
    A = [int(x) for x in input_data[2:2+N]]
    
    MOD = 998244353
    
    # Compute prefix sums S[0..N]
    # S[0] = 0, S[i] = A[0] + ... + A[i-1]
    S = [0] * (N + 1)
    for i in range(1, N + 1):
        S[i] = (S[i-1] + A[i-1]) % MOD
    
    # Precompute binomial coefficients C(K, m) for m in 0..K
    # Using Pascal's triangle or direct computation
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD
    
    # We need to compute:
    # sum_{0 <= j < r <= N} (S[r] - S[j])^K
    # = sum_{m=0}^K C(K, m) * (-1)^(K-m) * sum_{r=1}^N S[r]^m * (sum_{j=0}^{r-1} S[j]^(K-m))
    
    # For each power p in 0..K, maintain a running prefix sum of S[i]^p
    # prefix_sum_powers[r][p] = sum_{j=0}^{r-1} S[j]^p
    
    # We'll compute the answer incrementally as we iterate r from 1 to N
    # At each step r, we update the running prefix sums for all powers,
    # then compute the contribution for this r.
    
    # running_prefix[p] = sum_{j=0}^{r-1} S[j]^p
    running_prefix = [0] * (K + 1)
    
    # Initialize: before processing any r, we have S[0] in the "past"
    # So we need to add S[0]^p to running_prefix[p] for all p
    # S[0] = 0, so 0^p = 0 for p > 0, and 0^0 = 1
    for p in range(K + 1):
        if p == 0:
            running_prefix[p] = 1  # S[0]^0 = 1
        else:
            running_prefix[p] = 0  # S[0]^p = 0 for p > 0
    
    ans = 0
    
    for r in range(1, N + 1):
        # Before processing r, running_prefix[p] = sum_{j=0}^{r-1} S[j]^p
        
        # Compute the contribution for this r
        # sum_{m=0}^K C(K, m) * (-1)^(K-m) * S[r]^m * running_prefix[K-m]
        Sr = S[r]
        Sr_pow = [1] * (K + 1)  # Sr^0, Sr^1, ..., Sr^K
        for p in range(1, K + 1):
            Sr_pow[p] = (Sr_pow[p-1] * Sr) % MOD
        
        for m in range(K + 1):
            # Term: C(K, m) * (-1)^(K-m) * S[r]^m * running_prefix[K-m]
            sign = 1 if (K - m) % 2 == 0 else -1
            term = C[K][m] * Sr_pow[m] % MOD * running_prefix[K - m] % MOD
            if sign == -1:
                term = (-term) % MOD
            ans = (ans + term) % MOD
        
        # Now update running_prefix by adding S[r]^p for all p
        for p in range(K + 1):
            running_prefix[p] = (running_prefix[p] + Sr_pow[p]) % MOD
    
    print(ans % MOD)

solve()