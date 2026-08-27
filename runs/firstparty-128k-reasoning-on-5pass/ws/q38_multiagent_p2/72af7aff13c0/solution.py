import sys


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    nxt = it.__next__
    int_ = int
    MOD = 998244353

    H0 = int_(nxt())
    W0 = int_(nxt())
    N0 = H0 * W0
    raw = [int_(nxt()) for _ in range(N0)]

    Q = int_(nxt())
    sh = int_(nxt())
    sw = int_(nxt())

    moves = [0] * Q
    vals = [0] * Q
    cntU = cntD = cntL = cntR = 0

    for i in range(Q):
        d0 = nxt()[0]
        if d0 == 85:      # U
            code = 0
            cntU += 1
        elif d0 == 68:    # D
            code = 1
            cntD += 1
        elif d0 == 76:    # L
            code = 2
            cntL += 1
        else:             # R
            code = 3
            cntR += 1
        moves[i] = code
        vals[i] = int_(nxt())

    del data, it, nxt

    # Choose orientation minimizing estimated vertical-move work.
    # In the chosen orientation, U/D moves cost O(W), L/R moves cost O(1).
    cost_no = (cntU + cntD) * W0
    cost_trans = (cntL + cntR) * H0
    if cost_trans < cost_no or (cost_trans == cost_no and H0 < W0):
        trans = True
    else:
        trans = False

    if trans:
        H = W0
        W = H0
        A = [[0] * W for _ in range(H)]
        A_local = A
        raw_local = raw
        W0_local = W0
        H0_local = H0
        for h in range(H0_local):
            base = h * W0_local
            for w in range(W0_local):
                A_local[w][h] = raw_local[base + w]
        del raw

        r = sw - 1
        c = sh - 1

        # Original U,D,L,R -> transposed L,R,U,D
        mp = (2, 3, 0, 1)
        moves = [mp[m] for m in moves]
    else:
        H = H0
        W = W0
        A = [raw[i:i + W] for i in range(0, N0, W)]
        del raw

        r = sh - 1
        c = sw - 1

    P = [[0] * W for _ in range(H)]
    S = [[0] * W for _ in range(H)]

    # Neighbor arrays to avoid c-1 / c+1 inside hot loops:
    # AP[r][c] = A[r][c-1] for c > 0
    # AS[r][c] = A[r][c+1] for c < W-1
    AP = [[0] * W for _ in range(H)]
    AS = [[0] * W for _ in range(H)]

    for rr in range(H):
        row = A[rr]
        ap = AP[rr]
        as_ = AS[rr]
        for cc in range(1, W):
            ap[cc] = row[cc - 1]
        for cc in range(W - 1):
            as_[cc] = row[cc + 1]

    last_row = H - 1
    last_col = W - 1
    MOD_local = MOD
    W_local = W

    # Initial forward DP: P excludes the destination cell.
    for rr in range(H):
        prow = P[rr]
        aprow = AP[rr]
        if rr == 0:
            prow[0] = 1
            p = 1
            for cc in range(1, W_local):
                p = (p * aprow[cc]) % MOD_local
                prow[cc] = p
        else:
            prevp = P[rr - 1]
            preva = A[rr - 1]
            p = (prevp[0] * preva[0]) % MOD_local
            prow[0] = p
            for cc in range(1, W_local):
                p = (prevp[cc] * preva[cc] + p * aprow[cc]) % MOD_local
                prow[cc] = p

    # Initial backward DP: S excludes the source cell.
    for rr in range(last_row, -1, -1):
        srow = S[rr]
        asrow = AS[rr]
        if rr == last_row:
            srow[last_col] = 1
            s = 1
            for cc in range(last_col - 1, -1, -1):
                s = (s * asrow[cc]) % MOD_local
                srow[cc] = s
        else:
            nexts = S[rr + 1]
            nexta = A[rr + 1]
            s = (nexts[last_col] * nexta[last_col]) % MOD_local
            srow[last_col] = s
            for cc in range(last_col - 1, -1, -1):
                s = (nexts[cc] * nexta[cc] + s * asrow[cc]) % MOD_local
                srow[cc] = s

    ans = (A[last_row][last_col] * P[last_row][last_col]) % MOD_local

    def P_prefix(rr, ec, A=A, P=P, AP=AP, W=W, MOD=MOD, range=range):
        prow = P[rr]
        aprow = AP[rr]
        if rr == 0:
            prow[0] = 1
            p = 1
            for cc in range(1, ec + 1):
                p = (p * aprow[cc]) % MOD
                prow[cc] = p
        else:
            prevp = P[rr - 1]
            preva = A[rr - 1]
            p = (prevp[0] * preva[0]) % MOD
            prow[0] = p
            for cc in range(1, ec + 1):
                p = (prevp[cc] * preva[cc] + p * aprow[cc]) % MOD
                prow[cc] = p

    def P_suffix(rr, sc, A=A, P=P, AP=AP, W=W, MOD=MOD, range=range):
        prow = P[rr]
        aprow = AP[rr]
        if rr == 0:
            p = prow[sc - 1]
            for cc in range(sc, W):
                p = (p * aprow[cc]) % MOD
                prow[cc] = p
        else:
            prevp = P[rr - 1]
            preva = A[rr - 1]
            p = prow[sc - 1]
            for cc in range(sc, W):
                p = (prevp[cc] * preva[cc] + p * aprow[cc]) % MOD
                prow[cc] = p

    def S_suffix(rr, sc, A=A, S=S, AS=AS, W=W,
                 last_row=last_row, last_col=last_col,
                 last_col_minus_1=last_col - 1, MOD=MOD, range=range):
        srow = S[rr]
        asrow = AS[rr]
        if rr == last_row:
            srow[last_col] = 1
            s = 1
            for cc in range(last_col_minus_1, sc - 1, -1):
                s = (s * asrow[cc]) % MOD
                srow[cc] = s
        else:
            nexts = S[rr + 1]
            nexta = A[rr + 1]
            s = (nexts[last_col] * nexta[last_col]) % MOD
            srow[last_col] = s
            for cc in range(last_col_minus_1, sc - 1, -1):
                s = (nexts[cc] * nexta[cc] + s * asrow[cc]) % MOD
                srow[cc] = s

    def S_prefix(rr, ec, A=A, S=S, AS=AS, W=W,
                 last_row=last_row, MOD=MOD, range=range):
        srow = S[rr]
        asrow = AS[rr]
        if rr == last_row:
            s = srow[ec + 1]
            for cc in range(ec, -1, -1):
                s = (s * asrow[cc]) % MOD
                srow[cc] = s
        else:
            nexts = S[rr + 1]
            nexta = A[rr + 1]
            s = srow[ec + 1]
            for cc in range(ec, -1, -1):
                s = (nexts[cc] * nexta[cc] + s * asrow[cc]) % MOD
                srow[cc] = s

    ppre = P_prefix
    psuf = P_suffix
    ssuf = S_suffix
    spre = S_prefix

    A_q = A
    P_q = P
    S_q = S
    AP_q = AP
    AS_q = AS
    W_q = W
    MOD_q = MOD
    last_row_q = last_row
    moves_q = moves
    vals_q = vals

    out = []
    out_append = out.append
    str_ = str

    for i in range(Q):
        mv = moves_q[i]
        a = vals_q[i]

        if mv == 0:  # U
            old_r = r
            r -= 1

            arow = A_q[r]
            aprow = AP_q[r]
            asrow = AS_q[r]
            old = arow[c]
            if a != old:
                arow[c] = a
                if c + 1 < W_q:
                    aprow[c + 1] = a
                if c > 0:
                    asrow[c - 1] = a
                changed = True
            else:
                changed = False

            if c > 0:
                spre(old_r, c - 1)
            ssuf(r, c)

        elif mv == 1:  # D
            old_r = r
            r += 1

            arow = A_q[r]
            aprow = AP_q[r]
            asrow = AS_q[r]
            old = arow[c]
            if a != old:
                arow[c] = a
                if c + 1 < W_q:
                    aprow[c + 1] = a
                if c > 0:
                    asrow[c - 1] = a
                changed = True
            else:
                changed = False

            if c + 1 < W_q:
                psuf(old_r, c + 1)
            ppre(r, c)

        elif mv == 2:  # L
            c -= 1

            arow = A_q[r]
            aprow = AP_q[r]
            asrow = AS_q[r]
            old = arow[c]
            if a != old:
                arow[c] = a
                if c + 1 < W_q:
                    aprow[c + 1] = a
                if c > 0:
                    asrow[c - 1] = a
                changed = True
            else:
                changed = False

            srow = S_q[r]
            if r == last_row_q:
                srow[c] = (srow[c + 1] * asrow[c]) % MOD_q
            else:
                nexts = S_q[r + 1]
                nexta = A_q[r + 1]
                srow[c] = (nexts[c] * nexta[c] + srow[c + 1] * asrow[c]) % MOD_q

        else:  # R
            c += 1

            arow = A_q[r]
            aprow = AP_q[r]
            asrow = AS_q[r]
            old = arow[c]
            if a != old:
                arow[c] = a
                if c + 1 < W_q:
                    aprow[c + 1] = a
                if c > 0:
                    asrow[c - 1] = a
                changed = True
            else:
                changed = False

            prow = P_q[r]
            if r == 0:
                prow[c] = (prow[c - 1] * aprow[c]) % MOD_q
            else:
                prevp = P_q[r - 1]
                preva = A_q[r - 1]
                prow[c] = (prevp[c] * preva[c] + prow[c - 1] * aprow[c]) % MOD_q

        if changed:
            delta = a - old
            if delta < 0:
                delta += MOD_q
            C = (P_q[r][c] * S_q[r][c]) % MOD_q
            if C:
                ans = (ans + delta * C) % MOD_q

        out_append(str_(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()