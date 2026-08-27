import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    N = H * W

    def toint(tokens, cnt):
        try:
            return np.array(tokens, dtype=np.int64)
        except Exception:
            return np.fromiter(map(int, tokens), dtype=np.int64, count=cnt)

    Fflat = toint(data[2:2 + N], N)
    pos = 2 + N
    Q = int(data[pos]); pos += 1
    qtok = data[pos:pos + 6 * Q]
    qa = toint(qtok, 6 * Q).reshape(Q, 6)
    A = qa[:, 0]; B = qa[:, 1]; Y = qa[:, 2]
    C = qa[:, 3]; D = qa[:, 4]; Z = qa[:, 5]

    F2 = Fflat.reshape(H, W)
    idx = np.arange(N, dtype=np.int64).reshape(H, W)

    eus = []
    evs = []
    ews = []
    if W > 1:
        eus.append(idx[:, :-1].ravel())
        evs.append(idx[:, 1:].ravel())
        ews.append(np.minimum(F2[:, :-1], F2[:, 1:]).ravel())
    if H > 1:
        eus.append(idx[:-1, :].ravel())
        evs.append(idx[1:, :].ravel())
        ews.append(np.minimum(F2[:-1, :], F2[1:, :]).ravel())

    total = 2 * N - 1
    par = list(range(total))
    wt = [0] * total
    wt[:N] = Fflat.tolist()

    if eus:
        eu = np.concatenate(eus)
        ev = np.concatenate(evs)
        ew = np.concatenate(ews)
        # try scipy maximum spanning tree to shrink edge count
        try:
            from scipy.sparse import coo_matrix
            from scipy.sparse.csgraph import minimum_spanning_tree
            Cc = 1000001
            dat = (Cc - ew).astype(np.float64)
            g = coo_matrix((dat, (eu, ev)), shape=(N, N)).tocsr()
            mst = minimum_spanning_tree(g)
            mc = mst.tocoo()
            if mc.nnz == N - 1:
                eu = mc.row.astype(np.int64)
                ev = mc.col.astype(np.int64)
                ew = (Cc - mc.data).astype(np.int64)
        except Exception:
            pass

        order = np.argsort(-ew, kind='stable')
        eul = eu[order].tolist()
        evl = ev[order].tolist()
        ewl = ew[order].tolist()

        dsu = list(range(total))
        cnt = N
        for u, v, w in zip(eul, evl, ewl):
            ru = u
            while dsu[ru] != ru:
                dsu[ru] = dsu[dsu[ru]]
                ru = dsu[ru]
            rv = v
            while dsu[rv] != rv:
                dsu[rv] = dsu[dsu[rv]]
                rv = dsu[rv]
            if ru == rv:
                continue
            par[ru] = cnt
            par[rv] = cnt
            dsu[ru] = cnt
            dsu[rv] = cnt
            wt[cnt] = w
            cnt += 1
            if cnt == total:
                break

    # depth: parents always have larger ids than children
    depth_l = [0] * total
    for i in range(total - 2, -1, -1):
        depth_l[i] = depth_l[par[i]] + 1

    depth = np.array(depth_l, dtype=np.int32)
    wtarr = np.array(wt, dtype=np.int64)

    LOG = max(1, int(total).bit_length())
    up = [np.array(par, dtype=np.int32)]
    for k in range(1, LOG):
        prev = up[k - 1]
        up.append(prev[prev])

    lu = ((A - 1) * W + (B - 1)).astype(np.int32)
    lv = ((C - 1) * W + (D - 1)).astype(np.int32)
    du = depth[lu]
    dv = depth[lv]
    sw = du < dv
    u = np.where(sw, lv, lu).astype(np.int32)
    v = np.where(sw, lu, lv).astype(np.int32)
    diff = np.abs(du.astype(np.int64) - dv.astype(np.int64))

    for k in range(LOG):
        sh = diff >> k
        if not sh.any():
            break
        mask = (sh & 1).astype(bool)
        if mask.any():
            u[mask] = up[k][u[mask]]

    same = (u == v)
    ueq = u.copy()

    for k in range(LOG - 1, -1, -1):
        uk = up[k]
        pu = uk[u]
        pv = uk[v]
        mask = pu != pv
        if mask.any():
            u = np.where(mask, pu, u)
            v = np.where(mask, pv, v)

    lca = np.where(same, ueq, up[0][u]).astype(np.int64)
    Bq = wtarr[lca]

    ans = Y + Z - 2 * np.minimum(np.minimum(Y, Z), Bq)
    sys.stdout.write("\n".join(map(str, ans.tolist())))
    sys.stdout.write("\n")


main()