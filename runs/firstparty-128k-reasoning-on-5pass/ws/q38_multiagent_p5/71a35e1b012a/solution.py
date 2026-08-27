import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    intervals = []
    full_idx = -1

    start_idx = -1
    max_r_start = -1

    end_idx = -1
    min_l_end = N + 1

    for idx in range(M):
        l = int(next(it))
        r = int(next(it))
        intervals.append((l, r, idx))

        if l == 1 and r == N:
            if full_idx == -1:
                full_idx = idx

        if l == 1 and r > max_r_start:
            max_r_start = r
            start_idx = idx

        if r == N and l < min_l_end:
            min_l_end = l
            end_idx = idx

    del data
    del it

    ops = [0] * M

    def emit(k):
        sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: one type-1 operation on the whole range.
    if full_idx != -1:
        ops[full_idx] = 1
        emit(1)
        return

    intervals.sort()

    # Cost 2: one type-1 interval contains one type-2 interval.
    max_r_prev = -1
    max_r_prev_idx = -1
    i = 0
    while i < M:
        l = intervals[i][0]
        j = i + 1
        while j < M and intervals[j][0] == l:
            j += 1

        # A previous interval with smaller L contains the smallest-R interval
        # of this group if its R is at least that R.
        if max_r_prev >= intervals[i][1]:
            ops[max_r_prev_idx] = 1
            ops[intervals[i][2]] = 2
            emit(2)
            return

        # Same left endpoint: the largest right endpoint contains another one.
        if j - i > 1:
            group_max_r = -1
            group_max_idx = -1
            for k in range(i, j):
                rr = intervals[k][1]
                idd = intervals[k][2]
                if rr > group_max_r:
                    group_max_r = rr
                    group_max_idx = idd

            other_idx = intervals[i][2]
            if other_idx == group_max_idx:
                for k in range(i, j):
                    if intervals[k][2] != group_max_idx:
                        other_idx = intervals[k][2]
                        break

            ops[group_max_idx] = 1
            ops[other_idx] = 2
            emit(2)
            return

        if intervals[i][1] > max_r_prev:
            max_r_prev = intervals[i][1]
            max_r_prev_idx = intervals[i][2]

        i = j

    # Cost 2: two type-2 intervals with empty intersection.
    min_r = N + 1
    min_r_idx = -1
    for l, r, idx in intervals:
        if l > min_r:
            ops[idx] = 2
            ops[min_r_idx] = 2
            emit(2)
            return
        if r < min_r:
            min_r = r
            min_r_idx = idx

    # Cost 2: two type-1 intervals whose union is [1, N].
    if (
        start_idx != -1
        and end_idx != -1
        and start_idx != end_idx
        and min_l_end <= max_r_start + 1
    ):
        ops[start_idx] = 1
        ops[end_idx] = 1
        emit(2)
        return

    # Cost 3 fallback: no cost 1 or 2 exists, so no containment pair exists.
    # The first three sorted intervals have strictly increasing L and R.
    if M >= 3:
        a, b, c = intervals[0], intervals[1], intervals[2]
        ops[a[2]] = 2
        ops[b[2]] = 1
        ops[c[2]] = 2
        emit(3)
        return

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    solve()