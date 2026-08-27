import sys


def solve(S):
    n = len(S) // 2
    MOD = 998244353
    L = 2 * n

    beta = [0] * (L + 1)
    gamma = [0] * (L + 1)
    for i, ch in enumerate(S, start=1):
        beta[i] = beta[i - 1] + (1 if ch == 'B' else 0)
        gamma[i] = gamma[i - 1] + (1 if ch == 'W' else 0)

    fact = [1] * (L + 1)
    for i in range(1, L + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (L + 1)
    invfact[L] = pow(fact[L], MOD - 2, MOD)
    for i in range(L, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def fall(a, b):
        if b < 0 or a < b or a < 0:
            return 0
        return fact[a] * invfact[a - b] % MOD

    cand = [k for k in range(1, L) if beta[k] <= gamma[k]]
    cand.append(L)
    m = len(cand)
    B = [beta[k] for k in cand]
    Gm = [gamma[k] for k in cand]

    def ntt(a, invert):
        n_ = len(a)
        j = 0
        for i in range(1, n_):
            bit = n_ >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        length = 2
        while length <= n_:
            wlen = pow(3, (MOD - 1) // length, MOD)
            if invert:
                wlen = pow(wlen, MOD - 2, MOD)
            half = length >> 1
            for i in range(0, n_, length):
                w = 1
                for k in range(i, i + half):
                    u = a[k]
                    v = a[k + half] * w % MOD
                    a[k] = u + v if u + v < MOD else u + v - MOD
                    a[k + half] = u - v if u >= v else u - v + MOD
                    w = w * wlen % MOD
            length <<= 1
        if invert:
            inv_n = pow(n_, MOD - 2, MOD)
            for i in range(n_):
                a[i] = a[i] * inv_n % MOD

    def convolution(a, b):
        if not a or not b:
            return []
        size = 1
        need = len(a) + len(b) - 1
        while size < need:
            size <<= 1
        fa = a + [0] * (size - len(a))
        fb = b + [0] * (size - len(b))
        ntt(fa, False)
        ntt(fb, False)
        for i in range(size):
            fa[i] = fa[i] * fb[i] % MOD
        ntt(fa, True)
        return fa[:need]

    G = [0] * m
    sys.setrecursionlimit(1 << 25)

    def cdq(l, r):
        if r - l <= 1:
            if l < m:
                G[l] %= MOD
            return
        mid = (l + r) >> 1
        cdq(l, mid)
        maxw = max(B[l:mid]) + 1 if mid > l else 0
        A = [0] * maxw
        for i in range(l, mid):
            A[B[i]] = (A[B[i]] + G[i]) % MOD
        maxg = max(Gm[mid:r]) if mid < r else -1
        if maxg >= 0 and A:
            kern = fact[:maxg + 1]
            conv = convolution(A, kern)
            for j in range(mid, r):
                g = Gm[j]
                if g < len(conv):
                    G[j] = (G[j] - conv[g]) % MOD
        cdq(mid, r)

    for j in range(m):
        G[j] = fall(Gm[j], B[j])

    cdq(0, m)
    return G[m - 1] % MOD


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1].strip()
    print(solve(S))


main()