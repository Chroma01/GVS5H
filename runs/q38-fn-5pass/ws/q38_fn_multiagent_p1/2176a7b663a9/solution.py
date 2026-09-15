import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    p += 1

    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = data[p]
        p += 1

    M = 2 * N + 2
    INF = 10 ** 18

    # pref[x] = minimum W_i among intervals with R_i <= x
    # suff[x] = minimum W_i among intervals with L_i >= x
    pref = [INF] * (M + 2)
    suff = [INF] * (M + 2)

    L = [0] * (N + 1)
    R = [0] * (N + 1)

    for i in range(1, N + 1):
        l = data[p]
        r = data[p + 1]
        p += 2
        L[i] = l
        R[i] = r
        w = W[i]

        if w < pref[r]:
            pref[r] = w
        if w < suff[l]:
            suff[l] = w

    for i in range(1, M + 1):
        if pref[i - 1] < pref[i]:
            pref[i] = pref[i - 1]

    for i in range(M, -1, -1):
        if suff[i + 1] < suff[i]:
            suff[i] = suff[i + 1]

    Q = data[p]
    p += 1

    out = []
    append = out.append

    for _ in range(Q):
        s = data[p]
        t = data[p + 1]
        p += 2

        ls = L[s]
        rs = R[s]
        lt = L[t]
        rt = R[t]
        ws = W[s]
        wt = W[t]

        # Direct edge: intervals are disjoint.
        if rs < lt or rt < ls:
            append(str(ws + wt))
            continue

        # Intervals overlap. A shortest path has at most three edges.
        ml = ls if ls < lt else lt
        mr = rs if rs > rt else rt

        # Two-edge path through a common neighbor:
        # completely left of both, or completely right of both.
        best = pref[ml - 1]

        v = suff[mr + 1]
        if v < best:
            best = v

        # Three-edge paths through opposite sides.
        v = pref[ls - 1] + suff[rt + 1]
        if v < best:
            best = v

        v = suff[rs + 1] + pref[lt - 1]
        if v < best:
            best = v

        if best >= INF:
            append("-1")
        else:
            append(str(ws + wt + best))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()