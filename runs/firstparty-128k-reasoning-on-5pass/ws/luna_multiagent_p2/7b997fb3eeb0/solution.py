import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # p[j] is the first index whose mochi can be the bottom
    # for mochi j, using zero-based indices.
    p = [bisect_left(a, 2 * a[j]) for j in range(n)]
    b = [p[j] - j for j in range(n)]

    # Sparse table for range maximum queries on b.
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i // 2] + 1

    sparse = [b]
    k = 1
    while (1 << k) <= n:
        length = 1 << k
        half = length >> 1
        prev = sparse[-1]
        sparse.append([
            max(prev[i], prev[i + half])
            for i in range(n - length + 1)
        ])
        k += 1

    def range_max(left, right):
        length = right - left
        level = log[length]
        row = sparse[level]
        span = 1 << level
        return max(row[left], row[right - span])

    q = next(it)
    ans = []

    for _ in range(q):
        l = next(it) - 1
        r = next(it) - 1
        length = r - l + 1

        # At most half of the mochi can be used.
        low, high = 0, length // 2

        while low < high:
            mid = (low + high + 1) // 2

            # The first mid mochi are used as tops. The last mid
            # mochi are used as bottoms, matched in order.
            if range_max(l, l + mid) <= length - mid:
                low = mid
            else:
                high = mid - 1

        ans.append(str(low))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()