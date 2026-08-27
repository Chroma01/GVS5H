import sys


class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, x):
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res


def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    fw = FenwickTree(m)
    inv = 0
    for i, x in enumerate(a):
        idx = x + 1
        inv += i - fw.sum(idx)
        fw.add(idx, 1)

    count = [0] * m
    pos_sum = [0] * m
    for pos, x in enumerate(a, 1):
        count[x] += 1
        pos_sum[x] += pos

    # When original value x wraps from M-1 to 0:
    # pairs with earlier distinct values become inversions, and
    # pairs with later distinct values cease being inversions.
    delta = [0] * m
    for x in range(m):
        delta[x] = 2 * pos_sum[x] - count[x] * (n + 1)

    ans = []
    cur = inv
    for k in range(m):
        ans.append(str(cur))
        cur += delta[m - 1 - k]

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()