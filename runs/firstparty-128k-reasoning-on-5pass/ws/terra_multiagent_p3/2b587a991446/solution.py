import sys
import heapq
from collections import deque


INF = 10**18


def min_two_vertex_disjoint_paths(n, graph, s, t):
    # Min-cost flow for two internally vertex-disjoint S-T paths.
    # Each original vertex is split; each undirected edge gets a capacity-1
    # gadget so the same edge cannot be used by both paths.
    #
    # vertex nodes:
    #   vin(v) = 2*v, vout(v) = 2*v+1
    # edge gadget i:
    #   ein(i), eout(i)
    base = 2 * n
    total_nodes = base + 2 * len(graph[0])

    # The caller supplies a special edge list through graph[0].
    edges = graph[0]
    adj = [[] for _ in range(total_nodes)]

    def add_edge(fr, to, cap, cost):
        adj[fr].append([to, len(adj[to]), cap, cost])
        adj[to].append([fr, len(adj[fr]) - 1, 0, -cost])

    for v in range(n):
        cap = 2 if v == s or v == t else 1
        add_edge(2 * v, 2 * v + 1, cap, 0)

    for i, (u, v) in enumerate(edges):
        ein = base + 2 * i
        eout = ein + 1
        add_edge(ein, eout, 1, 1)
        add_edge(2 * u + 1, ein, 1, 0)
        add_edge(2 * v + 1, ein, 1, 0)
        add_edge(eout, 2 * u, 1, 0)
        add_edge(eout, 2 * v, 1, 0)

    source = 2 * s + 1
    sink = 2 * t

    result = 0
    flow = 0
    potential = [0] * total_nodes

    while flow < 2:
        dist = [INF] * total_nodes
        prev_v = [-1] * total_nodes
        prev_e = [-1] * total_nodes
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            cd, v = heapq.heappop(pq)
            if cd != dist[v]:
                continue
            for ei, e in enumerate(adj[v]):
                to, _, cap, cost = e
                if cap <= 0:
                    continue
                nd = cd + cost + potential[v] - potential[to]
                if nd < dist[to]:
                    dist[to] = nd
                    prev_v[to] = v
                    prev_e[to] = ei
                    heapq.heappush(pq, (nd, to))

        if dist[sink] == INF:
            return INF

        for v in range(total_nodes):
            if dist[v] < INF:
                potential[v] += dist[v]

        v = sink
        while v != source:
            pv = prev_v[v]
            pe = prev_e[v]
            e = adj[pv][pe]
            e[2] -= 1
            adj[v][e[1]][2] += 1
            v = pv

        result += potential[sink]
        flow += 1

    return result


def tree_style_candidate(n, adj, s, t):
    # BFS tree rooted at S supplies a shortest S-T path and valid
    # tree-like parking constructions.
    parent = [-1] * n
    q = deque([s])
    parent[s] = s

    while q:
        v = q.popleft()
        for to in adj[v]:
            if parent[to] == -1:
                parent[to] = v
                q.append(to)

    path = []
    v = t
    while v != s:
        path.append(v)
        v = parent[v]
    path.append(s)
    path.reverse()

    d = len(path) - 1
    on_path = [False] * n
    for v in path:
        on_path[v] = True

    ans = INF

    # Any strict internal path vertex with a neighbor outside the path
    # permits a two-move parking detour.
    for v in path[1:-1]:
        if len(adj[v]) >= 3:
            ans = min(ans, 2 * d + 2)

    # Build a multi-source BFS tree from the shortest path.  Its children
    # identify genuine side branches usable as parking areas.
    dist = [-1] * n
    root_parent = [-1] * n
    q = deque()

    for v in path:
        dist[v] = 0
        root_parent[v] = v
        q.append(v)

    child_count = [0] * n
    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                root_parent[to] = v
                child_count[v] += 1
                q.append(to)

    # For endpoint / off-path switching, two directions away from the
    # route are needed.  In the BFS forest this is represented by at least
    # two children, except that a non-path vertex also has its parent as
    # one direction and needs two total directions away from its route side.
    for v in range(n):
        if on_path[v] and v != s and v != t:
            continue

        usable = child_count[v]
        if not on_path[v]:
            # One child can park A and the parent-side component supplies
            # the route; a second child is needed to park B.
            if usable < 2:
                continue
        else:
            # At S or T, the route consumes one incident direction; two
            # side directions are necessary.
            if usable < 2:
                continue

        ans = min(ans, 2 * d + 4 * dist[v] + 4)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, s, t = data[:4]
    s -= 1
    t -= 1

    adj = [[] for _ in range(n)]
    edge_list = []
    p = 4
    for _ in range(m):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        adj[u].append(v)
        adj[v].append(u)
        edge_list.append((u, v))

    ans = tree_style_candidate(n, adj, s, t)

    # A pair of internally vertex-disjoint S-T paths directly gives a
    # collision-free exchange: send the two pieces through different paths.
    flow_input = [edge_list]
    disjoint_cost = min_two_vertex_disjoint_paths(n, flow_input, s, t)
    ans = min(ans, disjoint_cost)

    print(-1 if ans >= INF else ans)


if __name__ == "__main__":
    main()