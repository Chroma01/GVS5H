import sys

MOD = 998244353
G = 3


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
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        half = length >> 1
        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                u = a[i]
                v = a[i + half] * w % MOD
                a[i] = (u + v) % MOD
                a[i + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def convolution(a, b):
    need = len(a) + len(b) - 1
    size = 1
    while size < need:
        size <<= 1
    a = a + [0] * (size - len(a))
    b = b + [0] * (size - len(b))
    ntt(a, False)
    ntt(b, False)
    for i in range(size):
        a[i] = a[i] * b[i] % MOD
    ntt(a, True)
    return a[:need]


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    # A prefix with no black vertex can never receive a backward added edge.
    if s[0] == 'W':
        print(0)
        return

    fact = [1] * (n + 1)
    ifact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    ifact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    # wmax[b] is the maximum number of whites in a proper prefix
    # containing exactly b black vertices.
    wmax = [-1] * (n + 1)
    w = 0
    b = 0
    for i in range(2 * n - 1):
        if s[i] == 'W':
            w += 1
        else:
            b += 1
        if b >= 1:
            wmax[b] = w

    # dp[b] is the signed inclusion-exclusion sum for selected bad cuts
    # whose final selected cut has b black vertices.
    dp = [0] * (n + 1)
    dp[0] = 1
    accum = [0] * (n + 1)

    valid = [False] * (n + 1)
    for b in range(1, n + 1):
        valid[b] = (wmax[b] >= b)

    sys.setrecursionlimit(1 << 20)

    def add_cross(l, mid, r):
        src = [dp[a] for a in range(l, mid + 1)]

        targets = [x for x in range(mid + 1, r + 1) if valid[x]]
        if not targets:
            return

        if len(src) * len(targets) <= 8000:
            for x in targets:
                wx = wmax[x]
                total = 0
                for idx, val in enumerate(src):
                    if val:
                        a = l + idx
                        total += val * fact[wx - a]
                accum[x] = (accum[x] + total) % MOD
            return

        max_w = max(wmax[x] for x in targets)
        kernel = fact[:max_w - l + 1]
        conv = convolution(src, kernel)

        for x in targets:
            accum[x] = (accum[x] + conv[wmax[x] - l]) % MOD

    def cdq(l, r):
        if l == r:
            if l != 0 and valid[l]:
                dp[l] = (-accum[l] * ifact[wmax[l] - l]) % MOD
            return

        mid = (l + r) >> 1
        cdq(l, mid)
        add_cross(l, mid, r)
        cdq(mid + 1, r)

    cdq(0, n)

    ans = fact[n]
    for b in range(1, n + 1):
        ans += dp[b] * fact[n - b]
    print(ans % MOD)


if __name__ == "__main__":
    solve()