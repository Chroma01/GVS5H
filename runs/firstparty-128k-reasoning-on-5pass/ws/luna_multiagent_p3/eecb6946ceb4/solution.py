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
        exponent = (MOD - 1) // length
        if invert:
            exponent = MOD - 1 - exponent
        wlen = pow(PRIMITIVE_ROOT, exponent, MOD)
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
                y = u - v
                if y < 0:
                    y += MOD

                a[i] = x
                a[i + half] = y
                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    values = data[1:1 + n]
    maximum = max(values)

    size = 1
    while size <= 2 * maximum:
        size <<= 1

    polynomial = [0] * size
    for value in values:
        polynomial[value] = 1

    ntt(polynomial, False)

    for i in range(size):
        polynomial[i] = polynomial[i] * polynomial[i] % MOD

    ntt(polynomial, True)

    answer = 0
    for middle in values:
        answer += (polynomial[2 * middle] - 1) // 2

    print(answer)


if __name__ == "__main__":
    main()