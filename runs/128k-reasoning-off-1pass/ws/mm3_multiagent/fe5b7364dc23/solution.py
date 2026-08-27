import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # prefix sums S[0..N]
    S = [0] * (N + 1)
    for i in range(1, N + 1):
        S[i] = (S[i-1] + A[i-1]) % MOD
    
    # binomial coefficients C[t] for t=0..K
    C = [0] * (K + 1)
    # compute C[t] = C(K, t) mod MOD
    # C(K,0)=1, C(K,1)=K, etc. We can compute via multiplicative formula.
    # Use straightforward recurrence: C[t] = C[t-1] * (K - t + 1) / t
    # Since we have modular inverses, compute inv[t] once, but K<=10 so we can compute directly.
    # We'll compute using Python's integers and then mod.
    for t in range(K + 1):
        # compute C(K, t) exactly using math.comb
        import math
        C[t] = math.comb(K, t) % MOD
    
    # precompute powers P[j][p] = S[j]^p for p=0..K
    # Use list of lists
    P = [[0] * (K + 1) for _ in range(N + 1)]
    for j in range(N + 1):
        x = S[j]
        P[j][0] = 1
        for p in range(1, K + 1):
            P[j][p] = (P[j][p-1] * x) % MOD
    
    # prefix sums of powers: pref[p] = sum_{i<j} S[i]^p
    pref = [0] * (K + 1)
    ans = 0
    for j in range(N + 1):
        # contribution for this j
        for t in range(K + 1):
            # sign = (-1)^(K-t)
            if (K - t) % 2 == 0:
                sign = 1
            else:
                sign = MOD - 1  # -1 mod MOD
            term = C[t] * sign % MOD
            term = term * P[j][t] % MOD
            term = term * pref[K - t] % MOD
            ans = (ans + term) % MOD
        # update pref
        for p in range(K + 1):
            pref[p] = (pref[p] + P[j][p]) % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    main()