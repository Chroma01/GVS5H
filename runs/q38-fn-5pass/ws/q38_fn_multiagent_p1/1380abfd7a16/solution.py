import sys


def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    n = vals[0]

    # Pad the Fenwick tree to a power of two.  This lets the k-th search
    # avoid bounds checks: positions n+1..m are always zero.
    m = 1 << (n - 1).bit_length()

    # Fenwick tree over empty slots.
    # Initially slots 1..n are empty (value 1), padded slots are zero.
    bit = [0] * (m + 1)
    bit[1:n + 1] = [1] * n

    b = bit
    for i in range(1, m):
        j = i + (i & -i)
        if j <= m:
            b[j] += b[i]

    # Descending powers of two for binary lifting.
    steps = [m >> i for i in range(m.bit_length())]

    ans = [0] * n
    a = ans

    # Place values from N down to 1.
    for i in range(n, 0, -1):
        k = vals[i]
        idx = 0

        # Find the smallest 1-indexed position whose prefix sum is >= k.
        # idx becomes the 0-indexed answer position.
        for step in steps:
            nxt = idx + step
            val = b[nxt]
            if val < k:
                idx = nxt
                k -= val

        a[idx] = i

        # Mark this slot as occupied.
        j = idx + 1
        while j <= m:
            b[j] -= 1
            j += j & -j

    # Free large structures before building the output string.
    del vals, bit, b

    sys.stdout.write(" ".join(map(str, a)) + "\n")


if __name__ == "__main__":
    main()