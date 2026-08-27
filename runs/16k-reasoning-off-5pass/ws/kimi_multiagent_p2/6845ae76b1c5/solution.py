import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    A = data[p:p+N]; p += N
    B = data[p:p+N]; p += N
    K = data[p]; p += 1
    Xs = [0]*K
    Ys = [0]*K
    for q in range(K):
        Xs[q] = data[p]; Ys[q] = data[p+1]; p += 2

    PA = [0]*(N+1)
    for i in range(N):
        PA[i+1] = PA[i] + A[i]
    PB = [0]*(N+1)
    for j in range(N):
        PB[j+1] = PB[j] + B[j]

    sys.setrecursionlimit(1 << 25)

    # |a-b| = (a+b) - 2*min(a,b)
    # F(X,Y) = Y*PA(X) + X*PB(Y) - 2*(M1 + M2)
    #   M1 = sum over (i<=X, j<=Y, B_j <= A_i) of B_j
    #   M2 = sum over (i<=X, j<=Y, A_i <  B_j) of A_i
    # Single CDQ on A-index i vs query X computes both. At each node the
    # left-half A's are swept (desc by value) against all B's (desc by value)
    # with one pointer pa1 = #{left A >= B_j}; then for each B_j:
    #   M1 weight = B_j * pa1
    #   M2 weight = (total left-A sum) - (sum of the pa1 largest left A's)
    # accumulated into two Fenwicks over j; right-half queries read prefix(Y).
    M1 = [0]*K
    M2 = [0]*K

    U_sorted = [(i+1, A[i]) for i in range(N)]            # (idx, val), idx-sorted
    V_by_val = sorted(((B[j], j+1) for j in range(N)), reverse=True)  # (val, idx)
    queries = [(Xs[q], Ys[q], q) for q in range(K)]

    bit1 = [0]*(N+2)
    bit2 = [0]*(N+2)

    def rec(lo, hi, Ulist, qlist):
        if lo == hi or not qlist or not Ulist:
            return
        mid = (lo + hi) >> 1
        ql = []
        qr = []
        for q in qlist:
            if q[0] <= mid:
                ql.append(q)
            else:
                qr.append(q)
        Ul = []
        Ur = []
        for u in Ulist:
            if u[0] <= mid:
                Ul.append(u)
            else:
                Ur.append(u)
        if qr and Ul:
            leftU = sorted(Ul, key=lambda t: -t[1])
            lu = len(leftU)
            lvals = [0]*lu
            for t in range(lu):
                lvals[t] = leftU[t][1]
            psumA = [0]*(lu+1)
            s = 0
            for t in range(lu):
                s += lvals[t]
                psumA[t+1] = s
            totA = s

            b1 = bit1; b2 = bit2; n = N
            pa1 = 0
            upd1 = []
            upd2 = []
            for (vv, vj) in V_by_val:
                while pa1 < lu and lvals[pa1] >= vv:
                    pa1 += 1
                w1 = vv * pa1
                w2 = totA - psumA[pa1]
                if w1 or w2:
                    i = vj
                    if w1 and w2:
                        while i <= n:
                            b1[i] += w1
                            b2[i] += w2
                            i += i & (-i)
                        upd1.append((vj, w1))
                        upd2.append((vj, w2))
                    elif w1:
                        while i <= n:
                            b1[i] += w1
                            i += i & (-i)
                        upd1.append((vj, w1))
                    else:
                        while i <= n:
                            b2[i] += w2
                            i += i & (-i)
                        upd2.append((vj, w2))
            for (lim1, lim2, qid) in qr:
                s1 = 0
                s2 = 0
                i = lim2
                while i > 0:
                    s1 += b1[i]
                    s2 += b2[i]
                    i -= i & (-i)
                M1[qid] += s1
                M2[qid] += s2
            for (vj, w) in upd1:
                i = vj
                while i <= n:
                    b1[i] -= w
                    i += i & (-i)
            for (vj, w) in upd2:
                i = vj
                while i <= n:
                    b2[i] -= w
                    i += i & (-i)
            rec(mid + 1, hi, Ur, qr)
        elif qr:
            rec(mid + 1, hi, Ur, qr)
        if ql:
            rec(lo, mid, Ul, ql)

    rec(1, N, U_sorted, queries)

    out = []
    for q in range(K):
        x = Xs[q]; y = Ys[q]
        ans = y * PA[x] + x * PB[y] - 2 * (M1[q] + M2[q])
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

solve()