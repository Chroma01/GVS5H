import sys


class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
        for i in range(1, n + 1):
            self.bit[i] = i & -i

    def kth(self, k):
        index = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = index + step
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                index = nxt
            step >>= 1
        return index + 1

    def add(self, index, value):
        while index <= self.n:
            self.bit[index] += value
            index += index & -index


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    p = data[1:]

    fenwick = FenwickTree(n)
    answer = [0] * n

    for i in range(n, 0, -1):
        position = fenwick.kth(p[i - 1])
        answer[position - 1] = i
        fenwick.add(position, -1)

    print(*answer)


if __name__ == "__main__":
    main()