import sys


class DSU:
    def __init__(self, n, balance):
        self.parent = list(range(n))
        self.size = [1] * n
        self.balance = balance

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b, w):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return 0

        x = self.balance[a]
        y = self.balance[b]
        added_pairs = (abs(x) + abs(y) - abs(x + y)) // 2
        cost = w * added_pairs

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]
        self.balance[a] = x + y
        return cost


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    k = next(it)

    edges = []
    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        w = next(it)
        edges.append((w, u, v))

    balance = [0] * n
    for _ in range(k):
        balance[next(it) - 1] += 1
    for _ in range(k):
        balance[next(it) - 1] -= 1

    edges.sort()
    dsu = DSU(n, balance)

    answer = 0
    for w, u, v in edges:
        answer += dsu.union(u, v, w)

    print(answer)


if __name__ == "__main__":
    main()