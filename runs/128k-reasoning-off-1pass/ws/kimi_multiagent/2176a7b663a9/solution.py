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

    # Sorted by R: prefix minima of W  -> query "min W over u with R_u < x"
    orderR = sorted(range(1, N + 1), key=lambda i: R[i])
    Rsorted = [R[i] for i in orderR]
    prefMin = [INF] * N
    m = INF
    for k, i in enumerate(orderR):
        if W[i] < m:
            m = W[i]
        prefMin[k] = m

    def minW_Rlt(x):
        # min weight among vertices u with R_u < x
        idx = bisect_left(Rsorted, x)
        if idx == 0:
            return INF
        return prefMin[idx - 1]

    # Sorted by L: suffix minima of W  -> query "min W over u with L_u > y"
    orderL = sorted(range(1, N + 1), key=lambda i: L[i])
    Lsorted = [L[i] for i in orderL]
    sufMin = [INF] * (N + 1)
    m = INF
    for k in range(N - 1, -1, -1):
        if W[orderL[k]] < m:
            m = W[orderL[k]]
        sufMin[k] = m

    def minW_Lgt(y):
        # min weight among vertices u with L_u > y
        idx = bisect_right(Lsorted, y)
        return sufMin[idx]  # sufMin[N] = INF

    # A_v = min weight of a vertex disjoint from v (INF => v overlaps everything => isolated)
    A = [INF] * (N + 1)
    iso = [False] * (N + 1)
    for v in range(1, N + 1):
        a = minW_Rlt(L[v])
        b = minW_Lgt(R[v])
        av = a if a < b else b
        A[v] = av
        iso[v] = (av == INF)

    # has_cut: overlap graph disconnected => G connected
    has_cut = False
    maxR = -1
    for i in orderL:
        if maxR != -1 and maxR < L[i]:
            has_cut = True
            break
        if R[i] > maxR:
            maxR = R[i]

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        s = int(data[pos]); t = int(data[pos + 1]); pos += 2
        if not has_cut and (iso[s] or iso[t]):
            out.append("-1")
            continue
        if R[s] < L[t] or R[t] < L[s]:
            # disjoint => direct edge, shortest possible (positive weights)
            out.append(str(W[s] + W[t]))
            continue
        # overlap: best length-2 (common neighbor) or length-3 path
        lo = L[s] if L[s] < L[t] else L[t]
        hi = R[s] if R[s] > R[t] else R[t]
        C = minW_Rlt(lo)
        c2 = minW_Lgt(hi)
        if c2 < C:
            C = c2
        best = C
        s3 = A[s] + A[t]
        if s3 < best:
            best = s3
        if best == INF:
            out.append("-1")  # safety; unreachable for same-component pairs
        else:
            out.append(str(W[s] + W[t] + best))

    sys.stdout.write("\n".join(out) + "\n")

solve()