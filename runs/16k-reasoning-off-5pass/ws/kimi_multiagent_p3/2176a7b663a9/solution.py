import sys
from bisect import bisect_left, bisect_right

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(data[pos]); pos += 1
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2

    INF = 1 << 62

    # PM_R(x): min W over vertices with R_w < x  (prefix min over R-sorted order)
    orderR = sorted(range(1, N + 1), key=lambda i: R[i])
    sortedR = [R[i] for i in orderR]
    pref = [0] * N
    m = INF
    for k, i in enumerate(orderR):
        if W[i] < m:
            m = W[i]
        pref[k] = m

    # SM_L(x): min W over vertices with L_w > x  (suffix min over L-sorted order)
    orderL = sorted(range(1, N + 1), key=lambda i: L[i])
    sortedL = [L[i] for i in orderL]
    suff = [0] * N
    m = INF
    for k in range(N - 1, -1, -1):
        if W[orderL[k]] < m:
            m = W[orderL[k]]
        suff[k] = m

    def pm_r(x):
        k = bisect_left(sortedR, x)
        return pref[k - 1] if k > 0 else INF

    def sm_l(x):
        k = bisect_right(sortedL, x)
        return suff[k] if k < N else INF

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        s = int(data[pos]); t = int(data[pos + 1]); pos += 2
        base = W[s] + W[t]
        if R[s] < L[t] or R[t] < L[s]:
            # disjoint -> direct edge, optimal since weights positive
            out.append(str(base))
            continue
        loL = L[s] if L[s] < L[t] else L[t]
        hiR = R[s] if R[s] > R[t] else R[t]
        # 2-path: intermediate w disjoint from hull [loL, hiR]
        best = pm_r(loL)
        v = sm_l(hiR)
        if v < best:
            best = v
        # 3-paths: s-x-y-t with x right of s, y left of t (auto-disjoint), and symmetric
        a = sm_l(R[s]); b = pm_r(L[t])
        if a < INF and b < INF:
            v = a + b
            if v < best:
                best = v
        a = sm_l(R[t]); b = pm_r(L[s])
        if a < INF and b < INF:
            v = a + b
            if v < best:
                best = v
        out.append(str(base + best) if best < INF else "-1")
    sys.stdout.write("\n".join(out) + "\n")

solve()