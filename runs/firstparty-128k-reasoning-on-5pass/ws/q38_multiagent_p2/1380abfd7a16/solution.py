import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Fenwick tree over N positions, initially all available (all ones).
    # For an all-ones array, bit[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, n + 1)]

    ans = [0] * n
    top = 1 << (n.bit_length() - 1)

    # Process values in reverse order.
    for i in range(n, 0, -1):
        k = data[i]  # P_i, because data[0] = N and data[1..N] = P_1..P_N

        # Find the k-th available position using Fenwick binary lifting.
        idx = 0
        step = top
        while step:
            nxt = idx + step
            if nxt <= n:
                b = bit[nxt]
                if b < k:
                    idx = nxt
                    k -= b
            step >>= 1

        pos = idx + 1
        ans[pos - 1] = i

        # Mark this position as used.
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(' '.join(map(str, ans)))

if __name__ == "__main__":
    main()