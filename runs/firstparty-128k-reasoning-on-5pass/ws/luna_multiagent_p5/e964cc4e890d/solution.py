import sys

MOD = 998244353
PRIMITIVE_ROOT = 3


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
    if not a or not b:
        return []

    if len(a) * len(b) <= 5000:
        result = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    result[i + j] = (result[i + j] + x * y) % MOD
        return result

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


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    if s[0] != "B" or s[-1] != "W":
        print(0)
        return

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # a[k] is the number of whites before the (k+1)-th black.
    # Only indices 1..n-1 are used.
    a = [0] * n
    whites = 0
    blacks = 0
    for ch in s:
        if ch == "W":
            whites += 1
        else:
            blacks += 1
            if blacks >= 2:
                a[blacks - 1] = whites

    # g[k] is the signed contribution of subsets of bad events
    # whose largest selected event is k. g[0] is the empty subset.
    g = [0] * n
    g[0] = 1

    sys.setrecursionlimit(1_000_000)

    def cdq(left, right):
        if right - left == 1:
            k = left
            if k >= 1 and a[k] >= k:
                g[k] = -g[k] * inv_fact[a[k] - k] % MOD
            return

        mid = (left + right) >> 1
        cdq(left, mid)

        max_a = -1
        for k in range(mid, right):
            if a[k] >= k:
                if a[k] > max_a:
                    max_a = a[k]

        if max_a >= left:
            left_poly = g[left:mid]
            right_poly = fact[:max_a - left + 1]
            conv = convolution(left_poly, right_poly)

            for k in range(mid, right):
                if a[k] >= k:
                    g[k] = (g[k] + conv[a[k] - left]) % MOD

        cdq(mid, right)

    cdq(0, n)

    answer = fact[n]
    for k in range(1, n):
        answer = (answer + g[k] * fact[n - k]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()