import sys

MOD = 998244353
ROOT = 3
ROOT_INV = pow(ROOT, MOD - 2, MOD)


def ntt_forward_dif(a):
    """Forward NTT: natural-order input to bit-reversed-order output."""
    n = len(a)
    length = n
    mod = MOD

    while length > 1:
        half = length >> 1
        wlen = pow(ROOT, (mod - 1) // length, mod)

        for start in range(0, n, length):
            w = 1
            end = start + half
            right = start + half

            for i in range(start, end):
                u = a[i]
                v = a[right]

                x = u + v
                if x >= mod:
                    x -= mod

                y = u - v
                if y < 0:
                    y += mod

                a[i] = x
                a[right] = y * w % mod

                right += 1
                w = w * wlen % mod

        length >>= 1


def ntt_inverse_dit(a):
    """Inverse NTT: bit-reversed-order input to natural-order output."""
    n = len(a)
    mod = MOD
    length = 2

    while length <= n:
        half = length >> 1
        wlen = pow(ROOT_INV, (mod - 1) // length, mod)

        for start in range(0, n, length):
            w = 1
            end = start + half
            right = start + half

            for i in range(start, end):
                u = a[i]
                v = a[right] * w % mod

                x = u + v
                if x >= mod:
                    x -= mod

                y = u - v
                if y < 0:
                    y += mod

                a[i] = x
                a[right] = y

                right += 1
                w = w * wlen % mod

        length <<= 1

    inv_n = pow(n, mod - 2, mod)
    for i in range(n):
        a[i] = a[i] * inv_n % mod


def main():
    data = sys.stdin.buffer.read()

    # First pass: determine max(S) without storing one million Python integers.
    first = True
    number = 0
    reading = False
    max_value = 0

    for ch in data:
        if 48 <= ch <= 57:
            number = number * 10 + ch - 48
            reading = True
        elif reading:
            if first:
                first = False
            elif number > max_value:
                max_value = number
            number = 0
            reading = False

    if reading and not first and number > max_value:
        max_value = number

    # Need transform length strictly greater than the largest possible index 2*max_value.
    size = 1
    limit = max_value << 1
    while size <= limit:
        size <<= 1

    present = bytearray(max_value + 1)
    poly = [0] * size

    # Second pass: fill the characteristic polynomial and membership table.
    first = True
    number = 0
    reading = False

    for ch in data:
        if 48 <= ch <= 57:
            number = number * 10 + ch - 48
            reading = True
        elif reading:
            if first:
                first = False
            else:
                present[number] = 1
                poly[number] = 1
            number = 0
            reading = False

    if reading and not first:
        present[number] = 1
        poly[number] = 1

    # DIF forward followed by DIT inverse avoids explicit O(size) bit-reversal passes.
    ntt_forward_dif(poly)

    for i in range(size):
        poly[i] = poly[i] * poly[i] % MOD

    ntt_inverse_dit(poly)

    answer = 0
    for b in range(1, max_value + 1):
        if present[b]:
            # poly[2*b] counts ordered pairs (A, C) with A+C=2*b.
            # Remove (b,b), then divide reversed endpoint orders.
            answer += (poly[b << 1] - 1) // 2

    print(answer)


if __name__ == "__main__":
    main()