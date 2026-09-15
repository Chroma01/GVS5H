import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    L = [0] * M
    R = [0] * M
    p = 2
    for i in range(M):
        L[i] = int(data[p])
        R[i] = int(data[p + 1])
        p += 2

    out = sys.stdout

    # ---- cost 1: some interval is exactly [1, N] (must be type 1) ----
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            res = [0] * M
            res[i] = 1
            out.write("1\n" + " ".join(map(str, res)) + "\n")
            return

    # ---- cost 2, mixed: type1 on A, type2 on B, valid iff B subset of A ----
    # Sort by (L asc, R asc). Within an equal-L run the LARGER R comes LAST.
    #  * same-L pair (prev,k): [L,R[prev]] subset of [L,R[k]]  -> outer=k, inner=prev
    #  * cross-L: prefix max R over strictly smaller L contains k if R[k] <= curMax
    order = sorted(range(M), key=lambda i: (L[i], R[i]))
    curMax = -1
    curIdx = -1
    prev = -1
    for k in order:
        if prev != -1 and L[prev] == L[k]:
            res = [0] * M
            res[k] = 1          # outer (larger R), contains prev
            res[prev] = 2       # inner
            out.write("2\n" + " ".join(map(str, res)) + "\n")
            return
        if R[k] <= curMax:      # contained in earlier interval with strictly smaller L
            res = [0] * M
            res[curIdx] = 1
            res[k] = 2
            out.write("2\n" + " ".join(map(str, res)) + "\n")
            return
        if R[k] > curMax:
            curMax = R[k]
            curIdx = k
        prev = k

    # ---- cost 2, two type-1: one covers 1, one covers N, union connected ----
    iS = -1
    maxR_S = -1
    iT = -1
    minL_T = N + 1
    for i in range(M):
        if L[i] == 1 and R[i] > maxR_S:
            maxR_S = R[i]
            iS = i
        if R[i] == N and L[i] < minL_T:
            minL_T = L[i]
            iT = i
    if iS != -1 and iT != -1 and iS != iT and maxR_S + 1 >= minL_T:
        res = [0] * M
        res[iS] = 1
        res[iT] = 1
        out.write("2\n" + " ".join(map(str, res)) + "\n")
        return

    # ---- cost 2, two type-2: valid iff the two intervals are disjoint ----
    iMinR = -1
    minR = N + 1
    iMaxL = -1
    maxL = 0
    for i in range(M):
        if R[i] < minR:
            minR = R[i]
            iMinR = i
        if L[i] > maxL:
            maxL = L[i]
            iMaxL = i
    if minR < maxL:             # iMinR != iMaxL automatically since L_i <= R_i
        res = [0] * M
        res[iMinR] = 2
        res[iMaxL] = 2
        out.write("2\n" + " ".join(map(str, res)) + "\n")
        return

    # ---- cost 3 (only possible when M >= 3 and no cost-2 exists) ----
    # No cost-2 => intervals form a pairwise-intersecting antichain => common point.
    # a = min L, c = max R overlap; every other b lies inside A_a union A_c.
    if M >= 3:
        a = min(range(M), key=lambda i: (L[i], R[i]))
        c = max(range(M), key=lambda i: (R[i], L[i]))
        b = -1
        for i in range(M):
            if i != a and i != c:
                b = i
                break
        res = [0] * M
        res[a] = 1
        res[c] = 1
        res[b] = 2
        out.write("3\n" + " ".join(map(str, res)) + "\n")
        return

    out.write("-1\n")


main()