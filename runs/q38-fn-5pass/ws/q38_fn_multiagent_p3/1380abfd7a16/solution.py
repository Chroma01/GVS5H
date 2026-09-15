import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    p = list(map(int, it))
    del data, it

    # Use a Fenwick tree of length size, where size is a power of two >= n.
    # The first n positions are initially available (value 1), the rest are 0.
    size = 1 << (n - 1).bit_length()
    tree = [0] * (size + 1)

    # Build Fenwick tree for array [1]*n + [0]*(size-n) in O(size).
    for i in range(1, n + 1):
        tree[i] = i & -i
    for i in range(n + 1, size + 1):
        v = (i & -i) + n - i
        if v > 0:
            tree[i] = v

    # Bits used for Fenwick binary lifting.
    bits = []
    b = size >> 1
    while b:
        bits.append(b)
        b >>= 1

    ans = [0] * n
    tr = tree
    sz = size

    # Process insertions backwards.
    for i in range(n, 0, -1):
        k = p[i - 1]
        idx = 0

        # Find the k-th available position.
        for bit in bits:
            nxt = idx + bit
            if tr[nxt] < k:
                idx = nxt
                k -= tr[nxt]

        pos = idx + 1
        ans[pos - 1] = i

        # Mark this position as unavailable.
        while pos <= sz:
            tr[pos] -= 1
            pos += pos & -pos

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    main()