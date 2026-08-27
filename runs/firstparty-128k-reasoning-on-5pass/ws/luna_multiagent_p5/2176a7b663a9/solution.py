import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    w = [next(it) for _ in range(n)]

    L = [0] * n
    R = [0] * n
    max_coord = 2 * n

    for i in range(n):
        L[i] = next(it)
        R[i] = next(it)

    INF = 10**30

    # Minimum weight among intervals whose R is at most x.
    by_r = [INF] * (max_coord + 1)
    # Minimum weight among intervals whose L is at least x.
    by_l = [INF] * (max_coord + 2)

    for i in range(n):
        if w[i] < by_r[R[i]]:
            by_r[R[i]] = w[i]
        if w[i] < by_l[L[i]]:
            by_l[L[i]] = w[i]

    pref = [INF] * (max_coord + 1)
    cur = INF
    for x in range(max_coord + 1):
        if by_r[x] < cur:
            cur = by_r[x]
        pref[x] = cur

    suf = [INF] * (max_coord + 2)
    cur = INF
    for x in range(max_coord, -1, -1):
        if by_l[x] < cur:
            cur = by_l[x]
        suf[x] = cur

    q = next(it)
    ans = []

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        # Direct edge.
        if R[s] < L[t] or R[t] < L[s]:
            ans.append(str(w[s] + w[t]))
            continue

        # Minimum-weight common neighbor:
        # either strictly left of both intervals, or strictly right of both.
        left_limit = min(L[s], L[t]) - 1
        right_limit = max(R[s], R[t]) + 1

        extra = INF
        if left_limit >= 0:
            extra = min(extra, pref[left_limit])
        if right_limit <= max_coord:
            extra = min(extra, suf[right_limit])

        # Three-edge path using:
        #   a right of s and b left of t, or
        #   a left of s and b right of t.
        right_s = suf[R[s] + 1] if R[s] + 1 <= max_coord else INF
        left_s = pref[L[s] - 1] if L[s] - 1 >= 0 else INF
        right_t = suf[R[t] + 1] if R[t] + 1 <= max_coord else INF
        left_t = pref[L[t] - 1] if L[t] - 1 >= 0 else INF

        if right_s < INF and left_t < INF:
            extra = min(extra, right_s + left_t)
        if left_s < INF and right_t < INF:
            extra = min(extra, left_s + right_t)

        if extra >= INF:
            ans.append("-1")
        else:
            ans.append(str(w[s] + w[t] + extra))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()