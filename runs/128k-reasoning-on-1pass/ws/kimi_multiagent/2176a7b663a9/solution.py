import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    W = [0] * (n + 1)
    for i in range(1, n + 1):
        W[i] = int(next(it))
    L = [0] * (n + 1)
    R = [0] * (n + 1)
    C = 2 * n
    INF = 1 << 62
    bestR = [INF] * (C + 2)  # min weight among intervals with exact right endpoint x
    bestL = [INF] * (C + 2)  # min weight among intervals with exact left endpoint x
    for i in range(1, n + 1):
        li = int(next(it)); ri = int(next(it))
        L[i] = li; R[i] = ri
        wi = W[i]
        if wi < bestR[ri]:
            bestR[ri] = wi
        if wi < bestL[li]:
            bestL[li] = wi
    # pref[x] = min weight among intervals with R <= x  (cheapest interval strictly left of x+1)
    pref = [INF] * (C + 2)
    m = INF
    for x in range(1, C + 1):
        if bestR[x] < m:
            m = bestR[x]
        pref[x] = m
    # suff[x] = min weight among intervals with L >= x  (cheapest interval strictly right of x-1)
    suff = [INF] * (C + 3)
    m = INF
    for x in range(C, 0, -1):
        if bestL[x] < m:
            m = bestL[x]
        suff[x] = m

    q = int(next(it))
    out = []
    for _ in range(q):
        s = int(next(it)); t = int(next(it))
        ws = W[s]; wt = W[t]
        ls = L[s]; rs = R[s]
        lt = L[t]; rt = R[t]
        # direct edge iff intervals are disjoint
        if rs < lt or rt < ls:
            out.append(str(ws + wt))
            continue
        base = ws + wt
        best = INF
        # 2-edge path via a common neighbor: strictly left of both, or strictly right of both
        m1 = pref[min(ls, lt) - 1]
        m2 = suff[max(rs, rt) + 1]
        mc = m1 if m1 < m2 else m2
        if mc < INF:
            cand = base + mc
            if cand < best:
                best = cand
        # 3-edge paths: one intermediate strictly left of s, one strictly right of t (and vice versa)
        a1 = pref[ls - 1]; b1 = suff[rt + 1]
        if a1 < INF and b1 < INF:
            cand = base + a1 + b1
            if cand < best:
                best = cand
        a2 = suff[rs + 1]; b2 = pref[lt - 1]
        if a2 < INF and b2 < INF:
            cand = base + a2 + b2
            if cand < best:
                best = cand
        out.append(str(best if best < INF else -1))
    sys.stdout.write("\n".join(out) + "\n")

main()