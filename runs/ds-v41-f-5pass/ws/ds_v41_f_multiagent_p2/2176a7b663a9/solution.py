import sys

def main():
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

    M = 2 * N + 2
    INF = 1 << 60
    # pref[x] = min W_i over intervals with R_i <= x
    # suff[x] = min W_i over intervals with L_i >= x
    pref = [INF] * (M + 2)
    suff = [INF] * (M + 2)
    for i in range(1, N + 1):
        if W[i] < pref[R[i]]:
            pref[R[i]] = W[i]
        if W[i] < suff[L[i]]:
            suff[L[i]] = W[i]
    for x in range(1, M + 2):
        if pref[x - 1] < pref[x]:
            pref[x] = pref[x - 1]
    for x in range(M, -1, -1):
        if suff[x + 1] < suff[x]:
            suff[x] = suff[x + 1]

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        s = int(data[pos]); t = int(data[pos + 1]); pos += 2
        Ls = L[s]; Rs = R[s]; Lt = L[t]; Rt = R[t]
        # direct edge: intervals disjoint
        if Rs < Lt or Rt < Ls:
            out.append(str(W[s] + W[t]))
            continue
        ans = INF
        # 3-vertex path s - u - t : u disjoint from both, i.e. strictly left of
        # both left endpoints or strictly right of both right endpoints
        lowL = Ls if Ls < Lt else Lt
        highR = Rs if Rs > Rt else Rt
        a = pref[lowL - 1]
        b = suff[highR + 1]
        u = a if a < b else b
        if u < INF:
            ans = W[s] + W[t] + u
        # 4-vertex induced path exists only for strictly crossing intervals:
        # earlier-starting endpoint takes a right neighbour, later-starting
        # endpoint takes a left neighbour
        if Ls < Lt and Rs < Rt:
            v = pref[Lt - 1] + suff[Rs + 1]
            if v < INF:
                c = W[s] + W[t] + v
                if c < ans:
                    ans = c
        elif Lt < Ls and Rt < Rs:
            v = pref[Ls - 1] + suff[Rt + 1]
            if v < INF:
                c = W[s] + W[t] + v
                if c < ans:
                    ans = c
        out.append(str(ans) if ans < INF else "-1")
    sys.stdout.write("\n".join(out) + "\n")

main()