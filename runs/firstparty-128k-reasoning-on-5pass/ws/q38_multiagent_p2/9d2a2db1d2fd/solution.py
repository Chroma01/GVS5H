import sys
from array import array


def main():
    data = array('I', map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    H = data[0]
    W = data[1]
    N = H * W

    F = data[2:2 + N].tolist()
    idx = 2 + N
    Q = data[idx]
    query_pos = idx + 1

    order = list(range(N))
    order.sort(key=F.__getitem__, reverse=True)

    max_nodes = 2 * N
    weight = array('I', [0]) * max_nodes
    tree_parent = array('I', [0]) * max_nodes

    dsu = [0] * N          # 0: inactive, negative: root size, non-negative: parent
    comp = [0] * N         # comp[dsu_root] = current reconstruction-tree node
    active = bytearray(N)

    def find(x, dsu=dsu):
        while dsu[x] >= 0:
            p = dsu[x]
            if dsu[p] >= 0:
                dsu[x] = dsu[p]
            x = dsu[x]
        return x

    next_node = N
    N_minus_W = N - W
    Wm1 = W - 1

    for v in order:
        h = F[v]
        weight[v] = h
        active[v] = 1
        dsu[v] = -1
        comp[v] = v
        col = v % W

        if v >= W:
            u = v - W
            if active[u]:
                ru = find(u)
                rv = find(v)
                if ru != rv:
                    x = next_node
                    next_node += 1
                    weight[x] = h
                    a = comp[ru]
                    b = comp[rv]
                    tree_parent[a] = x
                    tree_parent[b] = x
                    if dsu[ru] > dsu[rv]:
                        ru, rv = rv, ru
                    dsu[ru] += dsu[rv]
                    dsu[rv] = ru
                    comp[ru] = x

        if v < N_minus_W:
            u = v + W
            if active[u]:
                ru = find(u)
                rv = find(v)
                if ru != rv:
                    x = next_node
                    next_node += 1
                    weight[x] = h
                    a = comp[ru]
                    b = comp[rv]
                    tree_parent[a] = x
                    tree_parent[b] = x
                    if dsu[ru] > dsu[rv]:
                        ru, rv = rv, ru
                    dsu[ru] += dsu[rv]
                    dsu[rv] = ru
                    comp[ru] = x

        if col:
            u = v - 1
            if active[u]:
                ru = find(u)
                rv = find(v)
                if ru != rv:
                    x = next_node
                    next_node += 1
                    weight[x] = h
                    a = comp[ru]
                    b = comp[rv]
                    tree_parent[a] = x
                    tree_parent[b] = x
                    if dsu[ru] > dsu[rv]:
                        ru, rv = rv, ru
                    dsu[ru] += dsu[rv]
                    dsu[rv] = ru
                    comp[ru] = x

        if col != Wm1:
            u = v + 1
            if active[u]:
                ru = find(u)
                rv = find(v)
                if ru != rv:
                    x = next_node
                    next_node += 1
                    weight[x] = h
                    a = comp[ru]
                    b = comp[rv]
                    tree_parent[a] = x
                    tree_parent[b] = x
                    if dsu[ru] > dsu[rv]:
                        ru, rv = rv, ru
                    dsu[ru] += dsu[rv]
                    dsu[rv] = ru
                    comp[ru] = x

    M = next_node
    root = M - 1
    tree_parent[root] = root

    del find
    del F, order, dsu, comp, active

    depth = array('I', [0]) * M
    for i in range(M - 2, -1, -1):
        depth[i] = depth[tree_parent[i]] + 1

    LOG = M.bit_length()
    up = [tree_parent]
    for _ in range(1, LOG):
        prev = up[-1]
        cur = array('I', [0]) * M
        for i in range(M):
            cur[i] = prev[prev[i]]
        up.append(cur)

    rev_range = range(LOG - 1, -1, -1)

    def lca(u, v, up=up, depth=depth, rev_range=rev_range):
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
            pu = upk[u]
            pv = upk[v]
            if pu != pv:
                u = pu
                v = pv

        return up[0][u]

    out = []
    append = out.append
    w_arr = weight
    lca_func = lca
    W_local = W
    pos = query_pos

    for _ in range(Q):
        A = data[pos]
        B = data[pos + 1]
        Y = data[pos + 2]
        C = data[pos + 3]
        D = data[pos + 4]
        Z = data[pos + 5]
        pos += 6

        u = (A - 1) * W_local + (B - 1)
        v = (C - 1) * W_local + (D - 1)

        if u == v:
            b = w_arr[u]
        else:
            b = w_arr[lca_func(u, v)]

        mn = Y if Y < Z else Z
        ans = Y - Z if Y >= Z else Z - Y
        if mn > b:
            ans += (mn - b) * 2

        append(str(ans))

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()