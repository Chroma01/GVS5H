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

    if min(len(a), len(b)) <= 32:
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

    black_positions = []
    white_prefix = [0] * (2 * n + 1)

    for i, ch in enumerate(s):
        white_prefix[i + 1] = white_prefix[i] + (ch == "W")
        if ch == "B":
            black_positions.append(i)

    # d[i] = number of white vertices before the (i+1)-th black vertex.
    d = [0] * n
    for i in range(1, n):
        d[i] = white_prefix[black_positions[i]]

    # g[i] is the inclusion-exclusion coefficient for subsets
    # whose largest bad-event index is i.
    g = [0] * n
    g[0] = 1

    # acc[x] = sum of processed g[j] * (x-j)!.
    acc = [0] * (n + 1)

    sys.setrecursionlimit(1_000_000)

    def cdq(left, right):
        if right - left == 1:
            i = left
            if i > 0 and d[i] >= i:
                g[i] = (-acc[d[i]] * inv_fact[d[i] - i]) % MOD
            return

        mid = (left + right) >> 1
        cdq(left, mid)

        max_d = d[right - 1]
        if max_d >= left:
            poly_a = g[left:mid]
            poly_b = fact[:max_d - left + 1]
            conv = convolution(poly_a, poly_b)

            # Equal d-values share the same acc entry, so update each
            # distinct value only once in this CDQ merge.
            previous_d = -1
            for i in range(mid, right):
                value = d[i]
                if value == previous_d:
                    continue
                previous_d = value

                offset = value - left
                if 0 <= offset < len(conv):
                    acc[value] = (acc[value] + conv[offset]) % MOD

        cdq(mid, right)

    cdq(0, n)

    answer = fact[n]
    for i in range(1, n):
        answer = (answer + g[i] * fact[n - i]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()