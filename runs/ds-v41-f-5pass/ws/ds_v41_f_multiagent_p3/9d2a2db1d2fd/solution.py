import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    H = data[0]; W = data[1]
    N = H * W
    F = data[2:2 + N]
    p = 2 + N
    Q = data[p]; p += 1

    base = [0] * Q
    low = [0] * Q
    qat = [None] * N
    has = False

    for q in range(Q):
        a = data[p]; b = data[p + 1]; y = data[p + 2]
        c = data[p + 3]; d = data[p + 4]; z = data[p + 5]
        p += 6
        u = (a - 1) * W + (b - 1)
        v = (c - 1) * W + (d - 1)
        diff = y - z
        if diff < 0:
            diff = -diff
        base[q] = diff
        low[q] = y if y < z else z
        if u != v:
            has = True
            l = qat[u]
            if l is None:
                qat[u] = [q]
            else:
                l.append(q)
            l = qat[v]
            if l is None:
                qat[v] = [q]
            else:
                l.append(q)

    ans = base[:]

    if has:
        par = list(range(N))
        sz = [1] * N
        comp = [None] * N
        active = bytearray(N)
        order = sorted(range(N), key=F.__getitem__, reverse=True)

        def find(x, par=par):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        def merge(ru, rv, w, par=par, sz=sz, comp=comp, ans=ans, low=low):
            if sz[ru] < sz[rv]:
                ru, rv = rv, ru
            sv = comp[rv]
            if sv is not None:
                su = comp[ru]
                if su is None:
                    comp[ru] = sv
                else:
                    if len(su) < len(sv):
                        su, sv = sv, su
                    for qid in sv:
                        if qid in su:
                            dd = low[qid] - w
                            if dd > 0:
                                ans[qid] += dd + dd
                            su.discard(qid)
                        else:
                            su.add(qid)
                    comp[ru] = su
                comp[rv] = None
            par[rv] = ru
            sz[ru] += sz[rv]
            return ru

        for c in order:
            active[c] = 1
            ql = qat[c]
            if ql is not None:
                comp[c] = set(ql)
            fc = F[c]
            ci = c // W
            rc = c
            if ci:
                dd = c - W
                if active[dd]:
                    rv = find(dd)
                    if rv != rc:
                        rc = merge(rc, rv, fc)
            if ci + 1 < H:
                dd = c + W
                if active[dd]:
                    rv = find(dd)
                    if rv != rc:
                        rc = merge(rc, rv, fc)
            cj = c - ci * W
            if cj:
                dd = c - 1
                if active[dd]:
                    rv = find(dd)
                    if rv != rc:
                        rc = merge(rc, rv, fc)
            if cj + 1 < W:
                dd = c + 1
                if active[dd]:
                    rv = find(dd)
                    if rv != rc:
                        rc = merge(rc, rv, fc)

    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

main()