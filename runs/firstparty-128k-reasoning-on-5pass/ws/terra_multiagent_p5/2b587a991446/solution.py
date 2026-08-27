import sys
import heapq
from collections import deque


def solve():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    adj = [[] for _ in range(n)]
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))

    # Any shortest S-T path is sufficient.  If an internal vertex on it
    # has degree at least 3, its third neighbor is outside this shortest
    # path (a chord would shorten the path), so it is a temporary buffer.
    dist = [-1] * n
    parent = [-1] * n
    dist[s] = 0
    q = deque([s])

    while q:
        v = q.popleft()
        for w in adj[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                parent[w] = v
                q.append(w)

    d = dist[t]
    path = []
    v = t
    while v != -1:
        path.append(v)
        if v == s:
            break
        v = parent[v]
    path.reverse()

    INF = 10**30
    answer = INF

    for v in path[1:-1]:
        if len(adj[v]) >= 3:
            answer = 2 * d + 2
            break

    # Minimum total length of two internally vertex-disjoint S-T paths.
    # This is a min-cost flow of value 2 with vertex splitting.
    V = 2 * n
    graph = [[] for _ in range(V)]

    def add_edge(fr, to, cap, cost):
        graph[fr].append([to, cap, cost, len(graph[to])])
        graph[to].append([fr, 0, -cost, len(graph[fr]) - 1])

    def vin(v):
        return v * 2

    def vout(v):
        return v * 2 + 1

    for v in range(n):
        add_edge(vin(v), vout(v), 2 if v == s or v == t else 1, 0)

    for u, v in edges:
        add_edge(vout(u), vin(v), 1, 1)
        add_edge(vout(v), vin(u), 1, 1)

    source = vout(s)
    sink = vin(t)
    potential = [0] * V
    total_cost = 0
    flow = 0

    while flow < 2:
        dd = [INF] * V
        prev_v = [-1] * V
        prev_e = [-1] * V
        dd[source] = 0
        heap = [(0, source)]

        while heap:
            cur, v = heapq.heappop(heap)
            if cur != dd[v]:
                continue

            pv = potential[v]
            for ei, e in enumerate(graph[v]):
                to, cap, cost, _ = e
                if cap == 0:
                    continue
                nd = cur + cost + pv - potential[to]
                if nd < dd[to]:
                    dd[to] = nd
                    prev_v[to] = v
                    prev_e[to] = ei
                    heapq.heappush(heap, (nd, to))

        if dd[sink] == INF:
            break

        for v in range(V):
            if dd[v] != INF:
                potential[v] += dd[v]

        v = sink
        while v != source:
            pv = prev_v[v]
            ei = prev_e[v]
            e = graph[pv][ei]
            e[1] -= 1
            graph[v][e[3]][1] += 1
            total_cost += e[2]
            v = pv

        flow += 1

    if flow == 2:
        answer = min(answer, total_cost)

    print(-1 if answer == INF else answer)


if __name__ == "__main__":
    solve()