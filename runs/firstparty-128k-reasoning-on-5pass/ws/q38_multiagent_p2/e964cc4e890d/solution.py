import sys

MOD = 998244353

_fact_cache = {}


def factorials(n):
    if n in _fact_cache:
        return _fact_cache[n]
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    _fact_cache[n] = (fact, invfact)
    return fact, invfact


def build_R(N, S):
    R = [0] * (N + 1)
    w = 0
    b = 0
    for ch in S:
        if ch == 'W':
            w += 1
        else:
            R[b] = w
            b += 1
    R[N] = N
    return R


def get_R_info(N, S):
    R = build_R(N, S)

    L = 0
    for b in range(N, 0, -1):
        if R[b] == b:
            L += 1
        else:
            break

    M = 1  # final b = N is always present for valid endpoint strings
    for b in range(1, N):
        if R[b] > R[b - 1] and R[b] >= b:
            M += 1

    best = 0
    cur = 0
    curc = None
    for b in range(1, N + 1):
        db = R[b] - b
        if db >= 0:
            if curc is None:
                curc = db
                cur = 1
            elif db == curc:
                cur += 1
            else:
                if cur > best:
                    best = cur
                curc = db
                cur = 1
        else:
            if cur > best:
                best = cur
            cur = 0
            curc = None
    if cur > best:
        best = cur

    return R, L, M, best


# ---------------- NTT (AtCoder-style butterfly) ----------------

_rate2 = None
_irate2 = None
_inv_pow2 = None


def ensure_ntt():
    global _rate2, _irate2, _inv_pow2
    if _rate2 is not None:
        return

    cnt2 = 23
    e = pow(3, (MOD - 1) >> cnt2, MOD)
    ie = pow(e, MOD - 2, MOD)

    es = [0] * cnt2
    ies = [0] * cnt2
    for i in range(cnt2 - 1, -1, -1):
        es[i] = e
        ies[i] = ie
        e = e * e % MOD
        ie = ie * ie % MOD

    rate2 = [0] * cnt2
    irate2 = [0] * cnt2
    prod = 1
    iprod = 1
    for i in range(cnt2):
        rate2[i] = es[i] * prod % MOD
        irate2[i] = ies[i] * iprod % MOD
        prod = prod * ies[i] % MOD
        iprod = iprod * es[i] % MOD

    _rate2 = rate2
    _irate2 = irate2

    inv = [1] * (cnt2 + 1)
    for i in range(1, cnt2 + 1):
        inv[i] = pow(1 << i, MOD - 2, MOD)
    _inv_pow2 = inv


def butterfly(a):
    n = len(a)
    h = n.bit_length() - 1
    mod = MOD
    rate2 = _rate2

    for ph in range(1, h + 1):
        w = 1 << (h - ph)
        p = 1 << (ph - 1)
        now = 1
        rt = rate2[ph - 1]
        for s in range(p):
            offset = s * (w << 1)
            end = offset + w
            for i in range(offset, end):
                l = a[i]
                r = a[i + w] * now % mod
                x = l + r
                if x >= mod:
                    x -= mod
                y = l - r
                if y < 0:
                    y += mod
                a[i] = x
                a[i + w] = y
            now = now * rt % mod


def butterfly_inv(a):
    n = len(a)
    h = n.bit_length() - 1
    mod = MOD
    irate2 = _irate2

    for ph in range(h, 0, -1):
        w = 1 << (h - ph)
        p = 1 << (ph - 1)
        inow = 1
        rt = irate2[ph - 1]
        for s in range(p):
            offset = s * (w << 1)
            end = offset + w
            for i in range(offset, end):
                l = a[i]
                r = a[i + w]
                x = l + r
                if x >= mod:
                    x -= mod
                y = l - r
                if y < 0:
                    y += mod
                a[i] = x
                a[i + w] = y * inow % mod
            inow = inow * rt % mod


# ---------------- Generic convolution slice ----------------

DIRECT_CONV = 50000


