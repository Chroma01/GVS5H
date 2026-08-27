import sys
import numpy as np

MOD = 998244353
PRIMITIVE_ROOT = 3

# ---------------- NTT (numpy-vectorized, mod 998244353) ----------------

_ntt_cache = {}

def _ntt_precompute(n):
    """Return (bit-reversal permutation, forward roots dict, inverse roots dict) for size n."""
    if n in _ntt_cache:
        return _ntt_cache[n]
    logn = n.bit_length() - 1
    arr = np.arange(n, dtype=np.int64)
    rev = np.zeros(n, dtype=np.int64)
    for i in range(logn):
        rev |= ((arr >> i) & 1) << (logn - 1 - i)
    roots_f = {}
    roots_i = {}
    length = 2
    while length <= n:
        w = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        roots_f[length] = w
        roots_i[length] = pow(w, MOD - 2, MOD)
        length *= 2
    _ntt_cache[n] = (rev, roots_f, roots_i)
    return _ntt_cache[n]

def _ntt(a, invert, pre):
    """NTT of array a (size n = power of two); returns transformed numpy int64 array."""
    rev, roots_f, roots_i = pre
    n = a.shape[0]
    a = a[rev]  # bit-reversed copy
    length = 2
    while length <= n:
        h = length // 2
        wlen = (roots_i if invert else roots_f)[length]
        # wpow[j] = wlen^j, j = 0..h-1
        wpow = np.empty(h, dtype=np.int64)
        wpow[0] = 1
        if h > 1:
            wpow[1:] = np.multiply.accumulate(np.full(h - 1, wlen, dtype=np.int64)) % MOD
        X = a.reshape(-1, 2, h)
        u = X[:, 0, :]
        v = X[:, 1, :] * wpow % MOD
        X[:, 0, :] = (u + v) % MOD
        X[:, 1, :] = (u - v) % MOD
        length *= 2
    if invert:
        a = a * pow(n, MOD - 2, MOD) % MOD
    return a

def _multiply(a, b, need):
    """Multiply polynomials a, b (lists/arrays of residues); return first `need` coefficients."""
    size = len(a) + len(b) - 1
    n = 1
    while n < size:
        n <<= 1
    pre = _ntt_precompute(n)
    fa = np.zeros(n, dtype=np.int64)
    fb = np.zeros(n, dtype=np.int64)
    fa[:len(a)] = a
    fb[:len(b)] = b
    fa = _ntt(fa, False, pre)
    fb = _ntt(fb, False, pre)
    fa = fa * fb % MOD
    fa = _ntt(fa, True, pre)
    return fa[:need]

# ---------------- main ----------------

def main():
    data = sys.stdin.read().split()
    N = int(data[0])

    # factorials / inverse factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    inv2 = (MOD + 1) // 2

    # digit-length groups among 1..N
    groups = []  # (d, count, value_sum_mod, x = 10^d mod MOD)
    d = 1
    while True:
        lo = 10 ** (d - 1)
        if lo > N:
            break
        hi = min(10 ** d - 1, N)
        c = hi - lo + 1
        vsum = (lo + hi) % MOD * (c % MOD) % MOD * inv2 % MOD
        x = pow(10, d, MOD)
        groups.append((d, c, vsum, x))
        d += 1

    # Build group polynomials A_d[j] = C(c_d, j) * x_d^j, j = 0..min(c_d, N-1)
    polys = []
    for (d, c, vsum, x) in groups:
        m = min(c, N - 1)
        ad = [1] * (m + 1)
        xj = 1
        fc = fact[c]
        for j in range(1, m + 1):
            xj = xj * x % MOD
            ad[j] = fc * invfact[j] % MOD * invfact[c - j] % MOD * xj % MOD
        polys.append(ad)

    # E(t) = product of A_d(t), truncated to N coefficients (degrees 0..N-1)
    polys.sort(key=len)
    E = polys[0]
    for p in polys[1:]:
        E = _multiply(E, p, N)
    e = [int(v) for v in E[:N]]
    if len(e) < N:
        e += [0] * (N - len(e))

    # w_k = k! * (N-1-k)!, k = 0..N-1
    w = [fact[k] * fact[N - 1 - k] % MOD for k in range(N)]
    w_arr = np.array(w, dtype=np.int64)

    # For each group g: eg_k = e_k - x_g * eg_{k-1}  (coefficients of E/(1+x_g t))
    # U_g = sum_k eg_k * w_k ; answer = sum_g vsum_g * U_g
    ans = 0
    for (d, c, vsum, x) in groups:
        prev = 0
        eg = [0] * N
        for k in range(N):
            cur = e[k] - x * prev % MOD
            eg[k] = cur
            prev = cur
        eg_arr = np.array(eg, dtype=np.int64)
        U = int((eg_arr * w_arr % MOD).sum() % MOD)
        ans = (ans + vsum * U) % MOD

    print(ans)

main()