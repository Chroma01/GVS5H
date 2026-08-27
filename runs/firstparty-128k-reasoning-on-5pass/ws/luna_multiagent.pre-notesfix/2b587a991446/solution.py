import sys
import heapq


class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap, cost):
        fwd = [to, len(self.g[to]), cap, cost]
        rev = [fr, len(self.g[fr]), 0, -cost]
        self.g[fr].append(fwd)
        self.g[to].append(rev)

    def shortest_path(self, s, t, potential):
        INF = 10**30
        dist = [INF] * self.n
        prev_v = [-1] * self.n
        prev_e = [-1] * self.n

        dist[s] = 0
        pq = [(0, s)]

        while pq:
            d, v = heapq.heappop(pq)
            if d != dist[v]:
                continue

            for ei, e in enumerate(self.g[v]):
                if e[2] <= 0:
                    continue
                to, cost = e[0], e[3]
                nd = d + cost + potential[v] - potential[to]
                if nd < dist[to]:
                    dist[to] = nd
                    prev_v[to] = v
                    prev_e[to] = ei
                    heapq.heappush(pq, (nd, to))

        return dist, prev_v, prev_e

    def min_cost_flow(self, s, t, required):
        INF = 10**30
        potential = [0] * self.n
        flow = 0
        cost = 0

        while flow < required:
            dist, prev_v, prev_e = self.shortest_path(s, t, potential)
            if dist[t] == INF:
                break

            for v in range(self.n):
                if dist[v] < INF:
                    potential[v] += dist[v]

            add = required - flow
            v = t
            while v != s:
                pv = prev_v[v]
                pe = prev_e[v]
                add = min(add, self.g[pv][pe][2])
                v = pv

            v = t
            while v != s:
                pv = prev_v[v]
                pe = prev_e[v]
                e = self.g[pv][pe]
                cost += add * e[3]
                e[2] -= add
                self.g[v][e[1]][2] += add
                v = pv

            flow += add

        return flow, cost


def solve():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    # Vertex v is represented by vin[v] -> vout[v].
    def vin(v):
        return 2 * v

    def vout(v):
        return 2 * v + 1

    source = 2 * n
    sink = source + 1
    mcf = MinCostFlow(2 * n + 2)

    # Internal vertices have capacity 1; S and T may be used by both paths.
    for v in range(n):
        cap = 2 if v == s or v == t else 1
        mcf.add_edge(vin(v), vout(v), cap, 0)

    # Two directed arcs represent each undirected edge.
    # Capacity 1 prevents both paths from using the same directed edge.
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        mcf.add_edge(vout(u), vin(v), 1, 1)
        mcf.add_edge(vout(v), vin(u), 1, 1)

    mcf.add_edge(source, vin(s), 2, 0)
    mcf.add_edge(vout(t), sink, 2, 0)

    flow, answer = mcf.min_cost_flow(source, sink, 2)
    print(answer if flow == 2 else -1)


if __name__ == "__main__":
    solve()