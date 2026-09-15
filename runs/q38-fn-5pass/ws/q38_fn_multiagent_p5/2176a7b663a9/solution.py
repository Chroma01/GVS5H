import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    p += 1

    W = data[p:p + N]
    p += N

    M = 2 * N
    INF = 10 ** 30

    exact_r = [INF] * (M + 2)
    exact_l = [INF] * (M + 2)
    L = [0] * N
    R = [0] * N

    for i in range(N):
        l = data[p]
        r = data[p + 1]
        p += 2
        L[i] = l
        R[i] = r
        w = W[i]
        if w < exact_r[r]:
            exact_r[r] = w
        if w < exact_l[l]:
            exact_l[l] = w

    # pref[x] = minimum weight among intervals with R <= x
    pref = [INF] * (M + 2)
    cur = INF
    for x in range(1, M + 1):
        v = exact_r[x]
        if v < cur:
            cur = v
        pref[x] = cur

    # suff[x] = minimum weight among intervals with L >= x
    suff = [INF] * (M + 2)
    cur = INF
    for x in range(M, 0, -1):
        v = exact_l[x]
        if v < cur:
            cur = v
        suff[x] = cur

    Q = data[p]
    p += 1

    out = []
    append = out.append

    Lloc = L
    Rloc = R
    Wloc = W
    prefloc = pref
    suffloc = suff
    INFloc = INF
    data_loc = data

    for _ in range(Q):
        s = data_loc[p] - 1
        t = data_loc[p + 1] - 1
        p += 2

        ws = Wloc[s]
        wt = Wloc[t]
        ls = Lloc[s]
        rs = Rloc[s]
        lt = Lloc[t]
        rt = Rloc[t]

        # Direct edge: intervals are disjoint.
        if rs < lt or rt < ls:
            append(str(ws + wt))
            continue

        # Order the two intervals as A, B with L_A <= L_B.
        # Tie by smaller R to keep the structural inequalities clean.
        if ls < lt or (ls == lt and rs <= rt):
            lA = ls
            rA = rs
            lB = lt
            rB = rt
        else:
            lA = lt
            rA = rt
            lB = ls
            rB = rs

        rmax = rA if rA >= rB else rB

        # One intermediate vertex:
        #   left of both: R < L_A
        #   right of both: L > max(R_A, R_B)
        extra = prefloc[lA - 1]
        v = suffloc[rmax + 1]
        if v < extra:
            extra = v

        # Two intermediate vertices:
        #   X right of A: L_X > R_A
        #   Y left of B:  R_Y < L_B
        # Any such X and Y are disjoint because R_Y < L_B <= R_A < L_X.
        v = suffloc[rA + 1] + prefloc[lB - 1]
        if v < extra:
            extra = v

        if extra >= INFloc:
            append("-1")
        else:
            append(str(ws + wt + extra))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()