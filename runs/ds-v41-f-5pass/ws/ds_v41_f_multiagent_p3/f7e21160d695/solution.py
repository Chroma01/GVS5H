import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    M = next(it)
    K = next(it)

    edges = []
    for _ in range(M):
        u = next(it)
        v = next(it)
        w = next(it)
        edges.append((w, u, v))

    A = [next(it) for _ in range(K)]
    B = [next(it) for _ in range(K)]

    diff = [0] * (N + 1)
    for a in A:
        diff[a] += 1
    for b in B:
        diff[b] -= 1

    parent = list(range(N + 1))
    size = [1] * (N + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges.sort(key=lambda e: e[0])
    ans = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        du = diff[ru]
        dv = diff[rv]

        if (du > 0 > dv) or (du < 0 < dv):
            ans += w * min(abs(du), abs(dv))

        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        diff[ru] = du + dv

    print(ans)

if __name__ == "__main__":
    main()