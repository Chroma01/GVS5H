import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1

    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(data[idx]); idx += 1

    M = 2 * N
    INF = 1 << 60
    minAtR = [INF] * (M + 2)
    minAtL = [INF] * (M + 2)
    L = [0] * (N + 1)
    R = [0] * (N + 1)

    for i in range(1, N + 1):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        L[i] = l; R[i] = r
        if W[i] < minAtR[r]:
            minAtR[r] = W[i]
        if W[i] < minAtL[l]:
            minAtL[l] = W[i]

    # bestR[c] = min W_u among u with R_u < c
    bestR = [INF] * (M + 2)
    for c in range(1, M + 2):
        a = bestR[c - 1]; b = minAtR[c - 1]
        bestR[c] = a if a < b else b

    # bestL[c] = min W_u among u with L_u > c
    bestL = [INF] * (M + 2)
    for c in range(M, -1, -1):
        a = bestL[c + 1]; b = minAtL[c + 1]
        bestL[c] = a if a < b else b

    Q = int(data[idx]); idx += 1
    out = []
    TH = INF >> 1

    for _ in range(Q):
        s = int(data[idx]); t = int(data[idx + 1]); idx += 2
        Ls = L[s]; Rs = R[s]; Lt = L[t]; Rt = R[t]

        # intervals disjoint -> direct edge, positive weights => optimal
        if Rs < Lt or Rt < Ls:
            out.append(W[s] + W[t])
            continue

        # s,t overlap: need at least one intermediate
        # single intermediate left of both
        ml = Ls if Ls < Lt else Lt
        m = bestR[ml]
        # single intermediate right of both
        mr = Rs if Rs > Rt else Rt
        v = bestL[mr]
        if v < m:
            m = v
        # left of s + right of t (automatically disjoint in overlap)
        a = bestR[Ls]; b = bestL[Rt]
        if a < TH and b < TH:
            c2 = a + b
            if c2 < m:
                m = c2
        # right of s + left of t (automatically disjoint in overlap)
        a = bestL[Rs]; b = bestR[Lt]
        if a < TH and b < TH:
            c2 = a + b
            if c2 < m:
                m = c2

        if m >= TH:
            out.append(-1)
        else:
            out.append(W[s] + W[t] + m)

    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()