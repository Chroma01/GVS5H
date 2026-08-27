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
        half = length >> 1
        root = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            root = pow(root, MOD - 2, MOD)

        roots = [1] * half
        for i in range(1, half):
            roots[i] = roots[i - 1] * root % MOD

        for start in range(0, n, length):
            end = start + half
            for j in range(half):
                u = a[start + j]
                v = a[end + j] * roots[j] % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD

                y = u - v
                if y < 0:
                    y += MOD

                a[start + j] = x
                a[end + j] = y

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    numbers = data[1:1 + n]
    max_value = max(numbers)

    present = bytearray(max_value + 1)
    for x in numbers:
        present[x] = 1

    size = 1
    while size <= 2 * max_value:
        size <<= 1

    convolution = [0] * size
    for x in numbers:
        convolution[x] = 1

    ntt(convolution, False)

    for i in range(size):
        convolution[i] = convolution[i] * convolution[i] % MOD

    ntt(convolution, True)

    answer = 0
    for b in numbers:
        answer += (convolution[2 * b] - 1) // 2

    print(answer)


if __name__ == "__main__":
    main()