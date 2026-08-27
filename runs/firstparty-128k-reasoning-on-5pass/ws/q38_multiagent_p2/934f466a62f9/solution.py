import sys

INF = 10**30


def combine_top2(c1, id1, c2, id2, best, off1, off2, toff):
    for m1 in range(8):
        i1 = off1 + m1
        a1c = c1[i1]
        a1id = id1[i1]
        if a1id < 0:
            continue
        a2c = c2[i1]
        a2id = id2[i1]
        for m2 in range(8):
            i2 = off2 + m2
            b1c = c1[i2]
            b1id = id1[i2]
            if b1id < 0:
                continue
            b2c = c2[i2]
            b2id = id2[i2]
            ti = toff + (m1 ^ m2)
            if i1 == i2:
                if a2id >= 0 and a1id != a2id:
                    val = a1c + a2c
                    if val < best[ti]:
                        best[ti] = val
            else:
                if a1id != b1id:
                    val = a1c + b1c
                    if val < best[ti]:
                        best[ti] = val
                if b2id >= 0 and a1id != b2id:
                    val = a1c + b2c
                    if val < best[ti]:
                        best[ti] = val
                if a2id >= 0 and a2id != b1id:
                    val = a2c + b1c
                    if val < best[ti]:
                        best[ti] = val
                if a2id >= 0 and b2id >= 0 and a2id != b2id:
                    val = a2c + b2c
                    if val < best[ti]:
                        best[ti] = val


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    T = next(it)
    out = []
    INF_LOCAL = INF

    for _ in range(T):
        N = next(it)
        K = next(it)
        x = [0] * N
        y = [0] * N
        z = [0] * N
        s = [0] * N

        for i in range(N):
            xi = next(it)
            yi = next(it)
            zi = next(it)
            x[i] = xi
            y[i] = yi
            z[i] = zi
            m = xi
            if yi > m:
                m = yi
            if zi > m:
                m = zi
            s[i] = m

        order = list(range(N))
        order.sort(key=s.__getitem__, reverse=True)
        M = 2 * K

        # selected-side top two candidates:
        # state 0: (r=0,q=0), 1: (1,0), 2: (2,0), 3: (0,1), 4: (1,1), 5: (0,2)
        sc1 = [INF_LOCAL] * 48
        sid1 = [-1] * 48
        sc2 = [INF_LOCAL] * 48
        sid2 = [-1] * 48

        # unselected-side top two candidates for one addition, by color mask
        ac1 = [INF_LOCAL] * 8
        aid1 = [-1] * 8
        ac2 = [INF_LOCAL] * 8
        aid2 = [-1] * 8

        B = 0
        p = 0

        for pos in range(N):
            i = order[pos]
            xi = x[i]
            yi = y[i]
            zi = z[i]
            si = s[i]

            if pos < M:
                B += si
                if xi == si:
                    c = 0
                elif yi == si:
                    c = 1
                else:
                    c = 2
                p ^= (1 << c)

                # remove this selected cake: state (r=1,q=0), mask = c
                u = 8 + (1 << c)
                cost = si
                if cost < sc1[u]:
                    sc2[u] = sc1[u]
                    sid2[u] = sid1[u]
                    sc1[u] = cost
                    sid1[u] = i
                elif cost < sc2[u]:
                    sc2[u] = cost
                    sid2[u] = i

                # recolor this selected cake: state (r=0,q=1)
                if c == 0:
                    u = 27  # mask 3
                    cost = si - yi
                    if cost < sc1[u]:
                        sc2[u] = sc1[u]
                        sid2[u] = sid1[u]
                        sc1[u] = cost
                        sid1[u] = i
                    elif cost < sc2[u]:
                        sc2[u] = cost
                        sid2[u] = i

                    u = 29  # mask 5
                    cost = si - zi
                    if cost < sc1[u]:
                        sc2[u] = sc1[u]
                        sid2[u] = sid1[u]
                        sc1[u] = cost
                        sid1[u] = i
                    elif cost < sc2[u]:
                        sc2[u] = cost
                        sid2[u] = i

                elif c == 1:
                    u = 27  # mask 3
                    cost = si - xi
                    if cost < sc1[u]:
                        sc2[u] = sc1[u]
                        sid2[u] = sid1[u]
                        sc1[u] = cost
                        sid1[u] = i
                    elif cost < sc2[u]:
                        sc2[u] = cost
                        sid2[u] = i

                    u = 30  # mask 6
                    cost = si - zi
                    if cost < sc1[u]:
                        sc2[u] = sc1[u]
                        sid2[u] = sid1[u]
                        sc1[u] = cost
                        sid1[u] = i
                    elif cost < sc2[u]:
                        sc2[u] = cost
                        sid2[u] = i

                else:
                    u = 29  # mask 5
                    cost = si - xi
                    if cost < sc1[u]:
                        sc2[u] = sc1[u]
                        sid2[u] = sid1[u]
                        sc1[u] = cost
                        sid1[u] = i
                    elif cost < sc2[u]:
                        sc2[u] = cost
                        sid2[u] = i

                    u = 30  # mask 6
                    cost = si - yi
                    if cost < sc1[u]:
                        sc2[u] = sc1[u]
                        sid2[u] = sid1[u]
                        sc1[u] = cost
                        sid1[u] = i
                    elif cost < sc2[u]:
                        sc2[u] = cost
                        sid2[u] = i

            else:
                # add this unselected cake with color 0/1/2: cost = -value
                u = 1
                cost = -xi
                if cost < ac1[u]:
                    ac2[u] = ac1[u]
                    aid2[u] = aid1[u]
                    ac1[u] = cost
                    aid1[u] = i
                elif cost < ac2[u]:
                    ac2[u] = cost
                    aid2[u] = i

                u = 2
                cost = -yi
                if cost < ac1[u]:
                    ac2[u] = ac1[u]
                    aid2[u] = aid1[u]
                    ac1[u] = cost
                    aid1[u] = i
                elif cost < ac2[u]:
                    ac2[u] = cost
                    aid2[u] = i

                u = 4
                cost = -zi
                if cost < ac1[u]:
                    ac2[u] = ac1[u]
                    aid2[u] = aid1[u]
                    ac1[u] = cost
                    aid1[u] = i
                elif cost < ac2[u]:
                    ac2[u] = cost
                    aid2[u] = i

        sel_best = [INF_LOCAL] * 48
        sel_best[0] = 0

        # one selected action
        for mask in range(8):
            c = sc1[8 + mask]
            if c < sel_best[8 + mask]:
                sel_best[8 + mask] = c
            c = sc1[24 + mask]
            if c < sel_best[24 + mask]:
                sel_best[24 + mask] = c

        # two selected actions
        combine_top2(sc1, sid1, sc2, sid2, sel_best, 8, 8, 16)    # two removals
        combine_top2(sc1, sid1, sc2, sid2, sel_best, 8, 24, 32)   # removal + recolor
        combine_top2(sc1, sid1, sc2, sid2, sel_best, 24, 24, 40)  # two recolors

        un_best = [INF_LOCAL] * 24
        un_best[0] = 0

        # one addition
        for mask in range(8):
            c = ac1[mask]
            if c < un_best[8 + mask]:
                un_best[8 + mask] = c

        # two additions
        combine_top2(ac1, aid1, ac2, aid2, un_best, 0, 0, 16)

        loss = INF_LOCAL
        # (r, selected-state offset), where r = number of removals = number of additions
        for r, off in ((0, 0), (0, 24), (0, 40), (1, 8), (1, 32), (2, 16)):
            ub_off = r * 8
            for ms in range(8):
                cs = sel_best[off + ms]
                if cs >= INF_LOCAL:
                    continue
                cu = un_best[ub_off + (ms ^ p)]
                if cu < INF_LOCAL:
                    val = cs + cu
                    if val < loss:
                        loss = val

        out.append(str(B - loss))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()