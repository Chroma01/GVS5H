import sys
from array import array


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    next_it = it.__next__
    int_ = int

    H = int_(next_it())
    W = int_(next_it())
    N = H * W

    F = [int_(next_it()) for _ in range(N)]

    SHIFT = 20
    MASK = (1 << SHIFT) - 1
    WSHIFT = 40

    E = H * (W - 1) + W * (H - 1)
    edges = [0] * E
    idx = 0

    # Horizontal edges
    for i in range(H):
        base = i * W
        end = base + W - 1
        for u in range(base, end):
            v = u + 1
            fu = F[u]
            fv = F[v]
            w = fu if fu < fv else fv
            edges[idx] = (w << WSHIFT) | (u << SHIFT) | v
            idx += 1

    # Vertical edges
    for i in range(H - 1):
        base = i * W
        nb = base + W
        for u in range(base, nb):
            v = u + W
            fu = F[u]
            fv = F[v]
            w = fu if fu < fv else fv
            edges[idx] = (w << WSHIFT) | (u << SHIFT) | v
            idx += 1

    max_nodes = 2 * N

    # Leaf values are building heights; internal nodes get merge weights.
    val = array('i', F)
    val.extend(array('i', [0]) * N)
    del F

    Q = int_(next_it())
    qu = array('i', [0]) * Q
    qv = array('i', [0]) * Q
    qy = array('i', [0]) * Q
    qz = array('i', [0]) * Q

    for qi in range(Q):
        A = int_(next_it()) - 1
        B = int_(next_it()) - 1
        Y = int_(next_it())
        C = int_(next_it()) - 1
        D = int_(next_it()) - 1
        Z = int_(next_it())

        qu[qi] = A * W + B
        qv[qi] = C * W + D
        qy[qi] = Y
        qz[qi] = Z

    del data, it, next_it

    edges.sort(reverse=True)

    parent = array('i', [-1]) * max_nodes

    dsu = list(range(N))
    size = [1] * N
    comp_root = list(range(N))

    def find(x, dsu=dsu):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    next_node = N
    remaining = N - 1

    find_local = find
    dsu_local = dsu
    size_local = size
    comp_root_local = comp_root
    parent_local = parent
    val_local = val
    mask = MASK
    shift = SHIFT
    wshift = WSHIFT

    if remaining > 0:
        for e in edges:
            w = e >> wshift
            u = (e >> shift) & mask
            v = e & mask

            ru = find_local(u)
            rv = find_local(v)

            if ru != rv:
                new = next_node
                next_node += 1

                val_local[new] = w

                cr_u = comp_root_local[ru]
                cr_v = comp_root_local[rv]
                parent_local[cr_u] = new
                parent_local[cr_v] = new

                if size_local[ru] < size_local[rv]:
                    ru, rv = rv, ru

                dsu_local[rv] = ru
                size_local[ru] += size_local[rv]
                comp_root_local[ru] = new

                remaining -= 1
                if remaining == 0:
                    break

    del edges, dsu, size, comp_root, find, find_local
    del dsu_local, size_local, comp_root_local, parent_local, val_local

    total_nodes = next_node
    root = total_nodes - 1
    parent[root] = root

    # Since every parent has a larger id than its child, depths can be
    # computed by scanning ids in decreasing order.
    depth = array('i', [0]) * total_nodes
    max_depth = 0
    for node in range(root - 1, -1, -1):
        p = parent[node]
        d = depth[p] + 1
        depth[node] = d
        if d > max_depth:
            max_depth = d

    LOG = max(1, max_depth.bit_length())

    up0 = parent[:total_nodes]
    del parent

    up = [up0]
    for _ in range(1, LOG):
        prev = up[-1]
        curr = array('i', [0]) * total_nodes
        prev_local = prev
        curr_local = curr
        for i, p in enumerate(prev_local):
            curr_local[i] = prev_local[p]
        up.append(curr)

    up0 = up[0]
    rev_range = range(LOG - 1, -1, -1)

    def lca(u, v, depth=depth, up=up, up0=up0, rev_range=rev_range):
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

        for k in rev_range:
            upk = up[k]
            uu = upk[u]
            vv = upk[v]
            if uu != vv:
                u = uu
                v = vv

        return up0[u]

    out = [''] * Q
    lca_local = lca
    val_local = val
    qu_local = qu
    qv_local = qv
    qy_local = qy
    qz_local = qz

    for qi in range(Q):
        u = qu_local[qi]
        v = qv_local[qi]
        y = qy_local[qi]
        z = qz_local[qi]

        if u == v:
            m = val_local[u]
        else:
            m = val_local[lca_local(u, v)]

        if y <= z:
            if y <= m:
                ans = z - y
            else:
                ans = y + z - 2 * m
        else:
            if z <= m:
                ans = y - z
            else:
                ans = y + z - 2 * m

        out[qi] = str(ans)

    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    main()