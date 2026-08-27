import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    p = data[1:1 + n]

    # Fenwick tree initially represents n available positions.
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    ans = [0] * (n + 1)
    highest = 1 << (n.bit_length() - 1)

    for i in range(n, 0, -1):
        k = p[i - 1]

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
        ans[pos] = i

        # Remove this position from the set of available slots.
        while pos <= n:
            bit[pos] -= 1
            pos += pos & -pos

    sys.stdout.write(" ".join(map(str, ans[1:])))


if __name__ == "__main__":
    main()