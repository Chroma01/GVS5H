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

    def union_and_charge(self, a, b, w):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return 0

        x = self.balance[ra]
        y = self.balance[rb]

        add = 0
        if x > 0 and y < 0:
            add = min(x, -y) * w
        elif x < 0 and y > 0:
            add = min(-x, y) * w

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.balance[ra] = x + y
        return add


def main():
    input = sys.stdin.buffer.readline

    n, m, k = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    balance = [0] * n
    for x in a:
        balance[x - 1] += 1
    for x in b:
        balance[x - 1] -= 1

    edges.sort()

    dsu = DSU(n, balance)
    answer = 0
    used = 0

    for w, u, v in edges:
        ru = dsu.find(u)
        rv = dsu.find(v)
        if ru == rv:
            continue

        answer += dsu.union_and_charge(ru, rv, w)
        used += 1
        if used == n - 1:
            break

    print(answer)


if __name__ == "__main__":
    main()