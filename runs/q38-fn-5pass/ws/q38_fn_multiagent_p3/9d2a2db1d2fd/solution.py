import sys


def solve():
    readline = sys.stdin.buffer.readline

    H, W = map(int, readline().split())
    N = H * W

    F = []
    for _ in range(H):
        F.extend(map(int, readline().split()))

    Q = int(readline())

    # Sort cells by height descending.  When a cell is activated, all already
    # active neighbours have height >= this cell's height, so every grid edge
    # is considered exactly once, in non-increasing order of min(F_u, F_v).
    order = list(range(N))
    parent = order.copy()
    comp_root = parent.copy()
    order.sort(key=F.__getitem__, reverse=True)

    size = [1] * N
    active = bytearray(N)

    # Kruskal reconstruction tree:
    # leaves 0..N-1 are blocks, internal nodes store the merge height.
    max_nodes = 2 * N - 1
    tree_parent = [-1] * max_nodes
    weight = [0] * max_nodes
    tot = N

    def find(x, par=parent):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    par = parent
    sz = size
    cr = comp_root
    act = active
    tp = tree_parent
    wt = weight
    heights = F
    w = W
    n = N
    n_minus_w = n - w
    w_minus_1 = w - 1
    find_local = find

    for u in order:
        act[u] = 1
        hu = heights[u]
        ru = u  # newly activated cell is still its own DSU root

        if u >= w:
            v = u - w
            if act[v]:
                rv = find_local(v)
                if ru != rv:
                    if sz[ru] < sz[rv]:
                        ru, rv = rv, ru
                    t = tot
                    tot = t + 1
                    wt[t] = hu
                    tp[cr[ru]] = t
                    tp[cr[rv]] = t
                    par[rv] = ru
                    sz[ru] += sz[rv]
                    cr[ru] = t

        if u < n_minus_w:
            v = u + w
            if act[v]:
                rv = find_local(v)
                if ru != rv:
                    if sz[ru] < sz[rv]:
                        ru, rv = rv, ru
                    t = tot
                    tot = t + 1
                    wt[t] = hu
                    tp[cr[ru]] = t
                    tp[cr[rv]] = t
                    par[rv] = ru
                    sz[ru] += sz[rv]
                    cr[ru] = t

        col = u % w

        if col:
            v = u - 1
            if act[v]:
                rv = find_local(v)
                if ru != rv:
                    if sz[ru] < sz[rv]:
                        ru, rv = rv, ru
                    t = tot
                    tot = t + 1
                    wt[t] = hu
                    tp[cr[ru]] = t
                    tp[cr[rv]] = t
                    par[rv] = ru
                    sz[ru] += sz[rv]
                    cr[ru] = t

        if col != w_minus_1:
            v = u + 1
            if act[v]:
                rv = find_local(v)
                if ru != rv:
                    if sz[ru] < sz[rv]:
                        ru, rv = rv, ru
                    t = tot
                    tot = t + 1
                    wt[t] = hu
                    tp[cr[ru]] = t
                    tp[cr[rv]] = t
                    par[rv] = ru
                    sz[ru] += sz[rv]
                    cr[ru] = t

    # The last created node is the root of the reconstruction tree.
    root = tot - 1
    tp[root] = root

    # Parent indices are always larger than child indices, so depth can be
    # computed iteratively from large indices down to small ones.
    depth = [0] * tot
    for node in range(tot - 2, -1, -1):
        depth[node] = depth[tp[node]] + 1

    # Free large structures no longer needed.
    parent = par = None
    size = sz = None
    comp_root = cr = None
    active = act = None
    order = None
    F = heights = None
    find = find_local = None
    wt = None

    # Binary lifting table for LCA on the reconstruction tree.
    up = [tp[:tot]]
    tp = None
    tree_parent = None

    # Maximum leaf depth is at most N-1.
    LOG = max(1, (N - 1).bit_length())
    for _ in range(1, LOG):
        prev = up[-1]
        up.append([prev[x] for x in prev])

    up_local = up
    up_rev = up[::-1]
    up0 = up[0]
    depth_local = depth
    weight_local = weight
    W_local = W

    out = []
    append = out.append

    for _ in range(Q):
        a, b, y, c, d, z = map(int, readline().split())
        u = (a - 1) * W_local + (b - 1)
        v = (c - 1) * W_local + (d - 1)

        if u == v:
            append(str(abs(y - z)))
            continue

        x = u
        yy = v
        dx = depth_local[x]
        dy = depth_local[yy]

        if dx < dy:
            x, yy = yy, x
            dx, dy = dy, dx

        diff = dx - dy
        bit = 0
        while diff:
            if diff & 1:
                x = up_local[bit][x]
            diff >>= 1
            bit += 1

        if x != yy:
            for upk in up_rev:
                nx = upk[x]
                ny = upk[yy]
                if nx != ny:
                    x = nx
                    yy = ny
            x = up0[x]

        bottleneck = weight_local[x]

        if y < z:
            mn = y
            mx = z
        else:
            mn = z
            mx = y

        if mn <= bottleneck:
            append(str(mx - mn))
        else:
            append(str(y + z - 2 * bottleneck))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()