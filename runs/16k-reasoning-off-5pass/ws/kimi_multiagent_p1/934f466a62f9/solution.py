import sys
from collections import defaultdict

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos+1]); pos += 2
        V = []
        for i in range(N):
            x = int(data[pos]); y = int(data[pos+1]); z = int(data[pos+2]); pos += 3
            V.append((x, y, z))
        m = [max(v) for v in V]
        idx = sorted(range(N), key=lambda i: -m[i])
        S = idx[:2*K]
        O = idx[2*K:]
        base = sum(m[i] for i in S)

        def mask(i):
            x, y, z = V[i]
            mm = m[i]
            r = 0
            if x == mm: r |= 1
            if y == mm: r |= 2
            if z == mm: r |= 4
            return r

        def w(i, c):
            return m[i] - V[i][c]

        parity = [0, 0, 0]
        flex = []
        for i in S:
            mk = mask(i)
            if mk in (1, 2, 4):
                c = {1:0, 2:1, 4:2}[mk]
                parity[c] ^= 1
            else:
                flex.append((mk, i))

        ftype = defaultdict(int)
        for mk, i in flex:
            ftype[mk] += 1

        def flex_feasible(p, fcounts):
            needs = [c for c in range(3) if p[c]]
            tot = sum(fcounts.values())
            if not needs:
                return tot % 2 == 0
            a, b = needs
            if tot < 2:
                return False
            ca = sum(cnt for mk, cnt in fcounts.items() if mk >> a & 1)
            cb = sum(cnt for mk, cnt in fcounts.items() if mk >> b & 1)
            cab = sum(cnt for mk, cnt in fcounts.items() if (mk >> a & 1) and (mk >> b & 1))
            pairs = ca * cb - cab
            return pairs > 0

        INF = float('inf')

        min_recolor_fixed = [[INF]*3 for _ in range(3)]
        for i in S:
            mk = mask(i)
            if mk in (1, 2, 4):
                u = {1:0, 2:1, 4:2}[mk]
                for c in range(3):
                    if c != u:
                        wi = w(i, c)
                        if wi < min_recolor_fixed[u][c]:
                            min_recolor_fixed[u][c] = wi

        best_in = [-1]*3
        for j in O:
            for c in range(3):
                if V[j][c] > best_in[c]:
                    best_in[c] = V[j][c]

        min_m_class = [INF]*3
        for i in S:
            mk = mask(i)
            if mk in (1, 2, 4):
                u = {1:0, 2:1, 4:2}[mk]
                if m[i] < min_m_class[u]:
                    min_m_class[u] = m[i]

        flex_min_m_by_mask = {}
        flex_min_w_by_mask_c = {}
        for mk, i in flex:
            if mk not in flex_min_m_by_mask or m[i] < flex_min_m_by_mask[mk]:
                flex_min_m_by_mask[mk] = m[i]
            for c in range(3):
                if not (mk >> c & 1):
                    wi = w(i, c)
                    key = (mk, c)
                    if key not in flex_min_w_by_mask_c or wi < flex_min_w_by_mask_c[key]:
                        flex_min_w_by_mask_c[key] = wi

        actions = []
        for u in range(3):
            for v in range(3):
                if u != v and min_recolor_fixed[u][v] < INF:
                    d = [0,0,0]; d[u]^=1; d[v]^=1
                    actions.append((min_recolor_fixed[u][v], tuple(d), None))
        for (mk, c), wi in flex_min_w_by_mask_c.items():
            d = [0,0,0]; d[c]^=1
            actions.append((wi, tuple(d), mk))
        for u in range(3):
            if min_m_class[u] < INF:
                for c in range(3):
                    if best_in[c] >= 0:
                        d = [0,0,0]; d[u]^=1; d[c]^=1
                        actions.append((min_m_class[u] - best_in[c], tuple(d), None))
        for mk, mm in flex_min_m_by_mask.items():
            for c in range(3):
                if best_in[c] >= 0:
                    d = [0,0,0]; d[c]^=1
                    actions.append((mm - best_in[c], tuple(d), mk))

        start_p = tuple(parity)
        best_fix = INF
        if flex_feasible(list(start_p), ftype):
            best_fix = 0
        for cost, d, fmask in actions:
            p2 = [start_p[c]^d[c] for c in range(3)]
            fc = dict(ftype)
            if fmask is not None:
                fc[fmask] -= 1
                if fc[fmask] == 0: del fc[fmask]
            if flex_feasible(p2, fc):
                if cost < best_fix: best_fix = cost
        A = len(actions)
        for a1 in range(A):
            c1, d1, fm1 = actions[a1]
            for a2 in range(A):
                c2, d2, fm2 = actions[a2]
                p2 = [start_p[c]^d1[c]^d2[c] for c in range(3)]
                fc = dict(ftype)
                ok = True
                for fmask in (fm1, fm2):
                    if fmask is not None:
                        if fc.get(fmask, 0) <= 0:
                            ok = False; break
                        fc[fmask] -= 1
                        if fc[fmask] == 0: del fc[fmask]
                if not ok: continue
                if flex_feasible(p2, fc):
                    tot = c1 + c2
                    if tot < best_fix: best_fix = tot

        out.append(str(base - best_fix))
    sys.stdout.write("\n".join(out) + "\n")

solve()