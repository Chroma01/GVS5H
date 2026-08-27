import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:]

    # Fenwick tree initially representing N available positions, all with value 1.
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    ans = [0] * n

    def kth(k: int) -> int:
        """Return the smallest 1-indexed index with prefix sum at least k."""
        idx = 0
        step = 1 << (n.bit_length() - 1)

        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1

        return idx + 1

    for value in range(n, 0, -1):
        pos = kth(p[value - 1])
        ans[pos - 1] = value

        i = pos
        while i <= n:
            bit[i] -= 1
            i += i & -i

    sys.stdout.write(" ".join(map(str, ans)))


if __name__ == "__main__":
    solve()