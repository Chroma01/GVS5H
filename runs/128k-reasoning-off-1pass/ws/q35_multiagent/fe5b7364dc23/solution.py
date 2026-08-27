import sys

def solve():
    MOD = 998244353
    
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    N = int(input_data[0])
    K = int(input_data[1])
    
    A = []
    for i in range(N):
        A.append(int(input_data[2 + i]))
    
    # Precompute binomial coefficients C(K, j) for j in 0..K
    # Since K is small (<= 10), we can compute them directly
    C = [0] * (K + 1)
    C[0] = 1
    for i in range(1, K + 1):
        C[i] = C[i-1] * (K - i + 1) // i
    
    # Precompute powers of -1: (-1)^p mod MOD
    # (-1)^p is 1 if p is even, -1 if p is odd
    # We'll handle the sign in the formula
    
    # Prefix sums S_0, S_1, ..., S_N
    # S_0 = 0
    # S_i = A[0] + A[1] + ... + A[i-1] for i >= 1
    
    # We need to compute sum_{1<=l<=r<=N} (S_r - S_{l-1})^K
    
    # Maintain sum_powers[p] = sum_{i=0}^{r-1} S_i^p for the current r
    # Initially for r=1, sum_powers[p] = S_0^p = 0^p
    # 0^0 = 1, 0^p = 0 for p > 0
    
    sum_powers = [0] * (K + 1)
    sum_powers[0] = 1  # S_0^0 = 1
    
    total = 0
    
    # Current prefix sum S_r
    S_r = 0
    
    for r in range(1, N + 1):
        # Update S_r by adding A[r-1]
        S_r = (S_r + A[r-1]) % MOD
        
        # Compute contribution of all subarrays ending at r
        # sum_{l=1}^r (S_r - S_{l-1})^K
        # = sum_{j=0}^K C(K,j) * S_r^j * (-1)^(K-j) * sum_{l=1}^r S_{l-1}^(K-j)
        # = sum_{j=0}^K C(K,j) * S_r^j * (-1)^(K-j) * sum_powers[K-j]
        
        # But sum_powers[p] currently holds sum_{i=0}^{r-1} S_i^p
        # which is exactly sum_{l=1}^r S_{l-1}^p since l-1 ranges from 0 to r-1
        
        contribution = 0
        for j in range(K + 1):
            # term: C(K, j) * S_r^j * (-1)^(K-j) * sum_powers[K-j]
            sign = 1 if (K - j) % 2 == 0 else -1
            term = C[j] * pow(S_r, j, MOD) % MOD
            term = term * sum_powers[K - j] % MOD
            if sign == -1:
                term = (-term) % MOD
            contribution = (contribution + term) % MOD
        
        total = (total + contribution) % MOD
        
        # Update sum_powers with S_r^p for all p from 0 to K
        # sum_powers[p] += S_r^p
        for p in range(K + 1):
            sp = pow(S_r, p, MOD)
            sum_powers[p] = (sum_powers[p] + sp) % MOD
    
    # Ensure total is non-negative
    total = total % MOD
    
    print(total)

solve()