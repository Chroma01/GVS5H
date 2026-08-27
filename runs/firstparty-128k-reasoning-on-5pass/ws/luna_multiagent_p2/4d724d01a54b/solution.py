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
    n = int(input())
    p = list(map(int, input().split()))

    fenwick = Fenwick(n)
    answer = 0

    for j, x in enumerate(p, 1):
        not_greater = fenwick.sum(x)
        larger = (j - 1) - not_greater

        # x crosses boundaries j-larger, ..., j-1.
        answer += larger * (2 * j - larger - 1) // 2

        fenwick.add(x, 1)

    print(answer)


if __name__ == "__main__":
    solve()