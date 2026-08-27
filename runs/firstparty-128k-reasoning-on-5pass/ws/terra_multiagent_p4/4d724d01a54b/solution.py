import sys


class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, x):
        n = self.n
        while i <= n:
            self.bit[i] += x
            i += i & -i

    def sum(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    p = list(map(int, input().split()))

    bit = FenwickTree(n)
    answer = 0

    for i, x in enumerate(p, 1):
        # k = number of earlier elements smaller than x.
        # After inserting x at the end of the sorted prefix of length i,
        # it moves left to position k + 1, crossing edges k+1,...,i-1.
        k = bit.sum(x - 1)
        answer += (i - 1) * i // 2 - k * (k + 1) // 2
        bit.add(x, 1)

    print(answer)


if __name__ == "__main__":
    main()