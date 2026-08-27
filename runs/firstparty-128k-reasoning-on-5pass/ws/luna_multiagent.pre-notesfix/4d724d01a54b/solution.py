import sys


class Fenwick:
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
    input = sys.stdin.readline

    n = int(input())
    p = list(map(int, input().split()))

    # pos[x] is the initial position of value x.
    pos = [0] * (n + 1)
    for i, value in enumerate(p, 1):
        pos[value] = i

    fw = Fenwick(n)
    answer = 0

    # Process values in increasing order.
    # For value x, c is the number of smaller values located before it.
    # In insertion-sort normal form, x crosses boundaries c+1 through pos[x]-1.
    for x in range(1, n + 1):
        current_position = pos[x]
        c = fw.sum(current_position - 1)

        a = current_position - 1
        answer += a * (a + 1) // 2 - c * (c + 1) // 2

        fw.add(current_position, 1)

    print(answer)


if __name__ == "__main__":
    main()