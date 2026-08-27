import sys


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

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = 0
    unions = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)

        if ru == rv:
            continue

        bu = balance[ru]
        bv = balance[rv]

        if (bu < 0 < bv) or (bv < 0 < bu):
            answer += w * min(abs(bu), abs(bv))

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        parent[rv] = ru
        size[ru] += size[rv]
        balance[ru] = bu + bv

        unions += 1
        if unions == n - 1:
            break

    print(answer)


if __name__ == "__main__":
    main()