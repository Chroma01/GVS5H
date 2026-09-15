import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H0 = int(data[pos]); pos += 1
    W0 = int(data[pos]); pos += 1
    g = []
    for _ in range(H0):
        row = [int(x) for x in data[pos:pos+W0]]
        pos += W0
        g.append(row)
    Q = int(data[pos]); pos += 1
    sh = int(data[pos]); pos += 1
    sw = int(data[pos]); pos += 1

    trans = H0 > W0
    if trans:
        # new colA[w1][h1] = old grid[w1][h1]; new H=W0, new W=H0
        colA = [g[w1][:] for w1 in range(H0)]
        H = W0
        W = H0
        r = sw - 1
        c = sh - 1
    else:
        colA = [[g[h][w] for h in range(H0)] for w in range(W0)]
        H = H0
        W = W0
        r = sh - 1
        c = sw - 1

    MOD = 998244353

    pr = [[0] * H for _ in range(W)]
    sf = [[0] * H for _ in range(W)]

    # prefix vectors: pr[w][h] = F(h,w) = sum of path products (1,1)->(h,w) incl. endpoints
    ac0 = colA[0]; p0 = pr[0]
    acc = ac0[0] % MOD
    p0[0] = acc
    for h in range(1, H):
        acc = ac0[h] * acc % MOD
        p0[h] = acc
    for cc in range(1, W):
        pcv = pr[cc]; pcp = pr[cc - 1]; ac = colA[cc]
        prev = 0
        for h in range(H):
            t = prev + pcp[h]
            if t >= MOD:
                t -= MOD
            prev = ac[h] * t % MOD
            pcv[h] = prev

    # suffix vectors: sf[w][h] = G(h,w) = sum of products on paths (h,w)->(H,W) excluding (h,w)
    acl = colA[W - 1]; sfl = sf[W - 1]
    sfl[H - 1] = 1
    for h in range(H - 2, -1, -1):
        sfl[h] = acl[h + 1] * sfl[h + 1] % MOD
    for cc in range(W - 2, -1, -1):
        scv = sf[cc]; scn = sf[cc + 1]; ac = colA[cc]; acn = colA[cc + 1]
        for h in range(H - 1, -1, -1):
            if h + 1 < H:
                scv[h] = (ac[h + 1] * scv[h + 1] + acn[h] * scn[h]) % MOD
            else:
                scv[h] = acn[h] * scn[h] % MOD

    ans = pr[W - 1][H - 1] % MOD
    out = []
    append = out.append

    for _ in range(Q):
        d0 = data[pos][0]; pos += 1
        a = int(data[pos]); pos += 1
        if trans:
            if d0 == 85:       # U -> L
                d0 = 76
            elif d0 == 76:     # L -> U
                d0 = 85
            elif d0 == 82:     # R -> D
                d0 = 68
            else:              # D -> R
                d0 = 82

        if d0 == 68:           # D
            r += 1
        elif d0 == 85:         # U
            r -= 1
        elif d0 == 82:         # R
            c += 1
            pcp = pr[c - 1]; pcv = pr[c]; ac = colA[c]
            prev = 0
            for h in range(H):
                t = prev + pcp[h]
                if t >= MOD:
                    t -= MOD
                prev = ac[h] * t % MOD
                pcv[h] = prev
        else:                  # L
            c -= 1
            scn = sf[c + 1]; scv = sf[c]; ac = colA[c]; acn = colA[c + 1]
            scv[H - 1] = acn[H - 1] * scn[H - 1] % MOD
            for h in range(H - 2, -1, -1):
                scv[h] = (ac[h + 1] * scv[h + 1] + acn[h] * scn[h]) % MOD

        # p = prefix excluding current cell
        pval = 0
        if r > 0:
            pval = pr[c][r - 1]
        if c > 0:
            pval += pr[c - 1][r]
        pval %= MOD
        gval = sf[c][r]

        cur = colA[c]
        old = cur[r]
        if a != old:
            delta = (a - old) * pval % MOD * gval % MOD
            ans = (ans + delta) % MOD
            cur[r] = a

            # fix pr[c] rows >= r
            pcv = pr[c]; ac = colA[c]
            if c > 0:
                pcp = pr[c - 1]
                prev = pcv[r - 1] if r > 0 else 0
                for h in range(r, H):
                    t = prev + pcp[h]
                    if t >= MOD:
                        t -= MOD
                    prev = ac[h] * t % MOD
                    pcv[h] = prev
            else:
                prev = pcv[r - 1] if r > 0 else 0
                for h in range(r, H):
                    if h == 0:
                        prev = ac[0] % MOD
                    else:
                        prev = ac[h] * prev % MOD
                    pcv[h] = prev

            # fix sf[c] rows < r
            scv = sf[c]
            if c + 1 < W:
                scn = sf[c + 1]; acn = colA[c + 1]
                for h in range(r - 1, -1, -1):
                    scv[h] = (ac[h + 1] * scv[h + 1] + acn[h] * scn[h]) % MOD
            else:
                for h in range(r - 1, -1, -1):
                    scv[h] = ac[h + 1] * scv[h + 1] % MOD

        append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")

main()