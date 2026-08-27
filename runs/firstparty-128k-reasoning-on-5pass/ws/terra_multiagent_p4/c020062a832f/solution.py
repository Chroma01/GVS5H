import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, value):
        i += 1
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += value
            i += i & -i

    def sum(self, i):
        """Sum of indices 0 through i inclusive."""
        i += 1
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

    freq = [0] * m
    for x in a:
        freq[x] += 1

    bit = Fenwick(m)
    inv = 0
    for i, x in enumerate(a):
        inv += i - bit.sum(x)
        bit.add(x, 1)

    # delta[x] = inversion count change when original value x wraps
    # from current maximum (M-1) to current minimum (0).
    delta = [0] * m
    seen = [0] * m
    for i, x in enumerate(a):
        same_before = seen[x]
        delta[x] += 2 * i - 2 * same_before - n + freq[x]
        seen[x] += 1

    out = []
    current = inv
    for k in range(m):
        out.append(str(current))
        if k + 1 < m:
            wrapping_value = m - 1 - k
            current += delta[wrapping_value]

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()