def convolve_slice(a, b, len_b, start, length):
    """Return (a * b)[start : start+length].  b is used only up to len_b."""
    if length <= 0:
        return []
    n = len(a)
    m = len_b
    if n == 0 or m == 0:
        return [0] * length

    if len(b) < m:
        b = b + [0] * (m - len(b))

    full = n + m - 1
    if start >= full:
        return [0] * length

    if min(n, m) <= 32 or n * m <= DIRECT_CONV:
        res = [0] * length
        for i, ai in enumerate(a):
            if ai:
                js = max(0, start - i)
                je = min(m, start + length - i)
                if js < je:
                    base = i - start
                    for j in range(js, je):
                        res[base + j] += ai * b[j]
        for i in range(length):
            res[i] %= MOD
        return res

    ensure_ntt()
    z = 1 << ((full - 1).bit_length())

    fa = a + [0] * (z - n)
    fb = b[:m]
    fb.extend([0] * (z - len(fb)))

    butterfly(fa)
    butterfly(fb)

    mod = MOD
    fa = [x * y % mod for x, y in zip(fa, fb)]
    del fb

    butterfly_inv(fa)
    invz = _inv_pow2[z.bit_length() - 1]

    end = min(start + length, z)
    res = [fa[i] * invz % mod for i in range(start, end)]
    if len(res) < length:
        res.extend([0] * (length - len(res)))
    return res


# ---------------- Polynomial inverse ----------------

def poly_inv(f, n):
    """Inverse of f modulo x^n.  f[0] must be nonzero."""
    if n == 0:
        return []
    mod = MOD

    if n <= 1000:
        g = [pow(f[0], mod - 2, mod)]
        flen = len(f)
        for i in range(1, n):
            s = 0
            lim = i if i < flen else flen
            for j in range(1, lim + 1):
                s += f[j] * g[i - j]
            g[i] = (-s % mod) * g[0] % mod
        return g

    g = [pow(f[0], mod - 2, mod)]
    m = 1

    while m < n:
        m2 = min(m * 2, n)

        if m2 * m <= 20000:
            t = [0] * m2
            for i, gi in enumerate(g):
                if gi:
                    lim = min(m2 - i, len(f))
                    for j in range(lim):
                        t[i + j] += gi * f[j]
            for i in range(m2):
                t[i] %= mod

            e = [0] * m2
            e[0] = (2 - t[0]) % mod
            for i in range(1, m2):
                e[i] = (-t[i]) % mod

            g_new = [0] * m2
            for i, gi in enumerate(g):
                if gi:
                    lim = min(m2 - i, m2)
                    for j in range(lim):
                        g_new[i + j] += gi * e[j]
            for i in range(m2):
                g_new[i] %= mod
            g = g_new
            m = m2
            continue

        ensure_ntt()
        full = m2 + m - 1
        z = 1 << ((full - 1).bit_length())

        fa = f[:m2]
        fa.extend([0] * (z - len(fa)))
        ga = g + [0] * (z - m)

        butterfly(fa)
        butterfly(ga)

        fa = [x * y % mod for x, y in zip(fa, ga)]
        butterfly_inv(fa)

        invz = _inv_pow2[z.bit_length() - 1]

        fa[0] = (2 - fa[0] * invz) % mod
        for i in range(1, m2):
            fa[i] = (-fa[i] * invz) % mod
        for i in range(m2, z):
            fa[i] = 0

        butterfly(fa)
        ga = [x * y % mod for x, y in zip(ga, fa)]
        butterfly_inv(ga)

        g = [ga[i] * invz % mod for i in range(m2)]
        m = m2

    return g


# ---------------- CDQ solver for the renewal recurrence ----------------

g_b = None
g_r = None
g_B = None
g_sum = None
g_fact = None
g_invfact = None

DIRECT_PROD = 100000
DIRECT_D = 500000
DIRECT_M = 1500
CDQ_DIRECT = 128


