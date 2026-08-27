import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # p[x] = first index j >= x such that A[j] >= 2*A[x].
    # Indices here are zero-based; p[x] == n means no such index exists.
    p = [n] * n
    j = 0
    for x in range(n):
        if j < x + 1:
            j = x + 1
        while j < n and a[j] < 2 * a[x]:
            j += 1
        p[x] = j

    g = [p[x] - x for x in range(n)]

    # Sparse table for range maximum queries on g.
    logs = [0] * (n + 1)
    for length in range(2, n + 1):
        logs[length] = logs[length // 2] + 1

    sparse = [g]
    width = 1
    while (1 << width) <= n:
        prev = sparse[-1]
        size = n - (1 << width) + 1
        half = 1 << (width - 1)
        row = [0] * size
        for i in range(size):
            left = prev[i]
            right = prev[i + half]
            row[i] = left if left >= right else right
        sparse.append(row)
        width += 1

    def range_max(left, right):
        """Maximum on g[left:right], with right exclusive."""
        length = right - left
        level = logs[length]
        span = 1 << level
        row = sparse[level]
        x = row[left]
        y = row[right - span]
        return x if x >= y else y

    q = next(it)
    answers = []

    for _ in range(q):
        l = next(it) - 1
        r = next(it) - 1
        length = r - l + 1
        upper = length // 2

        # k = 0 is always feasible; upper + 1 is only a binary-search sentinel.
        lo, hi = 0, upper + 1
        while hi - lo > 1:
            k = (lo + hi) // 2
            maximum_g = range_max(l, l + k)
            if k + maximum_g <= length:
                lo = k
            else:
                hi = k

        answers.append(str(lo))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()