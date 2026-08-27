import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N, M, K = data[idx], data[idx + 1], data[idx + 2]
    idx += 3

    edges = []
    append = edges.append
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        w = data[idx + 2]
        idx += 3
        append((w, u, v))

    net = [0] * N
    for _ in range(K):
        net[data[idx] - 1] += 1
        idx += 1
    for _ in range(K):
        net[data[idx] - 1] -= 1
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
    min_ = min

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        nu = net[ru]
        nv = net[rv]

        if nu > 0 and nv < 0:
            ans += w * min_(nu, -nv)
        elif nu < 0 and nv > 0:
            ans += w * min_(-nu, nv)

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        parent[rv] = ru
        size[ru] += size[rv]
        net[ru] += net[rv]

    print(ans)

if __name__ == "__main__":
    main()