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
            for i in range(start, start + half):
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
    if not a or not b:
        return []
    if min(len(a), len(b)) <= 40:
        res = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    res[i + j] = (res[i + j] + x * y) % MOD
        return res

    need = len(a) + len(b) - 1
    z = 1
    while z < need:
        z <<= 1

    fa = a + [0] * (z - len(a))
    fb = b + [0] * (z - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(z):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]


def main():
    input = sys.stdin.readline
    N = int(input())
    S = input().strip()

    fact = [1] * (N + 1)
    invfact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # r[b] = number of W vertices before the (b+1)-th B vertex.
    r = [0] * (N + 1)
    blacks_seen = 0
    whites_seen = 0
    for ch in S:
        if ch == 'B':
            blacks_seen += 1
            if blacks_seen >= 2:
                r[blacks_seen - 1] = whites_seen
        else:
            whites_seen += 1

    # A cut can be bad only if r[b] >= b.
    cuts = [b for b in range(1, N) if r[b] >= b]
    m = len(cuts)

    if m == 0:
        print(fact[N])
        return

    dp = [0] * m
    add = [0] * m

    # The virtual selected cut 0 has coefficient dp_0 = 1.
    # It contributes fact(r[b]) to every real cut b.
    for idx, b in enumerate(cuts):
        add[idx] = fact[r[b]]

    # CDQ: after solving its left half, add all transitions from
    # left selected cuts to right selected cuts by a convolution.
    def cdq(l, rr):
        if rr - l <= 1:
            b = cuts[l]
            dp[l] = (-add[l] * invfact[r[b] - b]) % MOD
            return

        mid = (l + rr) // 2
        cdq(l, mid)

        base = cuts[l]
        max_source = cuts[mid - 1]
        max_target = r[cuts[rr - 1]]

        a = [0] * (max_source - base + 1)
        for i in range(l, mid):
            a[cuts[i] - base] = dp[i]

        kernel = fact[:max_target - base + 1]
        conv = convolution(a, kernel)

        for j in range(mid, rr):
            pos = r[cuts[j]] - base
            if pos < len(conv):
                add[j] = (add[j] + conv[pos]) % MOD

        cdq(mid, rr)

    cdq(0, m)

    ans = fact[N]
    for i, b in enumerate(cuts):
        ans = (ans + dp[i] * fact[N - b]) % MOD
    print(ans)


if __name__ == "__main__":
    main()