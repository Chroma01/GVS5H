import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); pos += 1
    W = int(data[pos]); pos += 1
    A = [[0]*(W+2)]
    for _ in range(H):
        row = [0]*(W+2)
        for w in range(1, W+1):
            row[w] = int(data[pos]); pos += 1
        A.append(row)
    Q = int(data[pos]); pos += 1
    sh = int(data[pos]); pos += 1
    sw = int(data[pos]); pos += 1
    qs = []
    for _ in range(Q):
        d = data[pos]; pos += 1
        a = int(data[pos]); pos += 1
        qs.append((d, a))

    out = []
    B = 250
    h, w = sh, sw
    nblocks = (Q + B - 1)//B
    for blk in range(nblocks):
        lo = blk*B
        hi = min(Q, lo+B)
        # simulate moves to find dirty set and bounding box
        ch, cw = h, w
        cells = []
        cellset = set()
        for i in range(lo, hi):
            d, a = qs[i]
            if d == b'L': cw -= 1
            elif d == b'R': cw += 1
            elif d == b'U': ch -= 1
            else: ch += 1
            if (ch, cw) not in cellset:
                cellset.add((ch, cw))
                cells.append((ch, cw))
        rt = min(c[0] for c in cells); rb = max(c[0] for c in cells)
        ct = min(c[1] for c in cells); cb = max(c[1] for c in cells)
        # base F and G
        F = [[0]*(W+2) for _ in range(H+2)]
        F[0][1] = 1
        for i in range(1, H+1):
            Ai = A[i]; Fi = F[i]; Fim = F[i-1]
            s = 0
            for j in range(1, W+1):
                s = Ai[j] * ((Fim[j] + s) % MOD) % MOD
                Fi[j] = s
        base_ans = F[H][W]
        G = [[0]*(W+2) for _ in range(H+2)]
        G[H][W+1] = 1
        for i in range(H, 0, -1):
            Ai = A[i]; Gi = G[i]; Gip = G[i+1]
            s = 0
            for j in range(W, 0, -1):
                s = Ai[j] * ((Gip[j] + s) % MOD) % MOD
                Gi[j] = s
        # base through-box
        Fb = [[0]*(cb+2) for _ in range(rb+2)]
        Fbm1 = Fb[rt-1]
        Fm1 = F[rt-1]
        for j in range(ct, cb+1):
            Fbm1[j] = Fm1[j]
        ctm1 = ct-1
        for i in range(rt, rb+1):
            Fb[i][ctm1] = F[i][ctm1]
        for i in range(rt, rb+1):
            Ai = A[i]; Fbi = Fb[i]; Fbim = Fb[i-1]
            s = Fbi[ctm1]
            for j in range(ct, cb+1):
                s = Ai[j] * ((Fbim[j] + s) % MOD) % MOD
                Fbi[j] = s
        bt = 0
        Fbrb = Fb[rb]; Grbp1 = G[rb+1]
        for j in range(ct, cb+1):
            bt = (bt + Fbrb[j]*Grbp1[j]) % MOD
        cbp1 = cb+1
        for i in range(rt, rb+1):
            bt = (bt + Fb[i][cb]*G[i][cbp1]) % MOD
        # process queries
        cur = {}
        for i in range(lo, hi):
            d, a = qs[i]
            if d == b'L': w -= 1
            elif d == b'R': w += 1
            elif d == b'U': h -= 1
            else: h += 1
            cur[(h, w)] = a
            # build per-row override dicts once per query
            row_ov = {}
            for (ci, cj), cv in cur.items():
                rd = row_ov.get(ci)
                if rd is None:
                    row_ov[ci] = {cj: cv}
                else:
                    rd[cj] = cv
            # current through-box
            for j in range(ct, cb+1):
                Fbm1[j] = Fm1[j]
            for ii in range(rt, rb+1):
                Fb[ii][ctm1] = F[ii][ctm1]
            mod = MOD
            for ii in range(rt, rb+1):
                Ai = A[ii]; Fbi = Fb[ii]; Fbim = Fb[ii-1]
                ov = row_ov.get(ii)
                s = Fbi[ctm1]
                if ov is None:
                    for j in range(ct, cb+1):
                        s = Ai[j] * ((Fbim[j] + s) % mod) % mod
                        Fbi[j] = s
                else:
                    oget = ov.get
                    for j in range(ct, cb+1):
                        v = oget(j)
                        if v is None:
                            v = Ai[j]
                        s = v * ((Fbim[j] + s) % mod) % mod
                        Fbi[j] = s
            ct_through = 0
            Fbrb = Fb[rb]
            for j in range(ct, cb+1):
                ct_through = (ct_through + Fbrb[j]*Grbp1[j]) % MOD
            for ii in range(rt, rb+1):
                ct_through = (ct_through + Fb[ii][cb]*G[ii][cbp1]) % MOD
            ans = (base_ans - bt + ct_through) % MOD
            out.append(str(ans))
        # apply updates
        for (i, j), v in cur.items():
            A[i][j] = v
    sys.stdout.write('\n'.join(out) + '\n')

main()