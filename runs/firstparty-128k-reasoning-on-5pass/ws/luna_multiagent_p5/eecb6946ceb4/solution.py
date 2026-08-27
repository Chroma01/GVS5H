import sys

MOD = 998244353
ROOT = 3


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
    primitive = ROOT if not invert else pow(ROOT, MOD - 2, MOD)
    while length <= n:
        wlen = pow(primitive, (MOD - 1) // length, MOD)
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


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)

    max_value = 0
    present = bytearray(1000001)
    for _ in range(n):
        x = next(it)
        present[x] = 1
        if x > max_value:
            max_value = x

    size = 1
    required = 2 * max_value + 1
    while size < required:
        size <<= 1

    poly = [0] * size
    for x in range(1, max_value + 1):
        if present[x]:
            poly[x] = 1

    ntt(poly, False)
    for i in range(size):
        poly[i] = poly[i] * poly[i] % MOD
    ntt(poly, True)

    answer = 0
    for b in range(1, max_value + 1):
        if present[b]:
            answer += (poly[2 * b] - 1) // 2

    print(answer)


if __name__ == "__main__":
    solve()