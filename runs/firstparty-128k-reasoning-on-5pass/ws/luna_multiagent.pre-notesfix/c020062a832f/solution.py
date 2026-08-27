import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result


def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))

    counts = [0] * M
    position_sums = [0] * M

    bit = Fenwick(M)
    inversions = 0

    for i, x in enumerate(A):
        # Previous elements greater than x.
        inversions += i - bit.sum(x + 1)
        bit.add(x + 1, 1)

        counts[x] += 1
        position_sums[x] += i

    # For class x, all its elements currently have value M-1
    # immediately before the shift that wraps them to 0.
    #
    # For an element at position i in this class:
    # delta = (# non-class elements to its left)
    #       - (# non-class elements to its right).
    # Summing over the class gives:
    # delta[x] = 2 * position_sums[x] - (N - 1) * counts[x].
    delta = [
        2 * position_sums[x] - (N - 1) * counts[x]
        for x in range(M)
    ]

    answers = []
    current = inversions

    for k in range(M):
        answers.append(str(current))
        wrapping_class = (M - 1 - k) % M
        current += delta[wrapping_class]

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()