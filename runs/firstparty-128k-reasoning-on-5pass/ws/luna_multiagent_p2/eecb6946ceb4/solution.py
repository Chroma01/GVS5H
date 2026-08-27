import sys
from array import array

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
        half = length >> 1
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        roots = [1] * half
        for i in range(1, half):
            roots[i] = roots[i - 1] * wlen % MOD

        for start in range(0, n, length):
            for j in range(half):
                u = a[start + j]
                v = a[start + j + half] * roots[j] % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD
                y = u - v
                if y < 0:
                    y += MOD

                a[start + j] = x
                a[start + j + half] = y

        length <<= 1

    del roots


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    values = array('I', map(int, data[1:]))
    del data

    max_value = max(values)
    present = bytearray(max_value + 1)

    for x in values:
        present[x] = 1
    del values

    required = 2 * max_value + 1
    size = 1
    while size < required:
        size <<= 1

    polynomial = [0] * size
    for x in range(1, max_value + 1):
        if present[x]:
            polynomial[x] = 1

    ntt(polynomial, False)
    for i in range(size):
        polynomial[i] = polynomial[i] * polynomial[i] % MOD
    ntt(polynomial, True)

    inv_size = pow(size, MOD - 2, MOD)
    answer = 0

    for midpoint in range(1, max_value + 1):
        if present[midpoint]:
            coefficient = polynomial[midpoint * 2] * inv_size % MOD
            answer += (coefficient - 1) // 2

    print(answer)


if __name__ == "__main__":
    main()