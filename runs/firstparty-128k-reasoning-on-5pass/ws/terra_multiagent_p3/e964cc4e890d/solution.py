import sys

MOD = 998244353
G = 3

root_cache = {}
iroot_cache = {}


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
    cache = iroot_cache if invert else root_cache

    while length <= n:
        wlen = cache.get(length)
        if wlen is None:
            base = pow(G, (MOD - 1) // length, MOD)
            if invert:
                base = pow(base, MOD - 2, MOD)
            cache[length] = base
            wlen = base

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                u = a[i]
                v = a[i + half] * w % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD
                a[i] = x

                x = u - v
                if x < 0:
                    x += MOD
                a[i + half] = x

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
    size = 1
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


def poly_inverse(a, m):
    b = [pow(a[0], MOD - 2, MOD)]

    while len(b) < m:
        size = min(len(b) << 1, m)
        ab = convolution(a[:size], b)[:size]

        ab[0] = (2 - ab[0]) % MOD
        for i in range(1, size):
            ab[i] = (-ab[i]) % MOD

        b = convolution(b, ab)[:size]

    return b


def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    if s[0] != 'B' or s[-1] != 'W':
        print(0)
        return

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # a[k] = number of W vertices before the (k+1)-th B vertex.
    a = [0] * n
    white_count = 0
    black_count = 0
    for ch in s:
        if ch == 'W':
            white_count += 1
        else:
            black_count += 1
            if black_count >= 2:
                a[black_count - 1] = white_count

    # The alternating string BWBW... is the worst standard CDQ shape:
    # a[k] = k. In this case the recurrence is an ordinary series inverse.
    alternating = True
    for k in range(1, n):
        if a[k] != k:
            alternating = False
            break

    if alternating:
        # D(x) = 1 / sum(k! x^k).
        # The desired answer is -[x^N] D(x), because the omitted final
        # recurrence term is exactly what cancels this coefficient.
        inv_series = poly_inverse(fact, n + 1)
        print((-inv_series[n]) % MOD)
        return

    dp = [0] * n
    acc = [0] * n

    # Contribution from the virtual preceding barrier at index 0.
    for k in range(1, n):
        if a[k] >= k:
            acc[k] = fact[a[k]]

    # Direct multiplication is substantially faster than Python NTT on
    # small CDQ rectangles.
    DIRECT_LIMIT = 14000

    def add_contribution(left, mid, right):
        if left >= mid or mid >= right:
            return

        targets = [j for j in range(mid, right) if a[j] >= j]
        if not targets:
            return

        source_len = mid - left
        if source_len * len(targets) <= DIRECT_LIMIT:
            for j in targets:
                aj = a[j]
                total = 0
                cnt = 0
                for i in range(left, mid):
                    if dp[i]:
                        total += dp[i] * fact[aj - i]
                        cnt += 1
                        if cnt == 16:
                            total %= MOD
                            cnt = 0
                acc[j] = (acc[j] + total) % MOD
            return

        max_a = max(a[j] for j in targets)
        kernel_len = max_a - left + 1
        if kernel_len <= 0:
            return

        conv = convolution(dp[left:mid], fact[:kernel_len])

        for j in targets:
            acc[j] = (acc[j] + conv[a[j] - left]) % MOD

    sys.setrecursionlimit(1 << 20)

    def cdq(left, right):
        if right - left == 1:
            if a[left] >= left:
                dp[left] = (-acc[left] * invfact[a[left] - left]) % MOD
            return

        mid = (left + right) >> 1
        cdq(left, mid)
        add_contribution(left, mid, right)
        cdq(mid, right)

    if n >= 2:
        cdq(1, n)

    ans = fact[n]
    for k in range(1, n):
        ans += dp[k] * fact[n - k]

    print(ans % MOD)


if __name__ == "__main__":
    solve()