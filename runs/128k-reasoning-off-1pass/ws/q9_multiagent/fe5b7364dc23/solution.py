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

    # Precompute Binomial Coefficients C(K, j)
    # Since K is small (<= 10), we can compute them directly or use a small table.
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for n in range(K + 1):
        C[n][0] = 1
        for k in range(1, n + 1):
            C[n][k] = (C[n-1][k-1] + C[n-1][k]) % MOD

    # Prefix sums of A
    # P[i] = sum(A[0]...A[i-1])
    # P[0] = 0
    P = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        P[i+1] = current_sum

    # Precompute powers of P[i] for j in 0..K
    # pow_P[j][i] = P[i]^j
    pow_P = [[0] * (N + 1) for _ in range(K + 1)]
    for i in range(N + 1):
        val = P[i]
        pow_P[0][i] = 1
        curr = 1
        for j in range(1, K + 1):
            curr = (curr * val) % MOD
            pow_P[j][i] = curr

    # Precompute prefix sums for terms like sum_{i=1 to M} i * P[i-1]^j
    # PreSum_L_minus_1[j][M] = sum_{i=1 to M} i * P[i-1]^j
    PreSum_L_minus_1 = [[0] * (N + 1) for _ in range(K + 1)]
    for j in range(K + 1):
        current_acc = 0
        for i in range(1, N + 1):
            term = (i * pow_P[j][i-1]) % MOD
            current_acc = (current_acc + term) % MOD
            PreSum_L_minus_1[j][i] = current_acc

    # Precompute prefix sums for terms like sum_{i=1 to M} i * P[i]^j
    # PreSum_L[j][M] = sum_{i=1 to M} i * P[i]^j
    PreSum_L = [[0] * (N + 1) for _ in range(K + 1)]
    for j in range(K + 1):
        current_acc = 0
        for i in range(1, N + 1):
            term = (i * pow_P[j][i]) % MOD
            current_acc = (current_acc + term) % MOD
            PreSum_L[j][i] = current_acc

    # Helper to compute sum_{i=1 to M} i * (C - P[i-1])^K
    # Uses binomial expansion: (C - X)^K = sum_{j=0}^K C(K, j) * C^(K-j) * (-1)^j * X^j
    def calc_diff_prefix(C_val, M):
        if M == 0: return 0
        res = 0
        for j in range(K + 1):
            sign = 1 if j % 2 == 0 else -1
            term = (pow(C_val, K - j, MOD)) % MOD
            term = (term * PreSum_L_minus_1[j][M]) % MOD
            term = (term * sign) % MOD
            res = (res + term) % MOD
        return res

    # Helper to compute sum_{i=1 to M} i * (C - P[i])^K
    def calc_diff_prefix_L(C_val, M):
        if M == 0: return 0
        res = 0
        for j in range(K + 1):
            sign = 1 if j % 2 == 0 else -1
            term = (pow(C_val, K - j, MOD)) % MOD
            term = (term * PreSum_L[j][M]) % MOD
            term = (term * sign) % MOD
            res = (res + term) % MOD
        return res

    # Calculate T1 components
    # T1 = (N+1) * sum_{L=1}^N L * [ (P[N] - P[L-1])^K - (P[N] - P[L])^K ]
    term1_part1 = calc_diff_prefix(P[N], N)
    term1_part2 = calc_diff_prefix_L(P[N], N)
    T1 = (term1_part1 - term1_part2) % MOD
    T1 = (T1 * (N + 1)) % MOD

    # Calculate T2 components
    # T2 = Sum_A - Sum_B - Sum_C + Sum_D
    
    Sum_A = 0
    Sum_B = 0
    Sum_C = 0
    Sum_D = 0
    
    # Sum A: sum_{R=1}^N R * calc_diff_prefix(P[R], R)
    # Sum B: sum_{R=1}^N R * calc_diff_prefix_L(P[R], R)
    for R in range(1, N + 1):
        val_R = P[R]
        inner_A = calc_diff_prefix(val_R, R)
        Sum_A = (Sum_A + R * inner_A) % MOD
        inner_B = calc_diff_prefix_L(val_R, R)
        Sum_B = (Sum_B + R * inner_B) % MOD
        
    # Sum C: sum_{r=1}^{N-1} (r+1) * calc_diff_prefix(P[r], r+1)
    # Sum D: sum_{r=1}^{N-1} (r+1) * calc_diff_prefix_L(P[r], r+1)
    for r in range(1, N):
        val_r = P[r]
        inner_C = calc_diff_prefix(val_r, r + 1)
        Sum_C = (Sum_C + (r + 1) * inner_C) % MOD
        inner_D = calc_diff_prefix_L(val_r, r + 1)
        Sum_D = (Sum_D + (r + 1) * inner_D) % MOD

    T2 = (Sum_A - Sum_B - Sum_C + Sum_D) % MOD
    
    # Final Answer = (N+1)*T1 - T2
    ans = (T1 - T2) % MOD
    print(ans)

if __name__ == '__main__':
    solve()