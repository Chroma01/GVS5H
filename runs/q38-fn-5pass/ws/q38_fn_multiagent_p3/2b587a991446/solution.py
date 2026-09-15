import sys
from collections import deque
from heapq import heappush, heappop

INF = 10**18


def min_cost_two_flow(n, s, t, head, to, cap, cost, nxt, limit):
    pot = [0] * n
    flow = 0
    total = 0
    push = heappush
    pop = heappop

    while flow < 2:
        dist = [INF] * n
        prev = [-1] * n
        dist[s] = 0
        touched = [s]
        heap = [(0, s)]

        while heap:
            d, v = pop(heap)
            if d != dist[v]:
                continue
            pv = pot[v]
            e = head[v]
            while e != -1:
                if cap[e] > 0:
                    u = to[e]
                    nd = d + cost[e] + pv - pot[u]
                    if nd < dist[u]:
                        if dist[u] == INF:
                            touched.append(u)
                        dist[u] = nd
                        prev[u] = e
                        push(heap, (nd, u))
                e = nxt[e]

        if dist[t] == INF:
            break

        for v in touched:
            pot[v] += dist[v]

        addf = 2 - flow
        v = t
        while v != s:
            e = prev[v]
            if e == -1:
                addf = 0
                break
            if cap[e] < addf:
                addf = cap[e]
            v = to[e ^ 1]

        if addf == 0:
            break

        path_cost = 0
        v = t
        while v != s:
            e = prev[v]
            path_cost += cost[e]
            cap[e] -= addf
            cap[e ^ 1] += addf
            v = to[e ^ 1]

        flow += addf
        total += path_cost * addf

        if total >= limit:
            break

    if flow == 2 and total < limit:
        return total
    return INF


