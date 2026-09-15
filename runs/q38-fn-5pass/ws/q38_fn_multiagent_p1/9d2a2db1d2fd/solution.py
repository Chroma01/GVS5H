import sys


def solve():
    input = sys.stdin.buffer.readline
    H, W = map(int, input().split())
    N = H * W

    heights = []
    for _ in range(H):
        heights.extend(map(int, input().split()))

    shift = max(1, (N - 1).bit_length())
    shift2 = shift << 1
    mask = (1 << shift) - 1

    W_local = W
    edge_count = H * (W_local - 1) + (H - 1) * W_local
    edges = [0] * edge_count
    idx = 0
    h = heights

    if W_local > 1:
        for i in range(H):
            base = i * W_local
            end = base + W_local - 1
            for u in range(base, end):
                v = u + 1
                hu = h[u]
                hv = h[v]
                ww = hu if hu < hv else hv
                edges[idx] = (ww << shift2) | (u << shift) | v
                idx += 1

    if H > 1:
        for i in range(H - 1):
            base = i * W_local
            end = base + W_local
            for u in range(base, end):
                v = u + W_local
                hu = h[u]
                hv = h[v]
                ww = hu if hu < hv else hv
                edges[idx] = (ww << shift2) | (u << shift) | v
                idx += 1

    del h
    if idx != edge_count:
        edges = edges[:idx]

    edges.sort(reverse=True)

    max_nodes = N << 1
    parent = list(range(N))
    size = [1] * N
    comp_root = list(range(N))

    left = [0] * max_nodes
    right = [0] * max_nodes
    up0 = [0] * max_nodes
    weight = heights + [0] * N
    del heights

    tot = N
    par = parent
    sz = size
    comp = comp_root
    lft = left
    rgt = right
    up = up0
    wt = weight
    sh = shift
    sh2 = shift2
    msk = mask
    target = (N << 1) - 1

    for e in edges:
        v = e & msk
        u = (e >> sh) & msk

        x = u
        while True:
            px = par[x]
            if px == x:
                break
            gpx = par[px]
            par[x] = gpx
            x = gpx
        ru = x

        x = v
        while True:
            px = par[x]
            if px == x:
                break
            gpx = par[px]
            par[x] = gpx
            x = gpx
        rv = x

        if ru != rv:
            ww = e >> sh2
            if sz[ru] < sz[rv]:
                ru, rv = rv, ru

            c1 = comp[ru]
            c2 = comp[rv]

            lft[tot] = c1
            rgt[tot] = c2
            wt[tot] = ww
            up[c1] = tot
            up[c2] = tot

            par[rv] = ru
            sz[ru] += sz[rv]
            comp[ru] = tot
            tot += 1

            if tot == target:
                break

    del edges, parent, size, comp_root, par, sz, comp

    root = tot - 1
    up[root] = root

    depth = [0] * tot
    dep = depth
    max_depth = 0

    for v in range(tot - 1, N - 1, -1):
        dv = dep[v] + 1
        dep[lft[v]] = dv
        dep[rgt[v]] = dv
        if dv > max_depth:
            max_depth = dv

    del left, right, lft, rgt

    up0 = up[:tot]
    del up
    weight = wt[:tot]
    del wt

    LOG = max_depth.bit_length() or 1
    up_table = [up0]
    for _ in range(1, LOG):
        prev = up_table[-1]
        up_table.append([prev[x] for x in prev])

    rev_range = tuple(range(LOG - 1, -1, -1))

    def lca(u, v, dep=depth, tbl=up_table, rev_range=rev_range):
        if dep[u] < dep[v]:
            u, v = v, u

        diff = dep[u] - dep[v]
        k = 0
        while diff:
            if diff & 1:
                u = tbl[k][u]
            diff >>= 1
            k += 1

        if u == v:
            return u

        for k in rev_range:
            row = tbl[k]
            pu = row[u]
            pv = row[v]
            if pu != pv:
                u = pu
                v = pv

        return tbl[0][u]

    Q_line = input()
    while Q_line and Q_line.strip() == b'':
        Q_line = input()
    Q = int(Q_line)

    out = [''] * Q
    wt = weight
    abs_ = abs
    W_local = W

    for qi in range(Q):
        a, b, y, c, d, z = map(int, input().split())
        u = (a - 1) * W_local + (b - 1)
        v = (c - 1) * W_local + (d - 1)

        if u == v:
            out[qi] = str(abs_(y - z))
            continue

        l = lca(u, v)
        bb = wt[l]

        if bb >= (y if y < z else z):
            out[qi] = str(abs_(y - z))
        else:
            out[qi] = str(y + z - 2 * bb)

    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    solve()