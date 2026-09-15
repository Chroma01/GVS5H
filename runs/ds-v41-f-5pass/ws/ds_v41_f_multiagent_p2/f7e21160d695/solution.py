import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N = data[idx]
    M = data[idx + 1]
    K = data[idx + 2]
    idx += 3

    edges = []
    for _ in range(M):
        u = data[idx]
        v = data[idx + 1]
        w = data[idx + 2]
        idx += 3
        edges.append((w, u, v))

    balance = [0] * (N + 1)

    for _ in range(K):
        a = data[idx]
        idx += 1
        balance[a] += 1

    for _ in range(K):
        b = data[idx]
        idx += 1
        balance[b] -= 1

    edges.sort(key=lambda x: x[0])

    parent = list(range(N + 1))
    size = [1] * (N + 1)

    def find(x):
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

        bu = balance[ru]
        bv = balance[rv]

        if bu * bv < 0:
            au = bu if bu >= 0 else -bu
            av = bv if bv >= 0 else -bv
            ans += w * (au if au < av else av)

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        parent[rv] = ru
        size[ru] += size[rv]
        balance[ru] += balance[rv]

    print(ans)


if __name__ == "__main__":
    main()