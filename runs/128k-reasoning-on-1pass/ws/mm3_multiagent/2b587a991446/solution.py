import sys
import heapq

class Edge:
    __slots__ = ('to', 'rev', 'cap', 'cost')
    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

class MinCostMaxFlow:
    def __init__(self, N):
        self.N = N
        self.graph = [[] for _ in range(N)]

    def add_edge(self, fr, to, cap, cost):
        # forward edge
        fwd = Edge(to, len(self.graph[to]), cap, cost)
        # reverse edge
        rev = Edge(fr, len(self.graph[fr]), 0, -cost)
        self.graph[fr].append(fwd)
        self.graph[to].append(rev)

    def min_cost_flow(self, s, t, maxf):
        N = self.N
        INF = 10**18
        prevv = [0] * N   # previous vertex
        preve = [0] * N   # previous edge index
        dist = [0] * N
        pot = [0] * N      # potentials
        flow = 0
        cost = 0

        while flow < maxf:
            # Dijkstra with potentials
            dist = [INF] * N
            dist[s] = 0
            pq = [(0, s)]
            while pq:
                d, v = heapq.heappop(pq)
                if dist[v] < d:
                    continue
                for i, e in enumerate(self.graph[v]):
                    if e.cap > 0:
                        nd = d + e.cost + pot[v] - pot[e.to]
                        if nd < dist[e.to]:
                            dist[e.to] = nd
                            prevv[e.to] = v
                            preve[e.to] = i
                            heapq.heappush(pq, (nd, e.to))
            if dist[t] == INF:
                break  # cannot augment more

            # update potentials
            for v in range(N):
                if dist[v] < INF:
                    pot[v] += dist[v]

            # add as much as possible (at most 1 unit because capacities are 1)
            addf = maxf - flow
            v = t
            while v != s:
                e = self.graph[prevv[v]][preve[v]]
                addf = min(addf, e.cap)
                v = prevv[v]

            v = t
            while v != s:
                e = self.graph[prevv[v]][preve[v]]
                e.cap -= addf
                self.graph[v][e.rev].cap += addf
                cost += e.cost * addf
                v = prevv[v]
            flow += addf

        return flow, cost

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    S = int(next(it)) - 1
    T = int(next(it)) - 1

    V = 2 * N
    mcmf = MinCostMaxFlow(V)

    # vertex splitting: each vertex v becomes v_in -> v_out with capacity 1
    for i in range(N):
        mcmf.add_edge(i * 2, i * 2 + 1, 1, 0)

    # original edges
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        # directed edge u_out -> v_in
        mcmf.add_edge(u * 2 + 1, v * 2, 1, 1)
        # directed edge v_out -> u_in
        mcmf.add_edge(v * 2 + 1, u * 2, 1, 1)

    source = S * 2 + 1   # S_out
    sink   = T * 2       # T_in

    flow, cost = mcmf.min_cost_flow(source, sink, 2)
    if flow < 2:
        print(-1)
    else:
        print(cost)

if __name__ == "__main__":
    solve()