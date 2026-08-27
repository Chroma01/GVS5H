import sys
import bisect

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = data[p]; p += 1
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = data[p]; R[i] = data[p + 1]; p += 2
    Q = data[p]; p += 1
    qs = [0] * Q
    qt = [0] * Q
    for i in range(Q):
        qs[i] = data[p]; qt[i] = data[p + 1]; p += 2

    INF = float('inf')

    # ---------- A(X): min W over intervals with R < X ----------
    orderR = sorted(range(1, N + 1), key=lambda i: R[i])
    Rs = [R[i] for i in orderR]
    prefA = [INF] * N
    cur = INF
    for k, i in enumerate(orderR):
        if W[i] < cur:
            cur = W[i]
        prefA[k] = cur

    def A(X):
        k = bisect.bisect_left(Rs, X)
        if k == 0:
            return INF
        return prefA[k - 1]

    # ---------- B(X): min W over intervals with L > X ----------
    orderL = sorted(range(1, N + 1), key=lambda i: L[i])
    Ls = [L[i] for i in orderL]
    suffB = [INF] * N
    cur = INF
    for k in range(N - 1, -1, -1):
        i = orderL[k]
        if W[i] < cur:
            cur = W[i]
        suffB[k] = cur

    def B(X):
        k = bisect.bisect_right(Ls, X)
        if k == N:
            return INF
        return suffB[k]

    # ---------- compressed L coords ----------
    coords = sorted(set(L[1:]))
    comp = {v: idx + 1 for idx, v in enumerate(coords)}
    M = len(coords)
    Lc = [0] * (N + 1)
    for i in range(1, N + 1):
        Lc[i] = comp[L[i]]

    ans_base = [0] * Q
    disjoint = [False] * Q
    cand = [INF] * Q
    qa = [0] * Q
    qb = [0] * Q
    overl = [False] * Q

    for qi in range(Q):
        s = qs[qi]; t = qt[qi]
        if R[s] < L[t] or R[t] < L[s]:
            disjoint[qi] = True
            ans_base[qi] = W[s] + W[t]
        else:
            overl[qi] = True
            ans_base[qi] = W[s] + W[t]
            a, b = (s, t) if L[s] <= L[t] else (t, s)
            qa[qi] = a; qb[qi] = b
            v1 = A(L[a])            # 2-path via common left neighbor
            if v1 < cand[qi]:
                cand[qi] = v1
            v2 = B(max(R[s], R[t]))  # 2-path via common right neighbor
            if v2 < cand[qi]:
                cand[qi] = v2
            c1 = A(L[s]) + B(R[t])   # 3-path: a left of s, b right of t
            if c1 < cand[qi]:
                cand[qi] = c1
            c2 = A(L[t]) + B(R[s])   # 3-path: a right of s, b left of t
            if c2 < cand[qi]:
                cand[qi] = c2

    # ---------- both-left offline sweep ----------
    bit1 = [INF] * (M + 2)
    bit2 = [INF] * (M + 2)

    def bit1_update(i, v):
        while i <= M:
            if v < bit1[i]:
                bit1[i] = v
            i += i & (-i)

    def bit1_query(i):
        r = INF
        while i > 0:
            if bit1[i] < r:
                r = bit1[i]
            i -= i & (-i)
        return r

    def bit2_update(i, v):
        ri = M - i + 1
        while ri <= M:
            if v < bit2[ri]:
                bit2[ri] = v
            ri += ri & (-ri)

    def bit2_query(i):
        ri = M - i
        r = INF
        while ri > 0:
            if bit2[ri] < r:
                r = bit2[ri]
            ri -= ri & (-ri)
        return r

    q_events = []
    for qi in range(Q):
        if overl[qi]:
            q_events.append((L[qb[qi]], qi))
    q_events.sort()

    iv = 0
    res_q1 = [INF] * Q
    res_q2 = [INF] * Q
    for X, qi in q_events:
        while iv < N and R[orderR[iv]] < X:
            i = orderR[iv]
            bit1_update(Lc[i], W[i] + A(L[i]))
            bit2_update(Lc[i], W[i])
            iv += 1
        y = Lc[qa[qi]]
        res_q1[qi] = bit1_query(y)
        res_q2[qi] = bit2_query(y)

    for qi in range(Q):
        if overl[qi]:
            a = qa[qi]
            d = res_q1[qi]
            v2 = A(L[a]) + res_q2[qi]
            if v2 < d:
                d = v2
            if d < cand[qi]:
                cand[qi] = d

    # ---------- both-right offline sweep (mirrored) ----------
    coordsR = sorted(set(R[1:]))
    compR = {v: idx + 1 for idx, v in enumerate(coordsR)}
    M2 = len(coordsR)
    Rc = [0] * (N + 1)
    for i in range(1, N + 1):
        Rc[i] = compR[R[i]]

    bit3 = [INF] * (M2 + 2)
    bit4 = [INF] * (M2 + 2)

    def bit3_update(i, v):
        ri = M2 - i + 1
        while ri <= M2:
            if v < bit3[ri]:
                bit3[ri] = v
            ri += ri & (-ri)

    def bit3_query(i):
        ri = M2 - i
        r = INF
        while ri > 0:
            if bit3[ri] < r:
                r = bit3[ri]
            ri -= ri & (-ri)
        return r

    def bit4_update(i, v):
        while i <= M2:
            if v < bit4[i]:
                bit4[i] = v
            i += i & (-i)

    def bit4_query(i):
        r = INF
        i -= 1
        while i > 0:
            if bit4[i] < r:
                r = bit4[i]
            i -= i & (-i)
        return r

    q_events2 = []
    qA = [0] * Q
    for qi in range(Q):
        if overl[qi]:
            s = qs[qi]; t = qt[qi]
            a2, b2 = (s, t) if R[s] >= R[t] else (t, s)
            qA[qi] = a2
            q_events2.append((R[b2], qi))
    q_events2.sort(key=lambda x: -x[0])

    orderLdesc = sorted(range(1, N + 1), key=lambda i: -L[i])
    iv = 0
    res_q1m = [INF] * Q
    res_q2m = [INF] * Q
    for X, qi in q_events2:
        while iv < N and L[orderLdesc[iv]] > X:
            i = orderLdesc[iv]
            bit3_update(Rc[i], W[i] + B(R[i]))
            bit4_update(Rc[i], W[i])
            iv += 1
        y = Rc[qA[qi]]
        res_q1m[qi] = bit3_query(y)
        res_q2m[qi] = bit4_query(y)

    for qi in range(Q):
        if overl[qi]:
            a2 = qA[qi]
            d = res_q1m[qi]
            v2 = B(R[a2]) + res_q2m[qi]
            if v2 < d:
                d = v2
            if d < cand[qi]:
                cand[qi] = d

    out = []
    for qi in range(Q):
        if disjoint[qi]:
            out.append(str(ans_base[qi]))
        else:
            if cand[qi] == INF:
                out.append("-1")
            else:
                out.append(str(ans_base[qi] + cand[qi]))
    sys.stdout.write("\n".join(out) + "\n")

main()