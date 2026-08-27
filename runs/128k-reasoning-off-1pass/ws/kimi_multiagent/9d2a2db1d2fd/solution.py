import sys
from array import array

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    H = data[p]; W = data[p+1]; p += 2
    N = H * W
    F = data[p:p+N]; p += N

    # Build edges (right and down), weight = min(F_u, F_v)
    E = 2 * N - H - W
    eu = array('i', [0]) * E
    ev = array('i', [0]) * E
    ew = array('i', [0]) * E
    e = 0
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            fu = F[u]
            if j + 1 < W:
                v = u + 1
                fv = F[v]
                eu[e] = u; ev[e] = v
                ew[e] = fu if fu < fv else fv
                e += 1
            if i + 1 < H:
                v = u + W
                fv = F[v]
                eu[e] = u; ev[e] = v
                ew[e] = fu if fu < fv else fv
                e += 1

    # Sort edges descending by weight
    order = sorted(range(E), key=lambda k: -ew[k])

    # DSU
    parent = list(range(N))
    size = [1] * N
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    # Maximum spanning tree adjacency (packed: nbr * (1<<20) + w)
    adj = [[] for _ in range(N)]
    PACK = 1 << 20
    for k in order:
        u = eu[k]; v = ev[k]
        ru = find(u); rv = find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
            w = ew[k]
            adj[u].append(v * PACK + w)
            adj[v].append(u * PACK + w)

    # Root tree at 0, iterative DFS for depth, parent, min-edge-to-parent
    LOG = max(1, (N - 1).bit_length())
    depth = array('i', [0]) * N
    up0 = array('i', [0]) * N
    mn0 = array('i', [0]) * N
    visited = bytearray(N)
    stack = [0]
    visited[0] = 1
    up0[0] = 0
    mn0[0] = 1 << 30
    while stack:
        u = stack.pop()
        du = depth[u]
        for packed in adj[u]:
            v = packed // PACK
            if not visited[v]:
                visited[v] = 1
                w = packed - v * PACK
                up0[v] = u
                mn0[v] = w
                depth[v] = du + 1
                stack.append(v)

    # Binary lifting tables
    up = [up0]
    mn = [mn0]
    for k in range(1, LOG):
        prev_up = up[k-1]
        prev_mn = mn[k-1]
        cur_up = array('i', [0]) * N
        cur_mn = array('i', [0]) * N
        for v in range(N):
            a = prev_up[v]
            cur_up[v] = prev_up[a]
            m1 = prev_mn[v]
            m2 = prev_mn[a]
            cur_mn[v] = m1 if m1 < m2 else m2
        up.append(cur_up)
        mn.append(cur_mn)

    Q = data[p]; p += 1
    out = []
    INF = 1 << 30
    for _ in range(Q):
        A = data[p]; B = data[p+1]; Y = data[p+2]
        C = data[p+3]; D = data[p+4]; Z = data[p+5]
        p += 6
        s = (A - 1) * W + (B - 1)
        t = (C - 1) * W + (D - 1)
        if s == t:
            out.append(str(abs(Y - Z)))
            continue
        # Bottleneck (min edge weight) on tree path s-t
        u = s; v = t
        best = INF
        du = depth[u]; dv = depth[v]
        if du < dv:
            u, v = v, u
            du, dv = dv, du
        diff = du - dv
        k = 0
        while diff:
            if diff & 1:
                m = mn[k][u]
                if m < best:
                    best = m
                u = up[k][u]
            diff >>= 1
            k += 1
        if u != v:
            for k in range(LOG - 1, -1, -1):
                if up[k][u] != up[k][v]:
                    m = mn[k][u]
                    if m < best:
                        best = m
                    m = mn[k][v]
                    if m < best:
                        best = m
                    u = up[k][u]
                    v = up[k][v]
            m = mn[0][u]
            if m < best:
                best = m
            m = mn[0][v]
            if m < best:
                best = m
        T = best
        mnYZ = Y if Y < Z else Z
        if T >= mnYZ:
            out.append(str(abs(Y - Z)))
        else:
            out.append(str(Y + Z - 2 * T))

    sys.stdout.write('\n'.join(out) + '\n')

main()