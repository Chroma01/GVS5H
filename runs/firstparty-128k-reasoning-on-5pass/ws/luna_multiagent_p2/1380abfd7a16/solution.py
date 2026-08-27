import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    p = [0] + data[1:]

    # Fenwick tree containing 1 for every currently available position.
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    result = [0] * (n + 1)

    # Find the position of the k-th available slot.
    def kth(k):
        index = 0
        step = 1 << (n.bit_length() - 1)
        while step:
            nxt = index + step
            if nxt <= n and bit[nxt] < k:
                index = nxt
                k -= bit[nxt]
            step >>= 1
        return index + 1

    for value in range(n, 0, -1):
        pos = kth(p[value])
        result[pos] = value

        # Mark this position as unavailable.
        i = pos
        while i <= n:
            bit[i] -= 1
            i += i & -i

    sys.stdout.write(" ".join(map(str, result[1:])))


if __name__ == "__main__":
    main()