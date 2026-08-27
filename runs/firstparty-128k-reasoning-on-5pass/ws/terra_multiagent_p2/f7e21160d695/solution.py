import sys


class DSU:
    def __init__(self, n, count_a, count_b):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count_a = count_a
        self.count_b = count_b

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return -1

        if self.size[x] < self.size[y]:
            x, y = y, x

        self.parent[y] = x
        self.size[x] += self.size[y]
        self.count_a[x] += self.count_a[y]
        self.count_b[x] += self.count_b[y]

        paired = min(self.count_a[x], self.count_b[x])
        self.count_a[x] -= paired
        self.count_b[x] -= paired
        return paired


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

    count_a = [0] * n
    count_b = [0] * n

    for _ in range(k):
        count_a[next(it) - 1] += 1
    for _ in range(k):
        count_b[next(it) - 1] += 1

    edges.sort()
    dsu = DSU(n, count_a, count_b)

    answer = 0
    for w, u, v in edges:
        paired = dsu.merge(u, v)
        if paired > 0:
            answer += w * paired

    print(answer)


if __name__ == "__main__":
    main()