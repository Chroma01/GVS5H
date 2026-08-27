import sys
from array import array


def main():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W

    F = []
    for _ in range(H):
        F.extend(map(int, input().split()))

    order = list(range(N))
    dsu_parent = order.copy()
    order.sort(key=F.__getitem__, reverse=True)

    size = [1] * N
    active = bytearray(N)

    head = array('i', [-1]) * N
    max_edges = 2 * (N - 1) if N > 1 else 0
    to = array('i', [0]) * max_edges
    nxt = array('i', [0]) * max_edges
    wt = array('i', [0]) * max_edges
    edge_cnt = 0

    N_minus_W = N - W
    Wm1 = W - 1

    for u in order:
        active[u] = 1
        h = F[u]
        ru = u
        col = u % W

        if u >= W:
            v = u - W
            if active[v]:
                rv = v
                while dsu_parent[rv] != rv:
                    dsu_parent[rv] = dsu_parent[dsu_parent[rv]]
                    rv = dsu_parent[rv]
                if ru != rv:
                    if size[ru] < size[rv]:
                        dsu_parent[ru] = rv
                        size[rv] += size[ru]
                        ru = rv
                    else:
                        dsu_parent[rv] = ru
                        size[ru] += size[rv]

                    idx = edge_cnt
                    to[idx] = v
                    wt[idx] = h
                    nxt[idx] = head[u]
                    head[u] = idx
                    to[idx + 1] = u
                    wt[idx + 1] = h
                    nxt[idx + 1] = head[v]
                    head[v] = idx + 1
                    edge_cnt += 2

        if u < N_minus_W:
            v = u + W
            if active[v]:
                rv = v
                while dsu_parent[rv] != rv:
                    dsu_parent[rv] = dsu_parent[dsu_parent[rv]]
                    rv = dsu_parent[rv]
                if ru != rv:
                    if size[ru] < size[rv]:
                        dsu_parent[ru] = rv
                        size[rv] += size[ru]
                        ru = rv
                    else:
                        dsu_parent[rv] = ru
                        size[ru] += size[rv]

                    idx = edge_cnt
                    to[idx] = v
                    wt[idx] = h
                    nxt[idx] = head[u]
                    head[u] = idx
                    to[idx + 1] = u
                    wt[idx + 1] = h
                    nxt[idx + 1] = head[v]
                    head[v] = idx + 1
                    edge_cnt += 2

        if col:
            v = u - 1
            if active[v]:
                rv = v
                while dsu_parent[rv] != rv:
                    dsu_parent[rv] = dsu_parent[dsu_parent[rv]]
                    rv = dsu_parent[rv]
                if ru != rv:
                    if size[ru] < size[rv]:
                        dsu_parent[ru] = rv
                        size[rv] += size[ru]
                        ru = rv
                    else:
                        dsu_parent[rv] = ru
                        size[ru] += size[rv]

                    idx = edge_cnt
                    to[idx] = v
                    wt[idx] = h
                    nxt[idx] = head[u]
                    head[u] = idx
                    to[idx + 1] = u
                    wt[idx + 1] = h
                    nxt[idx + 1] = head[v]
                    head[v] = idx + 1
                    edge_cnt += 2

        if col != Wm1:
            v = u + 1
            if active[v]:
                rv = v
                while dsu_parent[rv] != rv:
                    dsu_parent[rv] = dsu_parent[dsu_parent[rv]]
                    rv = dsu_parent[rv]
                if ru != rv:
                    if size[ru] < size[rv]:
                        dsu_parent[ru] = rv
                        size[rv] += size[ru]
                        ru = rv
                    else:
                        dsu_parent[rv] = ru
                        size[ru] += size[rv]

                    idx = edge_cnt
                    to[idx] = v
                    wt[idx] = h
                    nxt[idx] = head[u]
                    head[u] = idx
                    to[idx + 1] = u
                    wt[idx + 1] = h
                    nxt[idx + 1] = head[v]
                    head[v] = idx + 1
                    edge_cnt += 2

    del order, dsu_parent, size, active, F

    INF = 10 ** 9
    parent0 = [0] * N
    mn0 = [INF] * N
    depth = [0] * N

    stack = [0]
    while stack:
        v = stack.pop()
        e = head[v]
        dv = depth[v] + 1
        pv = parent0[v]
        while e != -1:
            u = to[e]
            if u != pv:
                parent0[u] = v
                mn0[u] = wt[e]
                depth[u] = dv
                stack.append(u)
            e = nxt[e]

    del head, to, nxt, wt, stack

    LOG = N.bit_length()
    up = [parent0]
    mn = [mn0]
    del parent0, mn0

    for _ in range(1, LOG):
        pu = up[-1]
        pm = mn[-1]
        cu = [0] * N
        cm = [INF] * N
        for v, mid in enumerate(pu):
            cu[v] = pu[mid]
            a = pm[v]
            b = pm[mid]
            cm[v] = a if a < b else b
        up.append(cu)
        mn.append(cm)

    Q = int(input())
    out = []

    up_tbl = up
    mn_tbl = mn
    dep = depth
    rev_range = range(LOG - 1, -1, -1)
    W_local = W
    INF_local = INF

    for _ in range(Q):
        a, b, y, c, d, z = map(int, input().split())
        u = (a - 1) * W_local + (b - 1)
        v = (c - 1) * W_local + (d - 1)

        if u == v:
            out.append(str(abs(y - z)))
            continue

        x = u
        ynode = v
        if dep[x] < dep[ynode]:
            x, ynode = ynode, x

        res = INF_local
        diff = dep[x] - dep[ynode]
        k = 0
        while diff:
            if diff & 1:
                mk = mn_tbl[k]
                m = mk[x]
                if m < res:
                    res = m
                x = up_tbl[k][x]
            diff >>= 1
            k += 1

        if x != ynode:
            for k in rev_range:
                uk = up_tbl[k]
                ux = uk[x]
                vx = uk[ynode]
                if ux != vx:
                    mk = mn_tbl[k]
                    m = mk[x]
                    if m < res:
                        res = m
                    m = mk[ynode]
                    if m < res:
                        res = m
                    x = ux
                    ynode = vx

            m = mn_tbl[0][x]
            if m < res:
                res = m
            m = mn_tbl[0][ynode]
            if m < res:
                res = m

        B = res
        ans = abs(y - z)
        t = y + z - 2 * B
        if t > ans:
            ans = t
        out.append(str(ans))

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()