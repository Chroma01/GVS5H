import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); pos += 1
    W = int(data[pos]); pos += 1
    N = H * W
    F = [0] * N
    for i in range(N):
        F[i] = int(data[pos]); pos += 1

    # Build edges: weight = min(F_u, F_v)
    edges = []
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            fu = F[u]
            if j + 1 < W:
                v = u + 1
                fv = F[v]
                w = fu if fu < fv else fv
                edges.append((w, u, v))
            if i + 1 < H:
                v = u + W
                fv = F[v]
                w = fu if fu < fv else fv
                edges.append((w, u, v))

    # Kruskal: sort descending by weight -> maximum spanning tree
    edges.sort(key=lambda e: -e[0])

    parent = list(range(N))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    adj = [[] for _ in range(N)]
    cnt = 0
    for w, u, v in edges:
        ru = find(u); rv = find(v)
        if ru != rv:
            parent[ru] = rv
            adj[u].append((v, w))
            adj[v].append((u, w))
            cnt += 1
            if cnt == N - 1:
                break

    LOG = max(1, N.bit_length())
    INF = 1 << 62  # large integer infinity (weights <= 1e6)

    up = [[0] * N for _ in range(LOG)]
    mn = [[0] * N for _ in range(LOG)]
    depth = [0] * N

    # Iterative DFS from node 0 (grid is connected, so tree spans all nodes)
    visited = [False] * N
    stack = [0]
    visited[0] = True
    up[0][0] = 0
    mn[0][0] = INF
    while stack:
        u = stack.pop()
        for v, w in adj[u]:
            if not visited[v]:
                visited[v] = True
                depth[v] = depth[u] + 1
                up[0][v] = u
                mn[0][v] = w
                stack.append(v)

    for k in range(1, LOG):
        upk = up[k]; upk1 = up[k - 1]
        mnk = mn[k]; mnk1 = mn[k - 1]
        for v in range(N):
            a = upk1[v]
            upk[v] = upk1[a]
            m1 = mnk1[v]
            m2 = mnk1[a]
            mnk[v] = m1 if m1 < m2 else m2

    def path_min(u, v):
        if u == v:
            return INF
        res = INF
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                if mn[k][u] < res:
                    res = mn[k][u]
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return res
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                if mn[k][u] < res:
                    res = mn[k][u]
                if mn[k][v] < res:
                    res = mn[k][v]
                u = up[k][u]
                v = up[k][v]
        if mn[0][u] < res:
            res = mn[0][u]
        if mn[0][v] < res:
            res = mn[0][v]
        return res

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        A = int(data[pos]) - 1; B = int(data[pos + 1]) - 1
        Y = int(data[pos + 2])
        C = int(data[pos + 3]) - 1; D = int(data[pos + 4]) - 1
        Z = int(data[pos + 5])
        pos += 6
        u = A * W + B
        v = C * W + D
        M = path_min(u, v)
        yz = Y - Z
        if yz < 0:
            yz = -yz
        m = Y if Y < Z else Z
        extra = m - M
        if extra < 0:
            extra = 0
        out.append(str(yz + 2 * extra))
    sys.stdout.write('\n'.join(out) + '\n')

main()