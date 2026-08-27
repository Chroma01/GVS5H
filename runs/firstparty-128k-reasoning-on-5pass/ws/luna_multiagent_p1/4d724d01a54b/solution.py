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
    input = sys.stdin.readline
    n = int(input())
    permutation = list(map(int, input().split()))

    position = [0] * (n + 1)
    for i, value in enumerate(permutation, 1):
        position[value] = i

    fenwick = Fenwick(n)
    for i in range(1, n + 1):
        fenwick.add(i, 1)

    answer = 0

    for value in range(n, 0, -1):
        current_rank = fenwick.sum(position[value])

        # Move the value from current_rank to rank value.
        # It crosses boundaries current_rank, ..., value - 1.
        answer += (current_rank + value - 1) * (value - current_rank) // 2

        fenwick.add(position[value], -1)

    print(answer)


if __name__ == "__main__":
    solve()