import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input = sys.stdin.readline
    N, M, K = map(int, input().split())
    edges = []
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges.append((w, u-1, v-1))
    A = list(map(int, input().split()))
    B = list(map(int, input().split())
    A = [x-1 for x in A]
    B = [x-1 for x in B]

    # Build Kruskal reconstruction tree for Monge-compatible ordering
    edges_sorted = sorted(edges)
    dsu = list(range(N))
    def find_dsu(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    rec_adj = [[] for _ in range(2*N)]
    rec_weight = [0] * (2*N)
    comp = list(range(N))
    next_id = N

    for w, u, v in edges_sorted:
        ru = find_dsu(u)
        rv = find_dsu(v)
        if ru == rv:
            continue
        rec_weight[next_id] = w
        rec_adj[next_id].append(comp[ru])
        rec_adj[next_id].append(comp[rv])
        dsu[ru] = rv
        comp[rv] = next_id
        next_id += 1

    root = comp[find_dsu(0)]

    # Postorder traversal with children sorted by weight descending
    order = []
    def dfs(node):
        if node < N:
            order.append(node)
            return
        children = rec_adj[node]
        children.sort(key=lambda x: rec_weight[x], reverse=True)
        for child in children:
            dfs(child)
    dfs(root)

    rank = [0]*N
    for i, v in enumerate(order):
        rank[v] = i

    A_sorted = sorted(A, key=lambda x: rank[x])
    B_sorted = sorted(B, key=lambda x: rank[x])

    # Build MST for f(x,y) queries
    dsu2 = list(range(N))
    def find2(x):
        while dsu2[x] != x:
            dsu2[x] = dsu2[dsu2[x]]
            x = dsu2[x]
        return x
    def union2(x, y):
        px, py = find2(x), find2(y)
        if px == py: return False
        dsu2[px] = py
        return True

    mst_adj = [[] for _ in range(N)]
    for w, u, v in edges_sorted:
        if union2(u, v):
            mst_adj[u].append((v, w))
            mst_adj[v].append((u, w))

    # LCA preprocessing with max edge weight
    LOG = 18
    up = [[-1]*N for _ in range(LOG)]
    maxw = [[0]*N for _ in range(LOG)]
    depth = [0]*N

    def dfs_lca(u, p, d):
        depth[u] = d
        up[0][u] = p if p != -1 else u
        for v, w in mst_adj[u]:
            if v == p: continue
            dfs_lca(v, u, d+1)
            up[0][v] = u
            maxw[0][v] = w
    dfs_lca(0, -1, 0)

    for k in range(1, LOG):
        for v in range(N):
            up[k][v] = up[k-1][up[k-1][v]]
            maxw[k][v] = max(maxw[k-1][v], maxw[k-1][up[k-1][v]])

    def get_max(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        cur_max = 0
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if diff & (1 << k):
                cur_max = max(cur_max, maxw[k][u])
                u = up[k][u]
        if u == v:
            return cur_max
        for k in range(LOG-1, -1, -1):
            if up[k][u] != up[k][v]:
                cur_max = max(cur_max, maxw[k][u], maxw[k][v])
                u = up[k][u]
                v = up[k][v]
        cur_max = max(cur_max, maxw[0][u], maxw[0][v])
        return cur_max

    ans = 0
    for a, b in zip(A_sorted, B_sorted):
        ans += get_max(a, b)

    print(ans)

solve()