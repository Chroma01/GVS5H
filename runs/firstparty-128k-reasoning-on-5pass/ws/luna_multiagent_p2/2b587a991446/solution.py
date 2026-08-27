import sys
import heapq


class MinCostMaxFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap, cost):
        self.g[fr].append([to, len(self.g[to]), cap, cost])
        self.g[to].append([fr, len(self.g[fr]) - 1, 0, -cost])

    def flow(self, s, t, required):
        n = self.n
        inf = 10**18
        potential = [0] * n
        total_cost = 0
        sent = 0

        while sent < required:
            dist = [inf] * n
            prev_v = [-1] * n
            prev_e = [-1] * n
            dist[s] = 0
            pq = [(0, s)]

            while pq:
                d, v = heapq.heappop(pq)
                if d != dist[v]:
                    continue
                for i, e in enumerate(self.g[v]):
                    to, rev, cap, cost = e
                    if cap == 0:
                        continue
                    nd = d + cost + potential[v] - potential[to]
                    if nd < dist[to]:
                        dist[to] = nd
                        prev_v[to] = v
                        prev_e[to] = i
                        heapq.heappush(pq, (nd, to))

            if dist[t] == inf:
                break

            for v in range(n):
                if dist[v] < inf:
                    potential[v] += dist[v]

            add = required - sent
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
                e[2] -= add
                self.g[v][e[1]][2] += add
                total_cost += add * e[3]
                v = pv

            sent += add

        return sent, total_cost


def solve():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    edges = [tuple(map(int, input().split())) for _ in range(m)]

    # Vertex x has split nodes x_in and x_out.
    # 2 extra nodes are used only to keep indexing simple.
    def vin(x):
        return 2 * x

    def vout(x):
        return 2 * x + 1

    network = MinCostMaxFlow(2 * n)

    for v in range(n):
        capacity = 2 if v == s or v == t else 1
        network.add_edge(vin(v), vout(v), capacity, 0)

    for u, v in edges:
        u -= 1
        v -= 1
        network.add_edge(vout(u), vin(v), 1, 1)
        network.add_edge(vout(v), vin(u), 1, 1)

    sent, answer = network.flow(vout(s), vin(t), 2)
    print(answer if sent == 2 else -1)


if __name__ == "__main__":
    solve()