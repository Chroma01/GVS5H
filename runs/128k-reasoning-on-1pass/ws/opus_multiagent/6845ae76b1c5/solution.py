import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    n = int(data[ptr]); ptr += 1
    A = np.array(list(map(int, data[ptr:ptr + n])), dtype=np.int64); ptr += n
    B = np.array(list(map(int, data[ptr:ptr + n])), dtype=np.int64); ptr += n
    K = int(data[ptr]); ptr += 1
    qs = list(map(int, data[ptr:ptr + 2 * K]))
    Xl = qs[0::2]
    Yl = qs[1::2]

    # ---- dedupe identical (X,Y) queries -------------------------------
    seen = {}
    reps = []
    repof = [0] * K
    for i in range(K):
        key = Xl[i] * 200003 + Yl[i]          # injective, X,Y <= 1e5
        j = seen.get(key, -1)
        if j < 0:
            seen[key] = i
            j = i
            reps.append(i)
        repof[i] = j

    # ---- block size ---------------------------------------------------
    S = int(n / (K ** 0.5)) + 1
    if S > n:
        S = n
    if S < 1:
        S = 1

    x0l = [(x // S) * S for x in Xl]
    y0l = [(y // S) * S for y in Yl]

    X = np.array(Xl, dtype=np.intp)
    Y = np.array(Yl, dtype=np.intp)
    Y0 = np.array(y0l, dtype=np.intp)

    ans = np.zeros(K, dtype=np.int64)

    # ---- value compression (used for cheap boundary builds) -----------
    BU = np.unique(B)                       # sorted unique B values
    mB = BU.shape[0]
    rB = np.searchsorted(BU, B)             # rank of each B_j
    pA = np.searchsorted(BU, A)             # #unique B values < A_i

    AU = np.unique(A)
    mA = AU.shape[0]
    rA = np.searchsorted(AU, A)
    pB = np.searchsorted(AU, B)

    # ---- term 1 : sum_{i<=X} sum_{j<=y0} |A_i - B_j| ------------------
    g1 = {}
    for i in reps:
        v = y0l[i]
        if v:
            lst = g1.get(v)
            if lst is None:
                g1[v] = [i]
            else:
                lst.append(i)
    for v, lst in g1.items():
        cnt = np.asarray(np.bincount(rB[:v], minlength=mB), dtype=np.int64)
        pre_cnt = np.zeros(mB + 1, dtype=np.int64)
        np.cumsum(cnt, out=pre_cnt[1:])
        pre_sum = np.zeros(mB + 1, dtype=np.int64)
        np.cumsum(cnt * BU, out=pre_sum[1:])
        posv = pre_cnt[pA]
        sumv = pre_sum[pA]
        total = pre_sum[mB]
        F = A * (2 * posv - v) - 2 * sumv + total
        cumF = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(F, out=cumF[1:])
        idx = np.array(lst, dtype=np.intp)
        ans[idx] += cumF[X[idx]]

    # ---- term 2 : sum_{i<=x0} sum_{y0<j<=Y} |A_i - B_j| ---------------
    g2 = {}
    for i in reps:
        v = x0l[i]
        if v:
            lst = g2.get(v)
            if lst is None:
                g2[v] = [i]
            else:
                lst.append(i)
    for v, lst in g2.items():
        cnt = np.asarray(np.bincount(rA[:v], minlength=mA), dtype=np.int64)
        pre_cnt = np.zeros(mA + 1, dtype=np.int64)
        np.cumsum(cnt, out=pre_cnt[1:])
        pre_sum = np.zeros(mA + 1, dtype=np.int64)
        np.cumsum(cnt * AU, out=pre_sum[1:])
        posv = pre_cnt[pB]
        sumv = pre_sum[pB]
        total = pre_sum[mA]
        G = B * (2 * posv - v) - 2 * sumv + total
        cumG = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(G, out=cumG[1:])
        idx = np.array(lst, dtype=np.intp)
        ans[idx] += cumG[Y[idx]] - cumG[Y0[idx]]

    # ---- term 3 : leftover  A[x0:X] x B[y0:Y]  (both sides < S) -------
    blockcache = {}
    g3 = {}
    for i in reps:
        v = Yl[i]
        lst = g3.get(v)
        if lst is None:
            g3[v] = [i]
        else:
            lst.append(i)
    for v, lst in g3.items():
        yb = (v // S) * S
        ly = v - yb
        if ly == 0:
            continue
        lst2 = [i for i in lst if Xl[i] > x0l[i]]
        if not lst2:
            continue
        bc = blockcache.get(yb)
        if bc is None:
            L = n - yb
            if L > S:
                L = S
            blk = B[yb:yb + L]
            ordblk = np.argsort(blk, kind='stable')
            sortedblk = blk[ordblk]
            bc = (ordblk, sortedblk, L)
            blockcache[yb] = bc
        ordblk, sortedblk, L = bc
        if ly >= L:
            sb = sortedblk
        else:
            sb = sortedblk[ordblk < ly]
        m = sb.shape[0]
        PB = np.zeros(m + 1, dtype=np.int64)
        np.cumsum(sb, out=PB[1:])
        tot = PB[m]
        for i in lst2:
            xx = Xl[i]
            xb = x0l[i]
            a = A[xb:xx]
            p = np.searchsorted(sb, a)
            ans[i] += int((a * (2 * p - m) - 2 * PB[p] + tot).sum())

    res = ans.tolist()
    out = [None] * K
    for i in range(K):
        out[i] = res[repof[i]]
    sys.stdout.write('\n'.join(map(str, out)))
    sys.stdout.write('\n')


main()