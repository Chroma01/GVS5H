import sys

MOD = 998244353
ROOT = 3
ROOT_INV = 332748118


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
    root = ROOT_INV if invert else ROOT
    mod = MOD

    while length <= n:
        half = length >> 1
        wlen = pow(root, (mod - 1) // length, mod)

        for start in range(0, n, length):
            w = 1
            end = start + half
            for p in range(start, end):
                u = a[p]
                v = a[p + half] * w % mod

                x = u + v
                if x >= mod:
                    x -= mod
                y = u - v
                if y < 0:
                    y += mod

                a[p] = x
                a[p + half] = y
                w = w * wlen % mod

        length <<= 1

    if invert:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod


def main():
    data = sys.stdin.buffer.read()

    present = bytearray(1_000_001)
    count = 0
    maximum = 0
    value = 0
    in_number = False

    for ch in data:
        if 48 <= ch <= 57:
            value = value * 10 + ch - 48
            in_number = True
        elif in_number:
            if count > 0:
                present[value] = 1
                if value > maximum:
                    maximum = value
            count += 1
            value = 0
            in_number = False

    if in_number:
        if count > 0:
            present[value] = 1
            if value > maximum:
                maximum = value
        count += 1

    n = count - 1  # First parsed integer is N.
    if n < 3:
        print(0)
        return

    size = 1
    needed = maximum * 2 + 1
    while size < needed:
        size <<= 1

    poly = list(present[:maximum + 1])
    poly.extend([0] * (size - len(poly)))

    ntt(poly, False)
    for i, x in enumerate(poly):
        poly[i] = x * x % MOD
    ntt(poly, True)

    answer = 0
    for b in range(1, maximum + 1):
        if present[b]:
            answer += (poly[b + b] - 1) // 2

    print(answer)


if __name__ == "__main__":
    main()