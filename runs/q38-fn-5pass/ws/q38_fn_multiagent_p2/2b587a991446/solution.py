import sys
from collections import deque

INF = 10**18


def bfs_global(n, adj, src):
    dist = [-1] * n
    dist[src] = 0
    q = deque([src])
    while q:
        v = q.popleft()
        nd = dist[v] + 1
        for to, _ in adj[v]:
            if dist[to] == -1:
                dist[to] = nd
                q.append(to)
    return dist


def biconnected_components(n, adj, eu, ev):
    disc = [-1] * n
    low = [0] * n
    parent = [-1] * n
    pedge = [-1] * n
    it = [0] * n
    timer = 0
    edge_stack = []
    comps = []

    for root in range(n):
        if disc[root] != -1:
            continue

        disc[root] = low[root] = timer
        timer += 1
        it[root] = 0
        stack = [root]

        while stack:
            v = stack[-1]
            if it[v] < len(adj[v]):
                to, eid = adj[v][it[v]]
                it[v] += 1
                if eid == pedge[v]:
                    continue
                if disc[to] == -1:
                    edge_stack.append(eid)
                    parent[to] = v
                    pedge[to] = eid
                    disc[to] = low[to] = timer
                    timer += 1
                    it[to] = 0
                    stack.append(to)
                elif disc[to] < disc[v]:
                    edge_stack.append(eid)
                    if disc[to] < low[v]:
                        low[v] = disc[to]
            else:
                stack.pop()
                p = parent[v]
                if p != -1:
                    if low[v] >= disc[p]:
                        comp = []
                        while True:
                            eid = edge_stack.pop()
                            comp.append(eid)
                            if eid == pedge[v]:
                                break
                        comps.append(comp)
                    if low[v] < low[p]:
                        low[p] = low[v]

    return comps


def bfs_local(adj, src):
    k = len(adj)
    dist = [-1] * k
    dist[src] = 0
    q = deque([src])
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        nd = dist[v] + 1
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = nd
                q.append(to)
    return dist, order


def shortest_cycle_dom(adj, edges, root, target):
    """Shortest simple cycle containing root and target in an unweighted graph."""
    k = len(adj)
    dist, order = bfs_local(adj, root)
    if dist[target] < 0:
        return INF

    LOG = max(1, k.bit_length())
    idom = [-1] * k
    depth = [0] * k
    up = [[0] * k for _ in range(LOG)]

    idom[root] = root
    for j in range(LOG):
        up[j][root] = root

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        j = 0
        while diff:
            if diff & 1:
                a = up[j][a]
            diff >>= 1
            j += 1
        if a == b:
            return a
        for j in range(LOG - 1, -1, -1):
            ua = up[j][a]
            ub = up[j][b]
            if ua != ub:
                a = ua
                b = ub
        return up[0][a]

    # Dominators in the BFS shortest-path DAG.
    for v in order:
        if v != root:
            iv = idom[v]
            if iv == -1:
                iv = root
                idom[v] = iv
            depth[v] = depth[iv] + 1
            up[0][v] = iv
            for j in range(1, LOG):
                up[j][v] = up[j - 1][up[j - 1][v]]

        nd = dist[v] + 1
        for w in adj[v]:
            if dist[w] == nd:
                cur = idom[w]
                if cur == -1:
                    idom[w] = v
                elif cur != v:
                    if cur == root or v == root:
                        idom[w] = root
                    else:
                        idom[w] = lca(cur, v)

    del lca
    del up, depth

    children = [[] for _ in range(k)]
    for v in range(k):
        if v != root:
            p = idom[v]
            if p != -1:
                children[p].append(v)

    tin = [0] * k
    tout = [0] * k
    root_child = [-1] * k
    timer = 0

    stack = [(root, 0, -1)]
    while stack:
        v, i, rc = stack[-1]
        if i == 0:
            tin[v] = timer
            timer += 1
            root_child[v] = rc

        if i < len(children[v]):
            c = children[v][i]
            stack[-1] = (v, i + 1, rc)
            nrc = c if v == root else rc
            stack.append((c, 0, nrc))
        else:
            tout[v] = timer
            stack.pop()

    best = INF
    tt = tin[target]
    toutt = tout[target]

    for a, b in edges:
        if a == root or b == root:
            continue

        ra = root_child[a]
        rb = root_child[b]
        if ra == -1 or rb == -1 or ra == rb:
            continue

        if not ((tt <= tin[a] < toutt) or (tt <= tin[b] < toutt)):
            continue

        val = dist[a] + dist[b] + 1
        if val < best:
            best = val
            if best == 3:
                break

    return best


