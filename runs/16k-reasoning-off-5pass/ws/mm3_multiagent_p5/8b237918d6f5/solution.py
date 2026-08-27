import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    edges = []
    for _ in range(M):
        u = int(input_data[idx]) - 1; idx += 1
        v = int(input_data[idx]) - 1; idx += 1
        edges.append((u, v))
    
    def check(d):
        if d == 0:
            return True
        
        def vid(v, i):
            return 2 + v * (d + 1) + i
        def eid(e):
            return 2 + N * (d + 1) + e
        def did(e):
            return 2 + N * (d + 1) + M + e
        
        total = 2 + N * (d + 1) + 2 * M
        S_node = 0
        T_node = 1
        graph = [[] for _ in range(total)]
        
        def add_edge(u, v, cap):
            graph[u].append([v, cap, len(graph[v])])
            graph[v].append([u, 0, len(graph[u]) - 1])
        
        INF = 10**9
        
        add_edge(S_node, vid(0, 0), INF)
        for i in range(d):
            add_edge(vid(N-1, i), T_node, INF)
        
        for ei, (u, v) in enumerate(edges):
            en = eid(ei)
            dn = did(ei)
            # Horizontal edges (free, always available when edge is unselected)
            for i in range(d + 1):
                add_edge(vid(u, i), en, INF)
                add_edge(en, vid(v, i), INF)
            # Diagonal edges (used when edge is selected): shared bottleneck
            add_edge(en, dn, 1)  # shared capacity-1 bottleneck
            for i in range(d):
                add_edge(vid(u, i), en, INF)
                add_edge(dn, vid(v, i + 1), INF)
        
        # Dinic's max-flow
        def bfs():
            level = [-1] * total
            level[S_node] = 0
            q = deque([S_node])
            while q:
                u = q.popleft()
                for e in graph[u]:
                    if e[1] > 0 and level[e[0]] < 0:
                        level[e[0]] = level[u] + 1
                        q.append(e[0])
            return level
        
        def dfs(u, f, level, it):
            if u == T_node:
                return f
            for i in range(it[u], len(graph[u])):
                it[u] = i
                e = graph[u][i]
                if e[1] > 0 and level[u] + 1 == level[e[0]]:
                    ret = dfs(e[0], min(f, e[1]), level, it)
                    if ret > 0:
                        e[1] -= ret
                        graph[e[0]][e[2]][1] += ret
                        return ret
            return 0
        
        flow = 0
        while True:
            level = bfs()
            if level[T_node] < 0:
                break
            it = [0] * total
            while True:
                pushed = dfs(S_node, INF, level, it)
                if pushed == 0:
                    break
                flow += pushed
        
        return flow <= K
    
    lo, hi = 0, K
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1
    
    print(lo)

solve()