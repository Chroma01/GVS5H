import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # prefix sums S[i] = A_0 + ... + A_{i-1}, with S[0] = 0
    S = [0] * (N + 1)
    s = 0
    for i in range(N):
        s = (s + A[i]) % MOD
        S[i + 1] = s

    # factorials and inverse factorials up to K
    fact = [1] * (K + 1)
    for i in range(1, K + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (K + 1)
    inv_fact[K] = pow(fact[K], MOD - 2, MOD)
    for i in range(K, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # coefficient[t] = (-1)^{K-t} * C(K, t) (mod MOD)
    coeff = [0] * (K + 1)
    for t in range(K + 1):
        c = fact[K] * inv_fact[t] % MOD * inv_fact[K - t] % MOD
        if (K - t) & 1:          # odd exponent -> negative sign
            c = (-c) % MOD
        coeff[t] = c

    # acc[e] = sum_{i already processed} S_i^e
    acc = [0] * (K + 1)
    acc[0] = 1                     # S_0 = 0, only S_0^0 = 1
    cur = [1] * (K + 1)            # powers of the current S_j
    ans = 0

    for j in range(1, N + 1):
        sj = S[j]
        # compute cur[t] = sj^t
        cur[0] = 1
        for t in range(1, K + 1):
            cur[t] = cur[t - 1] * sj % MOD

        # add contributions of this j
        for t in range(K + 1):
            term = coeff[t] * cur[t] % MOD * acc[K - t] % MOD
            ans = (ans + term) % MOD

        # insert S_j into the accumulator
        for e in range(K + 1):
            acc[e] = (acc[e] + cur[e]) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    solve()