import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    w = [next(it) for _ in range(n)]

    L = [0] * n
    R = [0] * n
    max_coord = 2 * n

    best_r = [10**30] * (max_coord + 1)
    best_l = [10**30] * (max_coord + 2)

    for i in range(n):
        l = next(it)
        r = next(it)
        L[i] = l
        R[i] = r
        if w[i] < best_r[r]:
            best_r[r] = w[i]
        if w[i] < best_l[l]:
            best_l[l] = w[i]

    pref = [10**30] * (max_coord + 1)
    cur = 10**30
    for x in range(max_coord + 1):
        if best_r[x] < cur:
            cur = best_r[x]
        pref[x] = cur

    suff = [10**30] * (max_coord + 2)
    cur = 10**30
    for x in range(max_coord, -1, -1):
        if best_l[x] < cur:
            cur = best_l[x]
        suff[x] = cur

    q = next(it)
    out = []
    INF = 10**30

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        ls, rs = L[s], R[s]
        lt, rt = L[t], R[t]
        base = w[s] + w[t]

        if rs < lt or rt < ls:
            out.append(str(base))
            continue

        left_limit = min(ls, lt) - 1
        right_limit = max(rs, rt) + 1

        common = min(pref[left_limit], suff[right_limit])
        if common < INF:
            out.append(str(base + common))
            continue

        # Order by left endpoint. For overlapping intervals with
        # increasing right endpoints, a 3-edge path can use:
        # an interval right of the first, then one left of the second.
        if ls <= lt:
            if rs < rt:
                x = suff[rs + 1]
                y = pref[lt - 1]
            else:
                x = y = INF
        else:
            if rt < rs:
                x = suff[rt + 1]
                y = pref[ls - 1]
            else:
                x = y = INF

        if x >= INF or y >= INF:
            out.append("-1")
        else:
            out.append(str(base + x + y))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()