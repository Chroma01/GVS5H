import sys
from heapq import nsmallest, nlargest
from operator import sub


def main():
    data = sys.stdin.buffer.read().split()
    T = int(data[0])
    pos = 1
    INF = 1 << 60

    # all simple paths s -> t in the 4-node graph {0,1,2 = labels, 3 = W}
    SH = {}
    for s in range(3):
        for t in range(3):
            if s != t:
                r = 3 - s - t
                SH[(s, t)] = (((s, t),),
                              ((s, r), (r, t)),
                              ((s, 3), (3, t)),
                              ((s, r), (r, 3), (3, t)),
                              ((s, 3), (3, r), (r, t)))

    out = []
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos + 1]); pos += 2
        e = pos + 3 * N
        ch = data[pos:e]; pos = e
        X = list(map(int, ch[0::3]))
        Y = list(map(int, ch[1::3]))
        Z = list(map(int, ch[2::3]))
        mm = list(map(max, X, Y, Z))
        K2 = K + K
        order = sorted(range(N), key=mm.__getitem__, reverse=True)
        sel = order[:K2]
        M = sum(map(mm.__getitem__, sel))
        lab = [0 if v == x else (1 if v == y else 2) for v, x, y in zip(mm, X, Y)]
        g = ([], [], [])
        for i in sel:
            g[lab[i]].append(i)
        c0 = len(g[0]); c1 = len(g[1]); c2 = len(g[2])
        if not ((c0 | c1 | c2) & 1):
            out.append(M)
            continue
        cnt = (c0, c1, c2)
        odd = [u for u in range(3) if cnt[u] & 1]
        p = odd[0]; q = odd[1]; r = 3 - p - q
        V = (X, Y, Z)
        dif = (list(map(sub, mm, X)), list(map(sub, mm, Y)), list(map(sub, mm, Z)))
        uns = order[K2:]

        # L[group][type] = up to 2 cheapest (cost, cake_id)
        L = [[(), (), (), ()] for _ in range(4)]
        for u in range(3):
            gu = g[u]
            if not gu:
                continue
            for b in range(3):
                if b == u:
                    continue
                db = dif[b]
                L[u][b] = tuple((db[i], i) for i in nsmallest(2, gu, key=db.__getitem__))
            L[u][3] = tuple((mm[i], i) for i in nsmallest(2, gu, key=mm.__getitem__))
        if uns:
            for v in range(3):
                Vv = V[v]
                L[3][v] = tuple((-Vv[i], i) for i in nlargest(2, uns, key=Vv.__getitem__))

        C1 = [[INF] * 4 for _ in range(4)]
        C2 = [[[INF] * 4 for _ in range(4)] for _ in range(4)]
        for gr in range(4):
            Lg = L[gr]
            C1g = C1[gr]
            C2g = C2[gr]
            for b in range(4):
                Lb = Lg[b]
                if not Lb:
                    continue
                C1g[b] = Lb[0][0]
                for b2 in range(b, 4):
                    Lb2 = Lg[b2]
                    if not Lb2:
                        continue
                    bst = INF
                    for ca, ia in Lb:
                        for cb, ib in Lb2:
                            if ia != ib:
                                sm = ca + cb
                                if sm < bst:
                                    bst = sm
                    C2g[b][b2] = bst
                    C2g[b2][b] = bst

        best = INF
        # divergence (+1,-1,0) and (-1,+1,0): a single simple path
        for st in ((p, q), (q, p)):
            for sh in SH[st]:
                tot = 0
                for a, b in sh:
                    tot += C1[a][b]
                if tot < best:
                    best = tot
        # divergence (+1,+1,-2) and (-1,-1,+2): two simple paths, cakes distinct
        for a1, a2 in (((p, r), (q, r)), ((r, p), (r, q))):
            l1 = [sh for sh in SH[a1] if all(C1[a][b] < INF for a, b in sh)]
            if not l1:
                continue
            l2 = [sh for sh in SH[a2] if all(C1[a][b] < INF for a, b in sh)]
            if not l2:
                continue
            for sh1 in l1:
                for sh2 in l2:
                    d0 = []; d1 = []; d2 = []; d3 = []
                    dem = (d0, d1, d2, d3)
                    for a, b in sh1:
                        dem[a].append(b)
                    for a, b in sh2:
                        dem[a].append(b)
                    tot = 0
                    for gr in range(4):
                        d = dem[gr]
                        n = len(d)
                        if n == 1:
                            tot += C1[gr][d[0]]
                        elif n == 2:
                            tot += C2[gr][d[0]][d[1]]
                    if tot < best:
                        best = tot
        out.append(M - best)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()