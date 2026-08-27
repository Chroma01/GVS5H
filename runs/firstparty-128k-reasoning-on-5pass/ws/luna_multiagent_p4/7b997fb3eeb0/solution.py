import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    # p[i] is the first index j such that A[j] >= 2 * A[i].
    p = [bisect_left(a, 2 * x) for x in a]
    values = [p[i] - i for i in range(n)]

    # Sparse table for range maximum queries on values.
    logs = [0] * (n + 1)
    for i in range(2, n + 1):
        logs[i] = logs[i // 2] + 1

    sparse = [values]
    length = 2
    while length <= n:
        prev = sparse[-1]
        half = length // 2
        sparse.append([
            max(prev[i], prev[i + half])
            for i in range(n - length + 1)
        ])
        length <<= 1

    def range_max(left, right):
        """Maximum on the half-open interval [left, right)."""
        size = right - left
        level = logs[size]
        table = sparse[level]
        span = 1 << level
        return max(table[left], table[right - span])

    q = int(input())
    answers = []

    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        m = r - l + 1

        low = 0
        high = m // 2

        while low < high:
            k = (low + high + 1) // 2

            # The k smallest mochi are used as bottoms, and the k largest
            # as tops. Their feasibility condition is:
            # max(p[i] - i) for i in [l, l+k) <= m-k.
            if range_max(l, l + k) <= m - k:
                low = k
            else:
                high = k - 1

        answers.append(str(low))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()