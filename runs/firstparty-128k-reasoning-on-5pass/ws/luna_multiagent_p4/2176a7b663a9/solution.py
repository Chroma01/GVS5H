import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    weights = [next(it) for _ in range(n)]

    left_end = [0] * n
    right_end = [0] * n
    max_coord = 2 * n + 2

    by_r = [10**30] * (max_coord + 2)
    by_l = [10**30] * (max_coord + 2)

    for i in range(n):
        l = next(it)
        r = next(it)
        left_end[i] = l
        right_end[i] = r
        if weights[i] < by_r[r]:
            by_r[r] = weights[i]
        if weights[i] < by_l[l]:
            by_l[l] = weights[i]

    # left_before[x] = minimum weight of an interval with R < x
    left_before = [10**30] * (max_coord + 3)
    cur = 10**30
    for x in range(max_coord + 2):
        left_before[x] = cur
        if by_r[x] < cur:
            cur = by_r[x]

    # right_after[x] = minimum weight of an interval with L > x
    right_after = [10**30] * (max_coord + 3)
    cur = 10**30
    for x in range(max_coord + 1, -1, -1):
        right_after[x] = cur
        if by_l[x] < cur:
            cur = by_l[x]

    q = next(it)
    out = []
    inf = 10**30

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        ls, rs = left_end[s], right_end[s]
        lt, rt = left_end[t], right_end[t]
        ws, wt = weights[s], weights[t]

        # Direct edge: the intervals are disjoint.
        if rs < lt or rt < ls:
            out.append(str(ws + wt))
            continue

        best_middle = inf

        # A common neighbor lying strictly to the left of both intervals.
        cand = left_before[min(ls, lt)]
        if cand < best_middle:
            best_middle = cand

        # A common neighbor lying strictly to the right of both intervals.
        cand = right_after[max(rs, rt)]
        if cand < best_middle:
            best_middle = cand

        # Three-edge path: left of s, then right of t.
        a = left_before[ls]
        b = right_after[rt]
        if a < inf and b < inf and a + b < best_middle:
            best_middle = a + b

        # Three-edge path: right of s, then left of t.
        a = right_after[rs]
        b = left_before[lt]
        if a < inf and b < inf and a + b < best_middle:
            best_middle = a + b

        if best_middle == inf:
            out.append("-1")
        else:
            out.append(str(ws + wt + best_middle))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()