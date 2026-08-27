import sys
import heapq
from array import array


def solve():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    graph = [[] for _ in range(n)]
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)
        edges.append((u, v))

    def bfs(start):
        dist = [-1] * n
        dist[start] = 0
        q = [start]
        head_q = 0
        while head_q < len(q):
            v = q[head_q]
            head_q += 1
            nv = dist[v] + 1
            for w in graph[v]:
                if dist[w] == -1:
                    dist[w] = nv
                    q.append(w)
        return dist

    ds = bfs(s)
    dt = bfs(t)
    shortest = ds[t]

    # A shortest path admits the 2*d+2 buffer maneuver precisely when
    # an internal vertex on such a path has a neighbor outside that path.
    # Endpoint side branches do NOT suffice.
    has_internal_buffer = False
    for v in range(n):
        if v != s and v != t and ds[v] + dt[v] == shortest:
            if len(graph[v]) >= 3:
                has_internal_buffer = True
                break

    # Min-cost flow for two internally vertex-disjoint S-T paths.
    # vin(v)=2v, vout(v)=2v+1.
    V = 2 * n
    head = array('i', [-1]) * V
    to = array('i')
    nxt = array('i')
    cap = array('b')
    cost = array('b')

    def add_edge(fr, dest, capacity, c):
        i = len(to)
        to.append(dest)
        nxt.append(head[fr])
        cap.append(capacity)
        cost.append(c)
        head[fr] = i

        to.append(fr)
        nxt.append(head[dest])
        cap.append(0)
        cost.append(-c)
        head[dest] = i + 1

    for v in range(n):
        add_edge(2 * v, 2 * v + 1, 2 if v == s or v == t else 1, 0)

    for u, v in edges:
        add_edge(2 * u + 1, 2 * v, 1, 1)
        add_edge(2 * v + 1, 2 * u, 1, 1)

    source = 2 * s + 1
    sink = 2 * t
    INF = 10 ** 18
    potential = [0] * V
    total_cost = 0
    sent = 0

    while sent < 2:
        dist = [INF] * V
        prev = [-1] * V
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            d, v = heapq.heappop(pq)
            if d != dist[v]:
                continue
            if v == sink:
                break

            e = head[v]
            while e != -1:
                if cap[e] > 0:
                    w = to[e]
                    nd = d + cost[e] + potential[v] - potential[w]
                    if nd < dist[w]:
                        dist[w] = nd
                        prev[w] = e
                        heapq.heappush(pq, (nd, w))
                e = nxt[e]

        if dist[sink] == INF:
            break

        for v in range(V):
            if dist[v] != INF:
                potential[v] += dist[v]

        v = sink
        while v != source:
            e = prev[v]
            cap[e] -= 1
            cap[e ^ 1] += 1
            v = to[e ^ 1]

        total_cost += potential[sink]
        sent += 1

    ans = INF
    if sent == 2:
        ans = total_cost
    if has_internal_buffer:
        ans = min(ans, 2 * shortest + 2)

    print(-1 if ans == INF else ans)


if __name__ == "__main__":
    solve()