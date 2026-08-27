import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    A = data[p:p+N]; p += N
    B = data[p:p+N]; p += N
    K = data[p]; p += 1
    ans = [0]*K
    queries = []
    for qi in range(K):
        x = data[p]; y = data[p+1]; p += 2
        queries.append((x, y, qi))

    # ---------- Pass 1: pairs with A_i >= B_j ----------
    # CDQ over value: sort A-elements (desc value) and B-elements (desc value).
    # Recursively handle [lo, mid] A-elements against (mid, hi] B-elements:
    # every such cross pair satisfies A_i >= B_j, so within the node the
    # double sum factorises:
    #   sum_{i<=x, j<=y} (A_i - B_j)
    #     = prefSumA(x)*prefCntB(y) - prefCntA(x)*prefSumB(y)
    # computed with a two-pointer sweep over indices in O(len).
    a_elems = sorted([(A[i], i+1) for i in range(N)], key=lambda t: -t[0])
    b_elems = sorted([(B[j], j+1) for j in range(N)], key=lambda t: -t[0])

    sys.setrecursionlimit(1 << 22)

    def cdq1(al, ar, bl, br):
        if al > ar or bl > br:
            return
        if ar - al <= 1 and br - bl <= 1:
            # brute force tiny ranges
            for t1 in range(al, ar):
                va, ia = a_elems[t1]
                for t2 in range(bl, br):
                    vb, jb = b_elems[t2]
                    if va >= vb:
                        for (x, y, qi) in queries:
                            if ia <= x and jb <= y:
                                ans[qi] += va - vb
            return
        amid = (al + ar) >> 1
        bmid = (bl + br) >> 1
        # cross: a in [al, amid), b in [bmid, br)  -> all have va >= vb
        if al < amid and bmid < br:
            # gather i-indices (from a side) and j-indices (from b side)
            ilist = sorted(a_elems[t][1] for t in range(al, amid))
            jlist = sorted(b_elems[t][1] for t in range(bmid, br))
            # value maps: idx -> value
            # build dict lookups once
            # prefix sums over ilist / jlist
            m1 = len(ilist); m2 = len(jlist)
            prefA_sum = [0]*(m1+1)
            prefA_cnt = [0]*(m1+1)
            for t in range(m1):
                idx = ilist[t]
                prefA_sum[t+1] = prefA_sum[t] + A[idx-1]
                prefA_cnt[t+1] = prefA_cnt[t] + 1
            prefB_sum = [0]*(m2+1)
            prefB_cnt = [0]*(m2+1)
            for t in range(m2):
                idx = jlist[t]
                prefB_sum[t+1] = prefB_sum[t] + B[idx-1]
                prefB_cnt[t+1] = prefB_cnt[t] + 1
            import bisect
            for (x, y, qi) in queries:
                c1 = bisect.bisect_right(ilist, x)
                c2 = bisect.bisect_right(jlist, y)
                if c1 and c2:
                    ans[qi] += prefA_sum[c1]*prefB_cnt[c2] - prefA_cnt[c1]*prefB_sum[c2]
        cdq1(al, amid, bl, bmid)
        cdq1(amid, ar, bmid, br)

    cdq1(0, N, 0, N)

    # ---------- Pass 2: pairs with A_i < B_j ----------
    # symmetric: sort A ascending, B ascending; CDQ cross pairs have A_i < B_j
    # contribution (B_j - A_i):
    #   = prefCntA(x)*prefSumB(y) - prefSumA(x)*prefCntB(y)
    a_elems2 = sorted([(A[i], i+1) for i in range(N)], key=lambda t: t[0])
    b_elems2 = sorted([(B[j], j+1) for j in range(N)], key=lambda t: t[0])

    def cdq2(al, ar, bl, br):
        if al > ar or bl > br:
            return
        if ar - al <= 1 and br - bl <= 1:
            for t1 in range(al, ar):
                va, ia = a_elems2[t1]
                for t2 in range(bl, br):
                    vb, jb = b_elems2[t2]
                    if va < vb:
                        for (x, y, qi) in queries:
                            if ia <= x and jb <= y:
                                ans[qi] += vb - va
            return
        amid = (al + ar) >> 1
        bmid = (bl + br) >> 1
        # cross: a in [al, amid) (smaller A), b in (bmid, br] (larger B)
        if al < amid and bmid < br:
            ilist = sorted(a_elems2[t][1] for t in range(al, amid))
            jlist = sorted(b_elems2[t][1] for t in range(bmid, br))
            m1 = len(ilist); m2 = len(jlist)
            prefA_sum = [0]*(m1+1)
            prefA_cnt = [0]*(m1+1)
            for t in range(m1):
                idx = ilist[t]
                prefA_sum[t+1] = prefA_sum[t] + A[idx-1]
                prefA_cnt[t+1] = prefA_cnt[t] + 1
            prefB_sum = [0]*(m2+1)
            prefB_cnt = [0]*(m2+1)
            for t in range(m2):
                idx = jlist[t]
                prefB_sum[t+1] = prefB_sum[t] + B[idx-1]
                prefB_cnt[t+1] = prefB_cnt[t] + 1
            import bisect
            for (x, y, qi) in queries:
                c1 = bisect.bisect_right(ilist, x)
                c2 = bisect.bisect_right(jlist, y)
                if c1 and c2:
                    ans[qi] += prefA_cnt[c1]*prefB_sum[c2] - prefA_sum[c1]*prefB_cnt[c2]
        cdq2(al, amid, bl, bmid)
        cdq2(amid, ar, bmid, br)

    cdq2(0, N, 0, N)

    out = "\n".join(str(v) for v in ans)
    sys.stdout.write(out + "\n")

main()