def add_cross(l, mid, r, cnt_left, minb, maxb):
    right_len = r - mid

    LA = maxb - minb + 1
    rL = g_r[mid + 1]
    rR = g_r[r]
    D = rL - maxb
    LB = rR - minb - D + 1

    if cnt_left * right_len <= DIRECT_PROD:
        B_loc = g_B
        b_loc = g_b
        S_loc = g_sum
        r_loc = g_r
        fact_loc = g_fact
        mod = MOD

        nz_b = []
        nz_v = []
        for j in range(l, mid + 1):
            val = B_loc[j]
            if val:
                nz_b.append(b_loc[j])
                nz_v.append(val)

        if not nz_b:
            return

        nz_len = len(nz_b)
        if nz_len == 1:
            bj = nz_b[0]
            Bj = nz_v[0]
            for i in range(mid + 1, r + 1):
                S_loc[i] = (S_loc[i] + Bj * fact_loc[r_loc[i] - bj]) % mod
        elif nz_len <= right_len:
            for i in range(mid + 1, r + 1):
                ri = r_loc[i]
                s = S_loc[i]
                for idx in range(nz_len):
                    s += nz_v[idx] * fact_loc[ri - nz_b[idx]]
                S_loc[i] = s % mod
        else:
            for idx in range(nz_len):
                bj = nz_b[idx]
                Bj = nz_v[idx]
                for i in range(mid + 1, r + 1):
                    S_loc[i] += Bj * fact_loc[r_loc[i] - bj]
            for i in range(mid + 1, r + 1):
                S_loc[i] %= mod
        return

    ensure_ntt()

    need = LA + LB - 1
    z = 1 << ((need - 1).bit_length())

    A = [0] * LA
    B_loc = g_B
    b_loc = g_b
    for j in range(l, mid + 1):
        val = B_loc[j]
        if val:
            A[b_loc[j] - minb] = val

    fa = A
    fa.extend([0] * (z - LA))

    fb = g_fact[D:D + LB]
    fb.extend([0] * (z - len(fb)))

    butterfly(fa)
    butterfly(fb)

    mod = MOD
    fa = [x * y % mod for x, y in zip(fa, fb)]
    del fb

    butterfly_inv(fa)

    invz = _inv_pow2[z.bit_length() - 1]
    S_loc = g_sum
    r_loc = g_r
    base = LA - 1

    for i in range(mid + 1, r + 1):
        idx = base + (r_loc[i] - rL)
        val = fa[idx] * invz % mod
        s = S_loc[i] + val
        if s >= mod:
            s -= mod
        S_loc[i] = s


def cdq(l, r):
    if l == r:
        ri = g_r[l]
        val = (g_fact[ri] - g_sum[l]) % MOD
        val = val * g_invfact[ri - g_b[l]] % MOD
        g_B[l] = val
        if val:
            return 1, g_b[l], g_b[l]
        return 0, 0, -1

    if r - l + 1 <= CDQ_DIRECT:
        B_loc = g_B
        b_loc = g_b
        r_loc = g_r
        S_loc = g_sum
        fact_loc = g_fact
        inv_loc = g_invfact
        mod = MOD

        cnt = 0
        minb = 0
        maxb = -1
        active = []
        for i in range(l, r + 1):
            ri = r_loc[i]
            s = S_loc[i]
            for j in active:
                s += B_loc[j] * fact_loc[ri - b_loc[j]]
            s %= mod
            val = (fact_loc[ri] - s) % mod
            val = val * inv_loc[ri - b_loc[i]] % mod
            B_loc[i] = val
            if val:
                cnt += 1
                bi = b_loc[i]
                if minb == 0 or bi < minb:
                    minb = bi
                if bi > maxb:
                    maxb = bi
                active.append(i)
        return cnt, minb, maxb

    mid = (l + r) >> 1
    cnt1, minb1, maxb1 = cdq(l, mid)
    if cnt1:
        add_cross(l, mid, r, cnt1, minb1, maxb1)

    cnt2, minb2, maxb2 = cdq(mid + 1, r)

    cnt = cnt1 + cnt2
    if cnt1:
        minb = minb1
        maxb = maxb1
    else:
        minb = 0
        maxb = -1

    if cnt2:
        if cnt1 == 0:
            minb = minb2
            maxb = maxb2
        else:
            if minb2 < minb:
                minb = minb2
            if maxb2 > maxb:
                maxb = maxb2

    return cnt, minb, maxb


