import sys
import heapq
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1
    S = int(data[pos]) - 1; pos += 1
    T = int(data[pos]) - 1; pos += 1
    adj = [[] for _ in range(N)]
    for i in range(M):
        u = int(data[pos]) - 1; pos += 1
        v = int(data[pos]) - 1; pos += 1
        adj[u].append((v, i))
        adj[v].append((u, i))

    BIG = 1 << 60

    def bfs(src):
        dist = [-1] * N
        dist[src] = 0
        dq = deque([src])
        while dq:
            u = dq.popleft()
            du = dist[u] + 1
            for v, _ in adj[u]:
                if dist[v] == -1:
                    dist[v] = du
                    dq.append(v)
        return dist

    dS = bfs(S)
    dT = bfs(T)
    L = dS[T]

    # ---- buffer gadget: v on some shortest S-T path with deg>=3 ----
    ans = BIG
    for v in range(N):
        if len(adj[v]) >= 3 and dS[v] + dT[v] == L:
            pen = 4 if (v == S or v == T) else 2
            cand = 2 * L + pen
            if cand < ans:
                ans = cand

    # ---- biconnected components (blocks), iterative Tarjan ----
    disc = [-1] * N
    low = [0] * N
    pe = [-1] * N
    it = [0] * N
    estack = []
    blocks = []
    is_art = [False] * N
    timer = 0
    for s in range(N):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = timer; timer += 1
        stack = [s]
        child = 0
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v, eid = adj[u][it[u]]
                it[u] += 1
                if eid == pe[u]:
                    continue
                if disc[v] == -1:
                    estack.append((u, v))
                    pe[v] = eid
                    disc[v] = low[v] = timer; timer += 1
                    stack.append(v)
                    if u == s:
                        child += 1
                elif disc[v] < disc[u]:
                    estack.append((u, v))
                    if disc[v] < low[u]:
                        low[u] = disc[v]
            else:
                stack.pop()
                if stack:
                    p = stack[-1]
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if low[u] >= disc[p]:
                        comp = []
                        while True:
                            e = estack.pop()
                            comp.append(e)
                            if e == (p, u):
                                break
                        blocks.append(comp)
                        is_art[p] = True
        is_art[s] = (child >= 2)

    B = len(blocks)
    block_vertices = []
    block_of = [-1] * N
    for bi, comp in enumerate(blocks):
        vs = set()
        for u, v in comp:
            vs.add(u); vs.add(v)
        block_vertices.append(vs)
        for v in vs:
            if not is_art[v]:
                block_of[v] = bi

    total = B + N
    bct = [[] for _ in range(total)]
    for bi in range(B):
        for v in block_vertices[bi]:
            if is_art[v]:
                a = B + v
                bct[bi].append(a)
                bct[a].append(bi)

    start = B + S if is_art[S] else block_of[S]
    target = B + T if is_art[T] else block_of[T]

    par = [-1] * total
    seen = [False] * total
    dq = deque([start])
    seen[start] = True
    while dq:
        u = dq.popleft()
        if u == target:
            break
        for w in bct[u]:
            if not seen[w]:
                seen[w] = True
                par[w] = u
                dq.append(w)
    path = []
    cur = target
    while cur != -1:
        path.append(cur)
        cur = par[cur]
    path.reverse()

    # ---- min-cost 2-flow = shortest cycle through x,y inside a block ----
    def min_cycle(comp, x, y):
        vid = {}
        for u, v in comp:
            if u not in vid: vid[u] = len(vid)
            if v not in vid: vid[v] = len(vid)
        if x not in vid or y not in vid:
            return BIG
        n = len(vid)
        ix = vid[x]; iy = vid[y]
        N2 = 2 * n
        graph = [[] for _ in range(N2)]

        def add(u, v, cap, cost):
            graph[u].append([v, cap, cost, len(graph[v])])
            graph[v].append([u, 0, -cost, len(graph[u]) - 1])

        for i in range(n):
            c = 2 if (i == ix or i == iy) else 1
            add(2 * i, 2 * i + 1, c, 0)
        for u, v in comp:
            iu = vid[u]; iv = vid[v]
            add(2 * iu + 1, 2 * iv, 1, 1)
            add(2 * iv + 1, 2 * iu, 1, 1)
        s = 2 * ix; t = 2 * iy
        h = [0] * N2
        prevv = [0] * N2
        preve = [0] * N2
        flow = 0; cost = 0
        while flow < 2:
            dist = [BIG] * N2
            dist[s] = 0
            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                hu = h[u]
                for i, e in enumerate(graph[u]):
                    if e[1] > 0:
                        v = e[0]
                        nd = d + e[2] + hu - h[v]
                        if nd < dist[v]:
                            dist[v] = nd
                            prevv[v] = u; preve[v] = i
                            heapq.heappush(pq, (nd, v))
            if dist[t] >= BIG:
                return BIG
            for v in range(N2):
                if dist[v] < BIG:
                    h[v] += dist[v]
            d = 2 - flow
            v = t
            while v != s:
                e = graph[prevv[v]][preve[v]]
                if e[1] < d:
                    d = e[1]
                v = prevv[v]
            v = t
            while v != s:
                e = graph[prevv[v]][preve[v]]
                e[1] -= d
                graph[v][e[3]][1] += d
                v = prevv[v]
            flow += d
            cost += d * h[t]
        return cost

    plen = len(path)
    for i, node in enumerate(path):
        if node < B:
            if len(block_vertices[node]) < 3:
                continue
            x = S if i == 0 else path[i - 1] - B
            y = T if i == plen - 1 else path[i + 1] - B
            # quick lower bound: min_cycle >= 3
            if 2 * (dS[x] + dT[y]) + 3 >= ans:
                continue
            c = min_cycle(blocks[node], x, y)
            if c < BIG:
                cand = 2 * (dS[x] + dT[y]) + c
                if cand < ans:
                    ans = cand

    print(ans if ans < BIG else -1)


if __name__ == "__main__":
    main()