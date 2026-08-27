import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; M = data[p+1]; K = data[p+2]; p += 3

    edges = []
    for _ in range(M):
        u = data[p]; v = data[p+1]; w = data[p+2]; p += 3
        edges.append((w, u, v))

    A = data[p:p+K]; p += K
    B = data[p:p+K]; p += K

    # ---------- Kruskal MST ----------
    parent = list(range(N + 1))
    size = [1] * (N + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    edges.sort()
    adj = [[] for _ in range(N + 1)]
    cnt = 0
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))
            cnt += 1
            if cnt == N - 1:
                break

    # ---------- Binary lifting on MST ----------
    LOG = max(1, (N).bit_length())
    up = [[0] * (N + 1) for _ in range(LOG)]
    mx = [[0] * (N + 1) for _ in range(LOG)]
    depth = [0] * (N + 1)
    visited = [False] * (N + 1)

    # iterative DFS from vertex 1 (graph connected => MST spans all)
    stack = [(1, 0, 0, 0)]  # node, parent, edge weight, depth
    visited[1] = True
    order = [(1, 0, 0)]
    while stack:
        node, par, w, d = stack.pop()
        depth[node] = d
        up[0][node] = par
        mx[0][node] = w
        for nb, w2 in adj[node]:
            if nb != par and not visited[nb]:
                visited[nb] = True
                stack.append((nb, node, w2, d + 1))

    for k in range(1, LOG):
        upk = up[k]; upk1 = up[k - 1]
        mxk = mx[k]; mxk1 = mx[k - 1]
        for v in range(1, N + 1):
            a = upk1[v]
            upk[v] = upk1[a]
            m = mxk1[v]
            m2 = mxk1[a]
            mxk[v] = m if m > m2 else m2

    def query(u, v):
        # max edge weight on path u-v in MST
        res = 0
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                if mx[bit][u] > res:
                    res = mx[bit][u]
                u = up[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return res
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                if mx[k][u] > res:
                    res = mx[k][u]
                if mx[k][v] > res:
                    res = mx[k][v]
                u = up[k][u]
                v = up[k][v]
        if mx[0][u] > res:
            res = mx[0][u]
        if mx[0][v] > res:
            res = mx[0][v]
        return res

    # ---------- Cost matrix ----------
    cost = [[0] * K for _ in range(K)]
    for i in range(K):
        ai = A[i]
        row = cost[i]
        for j in range(K):
            row[j] = query(ai, B[j])

    # ---------- Hungarian (min cost, K x K) ----------
    n = K
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    pway = [0] * (n + 1)
    way = [0] * (n + 1)
    INF = float('inf')
    for i in range(1, n + 1):
        pway[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        ci = cost[i - 1]
        while True:
            used[j0] = True
            i0 = pway[j0]
            delta = INF
            j1 = 0
            ci0 = cost[i0 - 1]
            ui0 = u[i0]
            for j in range(1, n + 1):
                if not used[j]:
                    cur = ci0[j - 1] - ui0 - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[pway[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if pway[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            pway[j0] = pway[j1]
            j0 = j1

    ans = -v[0]
    sys.stdout.write(str(ans) + "\n")

main()