import sys

MOD = 998244353
PRIMITIVE_ROOT = 3
NAIVE_LIMIT = 32


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
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
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

    need = len(a) + len(b) - 1

    if min(len(a), len(b)) <= NAIVE_LIMIT:
        result = [0] * need
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    result[i + j] = (result[i + j] + x * y) % MOD
        return result

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


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # t[r] is the number of white vertices to the left of the
    # relevant cut for the bad event E_r.
    #
    # For r < n, use the cut immediately before the (r+1)-st black.
    # For r = n, use the cut immediately after the n-th black.
    t = [0] * (n + 1)
    black_count = 0
    white_count = 0

    for ch in s:
        if ch == "W":
            white_count += 1
        else:
            if black_count >= 1:
                t[black_count] = white_count
            black_count += 1
            if black_count == n:
                t[n] = white_count

    # dp[r] is the signed inclusion-exclusion contribution whose
    # last selected bad event is E_r. dp[0] represents no event.
    dp = [0] * (n + 1)
    dp[0] = 1

    def cdq(left, right):
        if right - left <= 1:
            return

        mid = (left + right) >> 1
        cdq(left, mid)

        max_t = -1
        for j in range(mid, right):
            if t[j] >= j and t[j] > max_t:
                max_t = t[j]

        if max_t >= mid:
            kernel = fact[:max_t - left + 1]
            product = convolution(dp[left:mid], kernel)

            for j in range(mid, right):
                if t[j] < j:
                    continue

                idx = t[j] - left
                contribution = product[idx] * invfact[t[j] - j] % MOD
                dp[j] = (dp[j] - contribution) % MOD

        cdq(mid, right)

    cdq(0, n + 1)

    answer = 0
    for r in range(n + 1):
        answer = (answer + dp[r] * fact[n - r]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()