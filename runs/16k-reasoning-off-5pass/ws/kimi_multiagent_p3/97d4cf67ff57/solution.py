import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        print(-1)
        return
    idx = 0
    N = int(data[idx]); idx += 1
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        adj[a].append(b)
        adj[b].append(a)

    # Iterative DFS from root 1 to get parent pointers and a traversal order
    parent = [0] * (N + 1)
    parent[1] = -1
    order = []
    stack = [1]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)

    NEG = -10**9
    # f[u]: best size of a valid selected subgraph inside u's rooted subtree such that
    #       u is included, the edge u-parent is used, u has degree 4 in the subgraph
    #       (so u uses exactly 3 children), and the subgraph contains a degree-4 vertex
    #       (u itself). NEG if impossible (fewer than 3 children).
    f = [NEG] * (N + 1)
    # h[u]: best contribution of u's subtree when edge u-parent is used:
    #       either u is a leaf (value 1, no degree-4 vertex below) or f[u].
    h = [1] * (N + 1)

    ans = NEG

    for u in reversed(order):
        # top4 largest h values among children; best f among children
        t0 = t1 = t2 = t3 = 0  # top four h values (h >= 1 always)
        cnt = 0
        bestf = NEG
        for v in adj[u]:
            if v == parent[u]:
                continue
            cnt += 1
            hv = h[v]
            if hv > t0:
                t0, t1, t2, t3 = hv, t0, t1, t2
            elif hv > t1:
                t1, t2, t3 = hv, t1, t2
            elif hv > t2:
                t2, t3 = hv, t2
            elif hv > t3:
                t3 = hv
            fv = f[v]
            if fv > bestf:
                bestf = fv

        if cnt >= 3:
            # u as degree-4 vertex connected to parent: exactly 3 children
            f[u] = 1 + t0 + t1 + t2
            h[u] = f[u]  # f[u] >= 4 > 1
        if cnt >= 4:
            # u as degree-4 top of the whole component: exactly 4 children
            g2 = 1 + t0 + t1 + t2 + t3
            if g2 > ans:
                ans = g2
        if bestf != NEG:
            # u as leaf-top of the component: exactly 1 child, and the child's
            # subtree must contain a degree-4 vertex (use f, not h)
            g1 = 1 + bestf
            if g1 > ans:
                ans = g1

    print(ans if ans != NEG else -1)

main()