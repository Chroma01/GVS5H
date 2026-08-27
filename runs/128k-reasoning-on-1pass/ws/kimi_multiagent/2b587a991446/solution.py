#!/usr/bin/env python3
import sys
from collections import deque
from heapq import heappush, heappop

INF = 10**18


# ------------------------- min-cost flow for one block -------------------------
def two_vertex_disjoint_cost(nv, edges, s, t):
    """
    vertices are local 0..nv-1, edges are undirected (a,b).
    Returns min total length of two internally vertex-disjoint s-t paths
    (= shortest simple cycle through s and t), or INF if impossible.
    Vertex capacities are 1 except s,t have capacity 2.
    """
    if s == t:
        return INF
    N2 = 2 * nv
    g = [[] for _ in range(N2)]

    def add(fr, to, cap, cost):
        g[fr].append([to, cap, cost, len(g[to])])
        g[to].append([fr, 0, -cost, len(g[fr]) - 1])

    def vin(v):
        return 2 * v

    def vout(v):
        return 2 * v + 1

    for v in range(nv):
        cap = 2 if v == s or v == t else 1
        add(vin(v), vout(v), cap, 0)
    for a, b in edges:
        add(vout(a), vin(b), 1, 1)
        add(vout(b), vin(a), 1, 1)

    src, snk = vin(s), vout(t)
    flow = 0
    cost = 0
    pot = [0] * N2

    while flow < 2:
        dist = [INF] * N2
        pv = [-1] * N2
        pe = [-1] * N2
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, v = heappop(pq)
            if d != dist[v]:
                continue
            for i, e in enumerate(g[v]):
                if e[1] <= 0:
                    continue
                nd = d + e[2] + pot[v] - pot[e[0]]
                if nd < dist[e[0]]:
                    dist[e[0]] = nd
                    pv[e[0]] = v
                    pe[e[0]] = i
                    heappush(pq, (nd, e[0]))
        if dist[snk] == INF:
            break
        for v in range(N2):
            if dist[v] < INF:
                pot[v] += dist[v]
        addf = 2 - flow
        v = snk
        while v != src:
            e = g[pv[v]][pe[v]]
            addf = min(addf, e[1])
            v = pv[v]
        v = snk
        while v != src:
            e = g[pv[v]][pe[v]]
            e[1] -= addf
            g[v][e[3]][1] += addf
            cost += addf * e[2]
            v = pv[v]
        flow += addf

    return cost if flow == 2 else INF


# --------------------------------- main solve ---------------------------------
def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    M = next(it)
    S = next(it) - 1
    T = next(it) - 1

    adj = [[] for _ in range(N)]
    edges = []
    deg = [0] * N
    for ei in range(M):
        u = next(it) - 1
        v = next(it) - 1
        edges.append((u, v))
        adj[u].append((v, ei))
        adj[v].append((u, ei))
        deg[u] += 1
        deg[v] += 1

    def bfs(src):
        dist = [-1] * N
        dist[src] = 0
        q = deque([src])
        while q:
            v = q.popleft()
            nd = dist[v] + 1
            for w, _ in adj[v]:
                if dist[w] == -1:
                    dist[w] = nd
                    q.append(w)
        return dist

    ds = bfs(S)
    dt = bfs(T)
    d = ds[T]

    ans = INF

    # Branch (degree >= 3) used as a one-step pocket.
    for v in range(N):
        if v != S and v != T and deg[v] >= 3 and ds[v] + dt[v] == d:
            ans = min(ans, 2 * d + 2)
            break
    if deg[S] >= 3 or deg[T] >= 3:
        ans = min(ans, 2 * d + 4)

    # Biconnected components (vertex blocks); bridges are 2-vertex blocks.
    sys.setrecursionlimit(1000000)
    disc = [0] * N
    low = [0] * N
    timer = 0
    estack = []
    block_edges = []     # list of lists of (u,v), global vertices
    block_vertices = []  # list of lists of global vertices

    def dfs(u, pe):
        nonlocal timer
        timer += 1
        disc[u] = low[u] = timer
        for v, ei in adj[u]:
            if ei == pe:
                continue
            if disc[v] == 0:
                estack.append((u, v))
                dfs(v, ei)
                if low[v] < low[u]:
                    low[u] = low[v]
                if low[v] >= disc[u]:
                    be = []
                    bv = set()
                    while True:
                        a, b = estack.pop()
                        be.append((a, b))
                        bv.add(a)
                        bv.add(b)
                        if (a == u and b == v) or (a == v and b == u):
                            break
                    block_edges.append(be)
                    block_vertices.append(list(bv))
            elif disc[v] < disc[u]:
                estack.append((u, v))
                if disc[v] < low[u]:
                    low[u] = disc[v]

    dfs(S, -1)

    B = len(block_edges)
    BN = N + B
    badj = [[] for _ in range(BN)]
    for bid, verts in enumerate(block_vertices):
        bn = N + bid
        for v in verts:
            badj[v].append(bn)
            badj[bn].append(v)

    # Path in the block-cut tree from S to T.
    par = [-1] * BN
    par[S] = S
    q = deque([S])
    while q:
        v = q.popleft()
        if v == T:
            break
        for w in badj[v]:
            if par[w] == -1:
                par[w] = v
                q.append(w)

    path = []
    v = T
    while v != S:
        path.append(v)
        v = par[v]
    path.append(S)
    path.reverse()

    loc = [-1] * N
    for i in range(1, len(path) - 1):
        node = path[i]
        if node < N:
            continue
        bid = node - N
        if len(block_edges[bid]) == 1:
            continue  # bridge block: no cycle inside
        x = path[i - 1]
        y = path[i + 1]
        if x == y:
            continue
        verts = block_vertices[bid]
        for idx, gv in enumerate(verts):
            loc[gv] = idx
        le = [(loc[a], loc[b]) for a, b in block_edges[bid]]
        c = two_vertex_disjoint_cost(len(verts), le, loc[x], loc[y])
        if c < INF:
            cand = 2 * ds[x] + c + 2 * dt[y]
            if cand < ans:
                ans = cand
        for gv in verts:
            loc[gv] = -1

    print(-1 if ans == INF else ans)


if __name__ == "__main__":
    main()