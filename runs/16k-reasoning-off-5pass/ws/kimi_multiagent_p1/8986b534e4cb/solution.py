import sys
from bisect import bisect_left, bisect_right


def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); M = int(data[pos+1]); Q = int(data[pos+2]); pos += 3

    A = [0] * (M + 1)
    B = [0] * (M + 1)
    Tp = [0] * (M + 1)
    for i in range(1, M + 1):
        S = int(data[pos]); Tt = int(data[pos + 1]); pos += 2
        if S < Tt:
            A[i] = S; B[i] = Tt; Tp[i] = 0
        else:
            A[i] = Tt; B[i] = S; Tp[i] = 1

    gL = [0] * (M + 1)

    # ---- shared endpoint conflicts (any type): same a or same b ----
    lastL = [0] * (N + 1)
    lastR = [0] * (N + 1)
    for j in range(1, M + 1):
        a = A[j]; b = B[j]
        if lastL[a] > gL[j]:
            gL[j] = lastL[a]
        if lastR[b] > gL[j]:
            gL[j] = lastR[b]
        lastL[a] = j
        lastR[b] = j

    # ---- same-type crossing conflicts via CDQ over index ----
    # For j: max i<j, same type, with
    #   (alpha) c_i < a_j and a_j < d_i < b_j   (i left-crosses j)
    #   (beta)  a_j < c_i < b_j and d_i > b_j   (i right-crosses j)

    # coordinate compression of B (d) and A (c) values, per type
    compB = [dict(), dict()]
    compBval = [None, None]
    compA = [dict(), dict()]
    compAval = [None, None]
    for t in (0, 1):
        svB = sorted({B[i] for i in range(1, M + 1) if Tp[i] == t})
        svA = sorted({A[i] for i in range(1, M + 1) if Tp[i] == t})
        compBval[t] = svB
        compAval[t] = svA
        compB[t] = {v: k for k, v in enumerate(svB)}
        compA[t] = {v: k for k, v in enumerate(svA)}

    # segment tree size: max over both shapes/types
    segsize = 1
    for t in (0, 1):
        for sv in (compBval[t], compAval[t]):
            n = max(1, len(sv))
            s = 1
            while s < n:
                s <<= 1
            if s > segsize:
                segsize = s

    # two segment trees, one per type (avoids cross-type contamination)
    seg0 = [0] * (2 * segsize)
    seg1 = [0] * (2 * segsize)

    def make_funcs(seg):
        def seg_upd(p, v):
            p += segsize
            if seg[p] >= v:
                return
            seg[p] = v
            p >>= 1
            while p:
                nv = seg[p << 1] if seg[p << 1] > seg[(p << 1) | 1] else seg[(p << 1) | 1]
                if seg[p] == nv:
                    break
                seg[p] = nv
                p >>= 1

        def seg_query(l, r):
            l += segsize
            r += segsize
            res = 0
            while l < r:
                if l & 1:
                    if seg[l] > res:
                        res = seg[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if seg[r] > res:
                        res = seg[r]
                l >>= 1
                r >>= 1
            return res

        def seg_reset(touched):
            for p in touched:
                seg[p + segsize] = 0
            parents = set()
            for p in touched:
                q = (p + segsize) >> 1
                while q:
                    parents.add(q)
                    q >>= 1
            for q in sorted(parents, reverse=True):
                seg[q] = seg[q << 1] if seg[q << 1] > seg[(q << 1) | 1] else seg[(q << 1) | 1]

        return seg_upd, seg_query, seg_reset

    upd0, qry0, rst0 = make_funcs(seg0)
    upd1, qry1, rst1 = make_funcs(seg1)

    idx = list(range(1, M + 1))  # identity permutation; CDQ never reorders it

    sys.setrecursionlimit(1 << 22)
    LEAF = 24

    def conflicts_pair(i, j):
        ai, bi, ti = A[i], B[i], Tp[i]
        aj, bj, tj = A[j], B[j], Tp[j]
        if ai == aj or bi == bj:
            return True
        if ti == tj:
            if ai < aj < bi < bj or aj < ai < bj < bi:
                return True
        return False

    def cdq(l, r):
        # processes index range [l, r) of idx (identity => indices l+1..r)
        if r - l <= LEAF:
            for x in range(l, r):
                j = idx[x]
                gj = gL[j]
                for y in range(l, x):
                    i = idx[y]
                    if i < j:
                        if conflicts_pair(i, j) and i > gj:
                            gj = i
                    else:
                        if conflicts_pair(j, i) and j > gj:
                            gj = j
                gL[j] = gj
            return
        mid = (l + r) >> 1
        cdq(l, mid)
        cdq(mid, r)

        # ---- shape alpha: c_i < a_j, d_i in (a_j, b_j) ----
        left = sorted(idx[l:mid], key=lambda i: A[i])
        right = sorted(idx[mid:r], key=lambda j: A[j])
        touched0 = []
        touched1 = []
        p = 0
        ln = len(left)
        for j in right:
            aj = A[j]; bj = B[j]; tj = Tp[j]
            while p < ln and A[left[p]] < aj:
                i = left[p]
                if Tp[i] == 0:
                    upd0(compB[0][B[i]], i)
                    touched0.append(compB[0][B[i]])
                else:
                    upd1(compB[1][B[i]], i)
                    touched1.append(compB[1][B[i]])
                p += 1
            cv = compBval[tj]
            lo = bisect_right(cv, aj)
            hi = bisect_left(cv, bj)
            if lo < hi:
                r1 = (qry0 if tj == 0 else qry1)(lo, hi)
                if r1 > gL[j]:
                    gL[j] = r1
        if touched0:
            rst0(touched0)
        if touched1:
            rst1(touched1)

        # ---- shape beta: c_i in (a_j, b_j), d_i > b_j ----
        left2 = sorted(idx[l:mid], key=lambda i: -B[i])
        right2 = sorted(idx[mid:r], key=lambda j: -B[j])
        touched0 = []
        touched1 = []
        p = 0
        ln = len(left2)
        for j in right2:
            aj = A[j]; bj = B[j]; tj = Tp[j]
            while p < ln and B[left2[p]] > bj:
                i = left2[p]
                if Tp[i] == 0:
                    upd0(compA[0][A[i]], i)
                    touched0.append(compA[0][A[i]])
                else:
                    upd1(compA[1][A[i]], i)
                    touched1.append(compA[1][A[i]])
                p += 1
            cv = compAval[tj]
            lo = bisect_right(cv, aj)
            hi = bisect_left(cv, bj)
            if lo < hi:
                r1 = (qry0 if tj == 0 else qry1)(lo, hi)
                if r1 > gL[j]:
                    gL[j] = r1
        if touched0:
            rst0(touched0)
        if touched1:
            rst1(touched1)

    cdq(0, M)

    # ---- sparse table over gL[1..M] for range max ----
    st = [gL[:]]
    k = 1
    while (1 << k) <= M:
        prev = st[-1]
        half = 1 << (k - 1)
        length = M - (1 << k) + 1
        cur = [0] * (M + 1)
        for i in range(1, length + 1):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if a > b else b
        st.append(cur)
        k += 1
    log2 = [0] * (M + 2)
    for i in range(2, M + 2):
        log2[i] = log2[i >> 1] + 1

    out = []
    for _ in range(Q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        k = log2[R - L + 1]
        a = st[k][L]
        b = st[k][R - (1 << k) + 1]
        m = a if a > b else b
        out.append("No" if m >= L else "Yes")
    sys.stdout.write("\n".join(out) + "\n")


solve()