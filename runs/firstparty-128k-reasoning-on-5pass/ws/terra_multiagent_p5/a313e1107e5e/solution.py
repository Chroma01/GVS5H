import sys
from bisect import bisect_right


class FenwickMax:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, value):
        n = self.n
        while i <= n:
            if value > self.bit[i]:
                self.bit[i] = value
            i += i & -i

    def query(self, i):
        result = 0
        while i > 0:
            if self.bit[i] > result:
                result = self.bit[i]
            i -= i & -i
        return result


def main():
    input = sys.stdin.buffer.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    queries = [tuple(map(int, input().split())) for _ in range(q)]

    values = sorted(set(a))
    m = len(values)
    compressed = [bisect_right(values, x) for x in a]

    # dp[i] = best strictly increasing subsequence length ending at A[i].
    lis_bit = FenwickMax(m)
    dp = [0] * n
    for i, idx in enumerate(compressed):
        dp[i] = lis_bit.query(idx - 1) + 1
        lis_bit.update(idx, dp[i])

    # Answer queries in nondecreasing prefix endpoint order.
    ordered_queries = sorted(
        ((r, x, qi) for qi, (r, x) in enumerate(queries)),
        key=lambda item: item[0]
    )

    answer_bit = FenwickMax(m)
    answers = [0] * q
    pos = 0

    for r, x, qi in ordered_queries:
        while pos < r:
            answer_bit.update(compressed[pos], dp[pos])
            pos += 1

        limit = bisect_right(values, x)
        answers[qi] = answer_bit.query(limit)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    main()