import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input = sys.stdin.readline
    H, W = map(int, input().split())
    F = []
    for _ in range(H):
        F.append(list(map(int, input().split())))
    N = H * W
    # Flatten heights
    height = [0] * N
    cells = []
    for i in range(H):
        for j in range(W):
            idx = i * W + j
            h = F[i][j]
            height[idx] = h
            cells.append((h, idx))
    cells.sort(reverse=True)  # sort by height descending

    # Union-Find
    parent_uf = list(range(N))
    size = [1] * N
    def find(x):
        while parent_uf[x] != x:
            parent_uf[x] = parent_uf[parent_uf[x]]
            x = parent_uf[x]
        return x
    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return
        if size[x] < size[y]:
            x, y = y, x
        parent_uf[y] = x
        size[x] += size[y]

    # Build tree
    tree_parent = [-1] * N
    edge_weight = [10**9] * N
    active = [False] * N

    for h, u in cells:
        active[u] = True
        i, j = divmod(u, W)
        # Check 4 neighbors
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < H and 0 <= nj < W:
                v = ni * W + nj
                if active[v]:
                    ru = find(u)
                    rv = find(v)
                    if ru != rv:
                        if tree_parent[u] == -1:
                            tree_parent[u] = rv
                            edge_weight[u] = h
                            union(u, rv)
                        else:
                            tree_parent[rv] = ru
                            edge_weight[rv] = h
                            union(rv, ru)

    # Build children adjacency list
    children = [[] for _ in range(N)]
    for u in range(N):
        if tree_parent[u] != -1:
            children[tree_parent[u]].append(u)

    # LCA preprocessing
    LOG = 19
    up = [[-1] * LOG for _ in range(N)]
    min_w = [[10**9] * LOG for _ in range(N)]
    depth = [0] * N

    def dfs(u, d):
        depth[u] = d
        if tree_parent[u] == -1:
            up[u][0] = u
            min_w[u][0] = 10**9
        else:
            up[u][0] = tree_parent[u]
            min_w[u][0] = edge_weight[u]
        for k in range(1, LOG):
            up[u][k] = up[up[u][k-1]][k-1]
            min_w[u][k] = min(min_w[u][k-1], min_w[up[u][k-1]][k-1])
        for v in children[u]:
            dfs(v, d+1)

    for u in range(N):
        if tree_parent[u] == -1:
            dfs(u, 0)

    def get_min(u, v):
        if u == v:
            return height[u]
        min_val = 10**9
        if depth[u] < depth[v]:
            u, v = v, u
        # Lift u
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if diff & (1 << k):
                min_val = min(min_val, min_w[u][k])
                u = up[u][k]
        if u == v:
            return min_val
        for k in range(LOG-1, -1, -1):
            if up[u][k] != up[v][k]:
                min_val = min(min_val, min_w[u][k], min_w[v][k])
                u = up[u][k]
                v = up[v][k]
        # u and v are children of LCA
        min_val = min(min_val, min_w[u][0], min_w[v][0])
        return min_val

    Q = int(input())
    out = []
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        u = (A-1) * W + (B-1)
        v = (C-1) * W + (D-1)
        m = get_min(u, v)
        ans = abs(Y - Z) + 2 * max(0, min(Y, Z) - m)
        out.append(str(ans))
    print('\n'.join(out))

solve()