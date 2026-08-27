import sys
from collections import deque

def solve():
    MOD = 998244353
    N, M = map(int, sys.stdin.readline().split())
    A = list(map(int, sys.stdin.readline().split()))
    A = [a - 1 for a in A]
    
    # Build graph
    adj = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]
    for i in range(N):
        adj[i].append(A[i])
        radj[A[i]].append(i)
    
    # Kosaraju to find SCCs
    sys.setrecursionlimit(10000)
    visited = [False] * N
    order = []
    
    def dfs1(v):
        visited[v] = True
        for u in adj[v]:
            if not visited[u]:
                dfs1(u)
        order.append(v)
    
    for i in range(N):
        if not visited[i]:
            dfs1(i)
    
    comp = [-1] * N
    
    def dfs2(v, c):
        comp[v] = c
        for u in radj[v]:
            if comp[u] == -1:
                dfs2(u, c)
    
    c = 0
    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, c)
            c += 1
    
    C = c  # number of components
    
    # Build contracted DAG
    # rev[v] = list of u such that u -> v (children of v)
    rev = [[] for _ in range(C)]
    in_degree = [0] * C
    out_degree = [0] * C
    edge_set = set()
    for i in range(N):
        u = comp[i]
        v = comp[A[i]]
        if u != v:
            if (u, v) not in edge_set:
                edge_set.add((u, v))
                rev[v].append(u)  # u is a child of v (u -> v)
                in_degree[v] += 1
                out_degree[u] += 1
    
    # Topological sort using Kahn's algorithm
    # We need forward edges to traverse. Build forward adjacency.
    forward = [[] for _ in range(C)]
    for u, v in edge_set:
        forward[u].append(v)
    
    q = deque()
    for i in range(C):
        if in_degree[i] == 0:
            q.append(i)
    
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in forward[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
    
    # DP: f[v][t] = number of ways to assign values to v and its descendants (in the reverse tree sense) such that x_v = t+1
    # Actually, t from 0 to M-1 representing values 1..M
    f = [[1] * M for _ in range(C)]
    
    for u in topo:
        # Initialize f[u] as 1s
        # Multiply by prefix sums of each child
        for c in rev[u]:
            # Compute prefix sums of f[c] and multiply to f[u]
            running = 0
            for t in range(M):
                running = (running + f[c][t]) % MOD
                f[u][t] = f[u][t] * running % MOD
    
    # Find roots (out_degree == 0) and compute answer
    ans = 1
    for i in range(C):
        if out_degree[i] == 0:
            total = sum(f[i]) % MOD
            ans = ans * total % MOD
    
    print(ans)

if __name__ == "__main__":
    solve()