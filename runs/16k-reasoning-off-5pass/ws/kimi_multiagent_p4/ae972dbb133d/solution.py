import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    allowed = {
        0: [(1,1,0,0), (0,1,1,0), (0,0,1,1), (1,0,0,1)],  # A: adjacent pairs (t,r,b,l)
        1: [(1,0,1,0), (0,1,0,1)],                          # B: opposite pairs
    }
    # trans[typ][t][l] = list of (r, b)
    trans = []
    for typ in (0, 1):
        tab = [[[] for _ in range(2)] for _ in range(2)]
        for (t, r, b, l) in allowed[typ]:
            tab[t][l].append((r, b))
        trans.append(tab)

    for _ in range(T):
        H = int(data[idx]); W = int(data[idx+1]); idx += 2
        rows = [data[idx + i].decode() for i in range(H)]
        idx += H
        # transpose so that W = min dimension (DP width)
        if H < W:
            rows = [''.join(rows[i][j] for i in range(H)) for j in range(W)]
            H, W = W, H
        m = W
        g = [[0 if rows[i][j] == 'A' else 1 for j in range(m)] for i in range(H)]

        # dp: key = (seam << m) | front -> count
        # seam = top edges of row 0 (must equal final frontier: vertical torus wrap)
        # front bit j = bottom edge of the last processed cell in column j
        dp = {}
        for s in range(1 << m):
            dp[(s << m) | s] = 1

        for i in range(H):
            grow = g[i]
            tabs = [trans[grow[j]] for j in range(m)]
            newdp = {}
            mask = (1 << m) - 1
            for key0, cnt in dp.items():
                seam = key0 >> m
                front = key0 & mask
                # h_start = left edge of cell (i,0); last cell's right edge must equal it
                for h_start in (0, 1):
                    cur = {(front << 1) | h_start: cnt}
                    for j in range(m):
                        tab = tabs[j]
                        bit = 1 << j
                        nxt = {}
                        for st, c in cur.items():
                            fr = st >> 1
                            l = st & 1
                            t = (fr >> j) & 1
                            for (r, b) in tab[t][l]:
                                fr2 = (fr & ~bit) | (b << j)
                                k = (fr2 << 1) | r
                                v = nxt.get(k, 0) + c
                                if v >= MOD:
                                    v -= MOD
                                nxt[k] = v
                        cur = nxt
                    for st, c in cur.items():
                        if (st & 1) == h_start:
                            fr = st >> 1
                            k = (seam << m) | fr
                            v = newdp.get(k, 0) + c
                            if v >= MOD:
                                v -= MOD
                            newdp[k] = v
            dp = newdp

        ans = 0
        for key, c in dp.items():
            if (key >> m) == (key & ((1 << m) - 1)):
                ans = (ans + c) % MOD
        out.append(ans)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()