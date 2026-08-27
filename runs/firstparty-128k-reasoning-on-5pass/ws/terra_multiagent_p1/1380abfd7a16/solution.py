import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:]

    # Fenwick tree initialized with 1 at every position.
    # For an all-ones array, tree[i] = lowbit(i).
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    ans = [0] * (n + 1)

    # Largest power of two not exceeding n, for Fenwick binary lifting.
    step_start = 1 << (n.bit_length() - 1)

    for value in range(n, 0, -1):
        k = p[value - 1]

        # Find the smallest index pos whose prefix sum is at least k.
        pos = 0
        step = step_start
        while step:
            nxt = pos + step
            if nxt <= n and bit[nxt] < k:
                pos = nxt
                k -= bit[nxt]
            step >>= 1
        pos += 1

        ans[pos] = value

        # Mark this position occupied: subtract one from free-position count.
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(" ".join(map(str, ans[1:])))


if __name__ == "__main__":
    solve()