def cdq_solve(b_arr, r_arr, init_sum, fact, invfact):
    M = len(b_arr)
    if M == 0:
        return []

    global g_b, g_r, g_B, g_sum, g_fact, g_invfact
    g_b = b_arr
    g_r = r_arr
    g_B = [0] * M
    g_sum = init_sum[:]
    g_fact = fact
    g_invfact = invfact

    sys.setrecursionlimit(1_000_000)
    cdq(0, M - 1)
    return g_B


def compute_D(pref_nz, s, L, fact):
    """D[s+k] = sum_{a<s} C_a fact[s+k-a]."""
    if L <= 0:
        return []
    if not pref_nz:
        return [0] * L

    if len(pref_nz) * L <= DIRECT_D:
        D = [0] * L
        if len(pref_nz) <= L:
            for k in range(L):
                sm = 0
                for b, c in pref_nz:
                    sm += c * fact[s + k - b]
                D[k] = sm % MOD
        else:
            for b, c in pref_nz:
                base = s - b
                for k in range(L):
                    D[k] += c * fact[base + k]
            for k in range(L):
                D[k] %= MOD
        return D

    P = s - 1
    A = [0] * (P + 1)
    for b, c in pref_nz:
        A[b] = c

    return convolve_slice(A, fact, len(fact), s, L)


def compute_init(pref_nz, b_arr, r_arr, fact, N):
    M = len(b_arr)
    init = [0] * M
    if M == 0 or not pref_nz:
        return init

    if len(pref_nz) * M <= DIRECT_D:
        for i in range(M):
            r = r_arr[i]
            sm = 0
            for a, c in pref_nz:
                sm += c * fact[r - a]
            init[i] = sm % MOD
        return init

    max_a = max(b for b, _ in pref_nz)
    A = [0] * (max_a + 1)
    for a, c in pref_nz:
        A[a] = c

    minR = r_arr[0]
    maxR = r_arr[-1]
    conv = convolve_slice(A, fact, N + 1, minR, maxR - minR + 1)
    for i, r in enumerate(r_arr):
        init[i] = conv[r - minR]
    return init


def build_b_arr(R, start, end, include_final):
    N = len(R) - 1
    b_arr = []
    r_arr = []
    for b in range(start, end + 1):
        if R[b] > R[b - 1] and R[b] >= b:
            b_arr.append(b)
            r_arr.append(R[b])
    if include_final and end == N:
        if not b_arr or b_arr[-1] != N:
            b_arr.append(N)
            r_arr.append(N)
    return b_arr, r_arr


def solve_range_cdq(N, R, fact, invfact, start, end, pref_nz, include_final=False):
    if start > end:
        return [], []

    b_arr, r_arr = build_b_arr(R, start, end, include_final)
    M = len(b_arr)
    if M == 0:
        return [], []

    init = compute_init(pref_nz, b_arr, r_arr, fact, N)

    if M <= DIRECT_M:
        B = [0] * M
        active = []
        for i in range(M):
            b = b_arr[i]
            r = r_arr[i]
            s = init[i]
            for j in active:
                s += B[j] * fact[r - b_arr[j]]
            s %= MOD
            val = (fact[r] - s) % MOD
            val = val * invfact[r - b] % MOD
            B[i] = val
            if val:
                active.append(i)
        nz = [(b_arr[i], B[i]) for i in range(M) if B[i]]
        return B, nz

    B = cdq_solve(b_arr, r_arr, init, fact, invfact)
    nz = [(b_arr[i], B[i]) for i in range(M) if B[i]]
    return B, nz


def solve_suffix_fps(N, s, L, pref_nz, fact):
    """Solve a final suffix R_b = b for b = s..N."""
    if L <= 0:
        return 0
    D = compute_D(pref_nz, s, L, fact)
    H = poly_inv(fact, L)

    ans = 0
    for k in range(L):
        e = fact[N - k] - D[L - 1 - k]
        if e < 0:
            e += MOD
        ans = (ans + H[k] * e) % MOD
    return ans


