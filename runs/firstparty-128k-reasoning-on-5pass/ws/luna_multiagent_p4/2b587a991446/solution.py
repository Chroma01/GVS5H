import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    # Each vertex v has nodes vin=2v and vout=2v+1.
    # Internal vertices have a capacity-1 zero-cost arc vin -> vout.
    # S and T are endpoints and therefore have capacity 2 implicitly.
    size = 2 * n
    graph = [[] for _ in range(size)]

    def add_edge(u, v, cap, cost):
        graph[u].append([v, cap, cost, len(graph[v])])
        graph[v].append([u, 0, -cost, len(graph[u]) - 1])

    for v in range(n):
        if v != s and v != t:
            add_edge(2 * v, 2 * v + 1, 1, 0)

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        add_edge(2 * u + 1, 2 * v, 1, 1)
        add_edge(2 * v + 1, 2 * u, 1, 1)

    source = 2 * s + 1
    sink = 2 * t

    potential = [0] * size
    total_cost = 0

    for flow_no in range(2):
        inf = 10**18
        dist = [inf] * size
        prev_v = [-1] * size
        prev_e = [-1] * size
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for ei, edge in enumerate(graph[u]):
                v, cap, cost, rev = edge
                if cap <= 0:
                    continue
                nd = d + cost + potential[u] - potential[v]
                if nd < dist[v]:
                    dist[v] = nd
                    prev_v[v] = u
                    prev_e[v] = ei
                    heapq.heappush(pq, (nd, v))

        if dist[sink] == inf:
            print(-1)
            return

        for v in range(size):
            if dist[v] < inf:
                potential[v] += dist[v]

        v = sink
        while v != source:
            u = prev_v[v]
            ei = prev_e[v]
            edge = graph[u][ei]
            total_cost += edge[2]
            edge[1] -= 1
            graph[v][edge[3]][1] += 1
            v = u

    print(total_cost)


if __name__ == "__main__":
    solve()