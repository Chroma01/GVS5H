import sys

def solve():
    input = sys.stdin.readline
    H, W = map(int, input().split())
    F = [list(map(int, input().split())) for _ in range(H)]
    N = H * W
    
    # Build edges between adjacent cells with weight = min(height)
    edges = []
    for i in range(H):
        for j in range(W):
            u = i * W + j
            if i + 1 < H:
                v = (i + 1) * W + j
                w = min(F[i][j], F[i + 1][j])
                edges.append((w, u, v))
            if j + 1 < W:
                v = i * W + (j + 1)
                w = min(F[i][j], F[i][j + 1])
                edges.append((w, u, v))
    
    # Sort edges by weight descending for maximum spanning tree
    edges.sort(reverse=True)
    
    # DSU
    parent = list(range(N))
    size = [1] * N
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if size[rx] < size[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        size[rx] += size[ry]
        return True
    
    # Build adjacency list for the maximum spanning tree
    adj = [[] for _ in range(N)]
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))
    
    # Preprocess binary lifting
    LOG = 19  # since N <= 250000, 2^18 = 262144
    up = [[-1] * N for _ in range(LOG)]
    min_edge = [[float('inf')] * N for _ in range(LOG)]
    depth = [0] * N
    
    # Iterative DFS from node 0
    stack = [(0, -1, float('inf'))]  # (node, parent, edge_weight_to_parent)
    visited = [False] * N
    visited[0] = True
    while stack:
        u, p, w = stack.pop()
        up[0][u] = p
        min_edge[0][u] = w
        for v, wt in adj[u]:
            if not visited[v]:
                visited[v] = True
                depth[v] = depth[u] + 1
                stack.append((v, u, wt))
    
    # Compute binary lifting tables
    for k in range(1, LOG):
        for v in range(N):
            if up[k - 1][v] != -1:
                up[k][v] = up[k - 1][up[k - 1][v]]
                min_edge[k][v] = min(min_edge[k - 1][v], min_edge[k - 1][up[k - 1][v]])
    
    def get_min_on_path(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        # Bring u to same depth as v
        diff = depth[u] - depth[v]
        curr_min = float('inf')
        for k in range(LOG):
            if diff & (1 << k):
                curr_min = min(curr_min, min_edge[k][u])
                u = up[k][u]
        if u == v:
            return curr_min
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                curr_min = min(curr_min, min_edge[k][u], min_edge[k][v])
                u = up[k][u]
                v = up[k][v]
        # Now u and v are children of LCA
        curr_min = min(curr_min, min_edge[0][u], min_edge[0][v])
        return curr_min
    
    Q = int(input())
    out_lines = []
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        M = get_min_on_path(u, v)
        if M >= min(Y, Z):
            ans = abs(Y - Z)
        else:
            ans = Y + Z - 2 * M
        out_lines.append(str(ans))
    
    print('\n'.join(out_lines))

solve()