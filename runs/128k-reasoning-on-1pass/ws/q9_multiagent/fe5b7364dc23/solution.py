import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
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

    # Compute prefix sums S
    # S[i] is sum(A[0]...A[i-1])
    # We need S_0 to S_N
    # S_0 = 0
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        S[i+1] = current_sum

    # Precompute powers of S_i for k from 0 to K
    # S_pow[k][i] = S[i]^k
    # Dimensions: (K+1) x (N+1)
    # We compute iteratively to avoid pow overhead and improve cache locality
    S_pow = [[0] * (N + 1) for _ in range(K + 1)]
    
    for k in range(K + 1):
        for i in range(N + 1):
            if k == 0:
                S_pow[k][i] = 1
            else:
                S_pow[k][i] = (S_pow[k-1][i] * S[i]) % MOD

    # Precompute prefix sums of these powers
    # P[k][i] = sum_{j=0}^i S[j]^k
    P = [[0] * (N + 1) for _ in range(K + 1)]
    
    for k in range(K + 1):
        current_p_sum = 0
        for i in range(N + 1):
            current_p_sum = (current_p_sum + S_pow[k][i]) % MOD
            P[k][i] = current_p_sum

    # Precompute Binomial Coefficients C(K, k)
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD

    ans = 0
    
    # Iterate k from 0 to K
    # Formula: sum_{k=0}^K C(K, k) * (-1)^(K-k) * sum_{r=1}^N S[r]^k * P[K-k][r-1]
    
    for k in range(K + 1):
        # Coefficient from binomial expansion
        coeff = C[K][k]
        
        # Sign: (-1)^(K-k)
        if (K - k) % 2 == 1:
            sign = MOD - 1
        else:
            sign = 1
        
        # Calculate sum_{r=1}^N S[r]^k * P[K-k][r-1]
        # S[r]^k is S_pow[k][r]
        # P[K-k][r-1] is P[K-k][r-1]
        
        term_sum = 0
        # Optimization: accumulate without modulo inside loop to reduce overhead
        # Python handles large integers automatically
        for r in range(1, N + 1):
            term_sum += S_pow[k][r] * P[K-k][r-1]
        
        term_sum %= MOD
            
        contribution = (coeff * sign) % MOD
        contribution = (contribution * term_sum) % MOD
        ans = (ans + contribution) % MOD

    print(ans)

if __name__ == '__main__':
    solve()