def solve():
    input = sys.stdin.readline
    N, M, S, T = map(int, input().split())
    S -= 1
    T -= 1

    edges = []
    adj = [[] for _ in range(N)]
    for i in range(M):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        adj[u].append((v, i))
        adj[v].append((u, i))

    def bfs(src):
        dist = [-1] * N
        dist[src] = 0
        q = deque([src])
        while q:
            v = q.popleft()
            nd = dist[v] + 1
            for to, _ in adj[v]:
                if dist[to] == -1:
                    dist[to] = nd
                    q.append(to)
        for i in range(N):
            if dist[i] == -1:
                dist[i] = INF
        return dist

    distS = bfs(S)
    distT = bfs(T)

    ans = INF

    # Vertex gadgets: vertices of degree at least 3.
    for v in range(N):
        if len(adj[v]) < 3:
            continue
        a = distS[v]
        b = distT[v]
        if a >= INF or b >= INF:
            continue

        if a == 0 or b == 0:
            extra = 4
        else:
            cntS = cntT = 0
            predS = predT = -1
            am = a - 1
            bm = b - 1
            for to, _ in adj[v]:
                if distS[to] == am:
                    cntS += 1
                    predS = to
                if distT[to] == bm:
                    cntT += 1
                    predT = to

            if cntS == 0 or cntT == 0:
                extra = 4
            elif cntS == 1 and cntT == 1 and predS == predT:
                extra = 4
            else:
                extra = 2

        cand = 2 * (a + b) + extra
        if cand < ans:
            ans = cand

    sys.setrecursionlimit(1_000_000)

    disc = [-1] * N
    low = [0] * N
    parent = [-1] * N
    pedge = [-1] * N
    it = [0] * N
    edge_stack = []
    time = 0

    mark = [0] * N
    deg_tmp = [0] * N
    loc = [-1] * N
    token = 0

    def process_comp(comp, tok):
        nonlocal ans

        E = len(comp)
        if E <= 1:
            return

        verts = []
        for e in comp:
            u, v = edges[e]
            if mark[u] != tok:
                mark[u] = tok
                verts.append(u)
                deg_tmp[u] = 0
            if mark[v] != tok:
                mark[v] = tok
                verts.append(v)
                deg_tmp[v] = 0
            deg_tmp[u] += 1
            deg_tmp[v] += 1

        V = len(verts)

        minS = INF
        minT = INF
        for v in verts:
            ds = distS[v]
            dt = distT[v]
            if ds < minS:
                minS = ds
            if dt < minT:
                minT = dt

        # Simple cycle block.
        if E == V:
            simple = True
            for v in verts:
                if deg_tmp[v] != 2:
                    simple = False
                    break

            if simple:
                minS1 = INF
                minS2 = INF
                argS = -1
                minT1 = INF
                minT2 = INF
                argT = -1

                for v in verts:
                    ds = distS[v]
                    if ds < minS1:
                        minS2 = minS1
                        minS1 = ds
                        argS = v
                    elif ds < minS2:
                        minS2 = ds

                    dt = distT[v]
                    if dt < minT1:
                        minT2 = minT1
                        minT1 = dt
                        argT = v
                    elif dt < minT2:
                        minT2 = dt

                if argS != argT:
                    best = minS1 + minT1
                else:
                    best = min(minS1 + minT2, minS2 + minT1)

                if best < INF:
                    cand = E + 2 * best
                    if cand < ans:
                        ans = cand
                return

        # Non-simple non-bridge block: min-cost two vertex-disjoint paths.
        if V < 2:
            return
        if ans < INF and 2 * (minS + minT) >= ans:
            return

        for i, v in enumerate(verts):
            loc[v] = i

        n_nodes = 2 * V + 2
        s_node = 2 * V
        t_node = 2 * V + 1

        head = [-1] * n_nodes
        to = []
        cap = []
        cost = []
        nxt = []

        def add_edge(u, v, c, w):
            idx = len(to)
            to.append(v)
            cap.append(c)
            cost.append(w)
            nxt.append(head[u])
            head[u] = idx

            to.append(u)
            cap.append(0)
            cost.append(-w)
            nxt.append(head[v])
            head[v] = idx + 1

        if ans < INF:
            for i, v in enumerate(verts):
                out = 2 * i
                inn = out + 1

                ds = distS[v]
                if ds + minS < ans:
                    add_edge(s_node, out, 2, ds)

                dt = distT[v]
                if dt + minT < ans:
                    add_edge(inn, t_node, 2, dt)

                add_edge(inn, out, 1, 0)
        else:
            for i, v in enumerate(verts):
                out = 2 * i
                inn = out + 1
                add_edge(s_node, out, 2, distS[v])
                add_edge(inn, t_node, 2, distT[v])
                add_edge(inn, out, 1, 0)

        for e in comp:
            u, v = edges[e]
            i = loc[u]
            j = loc[v]
            add_edge(2 * i, 2 * j + 1, 1, 1)
            add_edge(2 * j, 2 * i + 1, 1, 1)

        fcost = min_cost_two_flow(
            n_nodes, s_node, t_node, head, to, cap, cost, nxt, ans
        )
        if fcost < ans:
            ans = fcost

    for root in range(N):
        if disc[root] != -1:
            continue

        disc[root] = low[root] = time
        time += 1
        stack = [root]

        while stack:
            v = stack[-1]

            if it[v] < len(adj[v]):
                to, eid = adj[v][it[v]]
                it[v] += 1

                if eid == pedge[v]:
                    continue

                if disc[to] == -1:
                    parent[to] = v
                    pedge[to] = eid
                    edge_stack.append(eid)
                    disc[to] = low[to] = time
                    time += 1
                    stack.append(to)
                elif disc[to] < disc[v]:
                    edge_stack.append(eid)
                    if disc[to] < low[v]:
                        low[v] = disc[to]
            else:
                stack.pop()
                p = parent[v]

                if p != -1:
                    if low[v] < low[p]:
                        low[p] = low[v]

                    if low[v] >= disc[p]:
                        comp = []
                        while True:
                            e = edge_stack.pop()
                            comp.append(e)
                            if e == pedge[v]:
                                break
                        token += 1
                        process_comp(comp, token)
                else:
                    if edge_stack:
                        comp = []
                        while edge_stack:
                            comp.append(edge_stack.pop())
                        token += 1
                        process_comp(comp, token)

    print(-1 if ans >= INF else ans)


if __name__ == "__main__":
    solve()