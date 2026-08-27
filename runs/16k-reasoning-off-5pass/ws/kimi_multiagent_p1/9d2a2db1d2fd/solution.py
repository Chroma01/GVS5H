import sys
from array import array

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos+1]); pos += 2
    N = H * W
    F = [0] * N
    for i in range(N):
        F[i] = int(data[pos]); pos += 1

    # Build edges (right and down neighbors), weight = min(F_u, F_v)
    edges = []
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            fu = F[u]
            if j + 1 < W:
                v = u + 1
                fv = F[v]
                edges.append((fu if fu < fv else fv, u, v))
            if i + 1 < H:
                v = u + W
                fv = F[v]
                edges.append((fu if fu < fv else fv, u, v))
    edges.sort(key=lambda e: -e[0])

    # Kruskal reconstruction tree
    # KRT nodes: 0..N-1 are leaves (blocks), N..2N-2 are internal merge nodes
    total = 2 * N - 1
    left = array('i', [0] * total)
    right = array('i', [0] * total)
    weight = [0] * total  # weight of internal nodes

    parent_dsu = list(range(N))
    def find(x):
        while parent_dsu[x] != x:
            parent_dsu[x] = parent_dsu[parent_dsu[x]]
            x = parent_dsu[x]
        return x

    krt_root_of = list(range(N))  # for DSU rep, the KRT node id representing the component
    nxt = N
    for w, u, v in edges:
        ru = find(u); rv = find(v)
        if ru == rv:
            continue
        parent_dsu[ru] = rv
        k = nxt
        nxt += 1
        left[k] = krt_root_of[ru]
        right[k] = krt_root_of[rv]
        weight[k] = w
        krt_root_of[rv] = k
    root = nxt - 1  # last created node; for N == 1 this is node 0 (a leaf)

    # Depth via iterative DFS from root
    depth = array('i', [0] * total)
    LOG = max(1, total.bit_length())
    up = [array('i', [0] * total) for _ in range(LOG)]
    up0 = up[0]
    stack = [root]
    order = [root]
    up0[root] = root
    while stack:
        v = stack.pop()
        if v >= N:  # internal node: has two children
            l = left[v]; r = right[v]
            dv = depth[v] + 1
            depth[l] = dv; up0[l] = v
            depth[r] = dv; up0[r] = v
            stack.append(l); stack.append(r)
            order.append(l); order.append(r)
    # Build lifting table
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for v in order:
            cur[v] = prev[prev[v]]

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            a = up[k][u]; b = up[k][v]
            if a != b:
                u = a; v = b
        return up0[u]

    Q = int(data[pos]); pos += 1
    out = []
    INF = 1 << 30
    for _ in range(Q):
        A = int(data[pos]); B = int(data[pos+1]); Y = int(data[pos+2])
        C = int(data[pos+3]); D = int(data[pos+4]); Z = int(data[pos+5])
        pos += 6
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        if u == v:
            b = INF
        else:
            b = weight[lca(u, v)]
        m = Y if Y > Z else Z
        h = b if b < m else m
        out.append(str(abs(Y - h) + abs(Z - h)))
    sys.stdout.write("\n".join(out) + "\n")

main()