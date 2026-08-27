import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:]

    bit = [0] * (n + 1)

    # Initialize Fenwick tree with all positions available (value 1).
    # For an all-ones array, prefix sum structure has bit[i] = lowbit(i).
    for i in range(1, n + 1):
        bit[i] = i & -i

    ans = [0] * n

    # Largest power of two not exceeding n, for Fenwick binary lifting.
    step_start = 1 << (n.bit_length() - 1)

    for value in range(n, 0, -1):
        k = p[value - 1]

        # Find the smallest index pos with prefix_sum(pos) >= k.
        idx = 0
        step = step_start
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1

        pos = idx + 1
        ans[pos - 1] = value

        # Mark this position unavailable: add -1 at pos.
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, ans)))


if __name__ == "__main__":
    solve()