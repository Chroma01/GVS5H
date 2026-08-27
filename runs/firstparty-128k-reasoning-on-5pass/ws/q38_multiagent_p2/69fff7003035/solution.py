import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])

    # Digit-length counts and sums of values for each length.
    D = len(str(N))
    cnt = [0] * (D + 1)
    val_sum = [0] * (D + 1)
    p = 1
    for l in range(1, D + 1):
        start = p
        end = min(N, p * 10 - 1)
        if start <= N:
            c = end - start + 1
            cnt[l] = c
            val_sum[l] = ((start + end) * c // 2) % MOD
        p *= 10

    lengths = [l for l in range(1, D + 1) if cnt[l] > 0]
    L = len(lengths)
    w = [pow(10, l, MOD) for l in lengths]
    cw = [(cnt[l] * w[i]) % MOD for i, l in enumerate(lengths)]

    # Factorials.
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # Modular inverses of 1..N.
    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # pair_fact[k] = k! * (N-1-k)!
    pair_fact = [fact[k] * fact[N - 1 - k] % MOD for k in range(N)]

    # b is the current coefficient b_k of F(z)=prod_l (1+10^l z)^{cnt[l]}.
    # R[i] is R_l(k)=sum_{j=0}^k b_{k-j}(-10^l)^j.
    # For length l, R_l(k) is also the coefficient q_k of F/(1+10^l z).
    R = [0] * L
    H = [0] * L
    b = 1
    mod = MOD
    idx = range(L)

    for k in range(N):
        pf = pair_fact[k]
        s = 0
        for i in idx:
            r = (b - w[i] * R[i]) % mod
            R[i] = r
            H[i] = (H[i] + r * pf) % mod
            s += cw[i] * r
        b = (s % mod) * inv[k + 1] % mod

    ans = 0
    for i, l in enumerate(lengths):
        ans = (ans + val_sum[l] * H[i]) % mod
    print(ans)

if __name__ == "__main__":
    main()