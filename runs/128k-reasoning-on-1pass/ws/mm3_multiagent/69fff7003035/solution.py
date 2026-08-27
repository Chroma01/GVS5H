import sys

MOD = 998244353
ROOT = 3                     # primitive root of MOD

# ---------- NTT ----------
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
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
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


def multiply(a, b, need=None):
    """convolution of a and b, truncated to at most need coefficients"""
    if not a or not b:
        return [0] * (need if need is not None else 0)
    total_len = len(a) + len(b) - 1
    if need is None:
        need = total_len
    else:
        need = min(need, total_len)
    n = 1
    while n < total_len:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]


# ---------- main ----------
def solve() -> None:
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)

    # factorials and inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # group numbers by decimal length
    max_len = len(str(N))
    cnt = [0] * (max_len + 1)          # c_L
    sum_grp = [0] * (max_len + 1)      # S_L (mod MOD)
    a = [0] * (max_len + 1)            # a_L = 10^L mod MOD

    for L in range(1, max_len + 1):
        low = 10 ** (L - 1)
        high = 10 ** L - 1
        if low > N:
            break
        high = min(high, N)
        c = high - low + 1
        cnt[L] = c
        # arithmetic series sum
        s = (low + high) * c // 2
        sum_grp[L] = s % MOD
        a[L] = pow(10, L, MOD)

    # build F(t) = product_L (1 + a_L t)^{c_L}
    F = [1]                     # start with constant polynomial
    need = N + 1                # we need coefficients 0..N
    for L in range(1, max_len + 1):
        c = cnt[L]
        if c == 0:
            continue
        al = a[L]
        # polynomial (1 + al t)^c  via binomial expansion
        poly = [0] * (c + 1)
        pow_al = 1
        fact_c = fact[c]
        for k in range(c + 1):
            binom = fact_c * inv_fact[k] % MOD * inv_fact[c - k] % MOD
            poly[k] = binom * pow_al % MOD
            pow_al = pow_al * al % MOD
        F = multiply(F, poly, need=need)
    if len(F) < need:
        F += [0] * (need - len(F))

    # build H(t) = Σ_L a_L * S_L * Σ_{m=0}^{N-1} (-a_L)^m t^m
    H = [0] * N
    for L in range(1, max_len + 1):
        if cnt[L] == 0:
            continue
        al = a[L]
        coeff = al * sum_grp[L] % MOD
        cur = 1
        neg_al = (MOD - al) % MOD
        for m in range(N):
            H[m] = (H[m] + coeff * cur) % MOD
            cur = cur * neg_al % MOD

    # R(t) = F(t) * H(t)   (only first N coefficients are needed)
    R = multiply(F, H, need=N)

    # g_k : g_0 = 0, g_k = coefficient of t^{k-1} in R(t)  (k>=1)
    g = [0] * N
    for k in range(1, N):
        g[k] = R[k - 1]

    total_sum = N * (N + 1) // 2 % MOD
    ans = 0
    for k in range(N):
        term = (total_sum * F[k] - g[k]) % MOD
        ans = (ans + fact[k] * fact[N - 1 - k] % MOD * term) % MOD

    print(ans)


if __name__ == "__main__":
    solve()