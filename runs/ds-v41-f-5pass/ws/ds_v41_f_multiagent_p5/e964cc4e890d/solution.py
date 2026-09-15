import sys
import numpy as np


def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = data[1].decode()

    # cut 1 forces vertex 1 black; cut 2N-1 forces vertex 2N white
    if S[0] != 'B' or S[-1] != 'W':
        sys.stdout.write("0\n")
        return

    # w[i] = number of 'W' before the (i+1)-th 'B'   (i = 0..N-1)
    w = [0] * N
    cnt = 0
    k = 0
    for ch in S:
        if ch == 'W':
            cnt += 1
        else:
            w[k] = cnt
            k += 1

    M = N + 1
    fact = [1] * (M + 1)
    for i in range(1, M + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (M + 1)
    inv_fact[M] = pow(fact[M], MOD - 2, MOD)
    for i in range(M, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    fl = fact
    ifl = inv_fact
    fact_np = np.array(fact, dtype=np.int64)
    w_np = np.array(w, dtype=np.int64)
    dp = np.zeros(N, dtype=np.int64)
    dp[0] = 1
    acc = np.zeros(N, dtype=np.int64)

    GM = 3
    _twf = {}
    _twi = {}

    def get_tw(L, inv):
        cache = _twi if inv else _twf
        arr = cache.get(L)
        if arr is None:
            half = L >> 1
            wlen = pow(GM, (MOD - 1) // L, MOD)
            if inv:
                wlen = pow(wlen, MOD - 2, MOD)
            arr = np.empty(half, dtype=np.int64)
            v = 1
            for j in range(half):
                arr[j] = v
                v = v * wlen % MOD
            cache[L] = arr
        return arr

    def ntt(a, inv):
        # DIF forward (natural -> bit-reversed), DIT inverse (bit-reversed -> natural)
        n = a.shape[0]
        if n == 1:
            return
        if not inv:
            L = n
            while L >= 2:
                half = L >> 1
                tw = get_tw(L, False)
                a2 = a.reshape(-1, L)
                u = a2[:, :half]
                v = a2[:, half:]
                t1 = u + v
                t1 %= MOD
                t2 = u - v
                t2 %= MOD
                t2 *= tw
                t2 %= MOD
                a2[:, :half] = t1
                a2[:, half:] = t2
                L >>= 1
        else:
            L = 2
            while L <= n:
                half = L >> 1
                tw = get_tw(L, True)
                a2 = a.reshape(-1, L)
                u = a2[:, :half]
                v = a2[:, half:] * tw
                v %= MOD
                t1 = u + v
                t1 %= MOD
                t2 = u - v
                t2 %= MOD
                a2[:, :half] = t1
                a2[:, half:] = t2
                L <<= 1
            a *= pow(n, MOD - 2, MOD)
            a %= MOD

    def convolve(A, C):
        la = A.shape[0]
        lc = C.shape[0]
        total = la + lc - 1
        n = 1
        while n < total:
            n <<= 1
        fa = np.zeros(n, dtype=np.int64)
        fa[:la] = A
        fb = np.zeros(n, dtype=np.int64)
        fb[:lc] = C
        ntt(fa, False)
        ntt(fb, False)
        fa *= fb
        fa %= MOD
        ntt(fa, True)
        return fa[:total]

    sys.setrecursionlimit(1 << 20)
    TH = 32
    DIRECT_TH = 16384

    def cdq(l, r):
        if r - l + 1 <= TH:
            dpl = dp[l:r + 1].tolist()
            acl = acc[l:r + 1].tolist()
            for i in range(l, r + 1):
                if i == 0:
                    dpl[0] = 1
                    continue
                wi = w[i]
                if wi < i:
                    dpl[i - l] = 0
                    continue
                cur = acl[i - l]
                for j in range(l, i):
                    dj = dpl[j - l]
                    if dj:
                        d = wi - j
                        if d >= 0:
                            cur += dj * fl[d]
                dpl[i - l] = (-ifl[wi - i] * (cur % MOD)) % MOD
            dp[l:r + 1] = dpl
            return

        mid = (l + r) >> 1
        cdq(l, mid)

        LA = mid - l + 1
        out = r - mid
        A = dp[l:mid + 1]
        if A.any():
            if LA * out <= DIRECT_TH:
                js = np.arange(l, mid + 1, dtype=np.int64)
                wi = w_np[mid + 1:r + 1]
                idxm = wi[None, :] - js[:, None]
                # negative indices only occur where dp[i]==0, so junk is harmless
                np.maximum(idxm, 0, out=idxm)
                vals = fact_np[idxm]
                vals *= A[:, None]
                vals %= MOD
                s = vals.sum(axis=0) % MOD
                acc[mid + 1:r + 1] = (acc[mid + 1:r + 1] + s) % MOD
            else:
                lo = w[mid + 1] - l
                hi = w[r] - l
                t_lo = lo if lo > 0 else 0
                if t_lo <= hi:
                    m0 = t_lo - (LA - 1)
                    if m0 < 0:
                        m0 = 0
                    C = fact_np[m0:hi + 1]
                    conv = convolve(A, C)
                    ts = w_np[mid + 1:r + 1] - l
                    pos = np.nonzero(ts >= t_lo)[0]
                    if pos.shape[0]:
                        vals = conv[ts[pos] - m0]
                        sub = acc[mid + 1:r + 1]
                        sub[pos] = (sub[pos] + vals) % MOD

        cdq(mid + 1, r)

    cdq(0, N - 1)

    idxs = N - np.arange(N, dtype=np.int64)
    terms = fact_np[idxs]
    ans = int(((dp * terms) % MOD).sum() % MOD)
    sys.stdout.write(str(ans) + "\n")


main()