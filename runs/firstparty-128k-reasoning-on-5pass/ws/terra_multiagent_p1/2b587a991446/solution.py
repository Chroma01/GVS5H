import sys
import heapq
from array import array
from collections import deque


def solve():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    edges = []
    graph = [[] for _ in range(n)]
    for eid in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        graph[u].append((v, eid))
        graph[v].append((u, eid))

    def bfs(start):
        dist = [-1] * n
        dist[start] = 0
        q = deque([start])
        while q:
            v = q.popleft()
            nd = dist[v] + 1
            for to, _ in graph[v]:
                if dist[to] == -1:
                    dist[to] = nd
                    q.append(to)
        return dist

    ds = bfs(s)
    dt = bfs(t)
    d_st = ds[t]

    # If an S-T shortest path uses all vertices, every extra edge would be a
    # chord shortening it. Hence the graph is a path, where swapping is
    # impossible because the pieces cannot pass one another.
    if d_st == n - 1:
        print(-1)
        return

    # A shortest S-T path omits at least one vertex. One can park a piece in
    # an off-path component, allowing the other to cross.
    ans = 2 * d_st + 2

    # Tarjan decomposition into vertex-biconnected edge blocks.
    sys.setrecursionlimit(1_000_000)
    disc = [0] * n
    low = [0] * n
    edge_stack = []
    blocks = []
    timer = 0

    def dfs(v, parent_edge):
        nonlocal timer
        timer += 1
        disc[v] = low[v] = timer

        for to, eid in graph[v]:
            if eid == parent_edge:
                continue

            if disc[to] == 0:
                edge_stack.append(eid)
                dfs(to, eid)
                low[v] = min(low[v], low[to])

                if low[to] >= disc[v]:
                    comp = []
                    while True:
                        x = edge_stack.pop()
                        comp.append(x)
                        if x == eid:
                            break
                    blocks.append(comp)

            elif disc[to] < disc[v]:
                edge_stack.append(eid)
                low[v] = min(low[v], disc[to])

    dfs(0, -1)

    # Construct the block-cut tree.
    bcnt = len(blocks)
    bct = [[] for _ in range(n + bcnt)]

    for bi, comp in enumerate(blocks):
        node = n + bi
        verts = set()
        for eid in comp:
            u, v = edges[eid]
            verts.add(u)
            verts.add(v)
        for v in verts:
            bct[v].append(node)
            bct[node].append(v)

    # Locate the unique S-T path in the block-cut tree.
    total_nodes = n + bcnt
    parent = [-1] * total_nodes
    parent[s] = s
    q = deque([s])

    while q:
        v = q.popleft()
        if v == t:
            break
        for to in bct[v]:
            if parent[to] == -1:
                parent[to] = v
                q.append(to)

    route = []
    cur = t
    while cur != s:
        route.append(cur)
        cur = parent[cur]
    route.append(s)
    route.reverse()

    def shortest_cycle_through(block_edges, a, b):
        """
        Return the length of the shortest simple cycle containing a and b.

        This equals the minimum total length of two internally vertex-disjoint
        and edge-disjoint a-b paths. A two-unit min-cost flow with vertex and
        edge capacities enforces those conditions.
        """
        verts = []
        seen = set()
        for eid in block_edges:
            u, v = edges[eid]
            if u not in seen:
                seen.add(u)
                verts.append(u)
            if v not in seen:
                seen.add(v)
                verts.append(v)

        idx = {v: i for i, v in enumerate(verts)}
        k = len(verts)
        ecount = len(block_edges)

        # Each vertex has in=2*i and out=2*i+1.
        # Each original edge receives a two-node capacity-one gadget.
        V = 2 * k + 2 * ecount
        head = array('i', [-1]) * V
        to = array('i')
        nxt = array('i')
        cap = array('b')
        cost = array('i')

        def add_edge(fr, tv, ca, co):
            ei = len(to)
            to.append(tv)
            nxt.append(head[fr])
            cap.append(ca)
            cost.append(co)
            head[fr] = ei

            to.append(fr)
            nxt.append(head[tv])
            cap.append(0)
            cost.append(-co)
            head[tv] = ei + 1

        ia = idx[a]
        ib = idx[b]

        # Internal vertices can be used by only one of the two paths.
        for i in range(k):
            if i != ia and i != ib:
                add_edge(2 * i, 2 * i + 1, 1, 0)

        base = 2 * k
        for j, eid in enumerate(block_edges):
            u, v = edges[eid]
            iu = idx[u]
            iv = idx[v]
            ein = base + 2 * j
            eout = ein + 1

            # One shared unit of capacity represents use of this undirected
            # original edge in either direction, with unit traversal cost.
            add_edge(2 * iu + 1, ein, 1, 0)
            add_edge(2 * iv + 1, ein, 1, 0)
            add_edge(ein, eout, 1, 1)
            add_edge(eout, 2 * iu, 1, 0)
            add_edge(eout, 2 * iv, 1, 0)

        source = 2 * ia + 1
        sink = 2 * ib
        INF = 10 ** 18
        potential = [0] * V
        total_cost = 0

        for _ in range(2):
            dist = [INF] * V
            prev = array('i', [-1]) * V
            dist[source] = 0
            pq = [(0, source)]

            while pq:
                cd, v = heapq.heappop(pq)
                if cd != dist[v]:
                    continue
                if v == sink:
                    break

                e = head[v]
                while e != -1:
                    if cap[e]:
                        nv = to[e]
                        nd = cd + cost[e] + potential[v] - potential[nv]
                        if nd < dist[nv]:
                            dist[nv] = nd
                            prev[nv] = e
                            heapq.heappush(pq, (nd, nv))
                    e = nxt[e]

            if dist[sink] == INF:
                return INF

            for v in range(V):
                if dist[v] != INF:
                    potential[v] += dist[v]

            v = sink
            while v != source:
                e = prev[v]
                cap[e] -= 1
                cap[e ^ 1] += 1
                total_cost += cost[e]
                v = to[e ^ 1]

        return total_cost

    # Passing can happen in any block on the S-T route. All portions outside
    # that block are traversed once by each piece.
    for i, node in enumerate(route):
        if node < n:
            continue

        bi = node - n
        a = route[i - 1]
        b = route[i + 1]

        cycle_len = shortest_cycle_through(blocks[bi], a, b)
        if cycle_len < 10 ** 18:
            ans = min(ans, 2 * (ds[a] + dt[b]) + cycle_len)

    print(ans)


if __name__ == "__main__":
    solve()