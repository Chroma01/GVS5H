import sys
from bisect import bisect_right


def validate(n, left, right, chosen):
    points = {1, n + 1}
    for _, idx in chosen:
        points.add(left[idx])
        points.add(right[idx] + 1)
    points = sorted(points)

    for p, q in zip(points, points[1:]):
        covered = False
        for typ, idx in chosen:
            inside = left[idx] <= p <= right[idx]
            if (typ == 1 and inside) or (typ == 2 and not inside):
                covered = True
                break
        if not covered:
            return False
    return True


def output_answer(m, chosen):
    operations = [0] * m
    for typ, idx in chosen:
        operations[idx] = typ
    print(len(chosen))
    print(*operations)


def solve():
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())

    left = [0] * m
    right = [0] * m
    for i in range(m):
        left[i], right[i] = map(int, input().split())

    # One ordinary interval covers everything.
    for i in range(m):
        if left[i] == 1 and right[i] == n:
            output_answer(m, [(1, i)])
            return

    # For each possible lower bound x, keep the two intervals with
    # largest right endpoints among intervals with L <= x.
    order_l = sorted(range(m), key=lambda i: left[i])
    sorted_l = [left[i] for i in order_l]
    pref_best1 = [-1] * m
    pref_best2 = [-1] * m

    best1 = best2 = -1
    for pos, idx in enumerate(order_l):
        if best1 == -1 or right[idx] > right[best1]:
            best2 = best1
            best1 = idx
        elif idx != best1 and (best2 == -1 or right[idx] > right[best2]):
            best2 = idx
        pref_best1[pos] = best1
        pref_best2[pos] = best2

    def prefix_candidates(x):
        pos = bisect_right(sorted_l, x) - 1
        if pos < 0:
            return ()
        return pref_best1[pos], pref_best2[pos]

    # For each possible upper bound x, keep the two intervals with
    # smallest left endpoints among intervals with R >= x.
    order_r = sorted(range(m), key=lambda i: -right[i])
    neg_right = [-right[i] for i in order_r]
    suff_best1 = [-1] * m
    suff_best2 = [-1] * m

    best1 = best2 = -1
    for pos, idx in enumerate(order_r):
        if best1 == -1 or left[idx] < left[best1]:
            best2 = best1
            best1 = idx
        elif idx != best1 and (best2 == -1 or left[idx] < left[best2]):
            best2 = idx
        suff_best1[pos] = best1
        suff_best2[pos] = best2

    def suffix_candidates(x):
        pos = bisect_right(neg_right, -x) - 1
        if pos < 0:
            return ()
        return suff_best1[pos], suff_best2[pos]

    min_r_idx = min(range(m), key=lambda i: right[i])
    max_l_idx = max(range(m), key=lambda i: left[i])

    # Two complement operations suffice iff two original intervals are disjoint.
    if right[min_r_idx] < left[max_l_idx]:
        chosen = [(2, min_r_idx), (2, max_l_idx)]
        if validate(n, left, right, chosen):
            output_answer(m, chosen)
            return

    # Two ordinary intervals suffice if one starts at 1 and another ends at N.
    first_candidates = [i for i in range(m) if left[i] == 1]
    last_candidates = [i for i in range(m) if right[i] == n]

    if first_candidates and last_candidates:
        a = max(first_candidates, key=lambda i: right[i])
        b = min(last_candidates, key=lambda i: left[i])
        if a != b:
            chosen = [(1, a), (1, b)]
            if validate(n, left, right, chosen):
                output_answer(m, chosen)
                return

    # One ordinary interval and one complement suffice when the ordinary
    # interval contains the complement operation's original interval.
    for b in range(m):
        for a in prefix_candidates(left[b]):
            if a != -1 and a != b and right[a] >= right[b]:
                chosen = [(1, a), (2, b)]
                if validate(n, left, right, chosen):
                    output_answer(m, chosen)
                    return

    # If all intervals pairwise intersect, their common intersection is
    # [max L, min R]. Two complements leave this intersection, and any
    # third ordinary interval covers it.
    if m >= 3 and left[max_l_idx] <= right[min_r_idx]:
        p = max_l_idx
        q = min_r_idx

        if p == q:
            q = 0 if p != 0 else 1

        for t in range(m):
            if t != p and t != q:
                chosen = [(2, p), (2, q), (1, t)]
                if validate(n, left, right, chosen):
                    output_answer(m, chosen)
                    return

    # One complement and two ordinary intervals. The two ordinary intervals
    # must cover the complement operation's original interval.
    for b in range(m):
        l, r = left[b], right[b]

        for a in prefix_candidates(l):
            if a == -1 or a == b or right[a] < l:
                continue

            for c in suffix_candidates(r):
                if c == -1 or c == b or c == a:
                    continue
                if left[c] <= right[a] + 1:
                    chosen = [(1, a), (1, c), (2, b)]
                    if validate(n, left, right, chosen):
                        output_answer(m, chosen)
                        return

    print(-1)


if __name__ == "__main__":
    solve()