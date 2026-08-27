import sys


def solve():
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

    parent = list(range(n))
    size = [1] * n

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

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        if balance[ru] > 0 and balance[rv] < 0:
            answer += w * min(balance[ru], -balance[rv])
        elif balance[ru] < 0 and balance[rv] > 0:
            answer += w * min(-balance[ru], balance[rv])

        parent[rv] = ru
        size[ru] += size[rv]
        balance[ru] += balance[rv]

    print(answer)


if __name__ == "__main__":
    solve()