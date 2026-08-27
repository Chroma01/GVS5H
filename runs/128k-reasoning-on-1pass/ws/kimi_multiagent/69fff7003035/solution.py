import sys
import numpy as np

MOD = 998244353
G = 3

def main():
    data = sys.stdin.read().split()
    N = int(data[0])

    # ---- group values 1..N by digit length ----
    c = [0] * 7          # count of numbers with L digits
    s = [0] * 7          # sum (mod MOD) of numbers with L digits
    for L in range(1, 7):
        lo = 10 ** (L - 1)
        if lo > N:
            break
        hi = min(N, 10 ** L - 1)
        cnt = hi - lo + 1
        c[L] = cnt
        s[L] = (lo + hi) * cnt // 2 % MOD

    # ---- factorials / inverse factorials ----
    fact = np.empty(N + 1, dtype=np.int64)
    fact[0] = 1
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = np.empty(N + 1, dtype=np.int64)
    invfact[N] = pow(int(fact[N]), MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # ---- NTT setup ----
    size = 1
    while size < N + 1:
        size <<= 1
    logn = size.bit_length() - 1

    rev = np.arange(size, dtype=np.int64)
    rev = ((rev & 0x55555555) << 1) | ((rev >> 1) & 0x55555555)
    rev = ((rev & 0x33333333) << 2) | ((rev >> 2) & 0x33333333)
    rev = ((rev & 0x0F0F0F0F) << 4) | ((rev >> 4) & 0x0F0F0F0F)
    rev = ((rev & 0x00FF00FF) << 8) | ((rev >> 8) & 0x00FF00FF)
    rev = ((rev << 16) | (rev >> 16)) & 0xFFFFFFFF
    rev >>= (32 - logn)

    def pw_array(w, m):
        """return [w^0, w^1, ..., w^(m-1)] mod MOD"""
        res = np.empty(m, dtype=np.int64)
        res[0] = 1
        i = 1
        wi = w
        while i < m:
            res[i:2 * i] = res[:i] * wi % MOD
            wi = wi * wi % MOD
            i <<= 1
        return res

    stage_cache = {}

    def get_ws(length, invert):
        key = (length, invert)
        if key not in stage_cache:
            wlen = pow(G, (MOD - 1) // length, MOD)
            if invert:
                wlen = pow(wlen, MOD - 2, MOD)
            stage_cache[key] = pw_array(wlen, length >> 1)
        return stage_cache[key]

    def ntt(a, invert):
        a = a[rev]                      # bit-reversed copy
        length = 2
        while length <= size:
            half = length >> 1
            ws = get_ws(length, invert)
            a2 = a.reshape(-1, length)
            left = a2[:, :half]
            right = a2[:, half:]
            b = right * ws % MOD
            x = left + b
            x -= np.where(x >= MOD, MOD, 0)
            y = left - b
            y += np.where(y < 0, MOD, 0)
            a2[:, :half] = x
            a2[:, half:] = y
            length <<= 1
        if invert:
            a = a * pow(size, MOD - 2, MOD) % MOD
        return a

    # ---- E(t) = prod_L (1 + 10^L t)^{c_L}, via pointwise product in NTT domain ----
    acc = None
    for L in range(1, 7):
        cnt = c[L]
        if cnt == 0:
            continue
        a = pow(10, L, MOD)
        j = np.arange(cnt + 1, dtype=np.int64)
        coeff = fact[cnt] * invfact[cnt - j] % MOD * invfact[j] % MOD
        coeff = coeff * pw_array(a, cnt + 1) % MOD
        f = np.zeros(size, dtype=np.int64)
        f[:cnt + 1] = coeff
        F = ntt(f, False)
        acc = F if acc is None else acc * F % MOD

    e = ntt(acc, True)[:N + 1]          # elementary symmetric sums e_k of {10^{d_u}}

    # ---- weights fact[k] * fact[N-1-k], k = 0..N-1 ----
    factN1 = fact[:N]
    w = factN1 * factN1[::-1] % MOD

    # ---- for each digit length L: H = E / (1 + a t), g_L = sum_k w_k h_k ----
    ans = 0
    for L in range(1, 7):
        if c[L] == 0:
            continue
        a = pow(10, L, MOD)
        inv_a = pow(a, MOD - 2, MOD)
        neg_inv_a = (MOD - inv_a) % MOD
        pw1 = pw_array(neg_inv_a, N + 1)            # (-a)^{-i}
        prefix = np.cumsum(e * pw1 % MOD) % MOD     # sum_{i<=k} e_i (-a)^{-i}
        neg_a = (MOD - a) % MOD
        pw2 = pw_array(neg_a, N + 1)                # (-a)^k
        h = pw2 * prefix % MOD                      # h_k = (-a)^k * prefix_k
        g = int(np.sum(w * h[:N] % MOD) % MOD)
        ans = (ans + s[L] * g) % MOD

    print(ans)

main()