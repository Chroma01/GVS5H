import sys
sys.setrecursionlimit(1 << 25)

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = H * W
    F = [0] * N
    for i in range(H):
        for j in range(W):
            F[i * W + j] = int(next(it))
    # Build edges
    edges = []
    # directions: right and down
    for i in range(H):
        for j in range(W):
            u = i * W + j
            if j + 1 < W:
                v = i * W + (j + 1)
                w = min(F[u], F[v])
                edges.append((w, u, v))
            if i + 1 < H:
                v = (i + 1) * W + j
                w = min(F[u], F[v])
                edges.append((w, u, v))
    # Sort edges descending
    edges.sort(reverse=True, key=lambda x: x[0])
    # DSU
    parent = list(range(N))
    size = [1] * N
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return False
        if size[x] < size[y]:
            x, y = y, x
        parent[y] = x
        size[x] += size[y]
        return True
    # Build tree
    tree = [[] for _ in range(N)]
    for w, u, v in edges:
        if union(u, v):
            tree[u].append((v, w))
            tree[v].append((u, w))
    # LCA preprocessing
    LOG = (N).bit_length()
    up = [[-1] * N for _ in range(LOG)]
    minw = [[10**9] * N for _ in range(LOG)]
    depth = [0] * N
    # BFS/DFS from root 0
    stack = [0]
    up[0][0] = 0
    minw[0][0] = 10**9
    parent[0] = -1  # mark root
    # iterative DFS
    order = [0]
    parent[0] = 0
    visited = [False] * N
    visited[0] = True
    while stack:
        u = stack.pop()
        for v, w in tree[u]:
            if not visited[v]:
                visited[v] = True
                depth[v] = depth[u] + 1
                up[0][v] = u
                minw[0][v] = w
                stack.append(v)
                order.append(v)
    for k in range(1, LOG):
        for v in range(N):
            up[k][v] = up[k-1][ up[k-1][v] ]
            minw[k][v] = min(minw[k-1][v], minw[k-1][ up[k-1][v] ])
    def get_min(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        res = 10**9
        # lift u up
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                res = min(res, minw[k][u])
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return res
        for k in range(LOG-1, -1, -1):
            if up[k][u] != up[k][v]:
                res = min(res, minw[k][u], minw[k][v])
                u = up[k][u]
                v = up[k][v]
        # now u and v are children of LCA
        res = min(res, minw[0][u], minw[0][v])
        return res
    Q = int(next(it))
    out = []
    for _ in range(Q):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        Y = int(next(it))
        c = int(next(it)) - 1
        d = int(next(it)) - 1
        Z = int(next(it))
        u = a * W + b
        v = c * W + d
        m = get_min(u, v)
        if m >= min(Y, Z):
            ans = abs(Y - Z)
        else:
            ans = Y + Z - 2 * m
        out.append(str(ans))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()