import sys
from bisect import bisect_right

INF = 10**18


class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.data = [INF] * (2 * size)

    def set(self, index, value):
        p = index + self.size
        self.data[p] = value
        p >>= 1
        while p:
            self.data[p] = min(self.data[p << 1], self.data[p << 1 | 1])
            p >>= 1

    def minimum(self, left, right):
        if left >= right:
            return INF

        left += self.size
        right += self.size
        result = INF

        while left < right:
            if left & 1:
                result = min(result, self.data[left])
                left += 1
            if right & 1:
                right -= 1
                result = min(result, self.data[right])
            left >>= 1
            right >>= 1

        return result


def solve_case(a):
    n = len(a)

    positions = {}
    for i, value in enumerate(a):
        positions.setdefault(value, []).append(i)

    run_end = [n] * n
    for i in range(n - 2, -1, -1):
        if a[i] == a[i + 1]:
            run_end[i] = run_end[i + 1]
        else:
            run_end[i] = i + 1

    dp = [0] * (n + 1)
    seg = SegmentTree(n + 1)
    seg.set(n, 2 * n)

    for i in range(n - 1, -1, -1):
        best = 1 + dp[run_end[i]]

        if i + 1 < n and a[i] != a[i + 1]:
            same_positions = positions[a[i]]
            p = bisect_right(same_positions, i + 1)
            next_same = same_positions[p] if p < len(same_positions) else n

            middle_best = seg.minimum(i + 2, next_same)
            if middle_best < INF:
                best = min(best, 3 - 2 * (i + 2) + middle_best)

            if next_same < n:
                best = min(
                    best,
                    3 + 2 * (next_same - (i + 2))
                    + dp[run_end[next_same]],
                )
            else:
                best = min(best, 3 + 2 * (n - (i + 2)))

        dp[i] = best
        seg.set(i, dp[i] + 2 * i)

    return dp[0]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    ptr = 1
    answers = []

    for _ in range(t):
        n = data[ptr]
        ptr += 1
        a = data[ptr:ptr + n]
        ptr += n
        answers.append(str(solve_case(a)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()