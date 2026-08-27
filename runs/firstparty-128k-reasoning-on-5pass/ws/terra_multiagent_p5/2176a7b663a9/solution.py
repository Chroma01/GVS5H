import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    w = [next(it) for _ in range(n)]

    m = 2 * n + 2
    INF = 10 ** 30

    best_r = [INF] * (m + 1)  # minimum W among intervals with this R
    best_l = [INF] * (m + 1)  # minimum W among intervals with this L
    L = [0] * n
    R = [0] * n

    for i in range(n):
        l = next(it)
        r = next(it)
        L[i] = l
        R[i] = r
        if w[i] < best_r[r]:
            best_r[r] = w[i]
        if w[i] < best_l[l]:
            best_l[l] = w[i]

    # pref[x] = min W_i such that R_i <= x
    pref = [INF] * (m + 1)
    cur = INF
    for x in range(m + 1):
        if best_r[x] < cur:
            cur = best_r[x]
        pref[x] = cur

    # suff[x] = min W_i such that L_i >= x
    suff = [INF] * (m + 2)
    cur = INF
    for x in range(m, -1, -1):
        if best_l[x] < cur:
            cur = best_l[x]
        suff[x] = cur

    q = next(it)
    out = []

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        ls, rs = L[s], R[s]
        lt, rt = L[t], R[t]

        extra = INF

        # Direct edge.
        if rs < lt or rt < ls:
            extra = 0
        else:
            # One intermediate vertex, left of both or right of both.
            extra = min(
                pref[min(ls, lt) - 1],
                suff[max(rs, rt) + 1]
            )

            # Two intermediate vertices.
            # left of s -> right of t
            a = pref[ls - 1]
            b = suff[rt + 1]
            if a + b < extra:
                extra = a + b

            # right of s -> left of t
            a = suff[rs + 1]
            b = pref[lt - 1]
            if a + b < extra:
                extra = a + b

        if extra >= INF:
            out.append("-1")
        else:
            out.append(str(w[s] + w[t] + extra))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()