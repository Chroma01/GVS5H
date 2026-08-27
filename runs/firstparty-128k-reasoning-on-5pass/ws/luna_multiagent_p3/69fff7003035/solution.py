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
            end = start + half
            for i in range(start, end):
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

    if len(a) * len(b) <= 5000:
        c = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    c[i + j] = (c[i + j] + x * y) % MOD
        return c

    need = len(a) + len(b) - 1
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
    n = int(sys.stdin.readline())

    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD

    invfac = [1] * (n + 1)
    invfac[n] = pow(fac[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfac[i - 1] = invfac[i] * i % MOD

    inv = [0] * (n + 2)
    inv[1] = 1
    for i in range(2, n + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    groups = []
    start = 1
    digit_length = 1
    while start <= n:
        end = min(n, 10 ** digit_length - 1)
        count = end - start + 1
        weight_sum = (start + end) * count // 2
        groups.append((count, weight_sum, (pow(10, digit_length, MOD) - 1) % MOD))
        start = end + 1
        digit_length += 1

    # F(t) = product over j of (1 + (10^{d_j} - 1)t)
    # Each group contributes (1 + a*t)^count.
    poly = [1]
    for count, _, a in groups:
        part = [1]
        for k in range(1, count + 1):
            value = part[-1]
            value = value * (count - k + 1) % MOD
            value = value * inv[k] % MOD
            value = value * a % MOD
            part.append(value)
        poly = convolution(poly, part)

    # For a group with factor (1 + a*t), obtain F(t)/(1 + a*t)
    # by coefficient recurrence, then integrate the quotient.
    weighted_sum = 0
    for _, group_sum, a in groups:
        quotient_coeff = 1
        integral = 1  # coefficient of t^0 divided by 1
        for k in range(1, n):
            quotient_coeff = (poly[k] - a * quotient_coeff) % MOD
            integral = (integral + quotient_coeff * inv[k + 1]) % MOD
        weighted_sum = (weighted_sum + (group_sum % MOD) * integral) % MOD

    answer = fac[n] * weighted_sum % MOD
    print(answer)


if __name__ == "__main__":
    solve()