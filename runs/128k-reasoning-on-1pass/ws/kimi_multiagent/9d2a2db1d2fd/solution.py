import sys
from array import array

def main():
    # C-level tokenization+conversion: much faster than a Python byte loop
    # (~1.45M tokens); peak token memory ~70MB, well within limits.
    it = iter(map(int, sys.stdin.buffer.read().split()))
    ni = it.__next__

    H = ni(); W = ni()
    N = H * W
    F = array('i', [0]) * N
    for i in range(N):
        F[i] = ni()

    bits = max(1, N.bit_length())
    mask = (1 << bits) - 1
    s2 = 2 * bits

    # Grid edges packed as (weight << 2*bits) | (u << bits) | v so that
    # sorting packed ints descending == sorting by weight descending.
    edges = []
    ap = edges.append
    for i in range(H):
        base = i * W
        for j in range(W - 1):
            u = base + j
            a = F[u]; b = F[u + 1]
            if b < a:
                a = b
            ap((a << s2) | (u << bits) | (u + 1))
    for i in range(H - 1):
        base = i * W
        for j in range(W):
            u = base + j
            v = u + W
            a = F[u]; b = F[v]
            if b < a:
                a = b
            ap((a << s2) | (u << bits) | v)

    edges.sort(reverse=True)

    # Kruskal (descending) -> maximum spanning tree
    parent = list(range(N))
    size = [1] * N

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    head = array('i', [-1]) * N
    m2 = 2 * (N - 1) if N > 1 else 0
    to = array('i', [0]) * m2
    nxt = array('i', [0]) * m2
    ew = array('i', [0]) * m2
    ei = 0
    added = 0
    for e in edges:
        u = (e >> bits) & mask
        v = e & mask
        w = e >> s2
        ru = find(u)
        rv = find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
            to[ei] = v; nxt[ei] = head[u]; ew[ei] = w; head[u] = ei; ei += 1
            to[ei] = u; nxt[ei] = head[v]; ew[ei] = w; head[v] = ei; ei += 1
            added += 1
            if added == N - 1:
                break
    del edges, parent, size

    INF = 1 << 30
    up0 = array('i', [0]) * N
    mn0 = array('i', [0]) * N
    depth = array('i', [0]) * N
    visited = bytearray(N)
    visited[0] = 1
    mn0[0] = INF  # root's "edge to parent" sentinel: never a true minimum
    order = [0]
    for u in order:
        e = head[u]
        while e != -1:
            v = to[e]
            if not visited[v]:
                visited[v] = 1
                up0[v] = u
                mn0[v] = ew[e]
                depth[v] = depth[u] + 1
                order.append(v)
            e = nxt[e]
    del visited, order, head, to, nxt, ew

    LOG = max(1, (N - 1).bit_length())
    up = [up0]
    mn = [mn0]
    for _ in range(1, LOG):
        pu = up[-1]
        pm = mn[-1]
        # cu[v] = pu[pu[v]] ; cm[v] = min(pm[v], pm[pu[v]])  (C-level loops)
        cu = array('i', map(pu.__getitem__, pu))
        cm = array('i', map(min, pm, map(pm.__getitem__, pu)))
        up.append(cu)
        mn.append(cm)

    # Pre-zipped table pairs avoid repeated list indexing inside query loops.
    tables_fwd = list(zip(up, mn))   # fine -> coarse (for depth equalization)
    tables_rev = tables_fwd[::-1]    # coarse -> fine (for simultaneous lift)
    dep = depth
    mn0l = mn0

    Q = ni()
    out = []
    oap = out.append
    for _ in range(Q):
        A = ni(); B = ni(); Y = ni(); C = ni(); D = ni(); Z = ni()
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        if u == v:
            oap(str(abs(Y - Z)))
            continue
        du = dep[u]; dv = dep[v]
        if du < dv:
            u, v = v, u
            du, dv = dv, du
        m = INF
        dd = du - dv
        if dd:
            for uk, mk in tables_fwd:
                if dd & 1:
                    val = mk[u]
                    if val < m:
                        m = val
                    u = uk[u]
                dd >>= 1
                if not dd:
                    break
        if u != v:
            for uk, mk in tables_rev:
                if uk[u] != uk[v]:
                    a = mk[u]
                    if a < m:
                        m = a
                    b = mk[v]
                    if b < m:
                        m = b
                    u = uk[u]
                    v = uk[v]
            a = mn0l[u]
            if a < m:
                m = a
            b = mn0l[v]
            if b < m:
                m = b
        # m = widest-path value M between the two blocks
        ans = Y + Z - 2 * m
        d = abs(Y - Z)
        if d > ans:
            ans = d
        oap(str(ans))

    sys.stdout.write('\n'.join(out) + '\n')

main()