def suffix_min(N):
    return max(2000, N // 10)


def run_min(N):
    return max(5000, N // 20)


def solve_remaining(N, R, fact, invfact, start, pref_nz, L_zero):
    if start > N:
        return 0

    s0 = N - L_zero + 1
    Lrem = N - s0 + 1

    if Lrem >= suffix_min(N):
        if s0 <= start:
            return solve_suffix_fps(N, start, N - start + 1, pref_nz, fact)
        else:
            if start <= s0 - 1:
                _, nzmid = solve_range_cdq(N, R, fact, invfact, start, s0 - 1, pref_nz, include_final=False)
                pref_nz = pref_nz + nzmid
            return solve_suffix_fps(N, s0, Lrem, pref_nz, fact)
    else:
        B, _ = solve_range_cdq(N, R, fact, invfact, start, N, pref_nz, include_final=True)
        return B[-1] % MOD if B else 0


def find_longest_run(N, R):
    best_l = best_r = best_len = 0
    cur_l = 0
    cur_c = None
    cur_len = 0

    for b in range(1, N + 1):
        db = R[b] - b
        if db >= 0:
            if cur_c is None:
                cur_l = b
                cur_c = db
                cur_len = 1
            elif db == cur_c:
                cur_len += 1
            else:
                if cur_len > best_len:
                    best_l, best_r, best_len = cur_l, b - 1, cur_len
                cur_l = b
                cur_c = db
                cur_len = 1
        else:
            if cur_len > best_len:
                best_l, best_r, best_len = cur_l, b - 1, cur_len
            cur_c = None
            cur_len = 0

    if cur_len > best_len:
        best_l, best_r, best_len = cur_l, N, cur_len

    return best_l, best_r, best_len


def try_long_constant_run(N, R, fact, invfact, L_zero):
    l, r, Lr = find_longest_run(N, R)
    if Lr < run_min(N):
        return None

    c = R[l] - l

    nz_prev = []
    if l > 1:
        _, nz_prev = solve_range_cdq(N, R, fact, invfact, 1, l - 1, [], include_final=False)

    # If this is the final zero suffix, the dedicated suffix FPS is slightly cheaper.
    if r == N and c == 0:
        return solve_suffix_fps(N, l, N - l + 1, nz_prev, fact)

    b_arr = list(range(l, r + 1))
    r_arr = [R[b] for b in b_arr]
    init = compute_init(nz_prev, b_arr, r_arr, fact, N)

    V = [0] * Lr
    for k in range(Lr):
        val = fact[R[l + k]] - init[k]
        if val < 0:
            val += MOD
        V[k] = val

    K = fact[c:c + Lr]
    if len(K) < Lr:
        K.extend([0] * (Lr - len(K)))
    H = poly_inv(K, Lr)
    A = convolve_slice(V, H, Lr, 0, Lr)

    if r == N:
        return A[-1] % MOD

    nz_run = [(l + k, A[k]) for k in range(Lr) if A[k]]
    nz = nz_prev + nz_run
    return solve_remaining(N, R, fact, invfact, r + 1, nz, L_zero)


def solve_fast(N, S):
    if N == 0:
        return 1
    if S[0] == 'W' or S[-1] == 'B':
        return 0

    fact, invfact = factorials(N)

    # The problem is invariant under reversing the line and swapping W/B.
    # Choose the orientation with the smaller estimated CDQ workload.
    R1, L1, M1, run1 = get_R_info(N, S)
    S2 = ''.join('W' if c == 'B' else 'B' for c in reversed(S))
    R2, L2, M2, run2 = get_R_info(N, S2)

    cost1 = (max(0, M1 - max(L1, run1)), M1, -L1)
    cost2 = (max(0, M2 - max(L2, run2)), M2, -L2)

    if cost2 < cost1:
        R = R2
        L = L2
    else:
        R = R1
        L = L1

    ans = try_long_constant_run(N, R, fact, invfact, L)
    if ans is not None:
        return ans

    return solve_remaining(N, R, fact, invfact, 1, [], L)


def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return

    N = int(data[0])
    S = data[1].decode().strip()

    ans = solve_fast(N, S)
    print(ans)


if __name__ == "__main__":
    main()