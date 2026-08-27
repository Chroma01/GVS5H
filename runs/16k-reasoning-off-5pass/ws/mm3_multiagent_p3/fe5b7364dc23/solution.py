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

    # prefix sums S[0..N], S[0]=0
    S = [0] * (N + 1)
    acc = 0
    for i in range(N):
        acc = (acc + A[i]) % MOD
        S[i + 1] = acc

    # precompute binomial coefficients C(K, t) for t=0..K
    # using simple multiplicative formula
    binom = [0] * (K + 1)
    binom[0] = 1
    for t in range(1, K + 1):
        binom[t] = binom[t - 1] * (K - t + 1) // t  # integer division, exact
    # precompute coefficients coeff[t] = C(K, t) * (-1)^(K - t) mod MOD
    coeff = [0] * (K + 1)
    for t in range(K + 1):
        sign = -1 if (K - t) % 2 == 1 else 1
        coeff[t] = binom[t] * sign % MOD

    # R[d] = sum_{p < current q} S[p]^d mod MOD
    R = [0] * (K + 1)
    ans = 0
    # iterate q from 0 to N
    for q in range(N + 1):
        s = S[q]
        # compute powers s^0 .. s^K
        pow_t = [1] * (K + 1)
        for d in range(1, K + 1):
            pow_t[d] = pow_t[d - 1] * s % MOD
        # contribution of this q
        for t in range(K + 1):
            term = coeff[t] * pow_t[t] % MOD
            term = term * R[K - t] % MOD
            ans = (ans + term) % MOD
        # update R with S[q]^d
        for d in range(K + 1):
            R[d] = (R[d] + pow_t[d]) % MOD

    print(ans)

if __name__ == "__main__":
    main()