import sys
from bisect import bisect_right


class FenwickMax:
    def __init__(self, size):
        self.size = size
        self.bit = [0] * (size + 1)

    def update(self, index, value):
        while index <= self.size:
            if self.bit[index] < value:
                self.bit[index] = value
            index += index & -index

    def query(self, index):
        result = 0
        while index > 0:
            if result < self.bit[index]:
                result = self.bit[index]
            index -= index & -index
        return result


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    q = next(it)
    a = [next(it) for _ in range(n)]

    values = sorted(set(a))
    rank = {value: i + 1 for i, value in enumerate(values)}

    queries_by_r = [[] for _ in range(n + 1)]
    for query_id in range(q):
        r = next(it)
        x = next(it)
        queries_by_r[r].append((x, query_id))

    fenwick = FenwickMax(len(values))
    answers = [0] * q

    for r in range(1, n + 1):
        value = a[r - 1]
        pos = rank[value]

        # Only strictly smaller values may precede value.
        current_length = fenwick.query(pos - 1) + 1
        fenwick.update(pos, current_length)

        for x, query_id in queries_by_r[r]:
            # All values <= x correspond to compressed positions <= this.
            limit = bisect_right(values, x)
            answers[query_id] = fenwick.query(limit)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()