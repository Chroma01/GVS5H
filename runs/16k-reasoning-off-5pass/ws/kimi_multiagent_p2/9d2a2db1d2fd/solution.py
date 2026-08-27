import sys
from array import array

def main():
    data = sys.stdin.buffer.read()
    n = len(data)
    pos = 0

    def read_int():
        nonlocal pos
        while pos < n and data[pos] <= 32:
            pos += 1
        num = 0
        while pos < n and data[pos] > 32:
            num = num * 10 + data[pos] - 48
            pos += 1
        return num

    H = read_int()
    W = read_int()
    N = H * W
    F = [read_int() for _ in range(N)]

    # Build grid edges (right and down), weight = min(F_u, F_v)
    edges = []
    ea = edges.append
    for i in range(H):
        base = i * W
        for j in range(W):
            u = base + j
            fu = F[u]
            if j + 1 < W:
                v = u + 1
                w = fu if fu < F[v] else F[v]
                ea((w, u, v))
            if i + 1 < H:
                v = u + W
                w = fu if fu < F[v] else F[v]
                ea((w, u, v))

    # Kruskal: maximum spanning tree (sort descending by weight)
    edges.sort(key=lambda e: -e[0])

    parent = list(range(N))
    size = [1] * N

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    # Tree edges stored for CSR build
    tu = array('i')
    tv = array('i')
    tw = array('i')

    cnt = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
            tu.append(u)
            tv.append(v)
            tw.append(w)
            cnt += 1
            if cnt == N - 1:
                break
    del edges

    # CSR adjacency for the tree
    M = N - 1
    deg = array('i', bytes(4 * N))
    for k in range(M):
        deg[tu[k]] += 1
        deg[tv[k]] += 1
    start = array('i', bytes(4 * (N + 1)))
    s = 0
    for v in range(N):
        start[v] = s
        s += deg[v]
    start[N] = s
    to = array('i', bytes(4 * s))
    wt = array('i', bytes(4 * s))
    fill = array('i', start[:-1])
    for k in range(M):
        u = tu[k]
        v = tv[k]
        w = tw[k]
        p = fill[u]
        to[p] = v
        wt[p] = w
        fill[u] = p + 1
        p = fill[v]
        to[p] = u
        wt[p] = w
        fill[v] = p + 1
    del tu, tv, tw, deg, fill

    # Iterative DFS from root 0: depth, immediate parent, min edge to parent
    LOG = max(1, (N - 1).bit_length())
    MASK = (1 << 20) - 1
    INF = MASK  # larger than any weight (weights <= 1e6 < 2^20-1)

    depth = array('i', bytes(4 * N))
    P0 = array('q', bytes(8 * N))  # packed: (parent << 20) | minedge
    visited = bytearray(N)
    visited[0] = 1
    P0[0] = (0 << 20) | INF
    stack = [0]
    while stack:
        u = stack.pop()
        du = depth[u]
        su = start[u]
        su1 = start[u + 1]
        for p in range(su, su1):
            v = to[p]
            if not visited[v]:
                visited[v] = 1
                depth[v] = du + 1
                P0[v] = (u << 20) | wt[p]
                stack.append(v)

    # Binary lifting tables, packed
    P = [P0]
    for k in range(1, LOG):
        prev = P[k - 1]
        cur = array('q', bytes(8 * N))
        for v in range(N):
            c = prev[v]
            mid = c >> 20
            w1 = c & MASK
            c2 = prev[mid]
            w2 = c2 & MASK
            if w2 < w1:
                w1 = w2
            cur[v] = ((c2 >> 20) << 20) | w1
        P.append(cur)

    # Read queries and answer
    Q = read_int()
    out = []
    oa = out.append
    Pr = P
    LOGr = range(LOG - 1, -1, -1)
    for _ in range(Q):
        a = read_int(); b = read_int(); y = read_int()
        c = read_int(); d = read_int(); z = read_int()
        s = (a - 1) * W + (b - 1)
        t = (c - 1) * W + (d - 1)
        diff0 = y - z
        if diff0 < 0:
            diff0 = -diff0
        if s == t:
            oa(str(diff0))
            continue
        u = s
        v = t
        du = depth[u]
        dv = depth[v]
        res = INF
        if du < dv:
            u, v = v, u
            du, dv = dv, du
        diff = du - dv
        k = 0
        while diff:
            if diff & 1:
                code = Pr[k][u]
                w = code & MASK
                if w < res:
                    res = w
                u = code >> 20
            diff >>= 1
            k += 1
        if u != v:
            for k in LOGr:
                Pk = Pr[k]
                cu = Pk[u]
                cv = Pk[v]
                # Compare ANCESTOR IDS, not packed codes: jumping when the
                # 2^k ancestors coincide (but mins differ) would land u == v
                # mid-loop and the final edge reads would then include an
                # edge above the LCA, corrupting B.
                if (cu >> 20) != (cv >> 20):
                    w = cu & MASK
                    if w < res:
                        res = w
                    w = cv & MASK
                    if w < res:
                        res = w
                    u = cu >> 20
                    v = cv >> 20
            code = Pr[0][u]
            w = code & MASK
            if w < res:
                res = w
            code = Pr[0][v]
            w = code & MASK
            if w < res:
                res = w
        B = res
        mn = y if y < z else z
        extra = mn - B
        if extra < 0:
            extra = 0
        oa(str(diff0 + 2 * extra))

    sys.stdout.write('\n'.join(out) + '\n')

main()