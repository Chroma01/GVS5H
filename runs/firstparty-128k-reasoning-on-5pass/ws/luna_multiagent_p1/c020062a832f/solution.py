import sys


class Fenwick:
    def __init__(self, size):
        self.size = size
        self.bit = [0] * (size + 1)

    def add(self, index, value):
        while index <= self.size:
            self.bit[index] += value
            index += index & -index

    def prefix_sum(self, index):
        result = 0
        while index > 0:
            result += self.bit[index]
            index -= index & -index
        return result


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    counts = [0] * m
    position_sums = [0] * m

    fenwick = Fenwick(m)
    inversion_count = 0

    for i, value in enumerate(a):
        # Previous elements greater than value.
        inversion_count += i - fenwick.prefix_sum(value + 1)
        fenwick.add(value + 1, 1)

        counts[value] += 1
        position_sums[value] += i

    answers = []

    for k in range(m):
        answers.append(str(inversion_count))

        # At this shift, original value x is currently M - 1.
        # It wraps to 0 when moving from shift k to k + 1.
        x = (m - 1 - k) % m
        inversion_count += (
            2 * position_sums[x] - counts[x] * (n - 1)
        )

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()