import sys

MOD = 998244353

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # prefix sums P[0..N]; P[0]=0
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = (P[i-1] + A[i-1]) % MOD
    
    # precompute binomial coefficients C(K, j) for j=0..K
    # C(K,0)=1
    binom = [0] * (K + 1)
    # compute using multiplicative formula
    binom[0] = 1
    for j in range(1, K + 1):
        binom[j] = binom[j-1] * (K - j + 1) // j  # integer division, exact
        # but we need modulo later; keep as int (small)
    # Alternatively compute directly via modular inverse
    # Since K <= 10, we can keep binom as integer.
    # Convert to modulo later.
    # Precompute powers of prefix sum: pow_e = P_r^e
    # We'll compute on the fly per r.
    # S[e] stores sum of P_l^e for l < r
    S = [0] * (K + 1)  # S[0] = count of previous l
    ans = 0
    
    for r in range(N + 1):
        # compute P_r^j for j=0..K
        pr = P[r]
        # precompute powers of pr
        pow_j = [1] * (K + 1)
        for j in range(1, K + 1):
            pow_j[j] = pow_j[j-1] * pr % MOD
        
        # contribution for this r: sum_{j=0..K} C(K,j) * (-1)^(K-j) * P_r^j * S[K-j]
        for j in range(K + 1):
            # term with exponent j on P_r and (K-j) on P_l
            # S index is K-j
            s_idx = K - j
            term = binom[j] % MOD
            if (K - j) % 2 == 1:  # sign from (-1)^(K-j) = -1 if K-j odd
                term = MOD - term
            # multiply by P_r^j
            term = term * pow_j[j] % MOD
            # multiply by S[s_idx]
            term = term * S[s_idx] % MOD
            ans = (ans + term) % MOD
        
        # update S with current P_r for future r
        # S[e] += P_r^e
        for e in range(K + 1):
            S[e] = (S[e] + pow_j[e]) % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    main()