import sys
import math
import numpy as np


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    N = data[pos]; pos += 1
    A = np.array(data[pos:pos + N], dtype=np.int64); pos += N
    B = np.array(data[pos:pos + N], dtype=np.int64); pos += N
    K = data[pos]; pos += 1
    qarr = np.array(data[pos:pos + 2 * K], dtype=np.int64)
    X = qarr[0::2].copy()
    Y = qarr[1::2].copy()

    # prefix sums of B
    SBpref = np.empty(N + 1, dtype=np.int64)
    SBpref[0] = 0
    np.cumsum(B, out=SBpref[1:])

    # choose block size for rows
    BL = int(N / math.sqrt(K) / 3.2)
    if BL < 1:
        BL = 1
    if BL > N:
        BL = N

    qx = X // BL  # block index for each query (rows < qx*BL are "full")

    # ---------- wavelet matrix over B (for count/sum of b <= a among prefix) ----------
    unique = np.unique(B)
    D = int(unique.size)
    ranks = np.searchsorted(unique, B, side='left').astype(np.int64)
    Wb = max(1, D.bit_length())
    levels = []
    cur_rank = ranks
    cur_val = B
    for b in range(Wb - 1, -1, -1):
        zero = ((cur_rank >> b) & 1) == 0
        zc = np.empty(N + 1, dtype=np.int64); zc[0] = 0
        np.cumsum(zero.astype(np.int64), out=zc[1:])
        zv = np.empty(N + 1, dtype=np.int64); zv[0] = 0
        np.cumsum(np.where(zero, cur_val, 0), out=zv[1:])
        Z = int(zc[N])
        levels.append((zc, zv, Z))
        cur_rank = np.concatenate((cur_rank[zero], cur_rank[~zero]))
        cur_val = np.concatenate((cur_val[zero], cur_val[~zero]))

    def wquery(tt, yy):
        E = tt.shape[0]
        l = np.zeros(E, dtype=np.int64)
        r = yy.astype(np.int64, copy=True)
        cnt = np.zeros(E, dtype=np.int64)
        sm = np.zeros(E, dtype=np.int64)
        for li in range(Wb):
            b = Wb - 1 - li
            zc, zv, Z = levels[li]
            Lz = zc.take(l); Rz = zc.take(r)
            mask = ((tt >> b) & 1).astype(bool)
            if mask.any():
                cnt += np.where(mask, Rz - Lz, 0)
                Lv = zv.take(l); Rv = zv.take(r)
                sm += np.where(mask, Rv - Lv, 0)
                l = np.where(mask, Z + (l - Lz), Lz)
                r = np.where(mask, Z + (r - Rz), Rz)
            else:
                l = Lz
                r = Rz
        return cnt, sm

    # ---------- partial rows: rows in [qx*BL, X) ----------
    partial = np.zeros(K, dtype=np.int64)
    start = qx * BL
    counts = X - start
    mask = counts > 0
    if mask.any():
        cnts_p = counts[mask]
        ids_p = np.nonzero(mask)[0]
        starts_p = np.cumsum(cnts_p) - cnts_p
        ends_p = np.cumsum(cnts_p)
        total = int(cnts_p.sum())
        rep_off = np.repeat(starts_p, cnts_p)
        within = np.arange(total, dtype=np.int64) - rep_off
        event_row = np.repeat(start[mask], cnts_p) + within
        event_a = A[event_row]
        event_y = np.repeat(Y[mask], cnts_p)
        del event_row, within, rep_off
        CH = 1000000
        for s0 in range(0, total, CH):
            e0 = min(total, s0 + CH)
            aa = event_a[s0:e0]
            yy = event_y[s0:e0]
            tt = np.searchsorted(unique, aa, side='right').astype(np.int64)
            cnt, sm = wquery(tt, yy)
            SBev = SBpref[yy]
            contrib = 2 * aa * cnt - 2 * sm + SBev - aa * yy
            t0 = int(np.searchsorted(ends_p, s0, side='right'))
            t1 = int(np.searchsorted(starts_p, e0, side='left')) - 1
            if t0 <= t1:
                locs = starts_p[t0:t1 + 1] - s0
                np.maximum(locs, 0, out=locs)
                sums = np.add.reduceat(contrib, locs)
                partial[ids_p[t0:t1 + 1]] += sums

    # ---------- full rows: rows < qx*BL, using cumulative rows array P ----------
    sortedBvals = np.sort(B)
    b_order = np.argsort(B, kind='stable')

    full = np.zeros(K, dtype=np.int64)
    order = np.argsort(qx, kind='stable')
    P = np.zeros(N, dtype=np.int64)
    b = 0
    ptr = 0
    while ptr < K:
        bcur = int(qx[order[ptr]])
        while b < bcur:
            st = b * BL
            en = st + BL
            if en > N:
                en = N
            if st < N:
                blk = A[st:en]
                nb = blk.shape[0]
                p = np.searchsorted(sortedBvals, blk, side='left')
                ordr = np.argsort(p, kind='stable')
                ps = p[ordr]
                as_ = blk[ordr]
                prefA = np.empty(nb + 1, dtype=np.int64); prefA[0] = 0
                np.cumsum(as_, out=prefA[1:])
                freq = np.bincount(ps, minlength=N + 1).astype(np.int64)
                cumfreq = np.cumsum(freq)
                cnt_le_sorted = cumfreq[:N]
                sum_le_sorted = prefA[cnt_le_sorted]
                tot = prefA[nb]
                contr_sorted = (2 * sortedBvals * cnt_le_sorted
                                - 2 * sum_le_sorted + tot - sortedBvals * nb)
                contr = np.empty(N, dtype=np.int64)
                contr[b_order] = contr_sorted
                P += contr
            b += 1
        prefP = np.empty(N + 1, dtype=np.int64); prefP[0] = 0
        np.cumsum(P, out=prefP[1:])
        j = ptr + 1
        while j < K and qx[order[j]] == bcur:
            j += 1
        gids = order[ptr:j]
        full[gids] = prefP[Y[gids]]
        ptr = j

    ans = full + partial
    sys.stdout.write('\n'.join(map(str, ans.tolist())))
    sys.stdout.write('\n')


main()