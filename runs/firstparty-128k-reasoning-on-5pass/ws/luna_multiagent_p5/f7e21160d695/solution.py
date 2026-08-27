import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    k = next(it)

    edges = []
    for _ in range(m):
        u = next(it)
        v = next(it)
        w = next(it)
        edges.append((w, u, v))

    balance = [0] * (n + 1)

    for _ in range(k):
        balance[next(it)] += 1

    for _ in range(k):
        balance[next(it)] -= 1

    edges.sort()

    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)

        if ru == rv:
            continue

        x = balance[ru]
        y = balance[rv]

        if x > 0 and y < 0:
            answer += w * min(x, -y)
        elif x < 0 and y > 0:
            answer += w * min(-x, y)

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        parent[rv] = ru
        size[ru] += size[rv]
        balance[ru] = x + y

    print(answer)


if __name__ == "__main__":
    solve()