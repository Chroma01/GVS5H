import sys


class FenwickTree:
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


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = data[2:]

    freq = [0] * m
    for x in a:
        freq[x] += 1

    # delta[x] is the inversion-count change when original value x wraps
    # from current value M-1 to 0.
    delta = [0] * m
    seen = [0] * m
    for pos, x in enumerate(a):
        delta[x] += 2 * pos - 2 * seen[x] - n + freq[x]
        seen[x] += 1

    # Initial inversion count for k = 0.
    fenwick = FenwickTree(m)
    inv = 0
    for i, x in enumerate(a):
        # Number of earlier elements strictly greater than x.
        inv += i - fenwick.sum(x + 1)
        fenwick.add(x + 1, 1)

    answer = []
    for k in range(m):
        answer.append(str(inv))
        if k + 1 < m:
            wrapping_value = m - 1 - k
            inv += delta[wrapping_value]

    sys.stdout.write("\n".join(answer))


if __name__ == "__main__":
    main()