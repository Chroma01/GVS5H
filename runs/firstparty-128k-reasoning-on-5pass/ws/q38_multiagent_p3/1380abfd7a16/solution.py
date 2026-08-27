import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]

    # Power of two >= n.  The Fenwick tree is padded to this size.
    size = 1 << ((n - 1).bit_length())

    # Fenwick tree for an array of ones on positions 1..n and zeros after.
    # For a full array of ones, bit[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, size + 1)]

    # Fix nodes whose interval extends beyond n.
    for i in range(n + 1, size + 1):
        left = i - (i & -i)
        if left < n:
            bit[i] = n - left
        else:
            bit[i] = 0

    ans = [0] * n

    # Binary lifting steps for kth-element search.
    # Starting from size/2 is enough because size is a power of two.
    steps = []
    step = size >> 1
    while step:
        steps.append(step)
        step >>= 1
    steps = tuple(steps)

    b = bit
    a = ans
    d = data
    sz = size

    for i in range(n, 0, -1):
        k = d[i]
        idx = 0

        # Find the k-th empty position (1-indexed position is idx + 1).
        for st in steps:
            nxt = idx + st
            v = b[nxt]
            if v < k:
                idx = nxt
                k -= v

        a[idx] = i

        # Mark this position occupied.
        # The root index sz is never read by the kth search, so stop before it.
        j = idx + 1
        while j < sz:
            b[j] -= 1
            j += j & -j

    sys.stdout.write(' '.join(map(str, a)))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()