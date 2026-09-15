import sys
from collections import deque

def main():
    sys.setrecursionlimit(10000)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it)); M = int(next(it)); K = int(next(it))
    edges = []
    for _ in range(M):
        u = int(next(it)); v = int(next(it))
        edges.append((u, v))

    INF = 1 << 30

    def feasible(L):
        # Is min number of edges to select (so every 1->N path has >= L of them) <= K ?
        if L <= 0:
            return True
        num = N * L
        S = num
        T = num + 1
        n = num + 2
        graph = [[] for _ in range(n)]

        def add(fr, to, cap):
            graph[fr].append([to, cap, len(graph[to])])
            graph[to].append([fr, 0, len(graph[fr]) - 1])

        def aid(v, t):        # v in 1..N, t in 1..L
            return (v - 1) * L + (t - 1)

        # Node A(v,t) on source side <=> d(v) >= t.
        # Monotonicity: d(v)>=t implies d(v)>=t-1
        for v in range(1, N + 1):
            base = (v - 1) * L
            for t in range(2, L + 1):
                add(base + t - 1, base + t - 2, INF)
        # d(1) = 0  -> A(1,t) forced to sink side
        for t in range(1, L + 1):
            add(aid(1, t), T, INF)
        # d(N) = L  -> A(N,t) forced to source side
        for t in range(1, L + 1):
            add(S, aid(N, t), INF)
        # Original edges u->v
        for (u, v) in edges:
            bu = (u - 1) * L
            bv = (v - 1) * L
            # cost: A(v,t) source and A(u,t) sink  => tight edge (d(v)=d(u)+1)
            for t in range(1, L + 1):
                add(bv + t - 1, bu + t - 1, 1)
            # constraint d(v) <= d(u)+1 : A(v,t) source => A(u,t-1) source
            for t in range(2, L + 1):
                add(bv + t - 1, bu + t - 2, INF)

        level = [-1] * n
        it_arr = [0] * n

        def bfs():
            for i in range(n):
                level[i] = -1
            level[S] = 0
            q = deque([S])
            while q:
                x = q.popleft()
                for to, cap, rev in graph[x]:
                    if cap > 0 and level[to] < 0:
                        level[to] = level[x] + 1
                        q.append(to)
            return level[T] >= 0

        def dfs(x, f):
            if x == T:
                return f
            while it_arr[x] < len(graph[x]):
                e = graph[x][it_arr[x]]
                to, cap, rev = e
                if cap > 0 and level[x] < level[to]:
                    d = dfs(to, f if f < cap else cap)
                    if d > 0:
                        e[1] -= d
                        graph[to][rev][1] += d
                        return d
                it_arr[x] += 1
            return 0

        flow = 0
        while bfs():
            for i in range(n):
                it_arr[i] = 0
            while True:
                f = dfs(S, INF)
                if f == 0:
                    break
                flow += f
                if flow > K:
                    break
            if flow > K:
                break
        return flow <= K

    ans = 0
    for L in range(N - 1, 0, -1):
        if feasible(L):
            ans = L
            break
    print(ans)

main()