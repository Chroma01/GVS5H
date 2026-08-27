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

    for j, value in enumerate(p, 1):
        smaller = fenwick.sum(value - 1)
        insertion_position = smaller + 1

        # Sum of boundaries insertion_position through j - 1.
        answer += (j - 1) * j // 2
        answer -= (insertion_position - 1) * insertion_position // 2

        fenwick.add(value, 1)

    print(answer)


if __name__ == "__main__":
    solve()