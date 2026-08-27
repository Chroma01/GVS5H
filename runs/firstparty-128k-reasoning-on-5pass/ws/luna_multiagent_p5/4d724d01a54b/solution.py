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
    input = sys.stdin.buffer.readline
    n = int(input())
    p = list(map(int, input().split()))

    fw = Fenwick(n)
    answer = 0

    for j, value in enumerate(p, 1):
        seen = j - 1
        not_greater = fw.sum(value)
        greater = seen - not_greater

        # The value shifts left across `greater` elements.
        # It uses boundaries j-greater, ..., j-1.
        answer += greater * (2 * j - greater - 1) // 2

        fw.add(value, 1)

    print(answer)


if __name__ == "__main__":
    solve()