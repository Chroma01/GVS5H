import sys

MOD = 998244353
ROOT = 3
ROOT_INV = pow(ROOT, MOD - 2, MOD)


def ntt_forward_dif(a):
    n = len(a)
    length = n
    mod = MOD

    while length >= 2:
        half = length >> 1
        wlen = pow(ROOT, (mod - 1) // length, mod)

        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                j = i + half
                x = a[i]
                y = a[j]

                s = x + y
                if s >= mod:
                    s -= mod
                d = x - y
                if d < 0:
                    d += mod

                a[i] = s
                a[j] = d * w % mod
                w = w * wlen % mod

        length >>= 1


def ntt_inverse_dit(a):
    n = len(a)
    mod = MOD
    length = 2

    while length <= n:
        half = length >> 1
        wlen = pow(ROOT_INV, (mod - 1) // length, mod)

        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                j = i + half
                x = a[i]
                y = a[j] * w % mod

                s = x + y
                if s >= mod:
                    s -= mod
                d = x - y
                if d < 0:
                    d += mod

                a[i] = s
                a[j] = d
                w = w * wlen % mod

        length <<= 1

    inv_n = pow(n, mod - 2, mod)
    for i in range(n):
        a[i] = a[i] * inv_n % mod


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    values = data[1:1 + n]
    maximum = max(values)

    size = 1
    required = maximum * 2 + 1
    while size < required:
        size <<= 1

    poly = [0] * size
    for value in values:
        poly[value] = 1

    ntt_forward_dif(poly)

    mod = MOD
    for i in range(size):
        poly[i] = poly[i] * poly[i] % mod

    ntt_inverse_dit(poly)

    answer = 0
    for middle in values:
        answer += (poly[middle * 2] - 1) // 2

    print(answer)


if __name__ == "__main__":
    solve()