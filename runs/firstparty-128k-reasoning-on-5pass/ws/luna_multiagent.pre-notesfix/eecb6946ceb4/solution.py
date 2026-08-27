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
        if invert:
            wlen = pow(PRIMITIVE_ROOT, (MOD - 1) - (MOD - 1) // length, MOD)
        else:
            wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)

        roots = [1] * half
        for i in range(1, half):
            roots[i] = roots[i - 1] * wlen % MOD

        for start in range(0, n, length):
            end = start + half
            for j in range(half):
                u = a[start + j]
                v = a[end + j] * roots[j] % MOD
                a[start + j] = u + v if u + v < MOD else u + v - MOD
                a[end + j] = u - v if u >= v else u - v + MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n_values = data[0]
    values = data[1:1 + n_values]
    maximum = max(values)

    size = 1
    while size <= 2 * maximum:
        size <<= 1

    present = bytearray(maximum + 1)
    for x in values:
        present[x] = 1

    a = list(present)
    a.extend([0] * (size - len(a)))

    ntt(a, False)

    for i in range(size):
        a[i] = a[i] * a[i] % MOD

    ntt(a, True)

    answer = 0
    for b in values:
        answer += (a[2 * b] - 1) // 2

    print(answer)


if __name__ == "__main__":
    solve()