import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    M = N * K

    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = data[idx]
        v = data[idx + 1]
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    del data

    parent = [0] * (M + 1)
    parent[1] = -1
    order = []
    stack = [1]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    sub = [1] * (M + 1)
    for v in reversed(order):
        p = parent[v]
        if p > 0:
            sub[p] += sub[v]

    dsu = list(range(M + 1))
    comp = [1] * (M + 1)
    deg = [0] * (M + 1)

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if comp[ra] < comp[rb]:
            ra, rb = rb, ra
        dsu[rb] = ra
        comp[ra] += comp[rb]

    for v in range(2, M + 1):
        if sub[v] % K != 0:
            p = parent[v]
            deg[v] += 1
            deg[p] += 1
            union(v, p)

    ok = True
    for v in range(1, M + 1):
        if deg[v] > 2:
            ok = False
            break
        if comp[find(v)] != K:
            ok = False
            break

    sys.stdout.write("Yes\n" if ok else "No\n")

if __name__ == "__main__":
    main()