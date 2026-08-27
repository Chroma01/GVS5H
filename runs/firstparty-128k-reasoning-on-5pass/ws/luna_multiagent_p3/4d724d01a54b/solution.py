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
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    p = data[1:]

    fenwick = Fenwick(n)
    answer = 0

    for j, x in enumerate(p, 1):
        previous_not_greater = fenwick.sum(x)
        greater_count = (j - 1) - previous_not_greater

        # The element crosses boundaries j-1, j-2, ..., j-greater_count.
        answer += greater_count * (2 * j - greater_count - 1) // 2
        fenwick.add(x, 1)

    print(answer)


if __name__ == "__main__":
    solve()