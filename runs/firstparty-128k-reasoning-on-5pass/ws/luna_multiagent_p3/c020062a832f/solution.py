import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, value):
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def sum(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * m
    pos_sum = [0] * m

    fenwick = Fenwick(m)
    inversions = 0

    for pos, value in enumerate(a, 1):
        seen = pos - 1
        not_greater = fenwick.sum(value + 1)
        inversions += seen - not_greater
        fenwick.add(value + 1, 1)

        freq[value] += 1
        pos_sum[value] += pos

    answers = []
    current = inversions

    for k in range(m):
        answers.append(str(current))
        if k < m - 1:
            x = m - 1 - k
            current += 2 * pos_sum[x] - freq[x] * (n + 1)

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()