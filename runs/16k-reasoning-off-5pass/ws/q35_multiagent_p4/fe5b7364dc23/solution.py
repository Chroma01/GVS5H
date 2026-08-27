import sys

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

    # Precompute binomial coefficients C(K, j) for j in 0..K
    # Since K is small (<= 10), we can compute them directly or use a simple DP
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD

    # Compute prefix sums S[0..N]
    # S[0] = 0
    # S[i] = A[0] + ... + A[i-1]
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        S[i+1] = current_sum

    # We want to compute sum_{0 <= l < r <= N} (S[r] - S[l])^K
    # Expand (S[r] - S[l])^K = sum_{j=0}^K C(K, j) * S[r]^j * (-1)^(K-j) * S[l]^(K-j)
    # Total sum = sum_{j=0}^K C(K, j) * (-1)^(K-j) * [ sum_{0 <= l < r <= N} S[r]^j * S[l]^(K-j) ]
    
    # Let m = K - j. Then we need sum_{0 <= l < r <= N} S[r]^j * S[l]^m
    # This can be computed by iterating r from 1 to N, and maintaining a running sum of S[l]^m for l < r.
    # Let T[m] = sum_{l=0}^{r-1} S[l]^m.
    # When we process r, the contribution for a fixed j (and thus m = K-j) is S[r]^j * T[m].
    # After processing r, we update T[m] by adding S[r]^m for all m in 0..K.

    # Initialize T[m] = 0 for all m in 0..K
    # Initially, before any r is processed, we have l=0 with S[0]=0.
    # So T[m] should start with S[0]^m = 0^m.
    # 0^0 = 1, 0^m = 0 for m > 0.
    T = [0] * (K + 1)
    T[0] = 1  # S[0]^0 = 1

    total_sum = 0

    for r in range(1, N + 1):
        Sr = S[r]
        
        # Compute powers of Sr: Sr^0, Sr^1, ..., Sr^K
        Sr_powers = [1] * (K + 1)
        for p in range(1, K + 1):
            Sr_powers[p] = (Sr_powers[p-1] * Sr) % MOD
            
        # For each j from 0 to K, m = K - j
        # Contribution: C(K, j) * (-1)^(K-j) * Sr^j * T[K-j]
        for j in range(K + 1):
            m = K - j
            term = (C[K][j] * Sr_powers[j]) % MOD
            term = (term * T[m]) % MOD
            
            if m % 2 == 1:  # (-1)^m = -1 if m is odd
                total_sum = (total_sum - term) % MOD
            else:           # (-1)^m = 1 if m is even
                total_sum = (total_sum + term) % MOD
        
        # Update T[m] by adding Sr^m for all m in 0..K
        for m in range(K + 1):
            T[m] = (T[m] + Sr_powers[m]) % MOD

    # Ensure the result is non-negative
    total_sum = (total_sum + MOD) % MOD
    
    print(total_sum)

if __name__ == '__main__':
    solve()