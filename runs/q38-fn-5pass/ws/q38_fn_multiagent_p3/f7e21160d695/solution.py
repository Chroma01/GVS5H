import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    idx = 3

    edges = [None] * M
    for i in range(M):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        edges[i] = (w, u, v)

    a = [0] * N
    b = [0] * N

    for _ in range(K):
        a[int(data[idx]) - 1] += 1
        idx += 1

    for _ in range(K):
        b[int(data[idx]) - 1] += 1
        idx += 1

    del data

    edges.sort()

    parent = list(range(N))
    size = [1] * N

    def find(x, parent=parent):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ans = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)

        if ru == rv:
            continue

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        au = a[ru]
        bu = b[ru]
        av = a[rv]
        bv = b[rv]

        matches = (
            min(au + av, bu + bv)
            - min(au, bu)
            - min(av, bv)
        )

        ans += matches * w

        parent[rv] = ru
        size[ru] += size[rv]
        a[ru] = au + av
        b[ru] = bu + bv

    print(ans)


if __name__ == "__main__":
    main()