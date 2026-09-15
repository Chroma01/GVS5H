import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    m = n * k

    adj = [[] for _ in range(m)]
    for _ in range(m - 1):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        adj[u].append(v)
        adj[v].append(u)

    # BFS from root 0 to get parent and traversal order
    parent = [-1] * m
    parent[0] = -2  # sentinel: root has no parent
    order = [0]
    head = 0
    while head < len(order):
        u = order[head]; head += 1
        pu = parent[u]
        for w in adj[u]:
            if w != pu:
                parent[w] = u
                order.append(w)

    # subtree sizes via reverse BFS order
    sz = [1] * m
    for u in reversed(order):
        p = parent[u]
        if p >= 0:
            sz[p] += sz[u]

    # count forced edges incident to each vertex; degree must be <= 2
    for u in order:
        d = 0
        for w in adj[u]:
            if parent[w] == u:            # w is a child of u
                if sz[w] % k != 0:
                    d += 1
        if parent[u] >= 0 and sz[u] % k != 0:
            d += 1                         # edge to parent is forced
        if d > 2:
            print("No")
            return

    print("Yes")

main()