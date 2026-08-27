import sys

# Increase recursion depth just in case, though this solution is iterative.
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

    # Precompute binomial coefficients C(K, j) for j in 0..K
    # Since K is small (<= 10), we can compute this directly.
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for n in range(K + 1):
        C[n][0] = 1
        for k in range(1, n + 1):
            C[n][k] = (C[n-1][k-1] + C[n-1][k]) % MOD

    # Compute prefix sums of A
    # S[i] will store sum(A[0]...A[i-1])
    # S[0] = 0
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        S[i+1] = current_sum

    # We need to compute: Sum_{1 <= p <= q <= N} (S[q] - S[p-1])^K
    # Using Binomial Theorem: (S[q] - S[p-1])^K = Sum_{j=0}^K C(K, j) * S[q]^j * (-1)^(K-j) * S[p-1]^(K-j)
    # Total Sum = Sum_{q=1}^N Sum_{j=0}^K C(K, j) * (-1)^(K-j) * S[q]^j * (Sum_{p=1}^q S[p-1]^(K-j))
    #
    # Let inner_sum[k] = Sum_{p=1}^q S[p-1]^k
    # As we iterate q from 1 to N:
    # 1. Update inner_sum[k] by adding S[q-1]^k for all k in 0..K.
    # 2. Compute the contribution for current q using the expanded formula.
    
    # Initialize inner_sum array for k from 0 to K
    inner_sum = [0] * (K + 1)
    
    total_ans = 0
    
    # Iterate q from 1 to N
    for q in range(1, N + 1):
        # Update inner_sum for the new p = q
        # The term added is S[p-1]^k where p=q, so we add S[q-1]^k
        val_p_minus_1 = S[q-1]
        
        # Compute powers of val_p_minus_1 iteratively
        power = 1 # (val_p_minus_1)^0
        for k in range(K + 1):
            inner_sum[k] = (inner_sum[k] + power) % MOD
            power = (power * val_p_minus_1) % MOD
        
        # Now compute contribution of this q to the total answer
        # Contribution = Sum_{j=0}^K C(K, j) * (-1)^(K-j) * S[q]^j * inner_sum[K-j]
        
        s_q = S[q]
        current_q_contribution = 0
        
        # We need s_q^j for j=0..K
        pow_s_q = 1
        for j in range(K + 1):
            # Term: C(K, j) * (-1)^(K-j) * S[q]^j * inner_sum[K-j]
            comb = C[K][j]
            sign = 1 if (K - j) % 2 == 0 else -1
            
            term_val = (comb * pow_s_q) % MOD
            term_val = (term_val * inner_sum[K-j]) % MOD
            
            if sign == -1:
                term_val = (MOD - term_val) % MOD
            
            current_q_contribution = (current_q_contribution + term_val) % MOD
            
            # Update pow_s_q for next j
            pow_s_q = (pow_s_q * s_q) % MOD
            
        total_ans = (total_ans + current_q_contribution) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()