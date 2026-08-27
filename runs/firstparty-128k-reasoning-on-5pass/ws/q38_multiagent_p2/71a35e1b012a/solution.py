import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    M = data[1]

    intervals = []
    full_idx = -1

    max_r_l1 = -1
    idx_max_r_l1 = -1
    min_l_rn = N + 1
    idx_min_l_rn = -1

    p = 2
    for i in range(M):
        L = data[p]
        R = data[p + 1]
        p += 2
        intervals.append((L, R, i))

        if L == 1 and R == N:
            if full_idx == -1:
                full_idx = i
        if L == 1 and R > max_r_l1:
            max_r_l1 = R
            idx_max_r_l1 = i
        if R == N and L < min_l_rn:
            min_l_rn = L
            idx_min_l_rn = i

    del data

    ops = [0] * M

    def emit(k):
        sys.stdout.write(str(k) + "\n")
        sys.stdout.write(" ".join(map(str, ops)) + "\n")

    if full_idx != -1:
        ops[full_idx] = 1
        emit(1)
        return

    intervals.sort()

    # Containment cost-2 check.
    # Prefix max R catches a previous interval with smaller L and R >= current R.
    # For the same L, larger R appears later, so if no previous interval contains
    # the current one, the current interval contains the first previous interval
    # with that same L.
    pref_max_r = -1
    pref_max_idx = -1
    prev_L = None
    first_idx_for_L = -1

    for L, R, i in intervals:
        if L != prev_L:
            prev_L = L
            first_idx_for_L = i

        if pref_max_r >= R:
            ops[pref_max_idx] = 1
            ops[i] = 2
            emit(2)
            return

        if first_idx_for_L != -1 and first_idx_for_L != i:
            ops[i] = 1
            ops[first_idx_for_L] = 2
            emit(2)
            return

        if R > pref_max_r:
            pref_max_r = R
            pref_max_idx = i

    # Two type-1 intervals cover [1, N].
    if (idx_max_r_l1 != -1 and idx_min_l_rn != -1 and
            idx_max_r_l1 != idx_min_l_rn and
            max_r_l1 + 1 >= min_l_rn):
        ops[idx_max_r_l1] = 1
        ops[idx_min_l_rn] = 1
        emit(2)
        return

    # Two type-2 intervals cover [1, N] iff their original intervals are disjoint.
    pref_min_r = N + 1
    pref_min_idx = -1
    for L, R, i in intervals:
        if pref_min_r < L:
            ops[pref_min_idx] = 2
            ops[i] = 2
            emit(2)
            return
        if R < pref_min_r:
            pref_min_r = R
            pref_min_idx = i

    # If no cost 1 or cost 2 exists and M >= 3, cost 3 is always achievable.
    if M >= 3:
        i1 = intervals[0][2]
        i2 = intervals[1][2]
        i3 = intervals[-1][2]
        ops[i1] = 1
        ops[i2] = 2
        ops[i3] = 1
        emit(3)
    else:
        sys.stdout.write("-1\n")

if __name__ == "__main__":
    solve()