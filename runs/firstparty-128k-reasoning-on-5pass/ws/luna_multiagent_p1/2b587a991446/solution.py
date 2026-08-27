import sys
import heapq
from collections import deque

INF = 10**18


def bfs(n, graph, start, blocked=-1):
    dist = [-1] * n
    parent = [-1] * n
    order = []

    if start == blocked:
        return dist, parent, order

    dist[start] = 0
    q = deque([start])

    while q:
        v = q.popleft()
        order.append(v)
        for u in graph[v]:
            if u == blocked or dist[u] != -1:
                continue
            dist[u] = dist[v] + 1
            parent[u] = v
            q.append(u)

    return dist, parent, order


def two_vertex_disjoint_paths(n, edges, s, t):
    # Vertex splitting. Internal vertices have capacity 1, while s and t
    # have capacity 2. Each original graph edge has cost 1.
    vn = 2 * n
    head = [-1] * vn
    to = []
    cap = []
    cost = []
    nxt = []

    def add_edge(a, b, capacity, weight):
        k = len(to)
        to.append(b)
        cap.append(capacity)
        cost.append(weight)
        nxt.append(head[a])
        head[a] = k

        to.append(a)
        cap.append(0)
        cost.append(-weight)
        nxt.append(head[b])
        head[b] = k + 1

    for v in range(n):
        add_edge(2 * v, 2 * v + 1, 2 if v == s or v == t else 1, 0)

    for u, v in edges:
        add_edge(2 * u + 1, 2 * v, 1, 1)
        add_edge(2 * v + 1, 2 * u, 1, 1)

    source = 2 * s + 1
    sink = 2 * t
    potential = [0] * vn
    answer = 0

    for _ in range(2):
        dist = [INF] * vn
        prev = [-1] * vn
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            d, v = heapq.heappop(pq)
            if d != dist[v]:
                continue

            e = head[v]
            while e != -1:
                if cap[e]:
                    u = to[e]
                    nd = d + cost[e] + potential[v] - potential[u]
                    if nd < dist[u]:
                        dist[u] = nd
                        prev[u] = e
                        heapq.heappush(pq, (nd, u))
                e = nxt[e]

        if dist[sink] == INF:
            return None

        for v in range(vn):
            if dist[v] < INF:
                potential[v] += dist[v]

        v = sink
        while v != source:
            e = prev[v]
            cap[e] -= 1
            cap[e ^ 1] += 1
            answer += cost[e]
            v = to[e ^ 1]

    return answer


def replacement_distances(n, graph, s, t, path, dist_s, dist_t):
    d = len(path) - 1
    if d <= 1:
        return []

    index = [-1] * n
    for i, v in enumerate(path):
        index[v] = i

    _, parent_s, order_s = bfs(n, graph, s)
    _, parent_t, order_t = bfs(n, graph, t)

    # Force the selected shortest path to be present in both BFS trees.
    for i in range(1, d + 1):
        parent_s[path[i]] = path[i - 1]
    for i in range(d):
        parent_t[path[i]] = path[i + 1]

    last_s = [-1] * n
    for v in order_s:
        p = parent_s[v]
        last_s[v] = max(index[v], last_s[p] if p != -1 else -1)

    first_t = [d + 1] * n
    for v in order_t:
        p = parent_t[v]
        first_t[v] = min(
            index[v] if index[v] != -1 else d + 1,
            first_t[p] if p != -1 else d + 1,
        )

    size = 1
    while size < d - 1:
        size <<= 1
    seg = [INF] * (2 * size)

    def range_chmin(left, right, value):
        if left > right:
            return
        left += size
        right += size
        while left <= right:
            if left & 1:
                if value < seg[left]:
                    seg[left] = value
                left += 1
            if not (right & 1):
                if value < seg[right]:
                    seg[right] = value
                right -= 1
            left >>= 1
            right >>= 1

    for u in range(n):
        for v in graph[u]:
            left = max(1, last_s[u] + 1)
            right = min(d - 1, first_t[v] - 1)
            if left <= right:
                range_chmin(
                    left - 1,
                    right - 1,
                    dist_s[u] + 1 + dist_t[v],
                )

    result = [INF] * (d - 1)
    for i in range(d - 1):
        p = i + size
        best = INF
        while p:
            if seg[p] < best:
                best = seg[p]
            p >>= 1
        result[i] = best

    return result


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, s, t = data[:4]
    s -= 1
    t -= 1

    graph = [[] for _ in range(n)]
    edges = []
    pos = 4

    for _ in range(m):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        edges.append((u, v))
        graph[u].append(v)
        graph[v].append(u)

    direct = two_vertex_disjoint_paths(n, edges, s, t)
    if direct is not None:
        print(direct)
        return

    dist_s, parent_s, _ = bfs(n, graph, s)
    dist_t, _, _ = bfs(n, graph, t)
    d = dist_s[t]

    path = []
    v = t
    while v != -1:
        path.append(v)
        v = parent_s[v]
    path.reverse()

    on_path = [False] * n
    for v in path:
        on_path[v] = True

    # If A parks at x:
    # S -> x avoids T,
    # T -> S avoids x,
    # x -> T avoids S.
    dist_s_avoid_t, _, _ = bfs(n, graph, s, blocked=t)
    dist_t_avoid_s, _, _ = bfs(n, graph, t, blocked=s)

    best = INF

    for x in range(n):
        if x == s or x == t:
            continue
        if not on_path[x]:
            a = dist_s_avoid_t[x]
            c = dist_t_avoid_s[x]
            if a != -1 and c != -1:
                best = min(best, a + d + c)

    repl = replacement_distances(n, graph, s, t, path, dist_s, dist_t)
    for i, middle in enumerate(repl, start=1):
        x = path[i]
        a = dist_s_avoid_t[x]
        c = dist_t_avoid_s[x]
        if a != -1 and c != -1 and middle < INF:
            best = min(best, a + middle + c)

    print(-1 if best == INF else best)


if __name__ == "__main__":
    solve()