import sys
from collections import deque

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M, S, T = data[0], data[1], data[2] - 1, data[3] - 1
    U = [0] * M
    V = [0] * M
    adj = [[] for _ in range(N)]
    ptr = 4
    for eid in range(M):
        u = data[ptr] - 1
        v = data[ptr + 1] - 1
        ptr += 2
        U[eid] = u
        V[eid] = v
        adj[u].append((v, eid))
        adj[v].append((u, eid))
    del data

    # Iterative Tarjan for vertex-biconnected components (edge partition).
    disc = [-1] * N
    low = [0] * N
    parent = [-1] * N
    pedge = [-1] * N
    it_idx = [0] * N
    edge_stack = []
    comps = []
    timer = 0

    for root in range(N):
        if disc[root] != -1:
            continue
        disc[root] = low[root] = timer
        timer += 1
        stack = [root]
        while stack:
            u = stack[-1]
            if it_idx[u] < len(adj[u]):
                v, eid = adj[u][it_idx[u]]
                it_idx[u] += 1
                if eid == pedge[u]:
                    continue
                if disc[v] == -1:
                    parent[v] = u
                    pedge[v] = eid
                    edge_stack.append(eid)
                    disc[v] = low[v] = timer
                    timer += 1
                    stack.append(v)
                elif disc[v] < disc[u]:
                    edge_stack.append(eid)
                    if disc[v] < low[u]:
                        low[u] = disc[v]
            else:
                stack.pop()
                if pedge[u] != -1:
                    p = parent[u]
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if low[u] >= disc[p]:
                        comp = []
                        while True:
                            x = edge_stack.pop()
                            comp.append(x)
                            if x == pedge[u]:
                                break
                        comps.append(comp)

    del disc, low, parent, pedge, it_idx, edge_stack

    B = len(comps)
    total_nodes = N + B
    tree_adj = [[] for _ in range(total_nodes)]
    edge_to_comp = [-1] * M
    mark = [-1] * N

    for cid, comp in enumerate(comps):
        node = N + cid
        for eid in comp:
            edge_to_comp[eid] = cid
            u = U[eid]
            v = V[eid]
            if mark[u] != cid:
                mark[u] = cid
                tree_adj[node].append(u)
                tree_adj[u].append(node)
            if mark[v] != cid:
                mark[v] = cid
                tree_adj[node].append(v)
                tree_adj[v].append(node)
    del mark

    # Path between S and T in the block-cut tree.
    par = [-1] * total_nodes
    par[S] = -2
    q = [S]
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        if u == T:
            break
        for v in tree_adj[u]:
            if par[v] == -1:
                par[v] = u
                q.append(v)

    if par[T] == -1:
        print(-1)
        return

    path = []
    cur = T
    while cur != -2:
        path.append(cur)
        cur = par[cur]
    path.reverse()

    path_block = bytearray(B)
    path_block_verts = {}

    for node in path:
        if node >= N:
            cid = node - N
            path_block[cid] = 1
            ce = comps[cid]
            if ce is not None and len(ce) > 1:
                path_block_verts[cid] = tree_adj[node]
            else:
                comps[cid] = None

    for cid in range(B):
        if not path_block[cid]:
            comps[cid] = None

    del tree_adj, par, q

    def bfs(start):
        dist = [-1] * N
        dist[start] = 0
        qq = [start]
        h = 0
        while h < len(qq):
            u = qq[h]
            h += 1
            nd = dist[u] + 1
            for v, _ in adj[u]:
                if dist[v] == -1:
                    dist[v] = nd
                    qq.append(v)
        return dist

    dS = bfs(S)
    dT = bfs(T)

    INF = 10 ** 18
    ans = INF

    # Vertex candidates on the block-cut path.
    for node in path:
        if node < N:
            v = node
            side = 0
            for _, eid in adj[v]:
                if not path_block[edge_to_comp[eid]]:
                    side += 1
            if v == S or v == T:
                if side >= 2:
                    cand = 2 * dS[v] + 2 * dT[v] + 4
                    if cand < ans:
                        ans = cand
            else:
                if side >= 1:
                    cand = 2 * dS[v] + 2 * dT[v] + 2
                    if cand < ans:
                        ans = cand

    del adj, edge_to_comp, path_block

    loc = [-1] * N
    dir_from = [-1] * M
    dir_to = [-1] * M

    def shortest_cycle(ce, verts, p, qv):
        L = len(verts)
        if L < 3:
            return INF

        for i, vv in enumerate(verts):
            loc[vv] = i
        p_loc = loc[p]
        q_loc = loc[qv]
        if p_loc < 0 or q_loc < 0:
            for vv in verts:
                loc[vv] = -1
            return INF

        local_adj = [[] for _ in range(L)]
        for eid in ce:
            i = loc[U[eid]]
            j = loc[V[eid]]
            local_adj[i].append((j, eid))
            local_adj[j].append((i, eid))

        dist = [-1] * L
        pv = [-1] * L
        pe = [-1] * L
        qq = [p_loc]
        dist[p_loc] = 0
        h = 0
        while h < len(qq):
            u = qq[h]
            h += 1
            nd = dist[u] + 1
            for v, eid in local_adj[u]:
                if dist[v] == -1:
                    dist[v] = nd
                    pv[v] = u
                    pe[v] = eid
                    qq.append(v)

        if len(qq) != L or dist[q_loc] == -1:
            for vv in verts:
                loc[vv] = -1
            return INF

        dist1 = dist[q_loc]
        used_v = bytearray(L)
        path_edge_ids = []

        cur = q_loc
        while True:
            used_v[cur] = 1
            if cur == p_loc:
                break
            eid = pe[cur]
            a = pv[cur]
            dir_from[eid] = a
            dir_to[eid] = cur
            path_edge_ids.append(eid)
            cur = a

        size = 2 * L
        INF2 = 10 ** 9
        dist2 = [INF2] * size
        src = 2 * p_loc
        sink = 2 * q_loc + 1
        dist2[src] = 0

        buckets = [deque(), deque(), deque()]
        buckets[0].append(src)
        rem = 1
        curd = 0
        res = INF2

        la = local_adj
        df = dir_from
        dt = dir_to
        dv = dist
        uv = used_v
        pl = p_loc
        ql = q_loc

        while rem:
            while not buckets[curd % 3]:
                curd += 1
            u = buckets[curd % 3].popleft()
            rem -= 1
            if dist2[u] != curd:
                continue
            if u == sink:
                res = curd
                break

            if (u & 1) == 0:  # in-node
                i = u >> 1
                # vertex arc in -> out
                if (not uv[i]) or i == pl or i == ql:
                    v = u + 1
                    if curd < dist2[v]:
                        dist2[v] = curd
                        buckets[curd % 3].append(v)
                        rem += 1

                di = dv[i]
                # reverse arcs of used directed edge arcs
                for j, eid in la[i]:
                    if df[eid] == j and dt[eid] == i:
                        v = (j << 1) | 1
                        w = -1 + di - dv[j]
                        if w < 0:
                            w = 0
                        nd = curd + w
                        if nd < dist2[v]:
                            dist2[v] = nd
                            buckets[nd % 3].append(v)
                            rem += 1
            else:  # out-node
                i = u >> 1
                # reverse vertex arc out -> in
                if uv[i]:
                    v = u - 1
                    if curd < dist2[v]:
                        dist2[v] = curd
                        buckets[curd % 3].append(v)
                        rem += 1

                di = dv[i]
                # forward directed edge arcs, except the one used by the first path
                for j, eid in la[i]:
                    if not (df[eid] == i and dt[eid] == j):
                        v = j << 1
                        w = 1 + di - dv[j]
                        if w < 0:
                            w = 0
                        nd = curd + w
                        if nd < dist2[v]:
                            dist2[v] = nd
                            buckets[nd % 3].append(v)
                            rem += 1

        for eid in path_edge_ids:
            dir_from[eid] = -1
            dir_to[eid] = -1
        for vv in verts:
            loc[vv] = -1

        if res >= INF2:
            return INF
        return 2 * dist1 + res

    # Block candidates on the block-cut path.
    for idx, node in enumerate(path):
        if node >= N:
            cid = node - N
            ce = comps[cid]
            if ce is None:
                continue
            p = path[idx - 1]
            qv = path[idx + 1]
            base = dS[p] + dT[qv]
            alt = dS[qv] + dT[p]
            if alt < base:
                base = alt

            # A non-bridge block contains a cycle of length at least 3.
            if 2 * base + 3 >= ans:
                comps[cid] = None
                path_block_verts.pop(cid, None)
                continue

            verts = path_block_verts[cid]
            cyc = shortest_cycle(ce, verts, p, qv)
            comps[cid] = None
            path_block_verts.pop(cid, None)

            if cyc < INF:
                cand = cyc + 2 * base
                if cand < ans:
                    ans = cand
                    if ans == 3:
                        print(3)
                        return

    print(ans if ans < INF else -1)

if __name__ == "__main__":
    solve()