def shortest_cycle_in_comp(comp_edges, s, t, eu, ev, loc):
    if s == t:
        return INF

    le = len(comp_edges)
    if le < 3:
        return INF

    touched = []
    local_adj = []
    local_edges = []

    for eid in comp_edges:
        u = eu[eid]
        v = ev[eid]

        lu = loc[u]
        if lu == -1:
            lu = len(touched)
            loc[u] = lu
            touched.append(u)
            local_adj.append([])

        lv = loc[v]
        if lv == -1:
            lv = len(touched)
            loc[v] = lv
            touched.append(v)
            local_adj.append([])

        local_adj[lu].append(lv)
        local_adj[lv].append(lu)
        local_edges.append((lu, lv))

    ls = loc[s]
    lt = loc[t]
    if ls < 0 or lt < 0:
        for v in touched:
            loc[v] = -1
        return INF

    if le == 3:
        for v in touched:
            loc[v] = -1
        return 3

    ans = shortest_cycle_dom(local_adj, local_edges, ls, lt)
    if ans == INF:
        ans = shortest_cycle_dom(local_adj, local_edges, lt, ls)

    for v in touched:
        loc[v] = -1

    return ans


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    n = next(it)
    m = next(it)
    s = next(it) - 1
    t = next(it) - 1

    eu = [0] * m
    ev = [0] * m
    adj = [[] for _ in range(n)]

    for eid in range(m):
        u = next(it) - 1
        v = next(it) - 1
        eu[eid] = u
        ev[eid] = v
        adj[u].append((v, eid))
        adj[v].append((u, eid))

    dist_s = bfs_global(n, adj, s)
    dist_t = bfs_global(n, adj, t)

    ans = INF

    # Family T: tree-like passing at a branching vertex.
    for v in range(n):
        if len(adj[v]) < 3:
            continue

        ds = dist_s[v]
        dt = dist_t[v]

        if v == s:
            cand = 2 * (dt + 2)
            if cand < ans:
                ans = cand
            continue

        if v == t:
            cand = 2 * (ds + 2)
            if cand < ans:
                ans = cand
            continue

        cnt_s = 0
        cnt_t = 0
        first_s = -1
        first_t = -1
        second_s = -1
        second_t = -1
        need_s = ds - 1
        need_t = dt - 1

        for nb, _ in adj[v]:
            if dist_s[nb] == need_s:
                cnt_s += 1
                if first_s == -1:
                    first_s = nb
                elif second_s == -1:
                    second_s = nb
            if dist_t[nb] == need_t:
                cnt_t += 1
                if first_t == -1:
                    first_t = nb
                elif second_t == -1:
                    second_t = nb

        if cnt_s == 0 or cnt_t == 0:
            continue

        if first_s != first_t or second_s != -1 or second_t != -1:
            k = 1
        else:
            k = 2

        cand = 2 * (ds + dt + k)
        if cand < ans:
            ans = cand

    comps = biconnected_components(n, adj, eu, ev)
    adj = None

    bcnt = len(comps)
    comp_vertices = [[] for _ in range(bcnt)]
    comp_count = [0] * n
    first_block = [-1] * n
    mark = [-1] * n

    for c, edges in enumerate(comps):
        verts = []
        for eid in edges:
            u = eu[eid]
            v = ev[eid]

            if mark[u] != c:
                mark[u] = c
                verts.append(u)
                comp_count[u] += 1
                if first_block[u] == -1:
                    first_block[u] = c

            if mark[v] != c:
                mark[v] = c
                verts.append(v)
                comp_count[v] += 1
                if first_block[v] == -1:
                    first_block[v] = c

        comp_vertices[c] = verts

    art_id = [-1] * n
    art_nodes = []
    for v in range(n):
        if comp_count[v] > 1:
            art_id[v] = bcnt + len(art_nodes)
            art_nodes.append(v)

    sole_block = [-1] * n
    for v in range(n):
        if comp_count[v] == 1:
            sole_block[v] = first_block[v]

    nodes = bcnt + len(art_nodes)
    bct = [[] for _ in range(nodes)]

    for c, verts in enumerate(comp_vertices):
        for v in verts:
            aid = art_id[v]
            if aid != -1:
                bct[c].append(aid)
                bct[aid].append(c)

    if comp_count[s] > 1:
        s_node = art_id[s]
    else:
        s_node = sole_block[s]

    if comp_count[t] > 1:
        t_node = art_id[t]
    else:
        t_node = sole_block[t]

    if s_node != -1 and t_node != -1:
        par = [-1] * nodes
        par[s_node] = -2
        stack = [s_node]

        while stack:
            v = stack.pop()
            if v == t_node:
                break
            for nb in bct[v]:
                if par[nb] == -1:
                    par[nb] = v
                    stack.append(nb)

        if par[t_node] != -1 or s_node == t_node:
            path = []
            cur = t_node
            while cur != -2:
                path.append(cur)
                if cur == s_node:
                    break
                cur = par[cur]
            path.reverse()

            del comp_vertices, comp_count, first_block, art_id, bct, mark, sole_block

            loc = [-1] * n

            for idx, node in enumerate(path):
                if node >= bcnt:
                    continue

                if idx == 0:
                    p_s = s
                else:
                    prev = path[idx - 1]
                    if prev >= bcnt:
                        p_s = art_nodes[prev - bcnt]
                    else:
                        p_s = s

                if idx == len(path) - 1:
                    p_t = t
                else:
                    nxt = path[idx + 1]
                    if nxt >= bcnt:
                        p_t = art_nodes[nxt - bcnt]
                    else:
                        p_t = t

                if p_s == p_t:
                    continue

                cyc = shortest_cycle_in_comp(comps[node], p_s, p_t, eu, ev, loc)
                if cyc < INF:
                    cand = 2 * dist_s[p_s] + 2 * dist_t[p_t] + cyc
                    if cand < ans:
                        ans = cand

    if ans >= INF // 2:
        print(-1)
    else:
        print(ans)


if __name__ == "__main__":
    solve()