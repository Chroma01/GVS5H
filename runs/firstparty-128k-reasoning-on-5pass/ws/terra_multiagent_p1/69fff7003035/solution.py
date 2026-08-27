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

    if len(a) * len(b) <= 10000:
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

    fa = a[:] + [0] * (size - len(a))
    fb = b[:] + [0] * (size - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:need]


def main():
    data = sys.stdin.buffer.readline()
    if not data:
        return
    n = int(data)

    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    groups = []
    low = 1
    d = 1
    while low <= n:
        high = min(n, 10 ** d - 1)
        count = high - low + 1
        groups.append((d, count, low, high))
        low *= 10
        d += 1

    # P(t) = product_d (1 + 10^d t)^c_d
    p = [1]
    for d, c, _, _ in groups:
        base = pow(10, d, MOD)
        factor = [0] * (c + 1)
        factor[0] = 1
        cur = 1
        for k in range(1, c + 1):
            cur = cur * (c - k + 1) % MOD
            cur = cur * inv[k] % MOD
            cur = cur * base % MOD
            factor[k] = cur
        p = convolution(p, factor)

    arrangement_weight = [0] * n
    for k in range(n):
        arrangement_weight[k] = fact[k] * fact[n - 1 - k] % MOD

    answer = 0

    # For a value whose digit length is d:
    # Q_d(t) = P(t) / (1 + 10^d t).
    # If q_k is its coefficient, its total multiplier is
    # sum_k q_k * k! * (N-1-k)!.
    for d, _, low, high in groups:
        base = pow(10, d, MOD)
        q_prev = 0
        multiplier_sum = 0

        for k in range(n):
            q_cur = p[k] - base * q_prev % MOD
            if q_cur < 0:
                q_cur += MOD
            multiplier_sum += q_cur * arrangement_weight[k]
            if multiplier_sum >= MOD:
                multiplier_sum %= MOD
            q_prev = q_cur

        multiplier_sum %= MOD
        value_sum = (low + high) * (high - low + 1) // 2
        answer = (answer + (value_sum % MOD) * multiplier_sum) % MOD

    print(answer)


if __name__ == "__main__":
    main()