import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    PAIRS = {3: ((0, 1), (1, 0)), 5: ((0, 2), (2, 0)), 6: ((1, 2), (2, 1))}
    ALLV = (3, 5, 6)
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos + 1]); pos += 2
        M = K + K
        xs = [0] * N; ys = [0] * N; zs = [0] * N
        mv = [0] * N; cv = [0] * N
        for i in range(N):
            x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2]); pos += 3
            xs[i] = x; ys[i] = y; zs[i] = z
            if x >= y and x >= z:
                cv[i] = 0; mv[i] = x
            elif y >= z:
                cv[i] = 1; mv[i] = y
            else:
                cv[i] = 2; mv[i] = z
        order = sorted(range(N), key=mv.__getitem__, reverse=True)
        inT = [False] * N
        U = 0; p = 0
        for k in range(M):
            i = order[k]
            inT[i] = True
            U += mv[i]
            p ^= (1 << cv[i])
        if p == 0:
            out.append(str(U)); continue

        TL = [[], [], []]                                    # T items per colour: (m, idx)
        NH = [[], [], []]                                    # non-T items: (value in coord c, idx)
        RECl = [[[], [], []], [[], [], []], [[], [], []]]    # [src][tgt]: (recolour cost, idx)
        for i in range(N):
            if inT[i]:
                c = cv[i]; m = mv[i]
                TL[c].append((m, i))
                vv = (xs[i], ys[i], zs[i])
                for tc in range(3):
                    if tc != c:
                        RECl[c][tc].append((m - vv[tc], i))
            else:
                NH[0].append((xs[i], i))
                NH[1].append((ys[i], i))
                NH[2].append((zs[i], i))
        for c in range(3):
            TL[c].sort(); del TL[c][4:]
            for tc in range(3):
                RECl[c][tc].sort(); del RECl[c][tc][4:]
        for tc in range(3):
            NH[tc].sort(reverse=True); del NH[tc][4:]

        def cands(V):
            r = []
            for sc, tc in PAIRS[V]:
                for cost, i in RECl[sc][tc]:
                    r.append((cost, (i,)))
                for mi, i in TL[sc]:
                    for vj, j in NH[tc]:
                        r.append((mi - vj, (i, j)))
            return r

        cp = cands(p)
        gp = min(c for c, _ in cp)
        oth = [v for v in ALLV if v != p]
        cq = cands(oth[0]); cr = cands(oth[1])
        minc = None
        for c1, s1 in cq:
            a = s1[0]; b = s1[1] if len(s1) > 1 else -1
            for c2, s2 in cr:
                e = s2[0]; f = s2[1] if len(s2) > 1 else -1
                if a == e or a == f:
                    continue
                if b != -1 and (b == e or b == f):
                    continue
                s = c1 + c2
                if minc is None or s < minc:
                    minc = s
        L = gp
        if minc is not None and minc < L:
            L = minc
        out.append(str(U - L))
    sys.stdout.write("\n".join(out) + "\n")

main()