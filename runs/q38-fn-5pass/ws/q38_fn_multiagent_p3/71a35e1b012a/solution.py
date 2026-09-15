import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    intervals = []
    ops = [0] * M

    full_idx = -1

    # For cost 2 using two type-1 operations:
    # one interval must start at 1, another must end at N.
    best_start_idx = -1
    best_start_r = -1
    best_end_idx = -1
    best_end_l = N + 1

    for i in range(M):
        l = int(next(it))
        r = int(next(it))
        intervals.append((l, r, i))

        if l == 1 and r == N:
            full_idx = i

        if l == 1 and r > best_start_r:
            best_start_r = r
            best_start_idx = i

        if r == N and l < best_end_l:
            best_end_l = l
            best_end_idx = i

    def finish(k):
        if k == -1:
            sys.stdout.write("-1\n")
        else:
            sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: one type-1 operation on a full interval.
    if full_idx != -1:
        ops[full_idx] = 1
        finish(1)
        return

    # Sort by L ascending, and for equal L by R descending.
    # Process equal-L intervals as a group.  This sweep finds:
    #   - a disjoint pair (two type-2 operations),
    #   - a containment pair (type-1 on container, type-2 on contained).
    intervals.sort(key=lambda x: (x[0], -x[1]))

    prev_min_r = N + 1
    prev_min_idx = -1
    prev_max_r = -1
    prev_max_idx = -1

    pos = 0
    while pos < M:
        l = intervals[pos][0]
        start = pos
        pos += 1
        while pos < M and intervals[pos][0] == l:
            pos += 1
        end = pos

        # Disjoint previous interval and current group.
        if prev_min_idx != -1 and prev_min_r < l:
            ops[prev_min_idx] = 2
            ops[intervals[start][2]] = 2
            finish(2)
            return

        # Previous interval contains some interval in the current group.
        if prev_max_idx != -1:
            for k in range(start, end):
                r = intervals[k][1]
                if prev_max_r >= r:
                    ops[prev_max_idx] = 1
                    ops[intervals[k][2]] = 2
                    finish(2)
                    return

        # Containment inside the same L-group.
        if end - start >= 2:
            ops[intervals[start][2]] = 1
            ops[intervals[start + 1][2]] = 2
            finish(2)
            return

        # Update extrema from strictly earlier L-groups only.
        group_min_r = intervals[end - 1][1]
        if group_min_r < prev_min_r:
            prev_min_r = group_min_r
            prev_min_idx = intervals[end - 1][2]

        group_max_r = intervals[start][1]
        if group_max_r > prev_max_r:
            prev_max_r = group_max_r
            prev_max_idx = intervals[start][2]

    # Cost 2: two type-1 operations covering [1, N].
    if (
        best_start_idx != -1
        and best_end_idx != -1
        and best_start_idx != best_end_idx
        and best_start_r + 1 >= best_end_l
    ):
        ops[best_start_idx] = 1
        ops[best_end_idx] = 1
        finish(2)
        return

    # Find an interval with maximum L and an interval with minimum R.
    max_l = -1
    min_r_val = N + 1
    p = -1
    q = -1

    for l, r, i in intervals:
        if l > max_l:
            max_l = l
            p = i
        if r < min_r_val:
            min_r_val = r
            q = i

    # If the same interval has both maximum L and minimum R, it is contained
    # in every other interval, giving a mixed type-1/type-2 cost-2 solution.
    if p == q:
        if M >= 2:
            other = 0 if p != 0 else 1
            ops[p] = 2
            ops[other] = 1
            finish(2)
            return
        finish(-1)
        return

    # With fewer than three operations, cost 3 is impossible.
    if M < 3:
        finish(-1)
        return

    # Fallback cost 3:
    # type-2 on max-L interval and min-R interval covers everything outside
    # their common intersection; any third interval contains that intersection.
    r_idx = 0
    if r_idx == p or r_idx == q:
        r_idx = 1
    if r_idx == p or r_idx == q:
        r_idx = 2

    ops[p] = 2
    ops[q] = 2
    ops[r_idx] = 1
    finish(3)


if __name__ == "__main__":
    solve()