import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:]

    # Fenwick tree initialized to [1, 1, ..., 1].
    # For this initialization, tree[i] equals lowbit(i).
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    ans = [0] * n

    # Greatest power of two not exceeding n, for Fenwick binary lifting.
    step = 1 << (n.bit_length() - 1)

    for value in range(n, 0, -1):
        k = p[value - 1]

        # Find the smallest position pos such that prefix_sum(pos) >= k.
        idx = 0
        d = step
        while d:
            nxt = idx + d
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            d >>= 1
        pos = idx + 1

        ans[pos - 1] = value

        # Remove this available position.
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, ans)))


if __name__ == "__main__":
    solve()