import sys


def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    n = vals[0]

    # Fenwick tree over final positions.
    # Initially every position is empty, so the underlying array is all 1s.
    # For an all-ones Fenwick tree, tree[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, n + 1)]
    ans = [0] * n

    # Largest power of two not exceeding n, for k-th-one binary lifting.
    top = 1 << (n.bit_length() - 1)

    b = bit
    a = ans
    v = vals
    limit = n
    step0 = top

    # Reconstruct backwards: value i goes to the P_i-th empty position.
    for i in range(n, 0, -1):
        k = v[i]
        idx = 0
        step = step0

        # Find the k-th empty position (1-indexed k).
        while step:
            nxt = idx + step
            if nxt <= limit:
                val = b[nxt]
                if val < k:
                    idx = nxt
                    k -= val
            step >>= 1

        # idx is the zero-based final position.
        a[idx] = i

        # Mark this position as filled: add -1 in the Fenwick tree.
        j = idx + 1
        while j <= limit:
            b[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, a)) + "\n")


if __name__ == "__main__":
    main()