import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    H = int(next(it))
    W = int(next(it))

    # Orient the grid so that R = min(H, W).
    if H <= W:
        R, C = H, W
        trans = False
        A = [[0] * R for _ in range(C)]
        for r in range(H):
            for c in range(W):
                A[c][r] = int(next(it))
    else:
        R, C = W, H
        trans = True
        A = [[0] * R for _ in range(C)]
        for r in range(H):
            col = A[r]
            for c in range(W):
                col[c] = int(next(it))

    Q = int(next(it))
    sh = int(next(it))
    sw = int(next(it))

    if trans:
        cur_r = sw - 1
        cur_c = sh - 1
    else:
        cur_r = sh - 1
        cur_c = sw - 1

    mod = MOD
    last_r = R - 1
    last_c = C - 1

    F = [[0] * R for _ in range(C)]
    G = [[0] * R for _ in range(C)]

    # Initial forward DP: F[c][r] = sum of products from (0,0) to (r,c), including (r,c).
    for c in range(C):
        colA = A[c]
        colF = F[c]
        if c == 0:
            colF[0] = colA[0]
            for i in range(1, R):
                colF[i] = (colA[i] * colF[i - 1]) % mod
        else:
            prev = F[c - 1]
            colF[0] = (colA[0] * prev[0]) % mod
            for i in range(1, R):
                s = prev[i] + colF[i - 1]
                if s >= mod:
                    s -= mod
                colF[i] = (colA[i] * s) % mod

    # Initial backward DP: G[c][r] = sum of products from (r,c) to (R-1,C-1), including (r,c).
    for c in range(C - 1, -1, -1):
        colA = A[c]
        colG = G[c]
        if c == last_c:
            colG[last_r] = colA[last_r]
            for i in range(last_r - 1, -1, -1):
                colG[i] = (colA[i] * colG[i + 1]) % mod
        else:
            nxt = G[c + 1]
            colG[last_r] = (colA[last_r] * nxt[last_r]) % mod
            for i in range(last_r - 1, -1, -1):
                s = nxt[i] + colG[i + 1]
                if s >= mod:
                    s -= mod
                colG[i] = (colA[i] * s) % mod

    # Initial answer.
    if cur_c < last_c:
        f = F[cur_c]
        g = G[cur_c + 1]
        ans = 0
        for i in range(R):
            ans = (ans + f[i] * g[i]) % mod
    else:
        ans = F[cur_c][last_r]

    # Precomputed ranges for the inner loops.
    rb = [range(1, i) for i in range(R)]                 # 1 .. r-1
    ra = [range(i + 1, R) for i in range(R)]             # r+1 .. R-1
    ru = [range(i - 1, -1, -1) for i in range(R)]        # r-1 .. 0
    rda = [range(last_r - 1, i, -1) for i in range(R)]   # R-2 .. r+1

    # Direction maps in the oriented grid.
    dr = [0] * 256
    dc = [0] * 256
    if trans:
        # Original L -> new U, R -> new D, U -> new L, D -> new R.
        dr[76] = -1
        dc[76] = 0
        dr[82] = 1
        dc[82] = 0
        dr[85] = 0
        dc[85] = -1
        dr[68] = 0
        dc[68] = 1
    else:
        dr[85] = -1
        dc[85] = 0
        dr[68] = 1
        dc[68] = 0
        dr[76] = 0
        dc[76] = -1
        dr[82] = 0
        dc[82] = 1

    out = []
    append = out.append

    for _ in range(Q):
        ch = next(it)[0]
        a = int(next(it))

        step = dc[ch]
        nr = cur_r + dr[ch]
        nc = cur_c + step

        old = A[nc][nr]
        delta = a - old
        if delta < 0:
            delta += mod
        A[nc][nr] = a

        if step == 0:
            # Vertical move: updated column is the current column.
            if delta:
                c = cur_c
                r = nr

                # p = sum of prefix products to (r,c), excluding (r,c).
                if c == 0:
                    p = 1 if r == 0 else F[c][r - 1]
                else:
                    p = F[c - 1][r]
                    if r > 0:
                        p += F[c][r - 1]
                        if p >= mod:
                            p -= mod

                # s = sum of suffix products from (r,c) to end, excluding (r,c).
                if c == last_c:
                    s = 1 if r == last_r else G[c][r + 1]
                else:
                    s = G[c + 1][r]
                    if r < last_r:
                        s += G[c][r + 1]
                        if s >= mod:
                            s -= mod

                ans = (ans + delta * p * s) % mod

                colA = A[c]

                dF = (delta * p) % mod
                if dF:
                    colF = F[c]
                    v = colF[r] + dF
                    if v >= mod:
                        v -= mod
                    colF[r] = v
                    d = dF
                    for i in ra[r]:
                        d = (d * colA[i]) % mod
                        if d == 0:
                            break
                        v = colF[i] + d
                        if v >= mod:
                            v -= mod
                        colF[i] = v

                dG = (delta * s) % mod
                if dG:
                    colG = G[c]
                    v = colG[r] + dG
                    if v >= mod:
                        v -= mod
                    colG[r] = v
                    d = dG
                    for i in ru[r]:
                        d = (d * colA[i]) % mod
                        if d == 0:
                            break
                        v = colG[i] + d
                        if v >= mod:
                            v -= mod
                        colG[i] = v

            cur_r = nr

        elif step == 1:
            # Move right: enter column c = cur_c + 1.
            c = nc
            r = nr

            # F[c] may be stale; recompute it fully from F[c-1].
            colA = A[c]
            colF = F[c]
            prev = F[c - 1]

            if r > 0:
                colF[0] = (colA[0] * prev[0]) % mod
                for i in rb[r]:
                    sm = prev[i] + colF[i - 1]
                    if sm >= mod:
                        sm -= mod
                    colF[i] = (colA[i] * sm) % mod
                p = prev[r] + colF[r - 1]
                if p >= mod:
                    p -= mod
            else:
                p = prev[0]

            colF[r] = (colA[r] * p) % mod
            for i in ra[r]:
                sm = prev[i] + colF[i - 1]
                if sm >= mod:
                    sm -= mod
                colF[i] = (colA[i] * sm) % mod

            if delta:
                # G[c] is correct before the update; compute s and update G[c] partially.
                if c == last_c:
                    s = 1 if r == last_r else G[c][r + 1]
                else:
                    s = G[c + 1][r]
                    if r < last_r:
                        s += G[c][r + 1]
                        if s >= mod:
                            s -= mod

                ans = (ans + delta * p * s) % mod

                dG = (delta * s) % mod
                if dG:
                    colG = G[c]
                    v = colG[r] + dG
                    if v >= mod:
                        v -= mod
                    colG[r] = v
                    d = dG
                    for i in ru[r]:
                        d = (d * colA[i]) % mod
                        if d == 0:
                            break
                        v = colG[i] + d
                        if v >= mod:
                            v -= mod
                        colG[i] = v

            cur_c = c
            cur_r = r

        else:
            # Move left: enter column c = cur_c - 1.
            c = nc
            r = nr

            # G[c] may be stale; recompute it fully from G[c+1].
            colA = A[c]
            colG = G[c]

            if c == last_c:
                if r < last_r:
                    colG[last_r] = colA[last_r]
                    for i in rda[r]:
                        sm = colG[i + 1]
                        colG[i] = (colA[i] * sm) % mod
                    s = colG[r + 1]
                else:
                    s = 1

                colG[r] = (colA[r] * s) % mod
                for i in ru[r]:
                    sm = colG[i + 1]
                    colG[i] = (colA[i] * sm) % mod
            else:
                nxt = G[c + 1]
                if r < last_r:
                    colG[last_r] = (colA[last_r] * nxt[last_r]) % mod
                    for i in rda[r]:
                        sm = nxt[i] + colG[i + 1]
                        if sm >= mod:
                            sm -= mod
                        colG[i] = (colA[i] * sm) % mod
                    s = nxt[r] + colG[r + 1]
                    if s >= mod:
                        s -= mod
                else:
                    s = nxt[last_r]

                colG[r] = (colA[r] * s) % mod
                for i in ru[r]:
                    sm = nxt[i] + colG[i + 1]
                    if sm >= mod:
                        sm -= mod
                    colG[i] = (colA[i] * sm) % mod

            if delta:
                # F[c] is correct before the update; compute p and update F[c] partially.
                if c == 0:
                    p = 1 if r == 0 else F[c][r - 1]
                else:
                    p = F[c - 1][r]
                    if r > 0:
                        p += F[c][r - 1]
                        if p >= mod:
                            p -= mod

                ans = (ans + delta * p * s) % mod

                dF = (delta * p) % mod
                if dF:
                    colF = F[c]
                    v = colF[r] + dF
                    if v >= mod:
                        v -= mod
                    colF[r] = v
                    d = dF
                    for i in ra[r]:
                        d = (d * colA[i]) % mod
                        if d == 0:
                            break
                        v = colF[i] + d
                        if v >= mod:
                            v -= mod
                        colF[i] = v

            cur_c = c
            cur_r = r

        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()