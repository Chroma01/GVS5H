import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

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

    # Prefix sums of A
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        S[i+1] = current_sum

    # Precompute Pre[i] = i*(i+1)/2
    # Pre[i] is used for the minimum index L (1-based)
    # Contribution factor for L is L*(L+1)/2
    Pre = [0] * (N + 1)
    for i in range(1, N + 1):
        Pre[i] = (i * (i + 1) // 2) % MOD

    # Precompute Suf[i] = (N-i+1)*(N-i+2)/2
    # Suf[i] is used for the maximum index R (1-based)
    # Contribution factor for R is (N-R+1)*(N-R+2)/2
    Suf = [0] * (N + 1)
    for i in range(1, N + 1):
        Suf[i] = ((N - i + 1) * (N - i + 2) // 2) % MOD

    # Precompute powers of S[i] for t in 0..K
    # pow_S[i][t] = S[i]^t % MOD
    pow_S = [[0] * (K + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        val = S[i]
        p = 1
        pow_S[i][0] = 1
        for t in range(1, K + 1):
            p = (p * val) % MOD
            pow_S[i][t] = p

    # Precompute binomial coefficients C(K, t)
    C = [0] * (K + 1)
    for t in range(K + 1):
        C[t] = 1
        for i in range(1, t + 1):
            C[t] = (C[t] * (t - i + 1)) % MOD
            C[t] = (C[t] * pow(i, MOD - 2, MOD)) % MOD

    # Helper to compute the sum for a specific term configuration
    # term_type: 1, 2, 3, 4 corresponding to the 4 cases in inclusion-exclusion
    def compute_term(term_type):
        total = 0
        
        if term_type == 1:
            # Case 1: L <= R <= N. Term: (S_R - S_{L-1})^K. C = -1.
            # Inner[t][L] = sum_{R=L}^N Suf[R] * S_R^t
            
            # Precompute inner sums
            inner = [[0] * (K + 1) for _ in range(N + 2)]
            for t in range(K + 1):
                curr = 0
                for L in range(N, 0, -1):
                    val = (Suf[L] * pow_S[L][t]) % MOD
                    curr = (curr + val) % MOD
                    inner[t][L] = curr
            
            # Compute main sum
            for t in range(K + 1):
                coeff = (C[t] * pow(-1, K - t, MOD)) % MOD
                if coeff == 0: continue
                
                term_sum = 0
                for L in range(1, N + 1):
                    s_prev = S[L-1]
                    s_prev_pow = pow_S[L-1][K-t]
                    inner_val = inner[t][L]
                    prod = (s_prev_pow * inner_val) % MOD
                    term_sum = (term_sum + prod) % MOD
                
                total = (total + coeff * term_sum) % MOD

        elif term_type == 2:
            # Case 2: L < R <= N. Term: (S_R - S_L)^K. C = 0.
            # Inner[t][L] = sum_{R=L+1}^N Suf[R] * S_R^t
            # This is inner[t][L+1] from Case 1 logic
            
            # Precompute inner sums (same as Case 1)
            inner = [[0] * (K + 1) for _ in range(N + 2)]
            for t in range(K + 1):
                curr = 0
                for L in range(N, 0, -1):
                    val = (Suf[L] * pow_S[L][t]) % MOD
                    curr = (curr + val) % MOD
                    inner[t][L] = curr
            
            for t in range(K + 1):
                coeff = (C[t] * pow(-1, K - t, MOD)) % MOD
                if coeff == 0: continue
                
                term_sum = 0
                for L in range(1, N + 1):
                    s_curr = S[L]
                    s_curr_pow = pow_S[L][K-t]
                    inner_val = inner[t][L+1]
                    prod = (s_curr_pow * inner_val) % MOD
                    term_sum = (term_sum + prod) % MOD
                
                total = (total + coeff * term_sum) % MOD

        elif term_type == 3:
            # Case 3: L <= R-1 <= N-1 => L <= R <= N. Term: (S_{R-1} - S_{L-1})^K.
            # Let j = R-1. Range j: L-1 to N-2.
            # Inner[t][L] = sum_{j=L-1}^{N-2} Suf[j+1] * S_j^t
            
            inner = [[0] * (K + 1) for _ in range(N + 2)]
            for t in range(K + 1):
                curr = 0
                for L in range(N, 0, -1):
                    if L - 1 <= N - 2:
                        j = L - 1
                        val = (Suf[j+1] * pow_S[j][t]) % MOD
                        curr = (curr + val) % MOD
                    inner[t][L] = curr
            
            for t in range(K + 1):
                coeff = (C[t] * pow(-1, K - t, MOD)) % MOD
                if coeff == 0: continue
                
                term_sum = 0
                for L in range(1, N + 1):
                    s_prev = S[L-1]
                    s_prev_pow = pow_S[L-1][K-t]
                    inner_val = inner[t][L]
                    prod = (s_prev_pow * inner_val) % MOD
                    term_sum = (term_sum + prod) % MOD
                total = (total + coeff * term_sum) % MOD

        elif term_type == 4:
            # Case 4: L < R-1 <= N-1 => L+1 <= R <= N. Term: (S_{R-1} - S_L)^K.
            # Let j = R-1. Range j: L to N-2.
            # Inner[t][L] = sum_{j=L}^{N-2} Suf[j+1] * S_j^t
            
            inner = [[0] * (K + 1) for _ in range(N + 2)]
            for t in range(K + 1):
                curr = 0
                for L in range(N, 0, -1):
                    if L <= N - 2:
                        j = L
                        val = (Suf[j+1] * pow_S[j][t]) % MOD
                        curr = (curr + val) % MOD
                    inner[t][L] = curr
            
            for t in range(K + 1):
                coeff = (C[t] * pow(-1, K - t, MOD)) % MOD
                if coeff == 0: continue
                
                term_sum = 0
                for L in range(1, N + 1):
                    s_curr = S[L]
                    s_curr_pow = pow_S[L][K-t]
                    inner_val = inner[t][L]
                    prod = (s_curr_pow * inner_val) % MOD
                    term_sum = (term_sum + prod) % MOD
                total = (total + coeff * term_sum) % MOD

        return total

    # Calculate the 4 terms
    # Ans = Term1 - Term2 - Term3 + Term4
    ans = compute_term(1)
    ans = (ans - compute_term(2)) % MOD
    ans = (ans - compute_term(3)) % MOD
    ans = (ans + compute_term(4)) % MOD

    print((ans + MOD) % MOD)

if __name__ == '__main__':
    solve()