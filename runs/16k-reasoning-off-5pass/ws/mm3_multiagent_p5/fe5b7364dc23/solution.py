import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it)) % MOD

    # prefix sums P[0..N]
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = (P[i - 1] + A[i]) % MOD

    # precompute powers of P[i] up to K: powP[i][e] = P[i]^e
    powP = [[1] * (K + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        pi = P[i]
        for e in range(1, K + 1):
            powP[i][e] = (powP[i][e - 1] * pi) % MOD

    # binomial coefficients C[j] = C(K, j)
    C = [0] * (K + 1)
    fact = [1] * (K + 1)
    for i in range(1, K + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (K + 1)
    inv_fact[K] = pow(fact[K], MOD - 2, MOD)
    for i in range(K, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    for j in range(K + 1):
        C[j] = fact[K] * inv_fact[j] % MOD * inv_fact[K - j] % MOD

    # suffix sums S[j][i] = sum_{r=i..N} (N - r + 1) * P[r]^j
    S = [[0] * (N + 2) for _ in range(K + 1)]
    for j in range(K + 1):
        cur = 0
        for i in range(N, -1, -1):
            weight = (N - i + 1) % MOD
            cur = (cur + weight * powP[i][j]) % MOD
            S[j][i] = cur

    # suffix sums S2[j][i] = sum_{r=i..N-1} (N - r) * P[r]^j
    S2 = [[0] * (N + 1) for _ in range(K + 1)]
    for j in range(K + 1):
        cur = 0
        for i in range(N - 1, -1, -1):
            weight = (N - i) % MOD
            cur = (cur + weight * powP[i][j]) % MOD
            S2[j][i] = cur

    # sign for (-1)^e: +1 for even e, -1 for odd e
    sign = [1] * (K + 1)
    for e in range(1, K + 1, 2):
        sign[e] = MOD - 1

    ans = 0
    for l in range(1, N + 1):
        term1 = term2 = term3 = term4 = 0
        p_l_1 = powP[l - 1]
        p_l = powP[l]
        idx = l
        idx2 = l - 1
        for j in range(K + 1):
            cj = C[j]
            e = K - j
            sgn = sign[e]
            p1 = p_l_1[e]
            p2 = p_l[e]
            term1 = (term1 + cj * sgn % MOD * p1 % MOD * S[j][idx]) % MOD
            term2 = (term2 + cj * sgn % MOD * p2 % MOD * S[j][idx]) % MOD
            term3 = (term3 + cj * sgn % MOD * p1 % MOD * S2[j][idx2]) % MOD
            term4 = (term4 + cj * sgn % MOD * p2 % MOD * S2[j][idx2]) % MOD

        val = (term1 - term2 - term3 + term4) % MOD
        ans = (ans + l * val) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    main()