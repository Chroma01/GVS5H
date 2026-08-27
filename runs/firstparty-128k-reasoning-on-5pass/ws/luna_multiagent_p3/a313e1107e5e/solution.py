import sys
from bisect import bisect_left, bisect_right


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index, value):
        while index <= self.n:
            self.bit[index] += value
            index += index & -index

    def sum(self, index):
        result = 0
        while index > 0:
            result += self.bit[index]
            index -= index & -index
        return result


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    q = next(it)
    a = [next(it) for _ in range(n)]

    queries_by_r = [[] for _ in range(n + 1)]
    for query_id in range(q):
        r = next(it)
        x = next(it)
        queries_by_r[r].append((x, query_id))

    values = sorted(set(a))
    rank = {value: i + 1 for i, value in enumerate(values)}

    fenwick = Fenwick(len(values))
    tails = []
    answers = [0] * q

    for r in range(1, n + 1):
        value = a[r - 1]
        position = bisect_left(tails, value)

        if position < len(tails):
            old_value = tails[position]
            fenwick.add(rank[old_value], -1)
            tails[position] = value
        else:
            tails.append(value)

        fenwick.add(rank[value], 1)

        for x, query_id in queries_by_r[r]:
            count = bisect_right(values, x)
            answers[query_id] = fenwick.sum(count)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()