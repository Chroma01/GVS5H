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

    # Precompute Binomial Coefficients C(n, k) for n up to K
    # Since K is small (<= 10), a simple 2D array is sufficient and fast.
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD

    # Prefix sums array S
    # S[i] = sum(A[0]...A[i-1])
    # S[0] = 0
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        S[i+1] = current_sum

    # sum_powers[p] will store sum_{i=0}^{r-1} (S[i])^p
    # We need powers up to K.
    # Initialization: Before processing r=1, we need the sum for i=0 to 0.
    # S[0] = 0.
    # sum_powers[p] = S[0]^p = 0^p.
    # 0^0 = 1, and 0^p = 0 for p > 0.
    sum_powers = [0] * (K + 1)
    sum_powers[0] = 1  # Fix: 0^0 = 1

    total_ans = 0

    # Iterate r from 1 to N
    for r in range(1, N + 1):
        sr = S[r]
        
        # Calculate contribution for current r
        # Formula: sum_{j=0}^K C(K, j) * (-1)^(K-j) * S_r^j * sum_{i=0}^{r-1} S_i^(K-j)
        # Let p = K-j. Then j = K-p.
        # Term: C(K, K-p) * (-1)^p * S_r^(K-p) * sum_powers[p]
        # p ranges from 0 to K.
        
        term_sum = 0
        for p in range(K + 1):
            # j = K - p
            j = K - p
            
            # Calculate S_r^j
            # Since j is small (<= 10), we can just multiply or use pow
            sr_pow_j = pow(sr, j, MOD)
            
            # Coefficient: C(K, j) * (-1)^p
            coeff = C[K][j]
            if p % 2 == 1:
                coeff = (MOD - coeff) % MOD
            
            # Contribution
            val = (coeff * sr_pow_j) % MOD
            val = (val * sum_powers[p]) % MOD
            term_sum = (term_sum + val) % MOD
            
        total_ans = (total_ans + term_sum) % MOD
        
        # Update sum_powers for the next iteration (r+1)
        # We need to add S[r]^p to sum_powers[p] for all p in 0..K
        for p in range(K + 1):
            # Calculate S[r]^p
            sp = pow(sr, p, MOD)
            sum_powers[p] = (sum_powers[p] + sp) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()