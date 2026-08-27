import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    # p[i] is the first zero-based index j with A[j] >= 2*A[i].
    # If it does not exist, p[i] = n.
    # D[i] = p[i] - i, equivalent to the 1-based definition p_i - i.
    d = [bisect_left(a, 2 * x) - i for i, x in enumerate(a)]

    # Sparse table for range maximum queries on D.
    logs = [0] * (n + 1)
    for length in range(2, n + 1):
        logs[length] = logs[length // 2] + 1

    sparse = [d]
    level = 1
    while (1 << level) <= n:
        width = 1 << level
        half = width >> 1
        prev = sparse[-1]
        sparse.append([
            max(prev[i], prev[i + half])
            for i in range(n - width + 1)
        ])
        level += 1

    def range_max(left, right):
        """Maximum on the half-open interval [left, right)."""
        length = right - left
        k = logs[length]
        row = sparse[k]
        span = 1 << k
        return max(row[left], row[right - span])

    q = int(input())
    out = []

    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        length = r - l + 1

        # At most half the mochi can be used in pairs.
        low = 0
        high = length // 2 + 1  # exclusive upper bound

        while high - low > 1:
            k = (low + high) // 2

            # Pair the first k mochi with the last k mochi.
            # Their index difference is length - k.
            if range_max(l, l + k) <= length - k:
                low = k
            else:
                high = k

        out.append(str(low))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()