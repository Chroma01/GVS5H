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
    while length <= n:
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
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

    if min(len(a), len(b)) <= 60:
        res = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    res[i + j] = (res[i + j] + x * y) % MOD
        return res

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


def binomial_power(c, q):
    """Coefficients of (1 + q z)^c."""
    res = [1] * (c + 1)
    if c == 0:
        return res

    inv = [0] * (c + 1)
    inv[1] = 1
    for i in range(2, c + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    cur = 1
    for k in range(1, c + 1):
        cur = cur * (c - k + 1) % MOD
        cur = cur * inv[k] % MOD
        cur = cur * q % MOD
        res[k] = cur
    return res


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])

    counts = [0] * 7
    sums = [0] * 7
    for x in range(1, n + 1):
        d = len(str(x))
        counts[d] += 1
        sums[d] += x
        if sums[d] >= MOD:
            sums[d] -= MOD

    # P(z) = product_d (1 + 10^d z)^{counts[d]}.
    poly = [1]
    for d in range(1, 7):
        if counts[d]:
            factor = binomial_power(counts[d], pow(10, d, MOD))
            poly = convolution(poly, factor)

    # factorials needed for k!(N-1-k)!.
    fact = [1] * n
    for i in range(1, n):
        fact[i] = fact[i - 1] * i % MOD

    answer = 0
    m = n - 1

    # Removing one element of digit length d divides P(z) by
    # (1 + 10^d z), yielding the subset polynomial for the other N-1 items.
    for d in range(1, 7):
        c = counts[d]
        if c == 0:
            continue

        q = pow(10, d, MOD)
        quotient = [0] * n
        quotient[0] = poly[0]
        for i in range(1, n):
            quotient[i] = (poly[i] - q * quotient[i - 1]) % MOD

        positional_sum = 0
        for k in range(n):
            positional_sum = (
                positional_sum
                + quotient[k] * fact[k] % MOD * fact[m - k]
            ) % MOD

        answer = (answer + sums[d] * positional_sum) % MOD

    print(answer)


if __name__ == "__main__":
    main()