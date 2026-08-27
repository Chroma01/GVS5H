import sys
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    W = [int(data[pos + i]) for i in range(n)]
    pos += n
    L = [0] * n
    R = [0] * n
    for i in range(n):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2
    q = int(data[pos]); pos += 1

    # ---- preprocessing ----
    # sort by R: prefix two-cheapest (by W)
    ordR = sorted(range(n), key=lambda i: (R[i], i))
    R_sorted = [R[i] for i in ordR]
    pre2 = [(-1, -1)] * n
    b1 = b2 = -1
    for k, i in enumerate(ordR):
        wi = W[i]
        if b1 == -1 or wi < W[b1]:
            b2 = b1; b1 = i
        elif b2 == -1 or wi < W[b2]:
            b2 = i
        pre2[k] = (b1, b2)

    # sort by L: suffix two-cheapest (by W)
    ordL = sorted(range(n), key=lambda i: (L[i], i))
    L_sorted = [L[i] for i in ordL]
    suf2 = [(-1, -1)] * n
    b1 = b2 = -1
    for k in range(n - 1, -1, -1):
        i = ordL[k]
        wi = W[i]
        if b1 == -1 or wi < W[b1]:
            b2 = b1; b1 = i
        elif b2 == -1 or wi < W[b2]:
            b2 = i
        suf2[k] = (b1, b2)

    def cheapest_R_lt(p):
        # two cheapest vertices with R < p (strict)
        k = bisect.bisect_left(R_sorted, p)
        if k == 0:
            return (-1, -1)
        return pre2[k - 1]

    def cheapest_L_gt(p):
        # two cheapest vertices with L > p (strict)
        k = bisect.bisect_right(L_sorted, p)
        if k == n:
            return (-1, -1)
        return suf2[k]

    # per-vertex cheapest/2nd-cheapest left and right neighbors
    left2 = [None] * n
    right2 = [None] * n
    for v in range(n):
        left2[v] = cheapest_R_lt(L[v])
        right2[v] = cheapest_L_gt(R[v])

    INF = 1 << 62
    out = []
    for _ in range(q):
        s = int(data[pos]) - 1; t = int(data[pos + 1]) - 1; pos += 2
        ws = W[s]; wt = W[t]
        Ls = L[s]; Rs = R[s]; Lt = L[t]; Rt = R[t]
        ans = INF

        # (i) direct edge
        if Rs < Lt or Rt < Ls:
            ans = ws + wt

        # (ii) 2-hop via cheapest common neighbor
        lo = Ls if Ls < Lt else Lt
        hi = Rs if Rs > Rt else Rt
        for c in cheapest_R_lt(lo):
            if c != -1 and c != s and c != t:
                ans = min(ans, ws + wt + W[c])
        for c in cheapest_L_gt(hi):
            if c != -1 and c != s and c != t:
                ans = min(ans, ws + wt + W[c])

        # (iii) 3-hop: x in N(s), y in N(t), x-y edge
        a1, a2 = left2[s]
        a3, a4 = right2[s]
        b1_, b2_ = left2[t]
        b3_, b4_ = right2[t]
        for x in (a1, a2, a3, a4):
            if x == -1 or x == t:
                continue
            Rx = R[x]; Lx = L[x]; wx = W[x]
            for y in (b1_, b2_, b3_, b4_):
                if y == -1 or y == s or y == x:
                    continue
                if Rx < L[y] or R[y] < Lx:
                    ans = min(ans, ws + wt + wx + W[y])

        out.append(str(ans if ans < INF else -1))

    sys.stdout.write("\n".join(out) + "\n")

main()