import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    total = N * K

    adj = [[] for _ in range(total + 1)]
    edges = []
    for _ in range(total - 1):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))

    # Iterative DFS from root 1: build parent array and traversal order
    parent = [0] * (total + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        node = stack.pop()
        order.append(node)
        for nb in adj[node]:
            if nb != parent[node]:
                parent[nb] = node
                stack.append(nb)

    # Subtree sizes via reverse accumulation
    size = [1] * (total + 1)
    for node in reversed(order):
        p = parent[node]
        if p != -1:
            size[p] += size[node]

    # DSU for kept components
    dsu_parent = list(range(total + 1))
    comp_size = [1] * (total + 1)

    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if comp_size[ra] < comp_size[rb]:
            ra, rb = rb, ra
        dsu_parent[rb] = ra
        comp_size[ra] += comp_size[rb]

    kept_deg = [0] * (total + 1)

    # Keep edge parent-child iff child subtree size is not a multiple of K
    for node in order:
        p = parent[node]
        if p == -1:
            continue
        if size[node] % K != 0:
            union(p, node)
            kept_deg[p] += 1
            kept_deg[node] += 1

    # Validation: kept-degree <= 2 everywhere
    for v in range(1, total + 1):
        if kept_deg[v] > 2:
            sys.stdout.write("No\n")
            return

    # Validation: every kept component has exactly K vertices
    for v in range(1, total + 1):
        if find(v) == v and comp_size[v] != K:
            sys.stdout.write("No\n")
            return

    sys.stdout.write("Yes\n")

main()