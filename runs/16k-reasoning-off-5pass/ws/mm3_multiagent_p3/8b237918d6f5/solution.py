import sys
import heapq

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges.append((u, v))

    # Min-cost max-flow with potentials (Johnson's algorithm)
    class MCMF:
        def __init__(self, n):
            self.n = n
            self.adj = [[] for _ in range(n)]

        def add_edge(self, fr, to, cap, cost):
            # forward edge
            self.adj[fr].append([to, cap, cost, len(self.adj[to])])
            # backward edge
            self.adj[to].append([fr, 0, -cost, len(self.adj[fr]) - 1])

        def min_cost_flow(self, s, t, maxf):
            n = self.n
            INF = 10**18
            res = 0
            h = [0] * n  # potentials
            prevv = [0] * n
            preve = [0] * n
            flow = 0
            while flow < maxf:
                dist = [INF] * n
                dist[s] = 0
                pq = [(0, s)]
                while pq:
                    d, v = heapq.heappop(pq)
                    if dist[v] < d:
                        continue
                    for i, e in enumerate(self.adj[v]):
                        to, cap, cost, rev = e
                        if cap > 0 and dist[to] > dist[v] + cost + h[v] - h[to]:
                            dist[to] = dist[v] + cost + h[v] - h[to]
                            prevv[to] = v
                            preve[to] = i
                            heapq.heappush(pq, (dist[to], to))
                if dist[t] == INF:
                    return None  # cannot send more flow
                for v in range(n):
                    if dist[v] < INF:
                        h[v] += dist[v]
                d = maxf - flow
                v = t
                while v != s:
                    d = min(d, self.adj[prevv[v]][preve[v]][1])
                    v = prevv[v]
                flow += d
                res += d * h[t]
                v = t
                while v != s:
                    e = self.adj[prevv[v]][preve[v]]
                    e[1] -= d
                    self.adj[v][e[3]][1] += d
                    v = prevv[v]
            return res

    # Build flow network for a given L (target distance)
    # We need to check if we can achieve shortest distance > L,
    # i.e., every 1->N path uses at least L+1 selected edges.
    # We send L+1 units of flow; min-cost = min selected edges needed.
    # Feasible if min-cost <= K.
    def feasible(L):
        # Node splitting: each vertex i -> i_in (id 2*i), i_out (id 2*i+1)
        node_in = lambda i: 2 * i
        node_out = lambda i: 2 * i + 1
        S = node_in(0)
        T = node_out(N - 1)
        total_nodes = 2 * N
        mcmf = MCMF(total_nodes)
        INF_CAP = 10**9
        # internal edges
        for i in range(N):
            mcmf.add_edge(node_in(i), node_out(i), INF_CAP, 0)
        # graph edges: two parallel edges
        for (u, v) in edges:
            # cost 1 (select)
            mcmf.add_edge(node_out(u), node_in(v), 1, 1)
            # cost 0 (don't select)
            mcmf.add_edge(node_out(u), node_in(v), 1, 0)
        cost = mcmf.min_cost_flow(S, T, L + 1)
        if cost is None:
            return False
        return cost <= K

    # Binary search on answer L (shortest distance)
    lo = 0
    hi = M  # max possible distance is M (all edges weight 1)
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)

if __name__ == "__main__":
    solve()