import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
        for i in range(1, n + 1):
            self.bit[i] = i & -i

    def kth(self, k):
        """Return the smallest index whose prefix sum is at least k."""
        idx = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            step >>= 1
        return idx + 1

    def remove(self, index):
        while index <= self.n:
            self.bit[index] -= 1
            index += index & -index


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    p = data[1:]

    fenwick = Fenwick(n)
    answer = [0] * n

    for value in range(n, 0, -1):
        position = fenwick.kth(p[value - 1])
        answer[position - 1] = value
        fenwick.remove(position)

    sys.stdout.write(" ".join(map(str, answer)))


if __name__ == "__main__":
    main()