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

    if len(a) * len(b) <= 4096:
        result = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    result[i + j] = (result[i + j] + x * y) % MOD
        return result

    needed = len(a) + len(b) - 1
    size = 1
    while size < needed:
        size <<= 1

    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:needed]


def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    length = 2 * n

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    whites = [0] * (length + 1)
    blacks = [0] * (length + 1)

    for i, c in enumerate(s, 1):
        whites[i] = whites[i - 1] + (c == "W")
        blacks[i] = blacks[i - 1] + (c == "B")

    balance = [whites[i] - blacks[i] for i in range(length + 1)]

    # e[j] is the first-return inclusion-exclusion coefficient at cut j.
    # The artificial initial term k=0 must not be subtracted: the
    # unrestricted count already represents the segment beginning at cut 0.
    e = [0] * (length + 1)

    # acc[j] = sum over 0 < k < j of
    # e[k] * fact(whites[j] - blacks[k]).
    acc = [0] * (length + 1)

    sys.setrecursionlimit(2 * length + 20)

    def cdq(left, right):
        if right - left == 1:
            if left == 0:
                return

            if balance[left] >= 0:
                value = (fact[whites[left]] - acc[left]) % MOD
                e[left] = value * inv_fact[balance[left]] % MOD
            return

        mid = (left + right) >> 1
        cdq(left, mid)

        min_black = blacks[left]
        max_black = blacks[mid - 1]
        max_white = whites[right - 1]

        if max_black >= min_black:
            first = [0] * (max_black - min_black + 1)

            for k in range(left, mid):
                if e[k]:
                    index = blacks[k] - min_black
                    first[index] = (first[index] + e[k]) % MOD

            max_shift = max_white - min_black
            if max_shift >= 0:
                second = fact[:max_shift + 1]
                product = convolution(first, second)

                for j in range(mid, right):
                    index = whites[j] - min_black
                    if 0 <= index < len(product):
                        acc[j] = (acc[j] + product[index]) % MOD

        cdq(mid, right)

    cdq(0, length + 1)
    print(e[length] % MOD)


if __name__ == "__main__":
    solve()