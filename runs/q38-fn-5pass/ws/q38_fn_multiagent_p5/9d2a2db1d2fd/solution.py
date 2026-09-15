import sys
from array import array


def solve():
    data = array('i', map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    H = data[p]
    W = data[p + 1]
    p += 2

    N = H * W
    F = data[p:p + N]
    p += N

    Q = data[p]
    p += 1
    query_start = p

    # Kruskal reconstruction tree.
    # Leaves are 0..N-1.  Each successful union creates a new node.
    max_nodes = 2 * N - 1

    parent = list(range(N))
    if max_nodes > N:
        parent.extend([0] * (max_nodes - N))

    val = array('i', F)
    if max_nodes > N:
        val.extend(array('i', [0]) * (max_nodes - N))

    # DSU over original cells, with union by size.
    # root_node[rep] is the current reconstruction-tree root of that component.
    dsu = parent[:N]
    root_node = parent[:N]
    size = [1] * N
    active = bytearray(N)

    order = parent[:N]
    order.sort(key=F.__getitem__, reverse=True)

    def find(x, dsu=dsu):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    node_count = N
    last_row_start = N - W
    w_minus_1 = W - 1

    for idx in order:
        active[idx] = 1
        h = F[idx]
        rep_cur = idx

        if idx >= W:
            nb = idx - W
            if active[nb]:
                rep_nb = find(nb)
                if rep_cur != rep_nb:
                    ru = root_node[rep_cur]
                    rv = root_node[rep_nb]
                    new = node_count
                    node_count += 1

                    val[new] = h
                    parent[ru] = new
                    parent[rv] = new
                    parent[new] = new

                    if size[rep_cur] < size[rep_nb]:
                        dsu[rep_cur] = rep_nb
                        size[rep_nb] += size[rep_cur]
                        root_node[rep_nb] = new
                        rep_cur = rep_nb
                    else:
                        dsu[rep_nb] = rep_cur
                        size[rep_cur] += size[rep_nb]
                        root_node[rep_cur] = new

        if idx < last_row_start:
            nb = idx + W
            if active[nb]:
                rep_nb = find(nb)
                if rep_cur != rep_nb:
                    ru = root_node[rep_cur]
                    rv = root_node[rep_nb]
                    new = node_count
                    node_count += 1

                    val[new] = h
                    parent[ru] = new
                    parent[rv] = new
                    parent[new] = new

                    if size[rep_cur] < size[rep_nb]:
                        dsu[rep_cur] = rep_nb
                        size[rep_nb] += size[rep_cur]
                        root_node[rep_nb] = new
                        rep_cur = rep_nb
                    else:
                        dsu[rep_nb] = rep_cur
                        size[rep_cur] += size[rep_nb]
                        root_node[rep_cur] = new

        col = idx % W

        if col:
            nb = idx - 1
            if active[nb]:
                rep_nb = find(nb)
                if rep_cur != rep_nb:
                    ru = root_node[rep_cur]
                    rv = root_node[rep_nb]
                    new = node_count
                    node_count += 1

                    val[new] = h
                    parent[ru] = new
                    parent[rv] = new
                    parent[new] = new

                    if size[rep_cur] < size[rep_nb]:
                        dsu[rep_cur] = rep_nb
                        size[rep_nb] += size[rep_cur]
                        root_node[rep_nb] = new
                        rep_cur = rep_nb
                    else:
                        dsu[rep_nb] = rep_cur
                        size[rep_cur] += size[rep_nb]
                        root_node[rep_cur] = new

        if col != w_minus_1:
            nb = idx + 1
            if active[nb]:
                rep_nb = find(nb)
                if rep_cur != rep_nb:
                    ru = root_node[rep_cur]
                    rv = root_node[rep_nb]
                    new = node_count
                    node_count += 1

                    val[new] = h
                    parent[ru] = new
                    parent[rv] = new
                    parent[new] = new

                    if size[rep_cur] < size[rep_nb]:
                        dsu[rep_cur] = rep_nb
                        size[rep_nb] += size[rep_cur]
                        root_node[rep_nb] = new
                        rep_cur = rep_nb
                    else:
                        dsu[rep_nb] = rep_cur
                        size[rep_cur] += size[rep_nb]
                        root_node[rep_cur] = new

    del order, active, F, dsu, size, root_node, find

    M = node_count
    if M != len(parent):
        parent = parent[:M]
        val = val[:M]

    # Parent ids are always larger than child ids, so depth can be computed
    # by scanning nodes in decreasing id order.
    depth = [0] * M
    max_depth = 0
    for i in range(M - 2, -1, -1):
        d = depth[parent[i]] + 1
        depth[i] = d
        if d > max_depth:
            max_depth = d

    LOG = max(1, max_depth.bit_length())
    up = [parent]
    for _ in range(1, LOG):
        prev = up[-1]
        up.append([prev[x] for x in prev])

    rev_range = range(LOG - 1, -1, -1)
    up0 = up[0]

    def lca(u, v, depth=depth, up=up, rev_range=rev_range, up0=up0):
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
            pu = up[k][u]
            pv = up[k][v]
            if pu != pv:
                u = pu
                v = pv

        return up0[u]

    out = []
    append = out.append
    p = query_start
    W_local = W
    val_local = val
    lca_local = lca
    data_local = data

    for _ in range(Q):
        A = data_local[p]
        B = data_local[p + 1]
        Y = data_local[p + 2]
        C = data_local[p + 3]
        D = data_local[p + 4]
        Z = data_local[p + 5]
        p += 6

        u = (A - 1) * W_local + (B - 1)
        v = (C - 1) * W_local + (D - 1)

        if u == v:
            bottleneck = val_local[u]
        else:
            bottleneck = val_local[lca_local(u, v)]

        if Y < Z:
            if Y <= bottleneck:
                append(str(Z - Y))
            else:
                append(str(Y + Z - 2 * bottleneck))
        else:
            if Z <= bottleneck:
                append(str(Y - Z))
            else:
                append(str(Y + Z - 2 * bottleneck))

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    solve()