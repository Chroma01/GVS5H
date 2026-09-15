import sys
from array import array


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W
    max_nodes = 2 * N - 1

    # Node weights: leaves are original buildings, internal nodes are merge weights.
    weight = array('i', [0]) * max_nodes

    # Pack each edge into one integer:
    # high bits: weight, middle: u, low: v.
    # N <= 250000 < 2^20, F <= 10^6 < 2^20.
    SHIFT = 20
    SHIFT2 = 40
    MASK = (1 << SHIFT) - 1

    edges = []
    append_edge = edges.append

    prev_row = None
    for i in range(H):
        row = list(map(int, input().split()))
        base = i * W

        for j in range(W):
            weight[base + j] = row[j]

        # Horizontal edges.
        for j in range(W - 1):
            a = row[j]
            b = row[j + 1]
            w = a if a < b else b
            u = base + j
            v = u + 1
            append_edge((w << SHIFT2) | (u << SHIFT) | v)

        # Vertical edges to the previous row.
        if prev_row is not None:
            prev_base = base - W
            for j in range(W):
                a = row[j]
                b = prev_row[j]
                w = a if a < b else b
                u = base + j
                v = prev_base + j
                append_edge((w << SHIFT2) | (u << SHIFT) | v)

        prev_row = row

    Q = int(input())
    del append_edge, prev_row

    # Kruskal reconstruction tree.
    edges.sort(reverse=True)

    lc = array('i', [-1]) * max_nodes
    rc = array('i', [-1]) * max_nodes
    parent = [0] * max_nodes

    dsu = list(range(N))
    sz = [1] * N
    root_node = list(range(N))

    next_id = N

    for e in edges:
        if next_id == max_nodes:
            break

        u = (e >> SHIFT) & MASK
        v = e & MASK

        # find(u) with path halving
        x = u
        while True:
            px = dsu[x]
            if px == x:
                break
            gx = dsu[px]
            dsu[x] = gx
            x = gx
        ru = x

        # find(v) with path halving
        x = v
        while True:
            px = dsu[x]
            if px == x:
                break
            gx = dsu[px]
            dsu[x] = gx
            x = gx
        rv = x

        if ru == rv:
            continue

        if sz[ru] < sz[rv]:
            ru, rv = rv, ru

        nid = next_id
        next_id += 1

        w = e >> SHIFT2
        weight[nid] = w

        a = root_node[ru]
        b = root_node[rv]

        lc[nid] = a
        rc[nid] = b
        parent[a] = nid
        parent[b] = nid

        dsu[rv] = ru
        sz[ru] += sz[rv]
        root_node[ru] = nid

    del edges, dsu, sz, root_node

    root = next_id - 1
    parent[root] = root

    # Heavy-Light Decomposition preprocessing.
    # Since every KRT parent has a larger id than its children, subtree sizes
    # can be computed by one increasing scan.
    size = [1] * max_nodes
    heavy = [-1] * max_nodes

    for i in range(max_nodes):
        p = parent[i]
        if p != i:
            size[p] += size[i]
            h = heavy[p]
            if h == -1 or size[i] > size[h]:
                heavy[p] = i

    depth = [0] * max_nodes
    head = [0] * max_nodes

    stack = [root]
    while stack:
        h = stack.pop()
        x = h
        while x != -1:
            head[x] = h

            l = lc[x]
            r = rc[x]
            hx = heavy[x]

            if l != -1:
                depth[l] = depth[x] + 1
                if l != hx:
                    stack.append(l)

            if r != -1:
                depth[r] = depth[x] + 1
                if r != hx:
                    stack.append(r)

            x = hx

    del lc, rc, size, heavy, stack

    out = []
    append_out = out.append

    head_arr = head
    depth_arr = depth
    parent_arr = parent
    weight_arr = weight

    for _ in range(Q):
        a, b, y1, c, d, z1 = map(int, input().split())

        u = (a - 1) * W + (b - 1)
        v = (c - 1) * W + (d - 1)

        if u == v:
            B = weight_arr[u]
        else:
            x = u
            y = v

            # HLD LCA.
            while True:
                hx = head_arr[x]
                hy = head_arr[y]
                if hx == hy:
                    break

                dhx = depth_arr[hx]
                dhy = depth_arr[hy]

                if dhx > dhy:
                    x = parent_arr[hx]
                elif dhx < dhy:
                    y = parent_arr[hy]
                else:
                    x = parent_arr[hx]
                    y = parent_arr[hy]

            if depth_arr[x] < depth_arr[y]:
                B = weight_arr[x]
            else:
                B = weight_arr[y]

        ans = y1 - z1
        if ans < 0:
            ans = -ans

        alt = y1 + z1 - 2 * B
        if alt > ans:
            ans = alt

        append_out(str(ans))

    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    solve()