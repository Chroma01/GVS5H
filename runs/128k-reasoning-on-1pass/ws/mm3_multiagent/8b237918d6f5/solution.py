import sys
sys.setrecursionlimit(1 << 25)

def solve() -> None:
    import sys
    input_data = sys.stdin.read().strip().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = [(int(next(it)), int(next(it))) for _ in range(M)]

    class Dinic:
        __slots__ = ("n", "adj", "level", "it")
        def __init__(self, n: int):
            self.n = n
            self.adj = [[] for _ in range(n)]

        def add_edge(self, fr: int, to: int, cap: int) -> None:
            forward = [to, cap, None]   # to, cap, rev_index placeholder
            backward = [fr, 0, None]
            forward[2] = len(self.adj[to])
            backward[2] = len(self.adj[fr])
            self.adj[fr].append(forward)
            self.adj[to].append(backward)

        def bfs(self, s: int, t: int) -> bool:
            self.level = [-1] * self.n
            q = [s]
            self.level[s] = 0
            for v in q:
                for e in self.adj[v]:
                    if e[1] > 0 and self.level[e[0]] < 0:
                        self.level[e[0]] = self.level[v] + 1
                        q.append(e[0])
            return self.level[t] >= 0

        def dfs(self, v: int, t: int, f: int) -> int:
            if v == t:
                return f
            for i in range(self.it[v], len(self.adj[v])):
                e = self.adj[v][i]
                if e[1] > 0 and self.level[v] < self.level[e[0]]:
                    ret = self.dfs(e[0], t, min(f, e[1]))
                    if ret > 0:
                        e[1] -= ret
                        rev = self.adj[e[0]][e[2]]
                        rev[1] += ret
                        return ret
                self.it[v] += 1
            return 0

        def max_flow(self, s: int, t: int) -> int:
            flow = 0
            INF = 10 ** 18
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    f = self.dfs(s, t, INF)
                    if f == 0:
                        break
                    flow += f
            return flow

    # feasibility test for a given distance D
    def min_edges_needed(D: int) -> int:
        if D == 0:
            return 0
        layers = D + 1
        node_id = lambda v, i: (v - 1) * layers + i   # v: 1..N, i:0..D
        total_nodes = N * layers + 1   # +1 for super sink
        sink = total_nodes - 1
        dinic = Dinic(total_nodes)
        src = node_id(1, 0)

        INF = K + 5   # any value > K is sufficient

        # horizontal (free) edges: capacity 1
        # diagonal (selected) edges: capacity INF
        for u, v in edges:
            for i in range(D):
                # free edge
                dinic.add_edge(node_id(u, i), node_id(v, i), 1)
                # selected edge (to next layer)
                dinic.add_edge(node_id(u, i), node_id(v, i + 1), INF)

        # connect sink nodes (N, i) for i < D to super sink
        for i in range(D):
            dinic.add_edge(node_id(N, i), sink, INF)

        return dinic.max_flow(src, sink)

    lo, hi = 0, K
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if min_edges_needed(mid) <= K:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()