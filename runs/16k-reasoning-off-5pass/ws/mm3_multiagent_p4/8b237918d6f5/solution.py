import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx+=1
    M = int(input_data[idx]); idx+=1
    K = int(input_data[idx]); idx+=1
    edges = []
    for _ in range(M):
        u = int(input_data[idx]); idx+=1
        v = int(input_data[idx]); idx+=1
        edges.append((u-1, v-1))
    
    # Compute shortest path length from 1 to N (BFS on directed)
    INF = 10**9
    dist = [INF]*N
    dist[0] = 0
    dq = deque([0])
    while dq:
        u = dq.popleft()
        for (a,b) in edges:
            if a == u and dist[b] == INF:
                dist[b] = dist[u]+1
                dq.append(b)
    shortest = dist[N-1]
    
    # Binary search D
    lo, hi = 0, min(K, shortest)
    # Build edges list for fast access
    # For feasibility of D: max flow from (1,0) to (N-1, D) in H
    # H has (D+1)*N vertices
    # Source = 0*... = 0, Sink = (N-1)*(D+1) + D
    
    def feasible(D):
        if D == 0:
            return True
        # Build H and compute max flow (Dinic)
        # Vertices: (v, i) = v*(D+1) + i
        def vid(v, i): return v*(D+1) + i
        nV = N*(D+1)
        s = vid(0, 0)
        t = vid(N-1, D)
        # Adjacency list for Dinic
        g = [[] for _ in range(nV)]
        def add_edge(u, v, cap):
            g[u].append([v, cap, len(g[v])])
            g[v].append([u, 0, len(g[u])-1])
        
        for (u, v) in edges:
            # Advance edges (u,i)->(v,i+1), cap 1
            for i in range(D):
                add_edge(vid(u,i), vid(v,i+1), 1)
            # Stay edges (u,i)->(v,i), cap INF
            for i in range(D+1):
                add_edge(vid(u,i), vid(v,i), INF)
        
        # Dinic
        def bfs():
            level = [-1]*nV
            level[s] = 0
            q = deque([s])
            while q:
                u = q.popleft()
                for (v, cap, rev) in g[u]:
                    if cap > 0 and level[v] == -1:
                        level[v] = level[u]+1
                        q.append(v)
            return level
        
        def dfs(u, f, level, it):
            if u == t:
                return f
            for i in range(it[u], len(g[u])):
                it[u] = i
                v, cap, rev = g[u][i]
                if cap > 0 and level[v] == level[u]+1:
                    ret = dfs(v, min(f, cap), level, it)
                    if ret > 0:
                        g[u][i][1] -= ret
                        g[v][rev][1] += ret
                        return ret
            return 0
        
        flow = 0
        while True:
            level = bfs()
            if level[t] == -1:
                break
            it = [0]*nV
            while True:
                pushed = dfs(s, INF, level, it)
                if pushed == 0:
                    break
                flow += pushed
        return flow <= K
    
    while lo < hi:
        mid = (lo+hi+1)//2
        if feasible(mid):
            lo = mid
        else:
            hi = mid-1
    print(lo)

solve()