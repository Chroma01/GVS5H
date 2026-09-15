import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N = data[idx]
    M = data[idx + 1]
    Q = data[idx + 2]
    idx += 3

    left = [0] * (M + 1)
    right = [0] * (M + 1)
    typ = [0] * (M + 1)  # 0: S < T (interior higher), 1: S > T (interior lower)

    for i in range(1, M + 1):
        s = data[idx]
        t = data[idx + 1]
        idx += 2
        if s < t:
            left[i] = s
            right[i] = t
            typ[i] = 0
        else:
            left[i] = t
            right[i] = s
            typ[i] = 1

    qlist = [0] * Q
    rlist = [0] * Q
    for k in range(Q):
        qlist[k] = data[idx]
        rlist[k] = data[idx + 1]
        idx += 2

    del data

    # Segment trees over town coordinates.
    # For each type:
    #   min_trees[t]: keyed by right endpoint, stores active id with minimum left endpoint.
    #   max_trees[t]: keyed by left endpoint, stores active id with maximum right endpoint.
    size = 1
    while size <= N:
        size <<= 1

    min_trees = [[0] * (2 * size) for _ in range(2)]
    max_trees = [[0] * (2 * size) for _ in range(2)]

    active_left = [0] * (N + 2)
    active_right = [0] * (N + 2)
    ans = [0] * (M + 1)

    def update_min(tree, pos, id_, size=size, left=left):
        p = pos + size
        tree[p] = id_
        p >>= 1
        while p:
            lc = p << 1
            rc = lc | 1
            a = tree[lc]
            b = tree[rc]
            if a == 0:
                tree[p] = b
            elif b == 0:
                tree[p] = a
            elif left[a] <= left[b]:
                tree[p] = a
            else:
                tree[p] = b
            p >>= 1

    def update_max(tree, pos, id_, size=size, right=right):
        p = pos + size
        tree[p] = id_
        p >>= 1
        while p:
            lc = p << 1
            rc = lc | 1
            a = tree[lc]
            b = tree[rc]
            if a == 0:
                tree[p] = b
            elif b == 0:
                tree[p] = a
            elif right[a] >= right[b]:
                tree[p] = a
            else:
                tree[p] = b
            p >>= 1

    def query_min(tree, ql, qr, size=size, left=left):
        if ql > qr:
            return 0
        ql += size
        qr += size
        best = 0
        while ql <= qr:
            if ql & 1:
                node = tree[ql]
                if node and (best == 0 or left[node] < left[best]):
                    best = node
                ql += 1
            if not (qr & 1):
                node = tree[qr]
                if node and (best == 0 or left[node] < left[best]):
                    best = node
                qr -= 1
            ql >>= 1
            qr >>= 1
        return best

    def query_max(tree, ql, qr, size=size, right=right):
        if ql > qr:
            return 0
        ql += size
        qr += size
        best = 0
        while ql <= qr:
            if ql & 1:
                node = tree[ql]
                if node and (best == 0 or right[node] > right[best]):
                    best = node
                ql += 1
            if not (qr & 1):
                node = tree[qr]
                if node and (best == 0 or right[node] > right[best]):
                    best = node
                qr -= 1
            ql >>= 1
            qr >>= 1
        return best

    def remove_id(i, j,
                  ans=ans,
                  active_left=active_left,
                  active_right=active_right,
                  left=left,
                  right=right,
                  typ=typ,
                  min_trees=min_trees,
                  max_trees=max_trees,
                  update_min=update_min,
                  update_max=update_max):
        if ans[i] == 0:
            ans[i] = j
        li = left[i]
        ri = right[i]
        t = typ[i]

        if active_left[li] == i:
            active_left[li] = 0
        if active_right[ri] == i:
            active_right[ri] = 0

        update_min(min_trees[t], ri, 0)
        update_max(max_trees[t], li, 0)

    upd_min = update_min
    upd_max = update_max
    qry_min = query_min
    qry_max = query_max

    # Sweep people in input order.  Active previous people have no forbidden pair
    # among themselves.  When a new person arrives, remove every active person
    # that forms a forbidden pair with it; that new index is their earliest conflict.
    for j in range(1, M + 1):
        lj = left[j]
        rj = right[j]
        tj = typ[j]

        i = active_left[lj]
        if i:
            remove_id(i, j)

        i = active_right[rj]
        if i:
            remove_id(i, j)

        ql = lj + 1
        qr = rj - 1
        mt = min_trees[tj]
        xt = max_trees[tj]

        while True:
            # Same-type crossing of form l_i < l_j < r_i < r_j.
            id1 = qry_min(mt, ql, qr)
            if id1 and left[id1] < lj:
                remove_id(id1, j)
                continue

            # Same-type crossing of form l_j < l_i < r_j < r_i.
            id2 = qry_max(xt, ql, qr)
            if id2 and right[id2] > rj:
                remove_id(id2, j)
                continue

            break

        active_left[lj] = j
        active_right[rj] = j
        upd_min(min_trees[tj], rj, j)
        upd_max(max_trees[tj], lj, j)

    # Answer range queries: [L, R] is feasible iff no i in [L, R] has ans[i] <= R.
    INF = M + 1
    size_m = 1
    while size_m <= M:
        size_m <<= 1

    seg = [INF] * (2 * size_m)
    base = size_m
    for i in range(1, M + 1):
        if ans[i]:
            seg[base + i] = ans[i]

    for p in range(base - 1, 0, -1):
        a = seg[p << 1]
        b = seg[p << 1 | 1]
        seg[p] = a if a < b else b

    def range_min(ql, qr, seg=seg, size_m=size_m, INF=INF):
        ql += size_m
        qr += size_m
        res = INF
        while ql <= qr:
            if ql & 1:
                v = seg[ql]
                if v < res:
                    res = v
                ql += 1
            if not (qr & 1):
                v = seg[qr]
                if v < res:
                    res = v
                qr -= 1
            ql >>= 1
            qr >>= 1
        return res

    out = []
    for k in range(Q):
        if range_min(qlist[k], rlist[k]) <= rlist[k]:
            out.append("No")
        else:
            out.append("Yes")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()