import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, value):
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += value
            i += i & -i

    def sum(self, i):
        result = 0
        bit = self.bit
        while i > 0:
            result += bit[i]
            i -= i & -i
        return result


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = data[2:]

    count = [0] * m
    pos_sum = [0] * m

    fenwick = Fenwick(m)
    inversions = 0

    for i, x in enumerate(a, 1):
        # Previous elements greater than x.
        inversions += (i - 1) - fenwick.sum(x + 1)
        fenwick.add(x + 1, 1)

        count[x] += 1
        pos_sum[x] += i

    delta = [0] * m
    n_plus_1 = n + 1
    for x in range(m):
        delta[x] = 2 * pos_sum[x] - count[x] * n_plus_1

    answers = []
    current = inversions

    for k in range(m):
        answers.append(str(current))
        wrapping_value = m - 1 - k
        current += delta[wrapping_value]

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()