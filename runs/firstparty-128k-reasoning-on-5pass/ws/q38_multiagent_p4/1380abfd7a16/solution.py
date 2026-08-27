import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Fenwick tree for empty positions.
    # Initially all N positions are empty, so bit[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, n + 1)]

    ans = [0] * (n + 1)

    # Powers of two for binary lifting, from largest to smallest.
    steps = tuple(1 << x for x in range(n.bit_length() - 1, -1, -1))

    b = bit
    a = ans
    d = data
    nn = n

    # Place labels in reverse order.
    for i in range(nn, 0, -1):
        k = d[i]  # P_i

        # Find the k-th empty position.
        idx = 0
        for step in steps:
            nxt = idx + step
            if nxt <= nn and b[nxt] < k:
                idx = nxt
                k -= b[nxt]
        pos = idx + 1

        a[pos] = i

        # Mark this position as occupied.
        j = pos
        while j <= nn:
            b[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, a[1:])))

if __name__ == "__main__":
    main()