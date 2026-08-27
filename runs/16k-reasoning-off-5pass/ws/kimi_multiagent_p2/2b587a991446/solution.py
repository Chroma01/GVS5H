import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it)); M = int(next(it)); S = int(next(it)); T = int(next(it))
    adj = [[] for _ in range(N + 1)]
    edges = []
    for i in range(M):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))

    def bfs(src):
        dist = [-1] * (N + 1)
        dist[src] = 0
        dq = deque([src])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if dist[y] == -1:
                    dist[y] = dist[x] + 1
                    dq.append(y)
        return dist

    dS = bfs(S)
    dT = bfs(T)
    d = dS[T]

    # ---- Bridges via iterative Tarjan ----
    adj2 = [[] for _ in range(N + 1)]
    for i, (u, v) in enumerate(edges):
        adj2[u].append((v, i))
        adj2[v].append((u, i))

    disc = [0] * (N + 1)
    low = [0] * (N + 1)
    is_bridge = [False] * M
    parent_edge = [-1] * (N + 1)
    timer = 0
    for start in range(1, N + 1):
        if disc[start]:
            continue
        timer += 1
        disc[start] = low[start] = timer
        vs = [start]
        iters = [iter(adj2[start])]
        while vs:
            u = vs[-1]
            advanced = False
            for (v, eid) in iters[-1]:
                if eid == parent_edge[u]:
                    continue
                if disc[v]:
                    if disc[v] < low[u]:
                        low[u] = disc[v]
                else:
                    parent_edge[v] = eid
                    timer += 1
                    disc[v] = low[v] = timer
                    vs.append(v)
                    iters.append(iter(adj2[v]))
                    advanced = True
                    break
            if not advanced:
                vs.pop()
                iters.pop()
                if vs:
                    p = vs[-1]
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if low[u] > disc[p]:
                        is_bridge[parent_edge[u]] = True

    # ---- 2-edge-connected components ----
    parent = list(range(N + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, (u, v) in enumerate(edges):
        if not is_bridge[i]:
            ra, rb = find(u), find(v)
            if ra != rb:
                parent[ra] = rb
    comp = [find(v) for v in range(N + 1)]
    comp_size = {}
    for v in range(1, N + 1):
        comp_size[comp[v]] = comp_size.get(comp[v], 0) + 1
    def is_cyclic_comp(c):
        return comp_size.get(c, 0) >= 2

    deg = [0] * (N + 1)
    for v in range(1, N + 1):
        deg[v] = len(adj[v])

    # ---- Bridge tree path from comp[S] to comp[T] ----
    cs, ct = comp[S], comp[T]
    btree = {}
    for i, (u, v) in enumerate(edges):
        if is_bridge[i]:
            cu, cv = comp[u], comp[v]
            btree.setdefault(cu, []).append(cv)
            btree.setdefault(cv, []).append(cu)
    prev = {cs: None}
    dq = deque([cs])
    while dq:
        x = dq.popleft()
        if x == ct:
            break
        for y in btree.get(x, []):
            if y not in prev:
                prev[y] = x
                dq.append(y)
    on_path = set()
    x = ct
    while x is not None:
        on_path.add(x)
        x = prev.get(x)

    # ---- Feasibility ----
    feasible = False
    for c in on_path:
        if is_cyclic_comp(c):
            feasible = True
            break
    if not feasible:
        for v in range(1, N + 1):
            if comp[v] in on_path and deg[v] >= 3:
                feasible = True
                break
    if not feasible:
        print(-1)
        return

    # ---- Minimum moves ----
    best = None
    if cs == ct and is_cyclic_comp(cs):
        best = 2 * d + (d & 1)

    cand = None
    for v in range(1, N + 1):
        if deg[v] >= 3 or is_cyclic_comp(comp[v]):
            cost = 2 * d + 2 + (dS[v] + dT[v] - d)
            if cand is None or cost < cand:
                cand = cost
    if cand is not None and (best is None or cand < best):
        best = cand

    print(best if best is not None else -1)

solve()