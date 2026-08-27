import sys


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    p = list(map(int, input().split()))

    # Fenwick tree initialized with 1 at every position.
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    result = [0] * n

    # Largest power of two not exceeding n.
    step = 1 << (n.bit_length() - 1)

    for i in range(n, 0, -1):
        k = p[i - 1]

        # Find the position of the k-th active slot.
        idx = 0
        s = step
        while s:
            nxt = idx + s
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            s >>= 1

        pos = idx + 1
        result[pos - 1] = i

        # Deactivate the selected slot.
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, result)))


if __name__ == "__main__":
    main()