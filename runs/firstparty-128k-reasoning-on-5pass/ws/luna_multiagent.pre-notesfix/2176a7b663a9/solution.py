import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    w = [next(it) for _ in range(n)]

    L = [0] * n
    R = [0] * n
    max_coord = 2 * n

    by_r = [10**30] * (max_coord + 2)
    by_l = [10**30] * (max_coord + 2)

    for i in range(n):
        l = next(it)
        r = next(it)
        L[i] = l
        R[i] = r
        if w[i] < by_r[r]:
            by_r[r] = w[i]
        if w[i] < by_l[l]:
            by_l[l] = w[i]

    pref = [10**30] * (max_coord + 2)
    cur = 10**30
    for x in range(1, max_coord + 1):
        if by_r[x] < cur:
            cur = by_r[x]
        pref[x] = cur

    suff = [10**30] * (max_coord + 3)
    cur = 10**30
    for x in range(max_coord, 0, -1):
        if by_l[x] < cur:
            cur = by_l[x]
        suff[x] = cur

    left_cost = [0] * n
    right_cost = [0] * n
    for i in range(n):
        left_cost[i] = pref[L[i] - 1]
        right_cost[i] = suff[R[i] + 1]

    q = next(it)
    out = []
    INF = 10**30

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        # Direct edge: the intervals are strictly disjoint.
        if R[s] < L[t] or R[t] < L[s]:
            out.append(str(w[s] + w[t]))
            continue

        best = INF

        # One common neighbor strictly to the left.
        c = pref[min(L[s], L[t]) - 1]
        if c < INF:
            best = c

        # One common neighbor strictly to the right.
        c = suff[max(R[s], R[t]) + 1]
        if c < best:
            best = c

        # Three-vertex path through a left neighbor of one endpoint
        # and a right neighbor of the other endpoint.
        if left_cost[s] < INF and right_cost[t] < INF:
            c = left_cost[s] + right_cost[t]
            if c < best:
                best = c
        if right_cost[s] < INF and left_cost[t] < INF:
            c = right_cost[s] + left_cost[t]
            if c < best:
                best = c

        if best >= INF:
            out.append("-1")
        else:
            out.append(str(w[s] + w[t] + best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()