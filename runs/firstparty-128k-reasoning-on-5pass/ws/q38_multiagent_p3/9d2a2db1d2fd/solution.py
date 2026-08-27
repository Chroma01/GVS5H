import sys


def main():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W

    F = []
    for _ in range(H):
        F.extend(map(int, input().split()))

    max_nodes = 2 * N - 1

    Q = int(input())
    Ys = [0] * Q
    Zs = [0] * Q
    ans = [0] * Q

    head = [-1] * max_nodes
    to = []
    qid = []
    nxt = []
    edge_idx = 0

    to_append = to.append
    qid_append = qid.append
    nxt_append = nxt.append

    for qi in range(Q):
        a, b, y, c, d, z = map(int, input().split())
        u = (a - 1) * W + (b - 1)
        v = (c - 1) * W + (d - 1)

        Ys[qi] = y
        Zs[qi] = z

        if u == v:
            ans[qi] = y - z if y >= z else z - y
        else:
            to_append(v)
            qid_append(qi)
            nxt_append(head[u])
            head[u] = edge_idx
            edge_idx += 1

            to_append(u)
            qid_append(qi)
            nxt_append(head[v])
            head[v] = edge_idx
            edge_idx += 1

    left = [-1] * max_nodes
    right = [-1] * max_nodes
    weight = [0] * max_nodes
    parent = [-1] * max_nodes
    active = bytearray(N)

    order = sorted(range(N), key=F.__getitem__, reverse=True)

    def find_build(x, p=parent):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    node_cnt = N
    L = left
    R = right
    Wt = weight
    P = parent
    act = active
    Flist = F
    Wd = W
    Nn = N
    find = find_build

    for v in order:
        h = Flist[v]
        act[v] = 1
        P[v] = v
        root_v = v

        if v >= Wd:
            nb = v - Wd
            if act[nb]:
                rv = find(nb)
                if root_v != rv:
                    new = node_cnt
                    node_cnt += 1
                    L[new] = root_v
                    R[new] = rv
                    Wt[new] = h
                    P[root_v] = new
                    P[rv] = new
                    P[new] = new
                    root_v = new

        if v < Nn - Wd:
            nb = v + Wd
            if act[nb]:
                rv = find(nb)
                if root_v != rv:
                    new = node_cnt
                    node_cnt += 1
                    L[new] = root_v
                    R[new] = rv
                    Wt[new] = h
                    P[root_v] = new
                    P[rv] = new
                    P[new] = new
                    root_v = new

        c = v % Wd
        if c:
            nb = v - 1
            if act[nb]:
                rv = find(nb)
                if root_v != rv:
                    new = node_cnt
                    node_cnt += 1
                    L[new] = root_v
                    R[new] = rv
                    Wt[new] = h
                    P[root_v] = new
                    P[rv] = new
                    P[new] = new
                    root_v = new

        if c != Wd - 1:
            nb = v + 1
            if act[nb]:
                rv = find(nb)
                if root_v != rv:
                    new = node_cnt
                    node_cnt += 1
                    L[new] = root_v
                    R[new] = rv
                    Wt[new] = h
                    P[root_v] = new
                    P[rv] = new
                    P[new] = new
                    root_v = new

    total_nodes = node_cnt
    root = find(0)

    del F, Flist, order, active, act

    if edge_idx:
        size = [0] * total_nodes
        ancestor = [0] * total_nodes
        black = bytearray(total_nodes)

        p = parent
        sz = size
        anc = ancestor
        blk = black
        L = left
        R = right
        Wt = weight
        hd = head
        TO = to
        QID = qid
        NX = nxt
        Yarr = Ys
        Zarr = Zs
        Ans = ans

        stack = [root]
        push = stack.append
        pop = stack.pop

        while stack:
            x = pop()

            if x >= 0:
                u = x
                p[u] = u
                sz[u] = 1
                anc[u] = u

                l = L[u]
                r = R[u]

                if l == -1 and r == -1:
                    blk[u] = 1
                    e = hd[u]
                    while e != -1:
                        v = TO[e]
                        if blk[v]:
                            rv = v
                            while p[rv] != rv:
                                p[rv] = p[p[rv]]
                                rv = p[rv]

                            lca = anc[rv]
                            m = Wt[lca]
                            qi = QID[e]
                            yy = Yarr[qi]
                            zz = Zarr[qi]

                            diff = yy - zz
                            if diff < 0:
                                diff = -diff
                            via_low = yy + zz - (m << 1)
                            Ans[qi] = diff if diff >= via_low else via_low

                        e = NX[e]
                else:
                    push(-(u * 2 + 2))
                    if r != -1:
                        push(r)
                    push(-(u * 2 + 1))
                    if l != -1:
                        push(l)

            else:
                y = -x
                if y & 1:
                    u = y >> 1
                    l = L[u]
                    if l != -1:
                        ru = u
                        while p[ru] != ru:
                            p[ru] = p[p[ru]]
                            ru = p[ru]

                        rl = l
                        while p[rl] != rl:
                            p[rl] = p[p[rl]]
                            rl = p[rl]

                        if ru != rl:
                            if sz[ru] < sz[rl]:
                                ru, rl = rl, ru
                            p[rl] = ru
                            sz[ru] += sz[rl]

                        anc[ru] = u
                else:
                    u = (y >> 1) - 1
                    r = R[u]
                    if r != -1:
                        ru = u
                        while p[ru] != ru:
                            p[ru] = p[p[ru]]
                            ru = p[ru]

                        rr = r
                        while p[rr] != rr:
                            p[rr] = p[p[rr]]
                            rr = p[rr]

                        if ru != rr:
                            if sz[ru] < sz[rr]:
                                ru, rr = rr, ru
                            p[rr] = ru
                            sz[ru] += sz[rr]

                        anc[ru] = u

                    blk[u] = 1
                    e = hd[u]
                    while e != -1:
                        v = TO[e]
                        if blk[v]:
                            rv = v
                            while p[rv] != rv:
                                p[rv] = p[p[rv]]
                                rv = p[rv]

                            lca = anc[rv]
                            m = Wt[lca]
                            qi = QID[e]
                            yy = Yarr[qi]
                            zz = Zarr[qi]

                            diff = yy - zz
                            if diff < 0:
                                diff = -diff
                            via_low = yy + zz - (m << 1)
                            Ans[qi] = diff if diff >= via_low else via_low

                        e = NX[e]

    sys.stdout.write("\n".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    main()