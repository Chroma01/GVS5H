import sys


class Fenwick:
    def __init__(self, size):
        self.size = size
        self.bit = [0] * (size + 1)

    def add(self, index, value):
        while index <= self.size:
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

    freq = [0] * m
    for x in a:
        freq[x] += 1

    bit = Fenwick(m)
    inversion = 0
    delta = [0] * m
    seen_count = [0] * m
    seen = 0

    for x in a:
        less_or_equal_before = bit.sum(x + 1)
        inversion += seen - less_or_equal_before

        same_before = seen_count[x]
        prior_non_equal = seen - same_before
        following_non_equal = (
            (n - seen - 1) - (freq[x] - same_before - 1)
        )
        delta[x] += prior_non_equal - following_non_equal

        bit.add(x + 1, 1)
        seen_count[x] += 1
        seen += 1

    answers = []
    current = inversion
    for x in range(m - 1, -1, -1):
        answers.append(str(current))
        current += delta[x]

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()