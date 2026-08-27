import sys
from bisect import bisect_left, bisect_right


class FenwickMax:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, value):
        while i <= self.n:
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

    queries = []
    for qi in range(q):
        r, x = map(int, input().split())
        queries.append((r, x, qi))

    values = sorted(set(a))
    m = len(values)

    # Process query prefixes in increasing order.
    queries.sort()

    bit = FenwickMax(m)
    answers = [0] * q
    processed = 0

    for r, x, qi in queries:
        while processed < r:
            value = a[processed]
            pos = bisect_left(values, value) + 1

            # Strictly increasing: only values with compressed index < pos
            # may precede this value.
            dp = bit.query(pos - 1) + 1
            bit.update(pos, dp)

            processed += 1

        # All compressed array values with index < limit are <= x.
        limit = bisect_right(values, x)
        answers[qi] = bit.query(limit)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    main()