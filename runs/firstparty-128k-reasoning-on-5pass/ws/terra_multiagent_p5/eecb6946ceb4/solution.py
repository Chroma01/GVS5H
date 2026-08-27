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
    mod = MOD
    root = PRIMITIVE_ROOT

    while length <= n:
        wlen = pow(root, (mod - 1) // length, mod)
        if invert:
            wlen = pow(wlen, mod - 2, mod)

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            end = start + half
            p = start
            q = end
            while p < end:
                u = a[p]
                v = a[q] * w % mod

                x = u + v
                if x >= mod:
                    x -= mod
                a[p] = x

                x = u - v
                if x < 0:
                    x += mod
                a[q] = x

                w = w * wlen % mod
                p += 1
                q += 1

        length <<= 1

    if invert:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    values = data[1:]

    present_set = set(values)

    # Pair enumeration is faster than NTT for genuinely sparse small inputs.
    if n <= 3000:
        vals = sorted(values)
        ans = 0
        contains = present_set
        for i in range(n):
            a = vals[i]
            for j in range(i + 1, n):
                c = vals[j]
                s = a + c
                if (s & 1) == 0 and (s >> 1) in contains:
                    ans += 1
        print(ans)
        return

    maximum = max(values)
    size = 1
    while size <= 2 * maximum:
        size <<= 1

    poly = [0] * size
    for x in values:
        poly[x] = 1

    ntt(poly, False)

    for i in range(size):
        poly[i] = poly[i] * poly[i] % MOD

    ntt(poly, True)

    ans = 0
    for b in values:
        # poly[2*b] counts ordered endpoint pairs.  The pair (b,b) is
        # included once; every valid pair with distinct endpoints appears twice.
        ans += (poly[b << 1] - 1) // 2

    print(ans)


if __name__ == "__main__":
    solve()