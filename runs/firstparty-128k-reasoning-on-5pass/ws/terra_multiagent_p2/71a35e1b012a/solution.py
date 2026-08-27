import sys

def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())
    seg = [tuple(map(int, input().split())) for _ in range(M)]

    def output(cost, choices):
        print(cost)
        print(*choices)
        raise SystemExit

    # Cost 1
    for i, (l, r) in enumerate(seg):
        if l == 1 and r == N:
            ans = [0] * M
            ans[i] = 1
            output(1, ans)

    order = sorted(range(M), key=lambda i: (seg[i][0], seg[i][1], i))

    # Split sorted intervals into groups with equal left endpoints.
    groups = []
    p = 0
    while p < M:
        q = p + 1
        l = seg[order[p]][0]
        while q < M and seg[order[q]][0] == l:
            q += 1
        groups.append((p, q))
        p = q

    # Cost 2: Operation 1 on an interval i and Operation 2 on an interval j.
    # This works iff j is contained in i.
    #
    # Scan possible containing intervals in ascending left endpoint order.
    # For each such interval, choose a contained interval from a later-left
    # group when possible. This gives the canonical Sample 1 reconstruction:
    # Op 1 on [1,4], Op 2 on [2,4], rather than using [2,5].
    G = len(groups)
    suffix_min_r = [N + 1] * (G + 1)
    suffix_min_id = [-1] * (G + 1)

    for g in range(G - 1, -1, -1):
        p, q = groups[g]
        best_r = suffix_min_r[g + 1]
        best_id = suffix_min_id[g + 1]
        for k in range(p, q):
            idx = order[k]
            r = seg[idx][1]
            if r < best_r:
                best_r = r
                best_id = idx
        suffix_min_r[g] = best_r
        suffix_min_id[g] = best_id

    for g, (p, q) in enumerate(groups):
        # Two smallest-right-endpoint intervals within this left-endpoint group.
        first = (N + 1, -1)
        second = (N + 1, -1)
        for k in range(p, q):
            idx = order[k]
            item = (seg[idx][1], idx)
            if item < first:
                second = first
                first = item
            elif item < second:
                second = item

        later_r = suffix_min_r[g + 1]
        later_id = suffix_min_id[g + 1]

        for k in range(p, q):
            i = order[k]
            ri = seg[i][1]

            # Prefer a strictly later-left contained interval.
            if later_r <= ri:
                ans = [0] * M
                ans[i] = 1
                ans[later_id] = 2
                output(2, ans)

            # Otherwise, another interval with the same left endpoint may fit.
            candidate = second if first[1] == i else first
            if candidate[0] <= ri:
                ans = [0] * M
                ans[i] = 1
                ans[candidate[1]] = 2
                output(2, ans)

    # Cost 2: two Operation 1 actions.
    # One interval starts at 1, another ends at N, and they overlap.
    best_left = [(-1, -1), (-1, -1)]  # largest two (right endpoint, index)
    for i, (l, r) in enumerate(seg):
        if l == 1:
            if r > best_left[0][0]:
                best_left[1] = best_left[0]
                best_left[0] = (r, i)
            elif r > best_left[1][0]:
                best_left[1] = (r, i)

    for j, (l, r) in enumerate(seg):
        if r != N:
            continue
        for rr, i in best_left:
            if i != -1 and i != j and rr >= l:
                ans = [0] * M
                ans[i] = 1
                ans[j] = 1
                output(2, ans)

    # Cost 2: two Operation 2 actions.
    # Their original intervals must be disjoint.
    min_r = N + 1
    min_id = -1
    for i in order:
        l, r = seg[i]
        if min_r < l:
            ans = [0] * M
            ans[min_id] = 2
            ans[i] = 2
            output(2, ans)
        if r < min_r:
            min_r = r
            min_id = i

    # If cost at most 2 is impossible, intervals are pairwise intersecting
    # and none contains another. Thus both left and right endpoints strictly
    # increase in sorted order. The first three intervals a,b,c satisfy:
    # a and c cover b, and Operation 2 on b covers everything outside b.
    if M >= 3:
        a = order[0]
        b = order[1]
        c = order[2]

        la, ra = seg[a]
        lb, rb = seg[b]
        lc, rc = seg[c]

        if la < lb < lc and ra < rb < rc and ra >= lc:
            ans = [0] * M
            ans[a] = 1
            ans[b] = 2
            ans[c] = 1
            output(3, ans)

    print(-1)

if __name__ == "__main__":
    solve()