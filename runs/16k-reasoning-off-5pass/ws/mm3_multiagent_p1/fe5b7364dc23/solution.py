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

    # Precompute binomial coefficients C(K, t) modulo MOD
    C = [0] * (K + 1)
    C[0] = 1
    for t in range(1, K + 1):
        # C(K, t) = C(K, t-1) * (K - t + 1) / t
        C[t] = C[t - 1] * (K - t + 1) % MOD
        C[t] = C[t] * pow(t, MOD - 2, MOD) % MOD

    # cur[m] = sum_{i processed} P_i^m, initially only i=0 (P_0=0)
    cur = [0] * (K + 1)
    cur[0] = 1  # P_0^0 = 1
    # V[t] = sum_{i<j} P_j^t * P_i^{K-t}
    V = [0] * (K + 1)

    prefix = 0
    for a in A:
        prefix = (prefix + a) % MOD
        p = prefix
        # compute powers of p: p_pow[m] = p^m
        p_pow = [1] * (K + 1)
        for m in range(1, K + 1):
            p_pow[m] = p_pow[m - 1] * p % MOD

        # update V[t]
        for t in range(K + 1):
            V[t] = (V[t] + p_pow[t] * cur[K - t]) % MOD

        # update cur[m] with current prefix powers
        for m in range(K + 1):
            cur[m] = (cur[m] + p_pow[m]) % MOD

    # combine with binomial coefficients and signs
    ans = 0
    for t in range(K + 1):
        sign = 1 if (K - t) % 2 == 0 else -1
        ans = (ans + sign * C[t] * V[t]) % MOD

    ans = (ans + MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()