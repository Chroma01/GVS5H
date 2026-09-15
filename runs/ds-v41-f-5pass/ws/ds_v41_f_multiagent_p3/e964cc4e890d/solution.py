import sys

def main():
    sys.setrecursionlimit(1 << 20)
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = data[1].decode()
    MOD = 998244353

    # Brute force for tiny N (safety net)
    if N <= 8:
        import itertools
        Bpos = [i for i, c in enumerate(S) if c == 'B']
        Wpos = [i for i, c in enumerate(S) if c == 'W']
        Vn = 2 * N
        base = [[i - 1] if i > 0 else [] for i in range(Vn)]
        cnt = 0
        for perm in itertools.permutations(range(N)):
            adj = [lst[:] for lst in base]
            for k in range(N):
                # reversed back edge black <- white
                adj[Bpos[k]].append(Wpos[perm[k]])
            seen = [False] * Vn
            seen[0] = True
            st = [0]
            c = 1
            while st:
                u = st.pop()
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        c += 1
                        st.append(v)
            if c == Vn:
                cnt += 1
        print(cnt % MOD)
        return

    if S[0] != 'B' or S[-1] != 'W':
        print(0)
        return

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # q[k] = number of whites before b_{k+1}
    q = [0] * (N + 1)
    w = 0
    bc = 0
    for ch in S:
        if ch == 'W':
            w += 1
        else:
            bc += 1
            if 2 <= bc <= N:
                q[bc - 1] = w

    Ls = [0]
    Vs = [0]
    prev = 0
    for l in range(1, N):
        if q[l] > prev:
            if q[l] >= l:
                Ls.append(l)
                Vs.append(q[l])
            prev = q[l]

    m = len(Ls) - 1
    if m == 0:
        print(fact[N] % MOD)
        return

    try:
        import numpy as np
        HAVE_NP = True
    except Exception:
        HAVE_NP = False

    DIRECT_LIMIT = 1 << 18

    if HAVE_NP:
        _MOD = MOD
        rev_cache = {}
        rootf_cache = {}
        rooti_cache = {}

        def get_rev(n):
            r = rev_cache.get(n)
            if r is not None:
                return r
            rev = np.zeros(1, dtype=np.int64)
            while rev.shape[0] < n:
                mm = rev.shape[0]
                nr = np.empty(2 * mm, dtype=np.int64)
                nr[0::2] = rev
                nr[1::2] = rev + mm
                rev = nr
            rev_cache[n] = rev
            return rev

        def get_roots(n, inv):
            cache = rooti_cache if inv else rootf_cache
            r = cache.get(n)
            if r is not None:
                return r
            w0 = pow(3, (_MOD - 1) // n, _MOD)
            if inv:
                w0 = pow(w0, _MOD - 2, _MOD)
            arr = np.ones(1, dtype=np.int64)
            l = 1
            while l < n:
                wl = pow(w0, l, _MOD)
                arr = np.concatenate([arr, arr * wl % _MOD])
                l <<= 1
            cache[n] = arr
            return arr

        def ntt(a, inv):
            n = a.shape[0]
            a = a[get_rev(n)]
            roots = get_roots(n, inv)
            length = 2
            while length <= n:
                half = length >> 1
                step = n // length
                wv = roots[::step][:half]
                a = a.reshape(-1, length)
                u = a[:, :half]
                v = a[:, half:] * wv % _MOD
                t1 = (u + v) % _MOD
                t2 = (u - v) % _MOD
                a[:, :half] = t1
                a[:, half:] = t2
                a = a.reshape(n)
                length <<= 1
            if inv:
                a = a * pow(n, _MOD - 2, _MOD) % _MOD
            return a

        def conv_np_ntt(na, nb):
            need = na.shape[0] + nb.shape[0] - 1
            size = 1
            while size < need:
                size <<= 1
            fa = np.zeros(size, dtype=np.int64)
            fb = np.zeros(size, dtype=np.int64)
            fa[:na.shape[0]] = na
            fb[:nb.shape[0]] = nb
            fa = ntt(fa, False)
            fb = ntt(fb, False)
            fa = fa * fb % _MOD
            fa = ntt(fa, True)
            return fa[:need].tolist()

        def conv_np_direct(na, nb):
            mask = 32767
            a0 = na & mask
            a1 = na >> 15
            b0 = nb & mask
            b1 = nb >> 15
            c00 = np.convolve(a0, b0)
            c01 = np.convolve(a0, b1)
            c10 = np.convolve(a1, b0)
            c11 = np.convolve(a1, b1)
            cross = (c01 + c10) % _MOD
            p30 = (1 << 30) % _MOD
            res = (c00 % _MOD + cross * 32768 % _MOD + (c11 % _MOD) * p30) % _MOD
            return res.tolist()

    def convolution(a, b):
        la = len(a)
        lb = len(b)
        if la == 0 or lb == 0:
            return []
        if la == 1:
            c0 = a[0]
            if c0 == 0:
                return [0] * lb
            return [c0 * x % MOD for x in b]
        if lb == 1:
            c0 = b[0]
            if c0 == 0:
                return [0] * la
            return [c0 * x % MOD for x in a]
        if HAVE_NP:
            na = np.array(a, dtype=np.int64)
            nb = np.array(b, dtype=np.int64)
            if la * lb <= DIRECT_LIMIT:
                return conv_np_direct(na, nb)
            return conv_np_ntt(na, nb)
        need = la + lb - 1
        if la * lb <= 200000:
            res = [0] * need
            for i in range(la):
                ai = a[i]
                if ai:
                    for j in range(lb):
                        res[i + j] = (res[i + j] + ai * b[j]) % MOD
            return res
        # Kronecker substitution fallback (80-bit limbs)
        WB = 10
        ba = b''.join(x.to_bytes(WB, 'little') for x in a)
        bb = b''.join(x.to_bytes(WB, 'little') for x in b)
        C = int.from_bytes(ba, 'little') * int.from_bytes(bb, 'little')
        cb = C.to_bytes(WB * need + WB, 'little')
        return [int.from_bytes(cb[WB * i:WB * i + WB], 'little') % MOD
                for i in range(need)]

    e = [0] * (m + 1)
    acc = [0] * (m + 1)
    SMALL = 32

    def add(lo, i1, j0, j1):
        M = Ls[lo]
        A = [0] * (Ls[i1] - M + 1)
        for i in range(lo, i1 + 1):
            A[Ls[i] - M] = e[i]
        b0 = Vs[j0] - Ls[i1]
        Flen = Vs[j1] - b0 - Ls[lo] + 1
        F = fact[b0:b0 + Flen]
        conv = convolution(A, F)
        for j in range(j0, j1 + 1):
            acc[j] = (acc[j] + conv[Vs[j] - M - b0]) % MOD

    def solve(lo, hi):
        if hi - lo <= SMALL:
            for j in range(lo, hi + 1):
                if j == 0:
                    e[0] = 1
                else:
                    s = acc[j]
                    Vj = Vs[j]
                    for i in range(lo, j):
                        ei = e[i]
                        if ei:
                            s += ei * fact[Vj - Ls[i]]
                    e[j] = (-(s % MOD)) * invfact[Vj - Ls[j]] % MOD
            return
        mid = (lo + hi) >> 1
        solve(lo, mid)
        add(lo, mid, mid + 1, hi)
        solve(mid + 1, hi)

    solve(0, m)

    ans = 0
    for j in range(m + 1):
        ans = (ans + e[j] * fact[N - Ls[j]]) % MOD
    print(ans % MOD)

main()