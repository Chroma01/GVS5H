import sys
from bisect import bisect_left, bisect_right


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
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    q = next(it)
    a = [next(it) for _ in range(n)]

    queries_by_r = [[] for _ in range(n + 1)]
    for qi in range(q):
        r = next(it)
        x = next(it)
        queries_by_r[r].append((x, qi))

    values = sorted(set(a))
    m = len(values)

    tails = []
    fenwick = FenwickMax(m)
    answers = [0] * q

    for i, value in enumerate(a, 1):
        pos = bisect_left(tails, value)
        dp = pos + 1

        if pos == len(tails):
            tails.append(value)
        else:
            tails[pos] = value

        compressed_pos = bisect_left(values, value) + 1
        fenwick.update(compressed_pos, dp)

        for x, qi in queries_by_r[i]:
            limit = bisect_right(values, x)
            answers[qi] = fenwick.query(limit)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    main()