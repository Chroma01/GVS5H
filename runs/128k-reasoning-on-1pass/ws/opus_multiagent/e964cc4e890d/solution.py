import sys
import numpy as np
from bisect import bisect_left

MOD = 998244353
_SIZES = None


def good_size(need):
    """smallest 5-smooth number >= need (fast sizes for numpy pocketfft)."""
    global _SIZES
    if _SIZES is None:
        limit = 1 << 23
        lst = []
        p2 = 1
        while p2 <= limit:
            p3 = p2
            while p3 <= limit:
                p5 = p3
                while p5 <= limit:
                    lst.append(p5)
                    p5 *= 5
                p3 *= 3
            p2 *= 2
        lst.sort()
        _SIZES = lst
    return _SIZES[bisect_left(_SIZES, need)]


def conv_mod(A, B):
    """cyclic-free convolution of two int64 arrays with entries in [0,MOD)."""
    la = int(A.size)
    lb = int(B.size)
    if la == 0 or lb == 0:
        return np.zeros(0, dtype=np.int64)
    need = la + lb - 1
    mn = la if la < lb else lb
    if mn <= 32:
        if la > lb:
            A, B = B, A
            la, lb = lb, la
        res = np.zeros(need, dtype=np.int64)
        for i, ai in enumerate(A.tolist()):
            if ai:
                res[i:i + lb] += (ai * B) % MOD
        res %= MOD
        return res
    n = good_size(need)
    rfft = np.fft.rfft
    irfft = np.fft.irfft
    if mn <= 8192:
        # two 15-bit limbs (max coeff ~ mn*2^30 <= 2^43 -> plenty of margin)
        fa0 = rfft((A & 32767).astype(np.float64), n)
        fa1 = rfft((A >> 15).astype(np.float64), n)
        fb0 = rfft((B & 32767).astype(np.float64), n)
        fb1 = rfft((B >> 15).astype(np.float64), n)
        r0 = np.rint(irfft(fa0 * fb0, n)[:need]).astype(np.int64)
        r2 = np.rint(irfft(fa1 * fb1, n)[:need]).astype(np.int64)
        fa0 *= fb1
        fa1 *= fb0
        fa0 += fa1
        r1 = np.rint(irfft(fa0, n)[:need]).astype(np.int64)
        r0 %= MOD
        r1 %= MOD
        r2 %= MOD
        res = r0 + r1 * 32768
        res %= MOD
        res += r2 * 75497471          # 2^30 mod MOD
        res %= MOD
        return res
    # three 10-bit limbs (max coeff ~ mn*2^20 <= 2^38 -> extremely safe)
    fa = (rfft((A & 1023).astype(np.float64), n),
          rfft(((A >> 10) & 1023).astype(np.float64), n),
          rfft((A >> 20).astype(np.float64), n))
    fb = (rfft((B & 1023).astype(np.float64), n),
          rfft(((B >> 10) & 1023).astype(np.float64), n),
          rfft((B >> 20).astype(np.float64), n))
    W = (1, 1024, 1048576, 75497471, (75497471 * 1024) % MOD)
    res = np.zeros(need, dtype=np.int64)
    for k in range(5):
        acc = None
        for i in range(3):
            j = k - i
            if 0 <= j < 3:
                t = fa[i] * fb[j]
                if acc is None:
                    acc = t
                else:
                    acc += t
        r = np.rint(irfft(acc, n)[:need]).astype(np.int64)
        r %= MOD
        wk = W[k]
        if wk == 1:
            res += r
        else:
            res += r * wk
        res %= MOD
    return res


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    Sb = data[1]
    L = len(Sb)

    if L == 0 or Sb[0] != 66 or Sb[-1] != 87:   # need S starts 'B', ends 'W'
        sys.stdout.write("0\n")
        return

    maxn = n + 10
    fact = [1] * maxn
    f = 1
    for i in range(1, maxn):
        f = f * i % MOD
        fact[i] = f
    invfact = [1] * maxn
    invfact[maxn - 1] = pow(fact[maxn - 1], MOD - 2, MOD)
    for i in range(maxn - 1, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # ---- run decomposition (vectorised) ----
    arr = np.frombuffer(Sb, dtype=np.uint8)
    isw = (arr == 87)
    if L > 1:
        ch = np.flatnonzero(isw[1:] != isw[:-1])
        ends = np.concatenate((ch, np.array([L - 1], dtype=ch.dtype)))
    else:
        ends = np.array([0])
    cw = np.cumsum(isw, dtype=np.int64)
    we = ends[isw[ends]]
    we = we[we != L - 1].astype(np.int64)
    om = cw[we]
    be = (we + 1) - om
    zero = np.zeros(1, dtype=np.int64)
    omega_np = np.concatenate((zero, om))
    beta_np = np.concatenate((zero, be))
    K = int(omega_np.size)

    if K == 1:
        sys.stdout.write(str(fact[n] % MOD) + "\n")
        return

    beta = beta_np.tolist()
    omega = omega_np.tolist()

    factnp = np.array(fact, dtype=np.int64)
    OFF = maxn
    factpad = np.zeros(2 * maxn, dtype=np.int64)
    factpad[OFF:] = factnp            # factpad[OFF+t] = t!, 0 for t < 0

    # ---------- direct O(K^2) reference path ----------
    if K <= 3000:
        D = [0] * K
        D[0] = 1
        Dnp = np.zeros(K, dtype=np.int64)
        Dnp[0] = 1
        for k in range(1, K):
            wk = omega[k]
            d = wk - beta[k]
            if d < 0:
                continue
            # beta strictly increasing => wk - beta[j] > 0 for j < k
            vals = factnp[wk - beta_np[:k]]
            H = int((Dnp[:k] * vals % MOD).sum() % MOD)
            v = (MOD - invfact[d] * H) % MOD
            D[k] = v
            Dnp[k] = v
        ans = 0
        for j in range(K):
            dj = D[j]
            if dj:
                ans = (ans + dj * fact[n - beta[j]]) % MOD
        sys.stdout.write(str(ans % MOD) + "\n")
        return

    # ---------- CDQ divide & conquer ----------
    sys.setrecursionlimit(10000)
    Dl = [0] * K
    Dnp = np.zeros(K, dtype=np.int64)
    H = np.zeros(K, dtype=np.int64)

    LEAF = 16
    DIRECT = 8192

    def leaf(l, r):
        hs = H[l:r].tolist()
        for k in range(l, r):
            if k == 0:
                Dl[0] = 1
                Dnp[0] = 1
                continue
            wk = omega[k]
            d = wk - beta[k]
            if d < 0:
                Dl[k] = 0
                Dnp[k] = 0
                continue
            s = hs[k - l]
            for j in range(l, k):
                dj = Dl[j]
                if dj:
                    s += dj * fact[wk - beta[j]]
            v = (MOD - invfact[d] * (s % MOD)) % MOD
            Dl[k] = v
            Dnp[k] = v

    def contribute(l, m, r):
        nl = m - l
        nr = r - m
        bl = beta[l]
        bm = beta[m - 1]
        La = bm - bl + 1
        t0 = omega[m] - bm
        Lg = (omega[r - 1] - omega[m]) + La
        prod = nl * nr
        if prod <= DIRECT or 8 * prod <= La + Lg:
            idx = omega_np[m:r, None] - beta_np[None, l:m] + OFF
            vals = factpad[idx]
            add = (vals * Dnp[None, l:m]) % MOD
            H[m:r] = (H[m:r] + add.sum(axis=1)) % MOD
            return
        A = np.zeros(La, dtype=np.int64)
        A[beta_np[l:m] - bl] = Dnp[l:m]
        Gk = factpad[t0 + OFF: t0 + OFF + Lg]
        C = conv_mod(A, Gk)
        sidx = omega_np[m:r] - (bl + t0)
        H[m:r] = (H[m:r] + C[sidx]) % MOD

    def solve(l, r):
        if r - l <= LEAF:
            leaf(l, r)
            return
        m = (l + r) >> 1
        solve(l, m)
        contribute(l, m, r)
        solve(m, r)

    solve(0, K)

    ans = 0
    for j in range(K):
        dj = Dl[j]
        if dj:
            ans = (ans + dj * fact[n - beta[j]]) % MOD
    sys.stdout.write(str(ans % MOD) + "\n")


main()