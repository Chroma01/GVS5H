import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    W = [0]*(N+1)
    for i in range(1, N+1):
        W[i] = int(data[pos]); pos += 1
    L = [0]*(N+1)
    R = [0]*(N+1)
    for i in range(1, N+1):
        L[i] = int(data[pos]); R[i] = int(data[pos+1]); pos += 2

    INF = float('inf')

    # ---- Component computation via universal-vertex criterion ----
    # Vertex i is isolated in G iff it intersects every other interval,
    # i.e. L_i <= min_{j != i} R_j  AND  R_i >= max_{j != i} L_j.
    # All non-universal vertices form a single connected component;
    # each universal vertex is its own singleton component.
    sR = sorted(R[1:])          # ascending R
    sL = sorted(L[1:])          # ascending L
    minR = sR[0]
    secMinR = sR[1] if N >= 2 else INF
    cntMinR = 0
    for i in range(1, N+1):
        if R[i] == minR:
            cntMinR += 1
    maxL = sL[N-1]
    secMaxL = sL[N-2] if N >= 2 else -INF
    cntMaxL = 0
    for i in range(1, N+1):
        if L[i] == maxL:
            cntMaxL += 1

    comp = [0]*(N+1)
    nxt = 1
    for i in range(1, N+1):
        # min R over j != i
        if R[i] == minR and cntMinR == 1:
            minRo = secMinR
        else:
            minRo = minR
        # max L over j != i
        if L[i] == maxL and cntMaxL == 1:
            maxLo = secMaxL
        else:
            maxLo = maxL
        if L[i] <= minRo and R[i] >= maxLo:
            # universal -> isolated singleton component
            comp[i] = nxt
            nxt += 1
        else:
            comp[i] = 0  # big shared component

    # ---- Prefix min weight over intervals sorted by R: min W with R_k < x ----
    byR = sorted(range(1, N+1), key=lambda i: R[i])
    Rsorted = [R[i] for i in byR]
    prefMin = [0]*N
    m = INF
    for idx, i in enumerate(byR):
        if W[i] < m:
            m = W[i]
        prefMin[idx] = m

    def minW_Rlt(x):
        # min weight over k with R_k < x
        k = bisect_left(Rsorted, x)
        if k == 0:
            return INF
        return prefMin[k-1]

    # ---- Suffix min weight over intervals sorted by L: min W with L_k > x ----
    byL = sorted(range(1, N+1), key=lambda i: L[i])
    Lsorted = [L[i] for i in byL]
    suffMin = [0]*N
    m = INF
    for idx in range(N-1, -1, -1):
        i = byL[idx]
        if W[i] < m:
            m = W[i]
        suffMin[idx] = m

    def minW_Lgt(x):
        # min weight over k with L_k > x
        k = bisect_right(Lsorted, x)
        if k == N:
            return INF
        return suffMin[k]

    # Per-vertex left/right mins
    LW = [0]*(N+1)  # min W_k with R_k < L_i
    RW = [0]*(N+1)  # min W_k with L_k > R_i
    for i in range(1, N+1):
        LW[i] = minW_Rlt(L[i])
        RW[i] = minW_Lgt(R[i])

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        s = int(data[pos]); t = int(data[pos+1]); pos += 2
        if comp[s] != comp[t]:
            out.append("-1")
            continue
        base = W[s] + W[t]
        ans = INF
        # direct edge
        if R[s] < L[t] or R[t] < L[s]:
            ans = base
        # 2-edge: k disjoint from both
        lo = L[s] if L[s] < L[t] else L[t]
        hi = R[s] if R[s] > R[t] else R[t]
        cand = minW_Rlt(lo)
        c2 = minW_Lgt(hi)
        if c2 < cand:
            cand = c2
        if cand < INF:
            v = base + cand
            if v < ans:
                ans = v
        # 3-edge: (left of s, right of t) or (right of s, left of t)
        cand = LW[s] + RW[t]
        c2 = RW[s] + LW[t]
        if c2 < cand:
            cand = c2
        if cand < INF:
            v = base + cand
            if v < ans:
                ans = v
        out.append(str(ans) if ans < INF else "-1")
    sys.stdout.write("\n".join(out) + "\n")

main()