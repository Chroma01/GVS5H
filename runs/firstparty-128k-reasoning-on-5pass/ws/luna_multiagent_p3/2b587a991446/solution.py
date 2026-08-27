import sys
from collections import deque


def bfs(graph, root):
    n = len(graph)
    dist = [-1] * n
    parent = [-1] * n
    order = []

    dist[root] = 0
    q = deque([root])

    while q:
        v = q.popleft()
        order.append(v)
        for to in graph[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                parent[to] = v
                q.append(to)

    return dist, parent, order


def solve():
    input = sys.stdin.readline

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

    ds, raw_parent_s, order_s = bfs(graph, s)
    dt, _, order_t = bfs(graph, t)

    shortest_distance = ds[t]

    # Recover one fixed shortest path from s to t.
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        if cur == s:
            break
        cur = raw_parent_s[cur]
    path.reverse()

    path_index = [-1] * n
    for i, v in enumerate(path):
        path_index[v] = i

    # Build a shortest-path tree from s containing the fixed path.
    parent_s = [-1] * n
    for i in range(1, len(path)):
        parent_s[path[i]] = path[i - 1]

    for v in order_s:
        if path_index[v] != -1:
            continue
        for to in graph[v]:
            if ds[to] == ds[v] - 1:
                parent_s[v] = to
                break

    # Build a shortest-path tree from t containing the fixed path in reverse.
    parent_t = [-1] * n
    for i in range(len(path) - 1):
        parent_t[path[i]] = path[i + 1]

    for v in order_t:
        if path_index[v] != -1:
            continue
        for to in graph[v]:
            if dt[to] == dt[v] - 1:
                parent_t[v] = to
                break

    # Index of the fixed-path vertex to which each tree branch attaches.
    attach_s = [-1] * n
    for v in order_s:
        if path_index[v] != -1:
            attach_s[v] = path_index[v]
        else:
            attach_s[v] = attach_s[parent_s[v]]

    attach_t = [-1] * n
    for v in order_t:
        if path_index[v] != -1:
            attach_t[v] = path_index[v]
        else:
            attach_t[v] = attach_t[parent_t[v]]

    path_edges = set()
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if u > v:
            u, v = v, u
        path_edges.add((u, v))

    # Find a shortest s-t path distinct from the fixed path.
    alternative = 10**30

    for u, v in edges:
        edge_key = (u, v) if u < v else (v, u)

        # A fixed-path edge must not be considered a detour.
        if edge_key in path_edges:
            continue

        a, b = attach_s[u], attach_t[v]
        if a < b:
            alternative = min(alternative, ds[u] + 1 + dt[v])

        a, b = attach_s[v], attach_t[u]
        if a < b:
            alternative = min(alternative, ds[v] + 1 + dt[u])

    if alternative == 10**30:
        print(-1)
    else:
        print(shortest_distance + alternative)


if __name__ == "__main__":
    solve()