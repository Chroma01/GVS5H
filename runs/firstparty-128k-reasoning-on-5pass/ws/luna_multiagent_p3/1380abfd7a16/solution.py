import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = [0] + data[1:n + 1]

    # Fenwick tree containing 1 for every currently available position.
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    result = [0] * (n + 1)
    highest = 1 << (n.bit_length() - 1)

    for value in range(n, 0, -1):
        k = p[value]

        # Find the position of the k-th available slot.
        idx = 0
        step = highest
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1

        pos = idx + 1
        result[pos] = value

        # Remove this position from the set of available slots.
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, result[1:])))


if __name__ == "__main__":
    main()