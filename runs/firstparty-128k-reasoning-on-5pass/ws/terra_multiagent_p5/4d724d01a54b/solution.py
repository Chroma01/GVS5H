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
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result


def main():
    input = sys.stdin.readline
    n = int(input())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, value in enumerate(p, 1):
        pos[value] = i

    bit = FenwickTree(n)
    answer = 0

    # Process values increasingly. For value v, let k be its position
    # among values 1..v after values greater than v are ignored.
    for v in range(1, n + 1):
        k = bit.sum(pos[v]) + 1
        answer += (v - 1) * v // 2 - (k - 1) * k // 2
        bit.add(pos[v], 1)

    print(answer)


if __name__ == "__main__":
    main()