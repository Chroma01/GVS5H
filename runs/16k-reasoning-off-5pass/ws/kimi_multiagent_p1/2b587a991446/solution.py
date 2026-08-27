import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    S = int(data[idx]); idx += 1
    T = int(data[idx]); idx += 1
    adj = [[] for _ in range(N + 1)]
    edges = []
    for _ in range(M):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))

    # ---- feasibility: graph is a path -> impossible ----
    if M == N - 1:
        maxdeg = max(len(a) for a in adj)
        if maxdeg <= 2:
            print(-1)
            return

    # ---- BFS from S and from T ----
    def bfs(src):
        dist = [-1] * (N + 1)
        dist[src] = 0
        dq = deque([src])
        while dq:
            x = dq.popleft()
            dx = dist[x] + 1
            for y in adj[x]:
                if dist[y] < 0:
                    dist[y] = dx
                    dq.append(y)
        return dist

    dS = bfs(S)
    dT = bfs(T)
    d = dS[T]

    INF = float('inf')
    ans = INF

    # ---- A1: shortest cycle through both S and T ----
    # min over edges (u,v) of dS[u] + 1 + dT[v]  (and symmetric),
    # valid when the S-side and T-side shortest paths are vertex-disjoint.
    # We compute the min and then verify disjointness via a check:
    # the two paths can be chosen disjoint iff S,T are in the same
    # biconnected component; we approximate with the standard formula
    # and guard with a reconstruction disjointness test.
    best_a1 = INF
    best_edge = None
    for (u, v) in edges:
        c1 = dS[u] + 1 + dT[v]
        c2 = dS[v] + 1 + dT[u]
        if c1 < best_a1:
            best_a1 = c1
            best_edge = (u, v, 0)
        if c2 < best_a1:
            best_a1 = c2
            best_edge = (v, u, 0)

    # Verify disjointness for the candidate: reconstruct one shortest
    # path S->u and one shortest path T->v (greedy by dist), check they
    # are internally disjoint; if not, fall back to checking whether
    # S and T are in the same biconnected component and use the
    # min-cycle-through-two-vertices via BFS on the "two-path" state.
    def reconstruct(dist, src, dst):
        # greedy shortest path from src to dst following decreasing dist
        path = [dst]
        x = dst
        while x != src:
            for y in adj[x]:
                if dist[y] == dist[x] - 1:
                    path.append(y)
                    x = y
                    break
        path.reverse()
        return path

    a1_valid = False
    if best_a1 < INF:
        (uu, vv, _) = best_edge
        p1 = reconstruct(dS, S, uu)
        p2 = reconstruct(dT, T, vv)
        set1 = set(p1[:-1]) if len(p1) > 1 else set()
        # internal vertices of p1 (exclude uu) and p2 (exclude vv)
        s1 = set(p1[:-1])
        s2 = set(p2[:-1])
        if not (s1 & s2) and uu not in s2 and vv not in s1:
            a1_valid = True

    if not a1_valid:
        # exact shortest cycle through S and T:
        # BFS over pairs (x, y) = positions of two disjoint walks
        # starting from S and T, meeting via an edge. Too big in general,
        # so instead: shortest cycle through S and T =
        #   min over edges e=(u,v) of dist_{G-e}(S,T) + 1?  -- not exact.
        # Exact approach: for each vertex w, cycle through S,T composed of
        # two disjoint paths. We use: shortest cycle through S,T =
        #   min over edges (u,v): dS[u]+1+dT[v] where paths disjoint.
        # Fallback: try all edges, reconstruct, keep min valid.
        best_a1 = INF
        for (u, v) in edges:
            for (a, b) in ((u, v), (v, u)):
                c = dS[a] + 1 + dT[b]
                if c >= best_a1:
                    continue
                p1 = reconstruct(dS, S, a)
                p2 = reconstruct(dT, T, b)
                s1 = set(p1[:-1])
                s2 = set(p2[:-1])
                if not (s1 & s2) and a not in s2 and b not in s1:
                    best_a1 = c
        # If still INF, no cycle through both S and T exists.
        if best_a1 < INF:
            a1_valid = True

    if a1_valid:
        ans = min(ans, best_a1)

    # ---- A3: shortest cycle through S (resp. T) + 2*dist(other, cycle) ----
    # shortest cycle through a vertex x: BFS tree from x; for each non-tree
    # edge (a,b) with different top-level children, length = dep[a]+dep[b]+1.
    def shortest_cycle_through(x):
        dep = [-1] * (N + 1)
        top = [-1] * (N + 1)  # top-level child of x through which reached
        dep[x] = 0
        dq = deque([x])
        order = [x]
        while dq:
            cur = dq.popleft()
            for y in adj[cur]:
                if dep[y] < 0:
                    dep[y] = dep[cur] + 1
                    top[y] = y if cur == x else top[cur]
                    dq.append(y)
                    order.append(y)
        best = INF
        for (u, v) in edges:
            if u == x or v == x:
                continue
            if top[u] != -1 and top[v] != -1 and top[u] != top[v]:
                cand = dep[u] + dep[v] + 1
                if cand < best:
                    best = cand
        return best, dep

    cycS, depS = shortest_cycle_through(S)
    if cycS < INF:
        # dist from T to the cycle: min over vertices on that cycle.
        # Approximate: min over edges realizing the cycle; simpler:
        # dist(T, cycle) = min over vertices v on cycle of dT[v].
        # We recompute the cycle vertices via the best non-tree edge.
        # Simpler bound: min over all vertices v of (dT[v]) where v lies on
        # some cycle through S. Use: dist(T,C) = min over the found cycle.
        # Recompute cycle vertices:
        dep = depS
        top = [-1] * (N + 1)
        dq = deque([S])
        seen = [False] * (N + 1)
        seen[S] = True
        top[S] = -1
        while dq:
            cur = dq.popleft()
            for y in adj[cur]:
                if not seen[y]:
                    seen[y] = True
                    top[y] = y if cur == S else top[cur]
                    dq.append(y)
        best_edge2 = None
        for (u, v) in edges:
            if u == S or v == S:
                continue
            if top[u] != -1 and top[v] != -1 and top[u] != top[v]:
                if dep[u] + dep[v] + 1 == cycS:
                    best_edge2 = (u, v)
                    break
        if best_edge2 is not None:
            (u, v) = best_edge2
            # cycle vertices: paths from u and v up to S
            cyc_vertices = set([S])
            x = u
            while x != S:
                cyc_vertices.add(x)
                for y in adj[x]:
                    if dep[y] == dep[x] - 1:
                        x = y
                        break
            x = v
            while x != S:
                cyc_vertices.add(x)
                for y in adj[x]:
                    if dep[y] == dep[x] - 1:
                        x = y
                        break
            distT = min(dT[vx] for vx in cyc_vertices)
            ans = min(ans, cycS + 2 * distT)

    cycT, depT = shortest_cycle_through(T)
    if cycT < INF:
        dep = depT
        top = [-1] * (N + 1)
        dq = deque([T])
        seen = [False] * (N + 1)
        seen[T] = True
        while dq:
            cur = dq.popleft()
            for y in adj[cur]:
                if not seen[y]:
                    seen[y] = True
                    top[y] = y if cur == T else top[cur]
                    dq.append(y)
        best_edge2 = None
        for (u, v) in edges:
            if u == T or v == T:
                continue
            if top[u] != -1 and top[v] != -1 and top[u] != top[v]:
                if dep[u] + dep[v] + 1 == cycT:
                    best_edge2 = (u, v)
                    break
        if best_edge2 is not None:
            (u, v) = best_edge2
            cyc_vertices = set([T])
            x = u
            while x != T:
                cyc_vertices.add(x)
                for y in adj[x]:
                    if dep[y] == dep[x] - 1:
                        x = y
                        break
            x = v
            while x != T:
                cyc_vertices.add(x)
                for y in adj[x]:
                    if dep[y] == dep[x] - 1:
                        x = y
                        break
            distS = min(dS[vx] for vx in cyc_vertices)
            ans = min(ans, cycT + 2 * distS)

    # ---- A2: pocket passing ----
    # min over w with a "pocket" neighbor x (x not forced onto routes):
    # cost = 2*(dS[w]+dT[w]) + 2, plus +2 penalty if w in {S,T}.
    # A pocket at w exists iff w has a neighbor x such that x is not on
    # the chosen S-w and T-w routes; a safe sufficient condition:
    # deg(w) >= 2 and there is a neighbor x with x != S, x != T that is
    # not the unique route continuation. We use: w has some neighbor x
    # with dS[x] >= dS[w] and dT[x] >= dT[w] (x not strictly on a
    # shortest route from either side), or deg(w) >= 3, or w lies on a
    # cycle (then a cycle neighbor serves as pocket).
    on_cycle = [False] * (N + 1)
    # vertex is on a cycle iff it has a non-tree edge in its BFS subtree
    # from S with same top-level... simpler: mark via cycle detection:
    # a vertex is on a cycle iff removing it... too heavy. Use: w on cycle
    # iff exists neighbor x with dS[x] == dS[w] (same level edge) or
    # two neighbors at level dS[w]+1 with different... skip: pocket via
    # degree/level condition suffices.
    best_a2 = INF
    for w in range(1, N + 1):
        if dS[w] < 0:
            continue
        pocket = False
        for x in adj[w]:
            if x == S or x == T:
                continue
            # x usable as pocket if it is not a forced route vertex:
            # i.e., not (dS[x] == dS[w]-1) and not (dT[x] == dT[w]-1)
            # simultaneously the only option; simplest: x not strictly
            # closer to both S and T than w.
            if not (dS[x] == dS[w] - 1 and dT[x] == dT[w] - 1):
                pocket = True
                break
        if not pocket:
            continue
        base = 2 * (dS[w] + dT[w]) + 2
        if w == S or w == T:
            base += 2
        if base < best_a2:
            best_a2 = base
    ans = min(ans, best_a2)

    if ans >= INF:
        print(-1)
    else:
        print(ans)

solve()