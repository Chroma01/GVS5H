import sys
import gc
from bisect import bisect_left, bisect_right

MOD = 998244353
G = 3


def solve_one(N, S):
    if isinstance(S, str):
        S = S.encode()

    # Necessary endpoint conditions.
    if S[0] != 66 or S[-1] != 87:  # 'B', 'W'
        return 0

    if N == 1:
        return 1

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Keep only first occurrences of distinct q values with q >= L.
    pairs = []
    black = 0
    white = 0
    last_q = -1

    for ch in S:
        if ch == 66:  # 'B'
            black += 1
            if black >= 2:
                q = white
                if q != last_q:
                    L = black - 1
                    if q >= L:
                        pairs.append((q, L))
                    last_q = q
        else:
            white += 1

    M = len(pairs)
    if M == 0:
        return fact[N]

    T = [0] * M
    L = [0] * M
    for i, (t, l) in enumerate(pairs):
        T[i] = t
        L[i] = l

    # For small M, plain O(M^2) is faster than setting up transforms.
    SMALL_M = 4000
    if M <= SMALL_M:
        C = [0] * M
        mod = MOD
        f = fact
        invf = invfact
        TT = T
        LL = L

        for i in range(M):
            total = 0
            ti = TT[i]
            for j in range(i):
                c = C[j]
                if c:
                    total += c * f[ti - LL[j]] % mod
                    if total >= mod:
                        total -= mod

            val = f[ti] - total
            if val < 0:
                val += mod
            C[i] = val * invf[ti - LL[i]] % mod

        ans = fact[N]
        for i in range(M):
            c = C[i]
            if c:
                ans -= c * fact[N - LL[i]] % mod
                if ans < 0:
                    ans += mod
        return ans

    # ---------- NTT (AtCoder-style radix-4 butterfly) ----------
    max_ntt = 1
    while max_ntt < 2 * N + 5:
        max_ntt <<= 1
    max_log = max_ntt.bit_length() - 1

    cnt2 = ((MOD - 1) & -(MOD - 1)).bit_length() - 1
    sum_e = [0] * 30
    sum_ie = [0] * 30
    es = [0] * 30
    ies = [0] * 30

    e = pow(G, (MOD - 1) >> cnt2, MOD)
    ie = pow(e, MOD - 2, MOD)
    for i in range(cnt2, 1, -1):
        es[i - 2] = e
        ies[i - 2] = ie
        e = e * e % MOD
        ie = ie * ie % MOD

    now = 1
    inow = 1
    for i in range(cnt2 - 1):
        sum_e[i] = es[i] * now % MOD
        sum_ie[i] = ies[i] * inow % MOD
        now = now * ies[i] % MOD
        inow = inow * es[i] % MOD

    # Explicit primitive 4th root.
    imag = pow(G, (MOD - 1) // 4, MOD)
    iimag = pow(imag, MOD - 2, MOD)

    inv_sizes = [1] * (max_log + 1)
    inv2 = (MOD + 1) // 2
    for i in range(1, max_log + 1):
        inv_sizes[i] = inv_sizes[i - 1] * inv2 % MOD

    # Precompute ctz for rotation updates.
    bsf = [0] * (max_ntt // 2 + 2)
    for i in range(1, len(bsf)):
        bsf[i] = (i & -i).bit_length() - 1

    def butterfly(a):
        n = len(a)
        if n == 1:
            return

        h = (n - 1).bit_length()
        length = 0
        mod = MOD
        se = sum_e
        im = imag
        bf = bsf

        while length < h:
            if h - length == 1:
                p = 1 << (h - length - 1)
                limit = 1 << length
                shift = h - length
                rot = 1

                for s in range(limit):
                    offset = s << shift
                    end = offset + p

                    for idx in range(offset, end):
                        l = a[idx]
                        r = a[idx + p] * rot % mod

                        x = l + r
                        if x >= mod:
                            x -= mod
                        y = l - r
                        if y < 0:
                            y += mod

                        a[idx] = x
                        a[idx + p] = y

                    if s + 1 != limit:
                        rot = rot * se[bf[s + 1]] % mod

                length += 1

            else:
                p = 1 << (h - length - 2)
                limit = 1 << length
                shift = h - length
                rot = 1

                for s in range(limit):
                    rot2 = rot * rot % mod
                    rot3 = rot2 * rot % mod
                    offset = s << shift
                    end = offset + p

                    for idx in range(offset, end):
                        a0 = a[idx]
                        a1 = a[idx + p] * rot % mod
                        a2 = a[idx + 2 * p] * rot2 % mod
                        a3 = a[idx + 3 * p] * rot3 % mod

                        a1na3 = a1 - a3
                        if a1na3 < 0:
                            a1na3 += mod
                        a1na3imag = a1na3 * im % mod

                        t0 = a0 + a2
                        if t0 >= mod:
                            t0 -= mod
                        t1 = a1 + a3
                        if t1 >= mod:
                            t1 -= mod
                        t2 = a0 - a2
                        if t2 < 0:
                            t2 += mod

                        x = t0 + t1
                        if x >= mod:
                            x -= mod
                        a[idx] = x

                        x = t0 - t1
                        if x < 0:
                            x += mod
                        a[idx + p] = x

                        x = t2 + a1na3imag
                        if x >= mod:
                            x -= mod
                        a[idx + 2 * p] = x

                        x = t2 - a1na3imag
                        if x < 0:
                            x += mod
                        a[idx + 3 * p] = x

                    if s + 1 != limit:
                        rot = rot * se[bf[s + 1]] % mod

                length += 2

    def butterfly_inv(a):
        n = len(a)
        if n == 1:
            return

        h = (n - 1).bit_length()
        length = h
        mod = MOD
        sie = sum_ie
        im = iimag
        bf = bsf

        while length:
            if length == 1:
                p = 1 << (h - length)
                limit = 1 << (length - 1)
                shift = h - length + 1
                irot = 1

                for s in range(limit):
                    offset = s << shift
                    end = offset + p

                    for idx in range(offset, end):
                        l = a[idx]
                        r = a[idx + p]

                        x = l + r
                        if x >= mod:
                            x -= mod
                        y = l - r
                        if y < 0:
                            y += mod

                        a[idx] = x
                        a[idx + p] = y * irot % mod

                    if s + 1 != limit:
                        irot = irot * sie[bf[s + 1]] % mod

                length -= 1

            else:
                p = 1 << (h - length)
                limit = 1 << (length - 2)
                shift = h - length + 2
                irot = 1

                for s in range(limit):
                    irot2 = irot * irot % mod
                    irot3 = irot2 * irot % mod
                    offset = s << shift
                    end = offset + p

                    for idx in range(offset, end):
                        a0 = a[idx]
                        a1 = a[idx + p]
                        a2 = a[idx + 2 * p]
                        a3 = a[idx + 3 * p]

                        a2na3 = a2 - a3
                        if a2na3 < 0:
                            a2na3 += mod
                        a2na3iimag = a2na3 * im % mod

                        x01 = a0 + a1
                        if x01 >= mod:
                            x01 -= mod
                        y23 = a2 + a3
                        if y23 >= mod:
                            y23 -= mod

                        x = x01 + y23
                        if x >= mod:
                            x -= mod
                        a[idx] = x

                        x = a0 - a1
                        if x < 0:
                            x += mod
                        x += a2na3iimag
                        if x >= mod:
                            x -= mod
                        a[idx + p] = x * irot % mod

                        x = x01 - y23
                        if x < 0:
                            x += mod
                        a[idx + 2 * p] = x * irot2 % mod

                        x = a0 - a1
                        if x < 0:
                            x += mod
                        x -= a2na3iimag
                        if x < 0:
                            x += mod
                        a[idx + 3 * p] = x * irot3 % mod

                    if s + 1 != limit:
                        irot = irot * sie[bf[s + 1]] % mod

                length -= 2

        iz = inv_sizes[h]
        for i in range(n):
            a[i] = a[i] * iz % mod

    def convolution(a, b):
        la = len(a)
        lb = len(b)
        if la == 0 or lb == 0:
            return []

        if la == 1:
            c = a[0]
            if c == 0:
                return [0] * lb
            return [(c * x) % MOD for x in b]

        if lb == 1:
            c = b[0]
            if c == 0:
                return [0] * la
            return [(c * x) % MOD for x in a]

        if la * lb <= 6000:
            if la > lb:
                a, b = b, a
                la, lb = lb, la

            res = [0] * (la + lb - 1)
            mod = MOD
            for i in range(la):
                ai = a[i]
                if ai:
                    for j in range(lb):
                        res[i + j] = (res[i + j] + ai * b[j]) % mod
            return res

        need = la + lb - 1
        n = 1 << (need - 1).bit_length()

        fa = a + [0] * (n - la)
        fb = b + [0] * (n - lb)

        butterfly(fa)
        butterfly(fb)

        mod = MOD
        for i in range(n):
            fa[i] = fa[i] * fb[i] % mod

        del fb
        butterfly_inv(fa)
        return fa

    def fps_inv(f, n):
        mod = MOD
        f0 = f[0]
        g = [1 if f0 == 1 else pow(f0, mod - 2, mod)]
        m = 1
        while m < n:
            m2 = min(m * 2, n)

            fg = convolution(f[:m2], g)
            if len(fg) < m2:
                fg += [0] * (m2 - len(fg))
            else:
                del fg[m2:]

            fg[0] = (2 - fg[0]) % mod
            for i in range(1, m2):
                if fg[i]:
                    fg[i] = mod - fg[i]

            g = convolution(g, fg)
            if len(g) < m2:
                g += [0] * (m2 - len(g))
            else:
                del g[m2:]

            m = m2
        return g

    # Fast path: constant D = T-L and arithmetic progression of T.
    # Then C * K = B with K[k] = fact[c*k + D], B[i] = fact[T_i].
    d0 = T[0] - L[0]
    t0 = T[0]
    c = T[1] - T[0] if M > 1 else 1
    ok = True
    TT = T
    LL = L
    for i in range(1, M):
        if TT[i] - LL[i] != d0 or TT[i] - TT[i - 1] != c:
            ok = False
            break

    if ok:
        if c == 1:
            K = fact[d0:d0 + M]
            B = fact[t0:t0 + M]
        else:
            K = [fact[c * i + d0] for i in range(M)]
            B = [fact[t0 + c * i] for i in range(M)]

        invK = fps_inv(K, M)
        C = convolution(B, invK)
        if len(C) < M:
            C += [0] * (M - len(C))

        ans = fact[N]
        mod = MOD
        for i in range(M):
            cv = C[i]
            if cv:
                ans -= cv * fact[N - LL[i]] % mod
                if ans < 0:
                    ans += mod
        return ans

    # ---------- CDQ online convolution ----------
    C = [0] * M
    Ssum = [0] * M
    nz_indices = []

    BLOCK = 256
    NAIVE_LIMIT = 50000
    NAIVE_HARD = 1500000
    NAIVE_FACTOR = 4

    def ntt_cost(x):
        if x <= 1:
            return 0
        n = 1 << (x - 1).bit_length()
        return n * (n.bit_length() - 1) * 3

    def add_sparse(start, end, m, r):
        mod = MOD
        f = fact
        TT = T
        LL = L
        CC = C
        SS = Ssum
        nzl = nz_indices
        nz = end - start
        rc = r - m

        if nz <= rc:
            for p in range(start, end):
                j = nzl[p]
                c = CC[j]
                if c:
                    lj = LL[j]
                    for i in range(m, r):
                        nv = SS[i] + c * f[TT[i] - lj] % mod
                        if nv >= mod:
                            nv -= mod
                        SS[i] = nv
        else:
            for i in range(m, r):
                pi = TT[i]
                total = SS[i]
                for p in range(start, end):
                    j = nzl[p]
                    c = CC[j]
                    if c:
                        total += c * f[pi - LL[j]] % mod
                        if total >= mod:
                            total -= mod
                SS[i] = total

    def add_contrib(l, m, r):
        lc = m - l
        rc = r - m
        if lc == 0 or rc == 0:
            return

        start = bisect_left(nz_indices, l)
        end = bisect_left(nz_indices, m)
        nz = end - start
        if nz == 0:
            return

        mod = MOD
        f = fact
        TT = T
        LL = L
        CC = C
        SS = Ssum

        minL = LL[l]
        maxL = LL[m - 1]
        lenA = maxL - minL + 1

        minArg = TT[m] - LL[m - 1]
        maxArg = TT[r - 1] - LL[l]
        lenB = maxArg - minArg + 1

        conv_len = lenA + lenB - 1
        ncost = ntt_cost(conv_len)

        sparse_cost = nz * rc
        if sparse_cost <= NAIVE_LIMIT or (
            sparse_cost <= NAIVE_HARD and sparse_cost * NAIVE_FACTOR < ncost
        ):
            add_sparse(start, end, m, r)
            return

        if lenA == lc:
            A = CC[l:m]
        else:
            A = [0] * lenA
            nzl = nz_indices
            for p in range(start, end):
                j = nzl[p]
                A[LL[j] - minL] = CC[j]

        B = f[minArg:minArg + lenB]
        conv = convolution(A, B)

        base = minL + minArg
        for idx in range(m, r):
            val = conv[TT[idx] - base]
            if val:
                nv = SS[idx] + val
                if nv >= mod:
                    nv -= mod
                SS[idx] = nv

    sys.setrecursionlimit(1_000_000)

    def cdq(l, r):
        if l >= r:
            return

        if r - l <= BLOCK:
            mod = MOD
            f = fact
            invf = invfact
            TT = T
            LL = L
            CC = C
            SS = Ssum
            nzl = nz_indices

            for i in range(l, r):
                total = SS[i]
                ti = TT[i]

                for j in range(l, i):
                    c = CC[j]
                    if c:
                        total += c * f[ti - LL[j]] % mod
                        if total >= mod:
                            total -= mod

                val = f[ti] - total
                if val < 0:
                    val += mod
                CC[i] = val * invf[ti - LL[i]] % mod
                SS[i] = total

                if CC[i]:
                    nzl.append(i)

            return

        m = (l + r) // 2
        cdq(l, m)
        add_contrib(l, m, r)
        cdq(m, r)

    cdq(0, M)

    ans = fact[N]
    mod = MOD
    for i in range(M):
        c = C[i]
        if c:
            ans -= c * fact[N - L[i]] % mod
            if ans < 0:
                ans += mod
    return ans


def main():
    if sys.implementation.name == "cpython":
        gc.disable()

    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1].strip()

    sys.stdout.write(str(solve_one(N, S)) + "\n")


if __name__ == "__main__":
    main()