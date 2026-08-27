import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, x):
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s


def main():
    input = sys.stdin.readline
    n = int(input())
    p = list(map(int, input().split()))

    fw = Fenwick(n)
    ans = 0

    # Insert P_j into the already sorted prefix P_1..P_{j-1}.
    # Its rank r among the first j values determines that it crosses
    # boundaries r, r+1, ..., j-1.
    for j, x in enumerate(p, 1):
        r = fw.sum(x - 1) + 1
        ans += (j - 1) * j // 2 - (r - 1) * r // 2
        fw.add(x, 1)

    print(ans)


if __name__ == "__main__":
    main()