import sys
from bisect import bisect_left

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    n = data[pos]
    pos += 1
    a = data[pos:pos + n]
    pos += n

    # p[i] = first index j > i with A[j] >= 2 * A[i],
    # or n if no such index exists.
    b = [0] * n
    for i, value in enumerate(a):
        j = bisect_left(a, 2 * value, i + 1, n)
        b[i] = j - i

    # Sparse table for range maximum queries on b.
    logs = [0] * (n + 1)
    for length in range(2, n + 1):
        logs[length] = logs[length // 2] + 1

    sparse = [b]
    level = 1
    while (1 << level) <= n:
        span = 1 << level
        half = span >> 1
        previous = sparse[-1]
        sparse.append([
            max(previous[i], previous[i + half])
            for i in range(n - span + 1)
        ])
        level += 1

    def range_max(left, right):
        length = right - left
        k = logs[length]
        span = 1 << k
        row = sparse[k]
        return max(row[left], row[right - span])

    q = data[pos]
    pos += 1
    answers = []

    for _ in range(q):
        left = data[pos] - 1
        right = data[pos + 1]
        pos += 2

        length = right - left
        low = 0
        high = length // 2 + 1

        while high - low > 1:
            k = (low + high) // 2
            if range_max(left, left + k) <= length - k:
                low = k
            else:
                high = k

        answers.append(str(low))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()