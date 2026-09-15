import sys

MOD = 998244353
G = 3


def _prepare_ntt():
    mod = MOD
    g = G
    rank2 = ((mod - 1) & -(mod - 1)).bit_length() - 1

    root = [1] * (rank2 + 1)
    iroot = [1] * (rank2 + 1)
    root[rank2] = pow(g, (mod - 1) >> rank2, mod)
    iroot[rank2] = pow(root[rank2], mod - 2, mod)
    for i in range(rank2 - 1, -1, -1):
        root[i] = root[i + 1] * root[i + 1] % mod
        iroot[i] = iroot[i + 1] * iroot[i + 1] % mod

    rate2 = [1] * (rank2 - 1)
    irate2 = [1] * (rank2 - 1)
    prod = 1
    iprod = 1
    for i in range(rank2 - 1):
        rate2[i] = root[i + 2] * prod % mod
        irate2[i] = iroot[i + 2] * iprod % mod
        prod = prod * iroot[i + 2] % mod
        iprod = iprod * root[i + 2] % mod

    rate3 = [1] * (rank2 - 2)
    irate3 = [1] * (rank2 - 2)
    prod = 1
    iprod = 1
    for i in range(rank2 - 2):
        rate3[i] = root[i + 3] * prod % mod
        irate3[i] = iroot[i + 3] * iprod % mod
        prod = prod * iroot[i + 3] % mod
        iprod = iprod * root[i + 3] % mod

    return root, iroot, rate2, irate2, rate3, irate3


_ROOT, _IROOT, _RATE2, _IRATE2, _RATE3, _IRATE3 = _prepare_ntt()
_INV_CACHE = {}


def _butterfly(a):
    mod = MOD
    n = len(a)
    h = (n - 1).bit_length()
    length = 0
    rate2 = _RATE2
    rate3 = _RATE3
    root = _ROOT

    while length < h:
        if h - length == 1:
            p = 1 << (h - length - 1)
            rot = 1
            for s in range(1 << length):
                offset = s << (h - length)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p] * rot % mod
                    x = l + r
                    if x >= mod:
                        x -= mod
                    y = l - r
                    if y < 0:
                        y += mod
                    a[i + offset] = x
                    a[i + offset + p] = y
                if s + 1 != (1 << length):
                    rot = rot * rate2[(~s & -~s).bit_length() - 1] % mod
            length += 1
        else:
            p = 1 << (h - length - 2)
            rot = 1
            imag = root[2]
            for s in range(1 << length):
                rot2 = rot * rot % mod
                rot3 = rot2 * rot % mod
                offset = s << (h - length)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p] * rot % mod
                    a2 = a[i + offset + p * 2] * rot2 % mod
                    a3 = a[i + offset + p * 3] * rot3 % mod
                    a1na3imag = (a1 - a3) % mod * imag % mod
                    na2 = mod - a2
                    a[i + offset] = (a0 + a2 + a1 + a3) % mod
                    a[i + offset + p] = (a0 + a2 - a1 - a3) % mod
                    a[i + offset + p * 2] = (a0 + na2 + a1na3imag) % mod
                    a[i + offset + p * 3] = (a0 + na2 - a1na3imag) % mod
                if s + 1 != (1 << length):
                    rot = rot * rate3[(~s & -~s).bit_length() - 1] % mod
            length += 2


def _butterfly_inv(a):
    mod = MOD
    n = len(a)
    h = (n - 1).bit_length()
    length = h
    irate2 = _IRATE2
    irate3 = _IRATE3
    iroot = _IROOT

    while length:
        if length == 1:
            p = 1 << (h - length)
            irot = 1
            for s in range(1 << (length - 1)):
                offset = s << (h - length + 1)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p]
                    x = l + r
                    if x >= mod:
                        x -= mod
                    y = l - r
                    if y < 0:
                        y += mod
                    a[i + offset] = x
                    a[i + offset + p] = y * irot % mod
                if s + 1 != (1 << (length - 1)):
                    irot = irot * irate2[(~s & -~s).bit_length() - 1] % mod
            length -= 1
        else:
            p = 1 << (h - length)
            irot = 1
            iimag = iroot[2]
            for s in range(1 << (length - 2)):
                irot2 = irot * irot % mod
                irot3 = irot2 * irot % mod
                offset = s << (h - length + 2)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p]
                    a2 = a[i + offset + p * 2]
                    a3 = a[i + offset + p * 3]
                    a2na3iimag = (a2 - a3) % mod * iimag % mod
                    a[i + offset] = (a0 + a1 + a2 + a3) % mod
                    a[i + offset + p] = (a0 - a1 + a2na3iimag) * irot % mod
                    a[i + offset + p * 2] = (a0 + a1 - a2 - a3) * irot2 % mod
                    a[i + offset + p * 3] = (a0 - a1 - a2na3iimag) * irot3 % mod
                if s + 1 != (1 << (length - 2)):
                    irot = irot * irate3[(~s & -~s).bit_length() - 1] % mod
            length -= 2

    inv_n = _INV_CACHE.get(n)
    if inv_n is None:
        inv_n = pow(n, mod - 2, mod)
        _INV_CACHE[n] = inv_n
    for i in range(n):
        a[i] = a[i] * inv_n % mod


