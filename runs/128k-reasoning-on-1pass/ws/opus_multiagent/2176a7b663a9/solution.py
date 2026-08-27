import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[0]); idx = 1
    W = list(map(int, data[1:1+n]))
    idx = 1 + n
    M = 2 * n
    INF = 1 << 60
    prefR = [INF] * (M + 2)   # prefR[v] = min W over intervals with R <= v
    sufL = [INF] * (M + 2)    # sufL[v]  = min W over intervals with L >= v
    L = [0] * n
    R = [0] * n
    for i in range(n):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        L[i] = l
        R[i] = r
        w = W[i]
        if w < prefR[r]:
            prefR[r] = w
        if w < sufL[l]:
            sufL[l] = w
    for v in range(1, M + 1):
        p = prefR[v - 1]
        if p < prefR[v]:
            prefR[v] = p
    for v in range(M, 0, -1):
        s = sufL[v + 1]
        if s < sufL[v]:
            sufL[v] = s

    q = int(data[idx]); idx += 1
    out = []
    ap = out.append
    d = data
    Lloc = L
    Rloc = R
    Wloc = W
    pR = prefR
    sL = sufL
    for _ in range(q):
        s = int(d[idx]) - 1
        t = int(d[idx + 1]) - 1
        idx += 2
        Ls = Lloc[s]; Rs = Rloc[s]
        Lt = Lloc[t]; Rt = Rloc[t]
        mls = pR[Ls - 1]      # minLeft(L_s)
        mrs = sL[Rs + 1]      # minRight(R_s)
        mlt = pR[Lt - 1]
        mrt = sL[Rt + 1]
        if (mls >= INF and mrs >= INF) or (mlt >= INF and mrt >= INF):
            ap(-1)
            continue
        base = Wloc[s] + Wloc[t]
        ans = INF * 4
        if Rs < Lt or Rt < Ls:
            ans = base
        # 3-vertex candidate
        a = pR[Ls - 1] if Ls < Lt else pR[Lt - 1]
        b = sL[Rs + 1] if Rs > Rt else sL[Rt + 1]
        c = a if a < b else b
        if c < INF:
            v = base + c
            if v < ans:
                ans = v
        # 4-vertex candidates
        c1 = mls + mrt
        c2 = mlt + mrs
        cc = c1 if c1 < c2 else c2
        if cc < INF:
            v = base + cc
            if v < ans:
                ans = v
        if ans >= INF:
            ap(-1)
        else:
            ap(ans)
    sys.stdout.write('\n'.join(map(str, out)))

main()