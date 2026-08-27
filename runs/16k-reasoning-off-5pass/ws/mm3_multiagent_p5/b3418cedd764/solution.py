import sys
sys.setrecursionlimit(10000)

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    
    # Build graph and reverse graph for Kosaraju
    graph = [[] for _ in range(N + 1)]
    rev_graph = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        graph[i].append(A[i])
        rev_graph[A[i]].append(i)
    
    # Kosaraju's algorithm to find SCCs
    visited = [False] * (N + 1)
    stack = []
    def dfs1(v):
        visited[v] = True
        for w in graph[v]:
            if not visited[w]:
                dfs1(w)
        stack.append(v)
    for i in range(1, N + 1):
        if not visited[i]:
            dfs1(i)
    
    visited = [False] * (N + 1)
    comp = [0] * (N + 1)
    comp_id = 0
    def dfs2(v):
        visited[v] = True
        comp[v] = comp_id
        for w in rev_graph[v]:
            if not visited[w]:
                dfs2(w)
    while stack:
        v = stack.pop()
        if not visited[v]:
            dfs2(v)
            comp_id += 1
    C = comp_id
    
    # Build DAG: contract SCCs, deduplicate edges
    out_adj = [[] for _ in range(C)]
    in_adj = [[] for _ in range(C)]
    edges = set()
    for i in range(1, N + 1):
        u = comp[i]
        v = comp[A[i]]
        if u != v:
            edges.add((u, v))
    for u, v in edges:
        out_adj[u].append(v)
        in_adj[v].append(u)
    
    out_degree = [len(out_adj[u]) for u in range(C)]
    sinks = [u for u in range(C) if out_degree[u] == 0]
    
    # DP on trees rooted at sinks
    dp = [None] * C
    prefix = [None] * C
    
    def dfs_dp(v):
        if dp[v] is not None:
            return
        dp[v] = [0] * (M + 1)
        # Process children first
        for u in in_adj[v]:
            dfs_dp(u)
        # Compute dp[v][k]
        for k in range(1, M + 1):
            ways = 1
            for u in in_adj[v]:
                ways = ways * prefix[u][k] % MOD
            dp[v][k] = ways
        # Compute prefix[v]
        prefix[v] = [0] * (M + 1)
        for k in range(1, M + 1):
            prefix[v][k] = (prefix[v][k - 1] + dp[v][k]) % MOD
    
    ans = 1
    for sink in sinks:
        dfs_dp(sink)
        total = sum(dp[sink][1:]) % MOD
        ans = ans * total % MOD
    
    print(ans)

if __name__ == "__main__":
    main()