def convolution(a, b):
    mod = MOD
    la = len(a)
    lb = len(b)
    if la == 0 or lb == 0:
        return []

    n = la + lb - 1

    if la == 1:
        av = a[0]
        if av == 1:
            return b[:]
        return [(av * x) % mod for x in b]

    if lb == 1:
        bv = b[0]
        if bv == 1:
            return a[:]
        return [(bv * x) % mod for x in a]

    if la * lb <= 50000:
        if la <= lb:
            small, large = a, b
        else:
            small, large = b, a
        res = [0] * n
        for i, av in enumerate(small):
            if av:
                for j, bv in enumerate(large):
                    res[i + j] += av * bv
        for i in range(n):
            res[i] %= mod
        return res

    z = 1 << (n - 1).bit_length()
    fa = a + [0] * (z - la)
    fb = b + [0] * (z - lb)

    _butterfly(fa)
    _butterfly(fb)
    for i in range(z):
        fa[i] = fa[i] * fb[i] % mod
    _butterfly_inv(fa)

    return fa[:n]


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1].decode()

    # If the first vertex is white or the last vertex is black,
    # that vertex cannot be reached / cannot leave, respectively.
    if S[0] == 'W' or S[-1] == 'B':
        print(0)
        return

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Collect prefix cuts (w, b) with 1 <= b <= w <= N-1.
    # For the same w, only the smallest b matters.
    min_b = [N + 1] * (N + 1)
    w = b = 0
    for ch in S[:-1]:
        if ch == 'W':
            w += 1
        else:
            b += 1
        if b > 0 and w < N and b <= w:
            if b < min_b[w]:
                min_b[w] = b

    # Pareto frontier: keep cuts not dominated by another cut
    # with larger/equal w and smaller/equal b.
    active = []
    cur = N + 1
    for ww in range(N - 1, 0, -1):
        bb = min_b[ww]
        if bb <= ww and bb < cur:
            active.append((ww, bb))
            cur = bb
    active.reverse()

    M = len(active)
    if M == 0:
        print(fact[N])
        return

    w_arr = [x[0] for x in active]
    b_arr = [x[1] for x in active]

    # Small cases: direct O(M^2) recurrence.
    DIRECT_LIMIT = 1800
    if M <= DIRECT_LIMIT:
        C = [0] * M
        for i in range(M):
            wi = w_arr[i]
            s = 0
            for j in range(i):
                s += C[j] * fact[wi - b_arr[j]]
            s %= MOD
            C[i] = (fact[wi] - s) % MOD * invfact[wi - b_arr[i]] % MOD

        bad = 0
        for i in range(M):
            bad = (bad + C[i] * fact[N - b_arr[i]]) % MOD
        print((fact[N] - bad) % MOD)
        return

    C = [0] * M
    Ssum = [0] * M

    BASE = 128
    NAIVE_SMALL = 100000
    NAIVE_CAP = 300000
    NAIVE_FACTOR = 64

    sys.setrecursionlimit(1_000_000)

    def solve(l, r):
        # Base block: compute sequentially and propagate inside the block.
        if r - l + 1 <= BASE:
            fact_l = fact
            invfact_l = invfact
            w_l = w_arr
            b_l = b_arr
            C_l = C
            S_l = Ssum
            mod = MOD

            for i in range(l, r + 1):
                si = S_l[i] % mod
                ci = (fact_l[w_l[i]] - si) % mod
                ci = ci * invfact_l[w_l[i] - b_l[i]] % mod
                C_l[i] = ci

                if ci:
                    bi = b_l[i]
                    for k in range(i + 1, r + 1):
                        S_l[k] += ci * fact_l[w_l[k] - bi]
            return

        mid = (l + r) // 2
        solve(l, mid)

        left_len = mid - l + 1
        right_len = r - mid
        prod = left_len * right_len
        span = (b_arr[mid] - b_arr[l]) + (w_arr[r] - b_arr[l]) + 1
        L = 1 << (span - 1).bit_length()

        # Add contributions from left half to right half.
        if prod <= NAIVE_SMALL or (prod <= NAIVE_CAP and prod <= L * NAIVE_FACTOR):
            fact_l = fact
            S_l = Ssum
            C_l = C
            w_l = w_arr
            b_l = b_arr
            mod = MOD

            for j in range(l, mid + 1):
                cj = C_l[j]
                if cj:
                    bj = b_l[j]
                    for i in range(mid + 1, r + 1):
                        S_l[i] += cj * fact_l[w_l[i] - bj]

            for i in range(mid + 1, r + 1):
                S_l[i] %= mod
        else:
            b0 = b_arr[l]
            LB = b_arr[mid] - b0 + 1
            A = [0] * LB
            C_l = C
            b_l = b_arr
            has = False

            for j in range(l, mid + 1):
                val = C_l[j]
                if val:
                    A[b_l[j] - b0] = val
                    has = True

            if has:
                Ymax = w_arr[r] - b0
                B = fact[:Ymax + 1]
                conv = convolution(A, B)

                S_l = Ssum
                w_l = w_arr
                mod = MOD
                for i in range(mid + 1, r + 1):
                    val = conv[w_l[i] - b0]
                    if val:
                        S_l[i] += val
                        if S_l[i] >= mod:
                            S_l[i] -= mod

        solve(mid + 1, r)

    solve(0, M - 1)

    bad = 0
    for i in range(M):
        bad = (bad + C[i] * fact[N - b_arr[i]]) % MOD

    print((fact[N] - bad) % MOD)


if __name__ == "__main__":
    main()