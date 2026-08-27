import sys

MOD = 998244353
PRIMITIVE_ROOT = 3

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:len(a) + len(b) - 1]

def main():
    sys.setrecursionlimit(1 << 25)
    N = int(sys.stdin.readline())
    if N == 0:
        print(0)
        return

    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # Determine digit lengths and counts
    max_len = len(str(N))
    cnt = [0] * (max_len + 1)
    w = [0] * (max_len + 1)
    for l in range(1, max_len + 1):
        lo = 10 ** (l - 1)
        hi = min(10 ** l - 1, N)
        if lo > N:
            cnt[l] = 0
        else:
            cnt[l] = hi - lo + 1
        w[l] = pow(10, l, MOD)

    # Compute F polynomial via NTT multiplication
    F = [1]
    for l in range(1, max_len + 1):
        if cnt[l] == 0:
            continue
        # Build polynomial (1 + w[l]*x)^{cnt[l]}
        deg = cnt[l]
        P = [0] * (deg + 1)
        wk = 1
        for k in range(deg + 1):
            # C(cnt[l], k) * w[l]^k
            P[k] = fact[cnt[l]] * inv_fact[k] % MOD * inv_fact[deg - k] % MOD * wk % MOD
            wk = wk * w[l] % MOD
        F = multiply(F, P)
        if len(F) > N + 1:
            F = F[:N + 1]

    # Pad F to length N+1
    if len(F) < N + 1:
        F += [0] * (N + 1 - len(F))

    # Compute S_w[l] = sum of numbers with length l
    S_w = [0] * (max_len + 1)
    for l in range(1, max_len + 1):
        lo = 10 ** (l - 1)
        hi = min(10 ** l - 1, N)
        if lo > N:
            continue
        cnt_l = hi - lo + 1
        S_w[l] = (lo + hi) * cnt_l // 2 % MOD

    # Precompute invC(N-1, m) for m=0..N-1
    invC = [0] * N
    if N - 1 >= 0:
        inv_fact_N_1 = inv_fact[N - 1]
        for m in range(N):
            invC[m] = inv_fact_N_1 * fact[m] % MOD * fact[N - 1 - m] % MOD

    # Compute answer
    ans = 0
    for l in range(1, max_len + 1):
        if cnt[l] == 0:
            continue
        # Compute G_l array
        G = [0] * N
        G[0] = 1
        for m in range(1, N):
            G[m] = (F[m] - w[l] * G[m - 1]) % MOD
        # Compute sum_G = sum_{m=0}^{N-1} G[m] * invC[m]
        sum_G = 0
        for m in range(N):
            sum_G = (sum_G + G[m] * invC[m]) % MOD
        ans = (ans + S_w[l] * sum_G) % MOD

    ans = ans * fact[N - 1] % MOD
    print(ans % MOD)

if __name__ == "__main__":
    main()