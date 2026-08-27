import sys


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
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    bit = Fenwick(m)
    inversions = 0

    for i, value in enumerate(a):
        index = value + 1
        inversions += i - bit.sum(index)
        bit.add(index, 1)

    delta = [0] * m
    for i, value in enumerate(a):
        delta[value] += 2 * (i + 1) - n - 1

    answers = []
    current = inversions

    for k in range(m):
        answers.append(str(current))
        current += delta[m - 1 - k]

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()