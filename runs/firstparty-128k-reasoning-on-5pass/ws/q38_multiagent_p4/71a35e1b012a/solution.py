import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    intervals = []
    full_idx = -1

    max_r_start = -1
    max_r_start_idx = -1
    min_l_end = N + 1
    min_l_end_idx = -1

    p = 2
    for i in range(M):
        L = int(data[p])
        R = int(data[p + 1])
        p += 2

        intervals.append((L, R, i))

        if L == 1 and R == N:
            full_idx = i

        if L == 1 and R > max_r_start:
            max_r_start = R
            max_r_start_idx = i

        if R == N and L < min_l_end:
            min_l_end = L
            min_l_end_idx = i

    del data

    ops = [0] * M

    def emit(k):
        sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: only a full interval with operation 1.
    if full_idx != -1:
        ops[full_idx] = 1
        emit(1)
        return

    # Sort by L ascending, then R ascending, then original index.
    intervals.sort()

    # Cost 2, mixed: one interval contains the other.
    # Use op 1 on the container and op 2 on the contained interval.
    max_r = -1
    max_r_idx = -1
    last_same_l_idx = -1
    last_l = -1

    for L, R, idx in intervals:
        if L != last_l:
            last_same_l_idx = -1
            last_l = L

        # A previous interval with smaller/equal L and larger/equal R contains current.
        if max_r >= R:
            ops[max_r_idx] = 1
            ops[idx] = 2
            emit(2)
            return

        # Same L, and because R is sorted ascending, current contains the previous same-L interval.
        if last_same_l_idx != -1:
            ops[idx] = 1
            ops[last_same_l_idx] = 2
            emit(2)
            return

        if R > max_r:
            max_r = R
            max_r_idx = idx

        last_same_l_idx = idx

    # Cost 2, both type 1: union of two intervals is [1, N].
    if (max_r_start_idx != -1 and min_l_end_idx != -1
            and max_r_start >= min_l_end - 1):
        ops[max_r_start_idx] = 1
        ops[min_l_end_idx] = 1
        emit(2)
        return

    # Cost 2, both type 2: original intervals are disjoint.
    min_r = N + 1
    min_r_idx = -1
    for L, R, idx in intervals:
        if min_r < L:
            ops[min_r_idx] = 2
            ops[idx] = 2
            emit(2)
            return
        if R < min_r:
            min_r = R
            min_r_idx = idx

    if M < 3:
        sys.stdout.write("-1\n")
        return

    # Cost 3 fallback: any three intervals suffice.
    a, b, c = intervals[0], intervals[1], intervals[2]

    coords = [1, N + 1]
    for L, R, _ in (a, b, c):
        coords.append(L)
        coords.append(R + 1)
    coords = sorted(set(coords))

    seen = 0
    for i in range(len(coords) - 1):
        pos = coords[i]
        mask = 0
        if a[0] <= pos <= a[1]:
            mask |= 1
        if b[0] <= pos <= b[1]:
            mask |= 2
        if c[0] <= pos <= c[1]:
            mask |= 4
        seen |= 1 << mask

    absent_mask = -1
    for m in range(8):
        if not ((seen >> m) & 1):
            absent_mask = m
            break

    # Should never happen for three intervals on a line, but keep a safe fallback.
    if absent_mask == -1:
        ops[a[2]] = 2
        ops[b[2]] = 1
        ops[c[2]] = 2
        emit(3)
        return

    if (absent_mask & 1) == 0:
        ops[a[2]] = 1
    else:
        ops[a[2]] = 2

    if (absent_mask & 2) == 0:
        ops[b[2]] = 1
    else:
        ops[b[2]] = 2

    if (absent_mask & 4) == 0:
        ops[c[2]] = 1
    else:
        ops[c[2]] = 2

    emit(3)


if __name__ == "__main__":
    solve()