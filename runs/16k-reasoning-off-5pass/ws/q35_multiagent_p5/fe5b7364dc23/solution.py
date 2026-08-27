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

    # Precompute binomial coefficients C(K, m) for m in 0..K
    # Since K is small (<= 10), we can compute them directly
    C = [0] * (K + 1)
    C[0] = 1
    for i in range(1, K + 1):
        C[i] = C[i-1] * (K - i + 1) // i

    # Compute prefix sums S[0..N]
    # S[0] = 0
    # S[i] = A[0] + ... + A[i-1]
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(N):
        current_sum = (current_sum + A[i]) % MOD
        S[i+1] = current_sum

    # We need to compute sum_{0 <= i < j <= N} (S[j] - S[i])^K
    # Expand (S[j] - S[i])^K = sum_{m=0}^K C(K, m) * S[j]^(K-m) * (-S[i])^m
    #                          = sum_{m=0}^K C(K, m) * (-1)^m * S[j]^(K-m) * S[i]^m
    
    # Maintain cumulative sums of S[i]^m for m in 0..K
    # cum_pow[m] = sum_{processed i} S[i]^m
    cum_pow = [0] * (K + 1)
    
    # Initialize with S[0] = 0
    # S[0]^m = 0 for m > 0, and S[0]^0 = 1
    cum_pow[0] = 1  # S[0]^0 = 1
    # cum_pow[m] for m > 0 remains 0 initially because S[0] = 0
    
    total_ans = 0
    
    # Iterate j from 1 to N
    for j in range(1, N + 1):
        sj = S[j]
        
        # For current j, add the contribution from all i < j
        # Contribution = sum_{m=0}^K C(K, m) * (-1)^m * sj^(K-m) * cum_pow[m]
        
        # Precompute powers of sj: sj^0, sj^1, ..., sj^K
        sj_powers = [1] * (K + 1)
        for p in range(1, K + 1):
            sj_powers[p] = (sj_powers[p-1] * sj) % MOD
        
        term_sum = 0
        for m in range(K + 1):
            # C(K, m) * (-1)^m * sj^(K-m) * cum_pow[m]
            sign = 1 if m % 2 == 0 else -1
            coeff = C[m] * cum_pow[m] % MOD
            coeff = coeff * sj_powers[K - m] % MOD
            if sign == -1:
                term_sum = (term_sum - coeff) % MOD
            else:
                term_sum = (term_sum + coeff) % MOD
        
        total_ans = (total_ans + term_sum) % MOD
        
        # Update cum_pow with S[j]^m for all m
        for m in range(K + 1):
            cum_pow[m] = (cum_pow[m] + sj_powers[m]) % MOD

    # Ensure the result is non-negative
    total_ans = total_ans % MOD
    
    print(total_ans)

if __name__ == '__main__':
    solve()