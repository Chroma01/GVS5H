import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Use a Fenwick tree over a power-of-two length.
    # The first n positions are initially empty (1), padding positions are 0.
    size = 1 << (n - 1).bit_length()
    tree = [0] + [1] * n + [0] * (size - n)

    # Build Fenwick tree from the initial array.
    t = tree
    sz = size
    for i in range(1, sz + 1):
        j = i + (i & -i)
        if j <= sz:
            t[j] += t[i]

    ans = [0] * n

    # For valid k, prefix(size) >= k, so the whole-tree check can be skipped.
    bit = size >> 1
    if bit == 0:
        bit = 1

    # Process insertions in reverse.
    for i in range(n, 0, -1):
        k = data[i]

        # Find the position of the k-th empty slot.
        idx = 0
        step = bit
        while step:
            nxt = idx + step
            if t[nxt] < k:
                idx = nxt
                k -= t[nxt]
            step >>= 1

        pos = idx + 1
        ans[pos - 1] = i

        # Mark this slot as filled.
        while pos <= sz:
            t[pos] -= 1
            pos += pos & -pos

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    main()