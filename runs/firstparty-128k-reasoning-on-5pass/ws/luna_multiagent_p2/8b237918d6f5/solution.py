import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        forward = [to, cap, len(self.graph[to])]
        backward = [fr, 0, len(self.graph[fr])]
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def max_flow(self, source, sink):
        flow = 0
        inf = 10**18

        while True:
            level = [-1] * self.n
            level[source] = 0
            queue = deque([source])

            while queue:
                v = queue.popleft()
                for to, cap, _ in self.graph[v]:
                    if cap > 0 and level[to] < 0:
                        level[to] = level[v] + 1
                        queue.append(to)

            if level[sink] < 0:
                return flow

            it = [0] * self.n

            def dfs(v, pushed):
                if v == sink:
                    return pushed

                while it[v] < len(self.graph[v]):
                    edge = self.graph[v][it[v]]
                    to, cap, rev = edge

                    if cap > 0 and level[to] == level[v] + 1:
                        amount = dfs(to, min(pushed, cap))
                        if amount:
                            edge[1] -= amount
                            self.graph[to][rev][1] += amount
                            return amount

                    it[v] += 1

                return 0

            while True:
                pushed = dfs(source, inf)
                if pushed == 0:
                    break
                flow += pushed


def minimum_selected_edges(n, m, edges, distance):
    if distance == 0:
        return 0

    label_count = n * distance
    source = label_count
    sink = source + 1
    dinic = Dinic(sink + 1)

    inf = m + 1

    def label(vertex, level):
        return vertex * distance + level

    # Vertex 1 must have potential 0:
    # every positive threshold label is on the sink side.
    for level in range(distance):
        dinic.add_edge(label(0, level), sink, inf)

    # Vertex N must have potential at least distance:
    # every threshold label is on the source side.
    for level in range(distance):
        dinic.add_edge(source, label(n - 1, level), inf)

    # Threshold monotonicity:
    # z[v][i+1] => z[v][i].
    for vertex in range(n):
        for level in range(1, distance):
            dinic.add_edge(label(vertex, level), label(vertex, level - 1), inf)

    for u, v in edges:
        u -= 1
        v -= 1

        for level in range(distance):
            # Capacity 1. This is cut exactly when the edge's
            # potential difference is one at this threshold.
            dinic.add_edge(label(v, level), label(u, level), 1)

            # Infinite capacity: d_v >= level+1 implies d_u >= level.
            # This enforces d_v <= d_u + 1.
            if level >= 1:
                dinic.add_edge(
                    label(v, level),
                    label(u, level - 1),
                    inf,
                )

    return dinic.max_flow(source, sink)


def main():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]

    low = 0
    high = n

    while low + 1 < high:
        mid = (low + high) // 2
        needed = minimum_selected_edges(n, m, edges, mid)

        if needed <= k:
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()