import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    H = int(data[0]); W = int(data[1])
    N = H * W
    vals = list(map(int, data[2:2 + N]))
    p = 2 + N
    Q = int(data[p]); sh = int(data[p + 1]) - 1; sw = int(data[p + 2]) - 1
    p += 3
    D = H + W - 1

    lo = [0] * D
    ln = [0] * D
    Hm1 = H - 1
    for d in range(D):
        l = d - W + 1
        if l < 0:
            l = 0
        hi = d if d < Hm1 else Hm1
        lo[d] = l
        ln[d] = hi - l + 1
    sF = [0] * D          # sF[d] = lo[d]-lo[d-1]     (valid for d>=1)
    for d in range(1, D):
        sF[d] = lo[d] - lo[d - 1]
    sG = [0] * D          # sG[d] = lo[d]-lo[d+1]+1   (valid for d<=D-2)
    for d in range(D - 1):
        sG[d] = lo[d] - lo[d + 1] + 1

    step = W - 1
    maxL = 0
    for d in range(D):
        if ln[d] > maxL:
            maxL = ln[d]

    use_np = maxL >= 32
    if use_np:
        try:
            import numpy as np
        except Exception:
            use_np = False

    out = []
    h = sh
    w = sw
    pg = 0   # G valid on pg..D-1
    Dm1 = D - 1

    if use_np:
        Aflat = np.array(vals, dtype=np.int64)
        Adg = []
        for d in range(D):
            L = ln[d]
            st = lo[d] * W + (d - lo[d])
            Adg.append(Aflat[st: st + (L - 1) * step + 1: step].copy())
        Fa = [np.zeros(ln[d] + 2, dtype=np.int64) for d in range(D)]
        Ga = [np.zeros(ln[d] + 2, dtype=np.int64) for d in range(D)]
        Fc = [Fa[d][1:ln[d] + 1] for d in range(D)]
        Gc = [Ga[d][1:ln[d] + 1] for d in range(D)]
        add = np.add
        Fc[0][0] = vals[0]
        for d in range(1, D):
            s = sF[d]; prev = Fa[d - 1]; L = ln[d]; fc = Fc[d]
            add(prev[s:s + L], prev[s + 1:s + 1 + L], out=fc)
            fc *= Adg[d]
            fc %= MOD
        Gc[Dm1][0] = vals[N - 1]
        for d in range(D - 2, -1, -1):
            s = sG[d]; nxt = Ga[d + 1]; L = ln[d]; gc = Gc[d]
            add(nxt[s:s + L], nxt[s + 1:s + 1 + L], out=gc)
            gc *= Adg[d]
            gc %= MOD
        buf = np.empty(maxL, dtype=np.int64)
        for _ in range(Q):
            ch = data[p]; a = int(data[p + 1]); p += 2
            if ch == b'L':
                w -= 1
            elif ch == b'R':
                w += 1
            elif ch == b'U':
                h -= 1
            else:
                h += 1
            d = h + w
            L = ln[d]
            Adg[d][h - lo[d]] = a
            if pg < d + 1:
                pg = d + 1
            if pg == d + 2:
                e = d + 1
                if e < Dm1:
                    s = sG[e]; nxt = Ga[e + 1]; Le = ln[e]; gc = Gc[e]
                    add(nxt[s:s + Le], nxt[s + 1:s + 1 + Le], out=gc)
                    gc *= Adg[e]
                    gc %= MOD
                else:
                    Gc[Dm1][0] = int(Adg[Dm1][0])
                pg = d + 1
            if d == 0:
                Fc[0][0] = int(Adg[0][0])
            else:
                s = sF[d]; prev = Fa[d - 1]; fc = Fc[d]
                add(prev[s:s + L], prev[s + 1:s + 1 + L], out=fc)
                fc *= Adg[d]
                fc %= MOD
            if d == Dm1:
                out.append(str(int(Fc[Dm1][0])))
            else:
                s = sG[d]; g = Ga[d + 1]
                bb = buf[:L]
                add(g[s:s + L], g[s + 1:s + 1 + L], out=bb)
                bb *= Fc[d]
                bb %= MOD
                out.append(str(int(bb.sum() % MOD)))
    else:
        Adiag = []
        for d in range(D):
            L = ln[d]
            st = lo[d] * W + (d - lo[d])
            Adiag.append(vals[st: st + (L - 1) * step + 1: step])
        Fp = [None] * D
        Gp = [None] * D
        Fp[0] = [0, vals[0], 0]
        for d in range(1, D):
            s = sF[d]; prev = Fp[d - 1]; ad = Adiag[d]; L = ln[d]
            Fp[d] = [0] + [x * (y + z) % MOD for x, y, z in
                           zip(ad, prev[s:s + L], prev[s + 1:s + 1 + L])] + [0]
        Gp[Dm1] = [0, vals[N - 1], 0]
        for d in range(D - 2, -1, -1):
            s = sG[d]; nxt = Gp[d + 1]; ad = Adiag[d]; L = ln[d]
            Gp[d] = [0] + [x * (y + z) % MOD for x, y, z in
                           zip(ad, nxt[s:s + L], nxt[s + 1:s + 1 + L])] + [0]
        for _ in range(Q):
            ch = data[p]; a = int(data[p + 1]); p += 2
            if ch == b'L':
                w -= 1
            elif ch == b'R':
                w += 1
            elif ch == b'U':
                h -= 1
            else:
                h += 1
            d = h + w
            L = ln[d]
            Adiag[d][h - lo[d]] = a
            if pg < d + 1:
                pg = d + 1
            if pg == d + 2:
                e = d + 1
                if e < Dm1:
                    s = sG[e]; nxt = Gp[e + 1]; Le = ln[e]; ade = Adiag[e]
                    Gp[e][1:Le + 1] = [x * (y + z) % MOD for x, y, z in
                                       zip(ade, nxt[s:s + Le], nxt[s + 1:s + 1 + Le])]
                else:
                    Gp[Dm1][1] = Adiag[Dm1][0]
                pg = d + 1
            if d == 0:
                Fp[0][1] = Adiag[0][0]
            else:
                s = sF[d]; prev = Fp[d - 1]; ad = Adiag[d]
                Fp[d][1:L + 1] = [x * (y + z) % MOD for x, y, z in
                                  zip(ad, prev[s:s + L], prev[s + 1:s + 1 + L])]
            if d == Dm1:
                out.append(str(Fp[Dm1][1] % MOD))
            else:
                s = sG[d]; g = Gp[d + 1]; f = Fp[d]
                out.append(str(sum(fv * (x + y) for fv, x, y in
                                   zip(f[1:L + 1], g[s:s + L], g[s + 1:s + 1 + L])) % MOD))

    sys.stdout.write('\n'.join(out) + '\n')

main()