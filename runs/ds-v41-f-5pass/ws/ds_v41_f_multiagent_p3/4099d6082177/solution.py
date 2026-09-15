import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    K = int(data[pos]); pos += 1
    n = N * K

    # K == 1: every vertex is its own path of 1 vertex -> always Yes
    if K == 1:
        sys.stdout.write("Yes\n")
        return

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        adj[u].append(v)
        adj[v].append(u)

    # iterative DFS to get an order where parents precede children
    parent = [0] * (n + 1)
    order = []
    visited = bytearray(n + 1)
    stack = [1]
    visited[1] = 1
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not visited[w]:
                visited[w] = 1
                parent[w] = u
                stack.append(w)

    # subtree sizes
    size = [1] * (n + 1)
    for i in range(len(order) - 1, -1, -1):
        u = order[i]
        p = parent[u]
        if p:
            size[p] += size[u]

    # Count "open" children (subtree_size % K != 0) and remember their residues
    cnt = [0] * (n + 1)
    r1 = [0] * (n + 1)
    r2 = [0] * (n + 1)
    for u in order:
        p = parent[u]
        if p:
            r = size[u] % K
            if r:
                c = cnt[p] + 1
                cnt[p] = c
                if c == 1:
                    r1[p] = r
                elif c == 2:
                    r2[p] = r

    for v in range(1, n + 1):
        c = cnt[v]
        if c > 2:
            sys.stdout.write("No\n")
            return
        if c == 2 and r1[v] + r2[v] != K - 1:
            sys.stdout.write("No\n")
            return

    # root has no parent: r(root) = 0, so it must close a fragment (not be a lone stub)
    c = cnt[1]
    if c == 0:
        sys.stdout.write("No\n")
        return
    if c == 1 and r1[1] != K - 1:
        sys.stdout.write("No\n")
        return

    sys.stdout.write("Yes\n")


main()