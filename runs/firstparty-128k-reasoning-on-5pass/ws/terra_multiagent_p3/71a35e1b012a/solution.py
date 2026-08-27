import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())
    intervals = [tuple(map(int, input().split())) for _ in range(M)]

    def output(choices):
        ans = [0] * M
        for idx, typ in choices:
            ans[idx] = typ
        sys.stdout.write(str(len(choices)) + "\n")
        sys.stdout.write(" ".join(map(str, ans)) + "\n")
        raise SystemExit

    # Minimum cost 1.
    for i, (l, r) in enumerate(intervals):
        if l == 1 and r == N:
            output([(i, 1)])

    order = sorted(range(M), key=lambda i: intervals[i][0])

    # Minimum cost 2: complements of two disjoint intervals.
    best_r = -1
    best_id = -1
    for idx in order:
        l, r = intervals[idx]
        if best_id != -1 and best_r < l:
            output([(best_id, 2), (idx, 2)])
        if r > best_r:
            best_r = r
            best_id = idx

    # Minimum cost 2: complement of interval I and ordinary operation
    # on a distinct interval J containing I.
    #
    # Process intervals by left endpoint. A Fenwick tree over reversed
    # right-endpoint ranks supports finding an interval with L_j <= L_i
    # and R_j >= R_i. Each Fenwick node stores two IDs, so I itself can
    # be excluded from the result.
    right_values = sorted(set(r for _, r in intervals))
    k_right = len(right_values)
    bit1 = [M] * (k_right + 1)
    bit2 = [M] * (k_right + 1)

    def add_to_node(pos, idx):
        a = bit1[pos]
        b = bit2[pos]
        if idx < a:
            bit2[pos] = a
            bit1[pos] = idx
        elif idx != a and idx < b:
            bit2[pos] = idx

    def update(right, idx):
        rank = bisect_left(right_values, right)
        pos = k_right - rank
        while pos <= k_right:
            add_to_node(pos, idx)
            pos += pos & -pos

    def merge_candidate(a, b, idx):
        if idx < a:
            return idx, a
        if idx != a and idx < b:
            return a, idx
        return a, b

    def query(right):
        rank = bisect_left(right_values, right)
        pos = k_right - rank
        a = b = M
        while pos > 0:
            a, b = merge_candidate(a, b, bit1[pos])
            a, b = merge_candidate(a, b, bit2[pos])
            pos -= pos & -pos
        return a, b

    containing = [-1] * M
    p = 0
    while p < M:
        q = p + 1
        current_left = intervals[order[p]][0]
        while q < M and intervals[order[q]][0] == current_left:
            q += 1

        for pos in range(p, q):
            idx = order[pos]
            update(intervals[idx][1], idx)

        for pos in range(p, q):
            idx = order[pos]
            a, b = query(intervals[idx][1])
            if a != idx and a < M:
                containing[idx] = a
            elif b != idx and b < M:
                containing[idx] = b

        p = q

    for i in range(M):
        if containing[i] != -1:
            output([(i, 2), (containing[i], 1)])

    # Minimum cost 2: two ordinary intervals. Since the disjoint-pair
    # case was already rejected, any interval starting at 1 and a distinct
    # interval ending at N overlap and cover the entire domain.
    left_ids = [i for i, (l, r) in enumerate(intervals) if l == 1]
    right_ids = [i for i, (l, r) in enumerate(intervals) if r == N]
    if left_ids and right_ids:
        for a in left_ids[:2]:
            for b in right_ids[:2]:
                if a != b:
                    output([(a, 1), (b, 1)])

    # No two intervals are disjoint. Thus all intervals pairwise intersect.
    # With at least three intervals, two complements leave a core contained
    # in every interval, and a third ordinary operation covers that core.
    if M >= 3:
        max_l_id = max(range(M), key=lambda i: intervals[i][0])
        min_r_id = min(range(M), key=lambda i: intervals[i][1])

        if max_l_id != min_r_id:
            ordinary_id = next(
                i for i in range(M)
                if i != max_l_id and i != min_r_id
            )
            output([
                (max_l_id, 2),
                (min_r_id, 2),
                (ordinary_id, 1),
            ])
        else:
            second_min_r_id = min(
                (i for i in range(M) if i != max_l_id),
                key=lambda i: intervals[i][1]
            )
            ordinary_id = next(
                i for i in range(M)
                if i != max_l_id and i != second_min_r_id
            )
            output([
                (max_l_id, 2),
                (second_min_r_id, 2),
                (ordinary_id, 1),
            ])

    print(-1)


if __name__ == "__main__":
    solve()