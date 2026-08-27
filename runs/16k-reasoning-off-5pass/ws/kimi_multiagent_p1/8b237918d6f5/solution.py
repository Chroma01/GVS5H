import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    edges = []
    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        edges.append((u, v))

    INF = 10**9

    class Dinic:
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]  # list of [to, cap, rev_index]

        def add_edge(self, fr, to, cap):
            self.g[fr].append([to, cap, len(self.g[to])])
            self.g[to].append([fr, 0, len(self.g[fr]) - 1])

        def bfs(self, s, t):
            self.level = [-1] * self.n
            q = deque([s])
            self.level[s] = 0
            while q:
                v = q.popleft()
                for to, cap, _ in self.g[v]:
                    if cap > 0 and self.level[to] < 0:
                        self.level[to] = self.level[v] + 1
                        q.append(to)
            return self.level[t] >= 0

        def dfs(self, v, t, f):
            if v == t:
                return f
            for i in range(self.it[v], len(self.g[v])):
                self.it[v] = i
                to, cap, rev = self.g[v][i]
                if cap > 0 and self.level[v] < self.level[to]:
                    d = self.dfs(to, t, min(f, cap))
                    if d > 0:
                        self.g[v][i][1] -= d
                        self.g[to][rev][1] += d
                        return d
            return 0

        def max_flow(self, s, t):
            flow = 0
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    f = self.dfs(s, t, INF)
                    if f == 0:
                        break
                    flow += f
            return flow

    def feasible(D):
        # Can we select <= K edges so that every 1->N path uses >= D selected edges?
        if D == 0:
            return True
        # Layered graph: node (v, d) for d in 0..D-1 (layer d = reached with d selected edges).
        # For each edge e=(u,v):
        #   - unselected traversal: (u,d) -> w_e_in -> w_e_out -> (v,d), with w_e_in->w_e_out capacity 1
        #     (cutting this capacity-1 arc = selecting edge e, removes same-layer traversal at ALL layers)
        #   - selected traversal: (u,d) -> (v,d+1) with INF capacity (always available).
        # Source = (1,0). Sinks = (N,d) for d < D merged into super-sink T.
        # Min cut = min number of edges to select to disconnect; feasible iff min cut <= K.
        layers = D  # layers 0..D-1 matter as source side; layer D is "safe"
        def node_id(v, d):
            return d * N + v
        num_layer_nodes = layers * N
        # gadget nodes: 2 per edge
        win_base = num_layer_nodes
        wout_base = num_layer_nodes + M
        S = num_layer_nodes + 2 * M
        T = S + 1
        din = Dinic(T + 1)

        src = node_id(0, 0)
        din.add_edge(S, src, INF)
        for d in range(D):
            din.add_edge(node_id(N - 1, d), T, INF)

        for ei, (u, v) in enumerate(edges):
            win = win_base + ei
            wout = wout_base + ei
            din.add_edge(win, wout, 1)  # cost 1 to "select" this edge
            for d in range(D):
                a = node_id(u, d)
                # unselected traversal (u,d) -> (v,d) through gadget
                din.add_edge(a, win, INF)
                din.add_edge(wout, node_id(v, d), INF)
                # selected traversal (u,d) -> (v,d+1); if d+1 == D it's safe (sink side only for d<D)
                if d + 1 < D:
                    din.add_edge(a, node_id(v, d + 1), INF)
                else:
                    # reaching layer D means distance >= D achieved along this path; no need to track
                    pass

        return din.max_flow(S, T) <= K

    lo, hi = 0, min(K, N - 1)
    # find max D in [lo, hi] that is feasible
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)

solve()