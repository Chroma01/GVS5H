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

    L = [0] * N
    R = [0] * N

    max_c = 2 * N
    INF = 10 ** 30

    at_r = [INF] * (max_c + 2)
    at_l = [INF] * (max_c + 2)

    for i in range(N):
        l = data[p]
        r = data[p + 1]
        p += 2
        L[i] = l
        R[i] = r
        w = W[i]
        if w < at_r[r]:
            at_r[r] = w
        if w < at_l[l]:
            at_l[l] = w

    Q = data[p]
    p += 1

    # pref[x] = minimum weight of an interval with R <= x
    pref = [INF] * (max_c + 2)
    cur = INF
    for x in range(1, max_c + 1):
        v = at_r[x]
        if v < cur:
            cur = v
        pref[x] = cur

    # suff[x] = minimum weight of an interval with L >= x
    suff = [INF] * (max_c + 3)
    cur = INF
    for x in range(max_c, 0, -1):
        v = at_l[x]
        if v < cur:
            cur = v
        suff[x] = cur

    del at_r, at_l

    # left_min[i]: min weight of an interval strictly to the left of i
    # right_min[i]: min weight of an interval strictly to the right of i
    left_min = [0] * N
    right_min = [0] * N
    for i in range(N):
        left_min[i] = pref[L[i] - 1]
        right_min[i] = suff[R[i] + 1]

    out = []
    append = out.append

    for _ in range(Q):
        s = data[p] - 1
        t = data[p + 1] - 1
        p += 2

        ls = L[s]
        lt = L[t]
        rs = R[s]
        rt = R[t]

        # Direct edge: disjoint intervals.
        if rs < lt or rt < ls:
            append(str(W[s] + W[t]))
            continue

        # Overlapping endpoints. Any optimal path has at most 3 edges.
        base = W[s] + W[t]
        best = INF

        # One intermediate vertex disjoint from both:
        # strictly left of both, or strictly right of both.
        if ls < lt:
            v = pref[ls - 1]
        else:
            v = pref[lt - 1]
        if v < best:
            best = v

        if rs > rt:
            v = suff[rs + 1]
        else:
            v = suff[rt + 1]
        if v < best:
            best = v

        # Two intermediate vertices on opposite sides.
        # s -- (left of s) -- (right of t) -- t
        v = left_min[s] + right_min[t]
        if v < best:
            best = v

        # s -- (right of s) -- (left of t) -- t
        v = right_min[s] + left_min[t]
        if v < best:
            best = v

        if best >= INF:
            append("-1")
        else:
            append(str(base + best))

    del data
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()