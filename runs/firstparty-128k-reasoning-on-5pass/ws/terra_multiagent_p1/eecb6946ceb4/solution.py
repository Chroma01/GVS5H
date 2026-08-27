import sys

MOD = 998244353
PRIMITIVE_ROOT = 3


def ntt(a, roots):
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
        step = n // length

        base = 0
        while base < n:
            left = base
            right = base + half
            root_index = 0
            end = right

            while left < end:
                u = a[left]
                v = a[right] * roots[root_index] % MOD

                x = u + v
                if x >= MOD:
                    x -= MOD

                y = u - v
                if y < 0:
                    y += MOD

                a[left] = x
                a[right] = y

                left += 1
                right += 1
                root_index += step

            base += length

        length <<= 1


def main():
    tokens = sys.stdin.buffer.read().split()
    if len(tokens) <= 1:
        print(0)
        return

    present = bytearray(1_000_001)
    maximum = 0

    for token in tokens[1:]:
        x = int(token)
        present[x] = 1
        if x > maximum:
            maximum = x

    del tokens

    size = 1 << (2 * maximum).bit_length()

    a = [0] * size
    for x in range(1, maximum + 1):
        if present[x]:
            a[x] = 1

    root_n = pow(PRIMITIVE_ROOT, (MOD - 1) // size, MOD)
    roots = [1] * (size >> 1)
    for i in range(1, size >> 1):
        roots[i] = roots[i - 1] * root_n % MOD

    ntt(a, roots)

    for i in range(size):
        a[i] = a[i] * a[i] % MOD

    # Inverse NTT can be obtained as:
    # inverse(a) = forward(reverse indices 1..n-1) / n.
    left = 1
    right = size - 1
    while left < right:
        a[left], a[right] = a[right], a[left]
        left += 1
        right -= 1

    ntt(a, roots)

    inv_size = pow(size, MOD - 2, MOD)
    answer = 0

    # For a present B:
    # convolution[2B] = 1 + 2 * (# valid endpoint pairs A < B < C).
    for b in range(1, maximum + 1):
        if present[b]:
            coefficient = a[b + b] * inv_size % MOD
            answer += (coefficient - 1) // 2

    print(answer)


if __name__ == "__main__":
    main()