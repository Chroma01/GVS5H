import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    M = int(data[p]); p += 1
    K = int(data[p]); p += 1

    edges = []
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(data[p]) - 1; p += 1
        v = int(data[p]) - 1; p += 1
        edges.append((u, v))
        adj[u].append(v)

    # Unweighted shortest path length L = upper bound for the answer.
    dist = [-1] * N
    dist[0] = 0
    q = deque([0])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if dist[y] == -1:
                dist[y] = dist[x] + 1
                q.append(y)
    L = dist[N - 1]
    target = N - 1

    # Convex-cost min flow: first use of an edge is free, every later use costs 1.
    # Marginal costs c_i are nondecreasing; K(D) = sum_{c_i < D} (D - c_i).
    h = [0] * M
    marginals = []
    INF = float('inf')
    truncated = False

    while True:
        # Residual arcs: (from, to, cost, edge_index, delta)
        arcs = []
        for i in range(M):
            u, v = edges[i]
            if h[i] == 0:
                arcs.append((u, v, 0, i, 1))
            else:
                arcs.append((u, v, 1, i, 1))
                arcs.append((v, u, -1 if h[i] >= 2 else 0, i, -1))

        # Bellman-Ford (backward arcs may be negative).
        d = [INF] * N
        d[0] = 0
        par = [-1] * N
        for _ in range(N - 1):
            upd = False
            for ai in range(len(arcs)):
                u, v, c, ei, delta = arcs[ai]
                du = d[u]
                if du != INF and du + c < d[v]:
                    d[v] = du + c
                    par[v] = ai
                    upd = True
            if not upd:
                break

        if d[target] == INF:
            break
        c = d[target]
        if c >= L:
            break
        marginals.append(c)
        if len(marginals) == K + 1:
            truncated = True
            break

        # Augment one unit along the found shortest residual path.
        cur = target
        while cur != 0:
            ai = par[cur]
            u, v, cc, ei, delta = arcs[ai]
            h[ei] += delta
            cur = u

    maxD = marginals[-1] if truncated else L
    ans = 0
    for D in range(maxD, -1, -1):
        s = 0
        ok = True
        for c in marginals:
            if c < D:
                s += D - c
                if s > K:
                    ok = False
                    break
        if ok:
            ans = D
            break
    sys.stdout.write(str(ans) + "\n")

main()