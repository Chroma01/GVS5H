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
        root = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            root = pow(root, MOD - 2, MOD)

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            for i in range(start, start + half):
                u = a[i]
                v = a[i + half] * w % MOD
                a[i] = (u + v) % MOD
                a[i + half] = (u - v) % MOD
                w = w * root % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def convolution(a, b):
    if not a or not b:
        return []

    need = len(a) + len(b) - 1

    if min(len(a), len(b)) <= 40:
        result = [0] * need
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    result[i + j] = (result[i + j] + x * y) % MOD
        return result

    size = 1
    while size < need:
        size <<= 1

    fa = a[:] + [0] * (size - len(a))
    fb = b[:] + [0] * (size - len(b))

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

    # The first prefix must have a black vertex, otherwise no backward
    # added edge can enter it.
    if s[0] != 'B':
        print(0)
        return

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # For black vertex number i+1, a[i] is the number of whites before it.
    a = [-1] * (n + 1)
    black_count = 0
    white_count = 0
    for ch in s:
        if ch == 'B':
            black_count += 1
            if black_count >= 2:
                a[black_count - 1] = white_count
        else:
            white_count += 1

    # At one white-coordinate x, only the earliest event is relevant:
    # later events with the same x are subsets of it.
    idx_at = [-1] * (n + 1)
    for i in range(1, n):
        x = a[i]
        if x >= i and idx_at[x] == -1:
            idx_at[x] = i

    dp_at = [0] * (n + 1)
    add = [0] * (n + 1)

    sys.setrecursionlimit(1 << 20)

    def propagate(left, mid, right):
        sources = []
        min_i = n + 1
        max_i = -1

        for x in range(left, mid + 1):
            i = idx_at[x]
            if i != -1 and dp_at[x]:
                value = dp_at[x]
                sources.append((i, value))
                if i < min_i:
                    min_i = i
                if i > max_i:
                    max_i = i

        targets = [x for x in range(mid + 1, right + 1) if idx_at[x] != -1]

        if not sources or not targets:
            return

        if len(sources) * len(targets) <= 5000:
            for i, value in sources:
                for x in targets:
                    add[x] = (add[x] + value * fact[x - i]) % MOD
            return

        poly = [0] * (max_i - min_i + 1)
        for i, value in sources:
            poly[i - min_i] = (poly[i - min_i] + value) % MOD

        kernel = fact[:right - min_i + 1]
        conv = convolution(poly, kernel)

        for x in targets:
            add[x] = (add[x] + conv[x - min_i]) % MOD

    def cdq(left, right):
        if left == right:
            i = idx_at[left]
            if i != -1:
                total = (fact[left] + add[left]) % MOD
                dp_at[left] = (-total * invfact[left - i]) % MOD
            return

        mid = (left + right) >> 1
        cdq(left, mid)
        propagate(left, mid, right)
        cdq(mid + 1, right)

    cdq(0, n)

    answer = fact[n]
    for x in range(n + 1):
        i = idx_at[x]
        if i != -1:
            answer = (answer + dp_at[x] * fact[n - i]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()