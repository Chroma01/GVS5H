import sys
from collections import deque
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    S = int(data[idx]) - 1; idx += 1
    T = int(data[idx]) - 1; idx += 1
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        adj[u].append(v)
        adj[v].append(u)

    INF = float('inf')

    def bfs(src):
        d = [INF] * N
        d[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            nd = d[u] + 1
            for w in adj[u]:
                if d[w] == INF:
                    d[w] = nd
                    q.append(w)
        return d

    ds = bfs(S)
    dt = bfs(T)
    D = ds[T]
    oncor = [ds[v] + dt[v] == D for v in range(N)]

    best = INF

    # case 2: internal corridor vertex with an off-corridor neighbour -> extra 2
    for v in range(N):
        if v == S or v == T or not oncor[v]:
            continue
        for w in adj[v]:
            if not oncor[w]:
                if best > 2:
                    best = 2
                break

    # case 3: endpoint detour needing two parking branches -> 4*(L+1)
    def endpoint_extra(E):
        dist = [-1] * N
        par = [-1] * N
        dist[E] = 0
        q = deque([E])
        while q:
            u = q.popleft()
            cnt = 0
            for w in adj[u]:
                if w != par[u] and not oncor[w]:
                    cnt += 1
                    if cnt >= 2:
                        return 4 * (dist[u] + 1)
            for w in adj[u]:
                if not oncor[w] and dist[w] == -1:
                    dist[w] = dist[u] + 1
                    par[w] = u
                    q.append(w)
        return INF

    for E in (S, T):
        e = endpoint_extra(E)
        if e < best:
            best = e

    # case 1: biconnected components (Tarjan, iterative)
    tin = [-1] * N
    low = [0] * N
    timer = 0
    edge_stack = []
    blocks = []
    for root in range(N):
        if tin[root] != -1:
            continue
        tin[root] = low[root] = timer
        timer += 1
        stk = [(root, -1, 0)]
        while stk:
            v, p, i = stk[-1]
            if i < len(adj[v]):
                stk[-1] = (v, p, i + 1)
                to = adj[v][i]
                if to == p:
                    continue
                if tin[to] != -1:
                    if tin[to] < tin[v]:
                        edge_stack.append((v, to))
                        if tin[to] < low[v]:
                            low[v] = tin[to]
                else:
                    edge_stack.append((v, to))
                    tin[to] = low[to] = timer
                    timer += 1
                    stk.append((to, v, 0))
            else:
                stk.pop()
                if stk:
                    pv = stk[-1][0]
                    if low[v] < low[pv]:
                        low[pv] = low[v]
                    if low[v] >= tin[pv]:
                        blk = []
                        while True:
                            e = edge_stack.pop()
                            blk.append(e)
                            if e == (pv, v):
                                break
                        blocks.append(blk)

    nb = len(blocks)
    block_verts = []
    blk_of = [[] for _ in range(N)]
    for bi, blk in enumerate(blocks):
        vs = set()
        for (u, w) in blk:
            vs.add(u); vs.add(w)
        vs = list(vs)
        block_verts.append(vs)
        for x in vs:
            blk_of[x].append(bi)

    cut_node = {}
    nc = 0
    for x in range(N):
        if len(blk_of[x]) >= 2:
            cut_node[x] = nb + nc
            nc += 1
    total_nodes = nb + nc
    bct = [[] for _ in range(total_nodes)]
    for bi in range(nb):
        for x in block_verts[bi]:
            if x in cut_node:
                cn = cut_node[x]
                bct[bi].append(cn)
                bct[cn].append(bi)
    cut_vert = [-1] * total_nodes
    for x, ch in cut_node.items():
        cut_vert[ch] = x

    def node_of(x):
        if x in cut_node:
            return cut_node[x]
        return blk_of[x][0]

    start = node_of(S)
    goal = node_of(T)
    par = [-1] * total_nodes
    par[start] = start
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            break
        for w in bct[u]:
            if par[w] == -1:
                par[w] = u
                q.append(w)
    path = []
    x = goal
    while x != start:
        path.append(x)
        x = par[x]
    path.append(start)
    path.reverse()
    K = len(path) - 1

    def min_cycle(bi, entry, exit_):
        verts = block_verts[bi]
        bedges = blocks[bi]
        loc = {v: i for i, v in enumerate(verts)}
        n = len(verts)
        NV = 2 * n
        to = []
        cap = []
        cost = []
        nxt = []
        head = [-1] * NV

        def add(a, b, c, w):
            to.append(b); cap.append(c); cost.append(w); nxt.append(head[a]); head[a] = len(to) - 1
            to.append(a); cap.append(0); cost.append(-w); nxt.append(head[b]); head[b] = len(to) - 1

        for i, v in enumerate(verts):
            c = 2 if (v == entry or v == exit_) else 1
            add(2 * i, 2 * i + 1, c, 0)
        for (u, w) in bedges:
            iu = loc[u]; iw = loc[w]
            add(2 * iu + 1, 2 * iw, 1, 1)
            add(2 * iw + 1, 2 * iu, 1, 1)

        src = 2 * loc[entry]
        snk = 2 * loc[exit_] + 1
        h = [0] * NV
        total = 0
        flow = 0
        while flow < 2:
            dist = [INF] * NV
            dist[src] = 0
            pre_v = [-1] * NV
            pre_e = [-1] * NV
            pq = [(0, src)]
            while pq:
                dcur, u = heapq.heappop(pq)
                if dcur > dist[u]:
                    continue
                hu = h[u]
                e = head[u]
                while e != -1:
                    if cap[e] > 0:
                        w2 = to[e]
                        nd = dcur + cost[e] + hu - h[w2]
                        if nd < dist[w2]:
                            dist[w2] = nd
                            pre_v[w2] = u
                            pre_e[w2] = e
                            heapq.heappush(pq, (nd, w2))
                    e = nxt[e]
            if dist[snk] == INF:
                break
            true_d = dist[snk] + h[snk]
            for v in range(NV):
                if dist[v] < INF:
                    h[v] += dist[v]
            f = 2 - flow
            v = snk
            while v != src:
                e = pre_e[v]
                if cap[e] < f:
                    f = cap[e]
                v = pre_v[v]
            v = snk
            while v != src:
                e = pre_e[v]
                cap[e] -= f
                cap[e ^ 1] += f
                v = pre_v[v]
            total += f * true_d
            flow += f
        if flow < 2:
            return INF
        return total

    for i, node in enumerate(path):
        if node >= nb:
            continue
        bi = node
        entry = S if i == 0 else cut_vert[path[i - 1]]
        exit_ = T if i == K else cut_vert[path[i + 1]]
        if entry == exit_ or len(block_verts[bi]) < 3:
            continue
        din = ds[exit_] - ds[entry]
        if din <= 0:
            continue
        cyc = min_cycle(bi, entry, exit_)
        if cyc < INF:
            val = cyc - 2 * din
            if val < best:
                best = val

    if best == INF:
        print(-1)
    else:
        print(2 * D + best)

main()