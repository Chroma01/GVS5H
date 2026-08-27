import sys
from bisect import bisect_left


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    intervals = []

    full_idx = -1

    maxR1 = -1
    idx_maxR1 = -1

    minLN = N + 1
    idx_minLN = -1

    maxL = -1
    idx_maxL = -1

    minR = N + 1
    idx_minR = -1

    pos = 2
    for i in range(M):
        L = int(data[pos])
        R = int(data[pos + 1])
        pos += 2

        intervals.append((L, R, i))

        if L == 1 and R == N:
            if full_idx == -1:
                full_idx = i

        if L == 1:
            if R > maxR1:
                maxR1 = R
                idx_maxR1 = i

        if R == N:
            if L < minLN:
                minLN = L
                idx_minLN = i

        if L > maxL:
            maxL = L
            idx_maxL = i

        if R < minR:
            minR = R
            idx_minR = i

    del data

    def emit(K, choices):
        ops = ['0'] * M
        for idx, op in choices:
            ops[idx] = str(op)
        sys.stdout.write(str(K) + '\n' + ' '.join(ops) + '\n')

    # Cost 1: only a full interval used as operation 1.
    if full_idx != -1:
        emit(1, [(full_idx, 1)])
        return

    # Cost 2, type 1+2:
    # operation 1 on a container interval, operation 2 on a contained interval.
    #
    # Sort by L ascending, R descending. Build prefix_max_R. For current
    # position p, if some previous interval has R >= current R, then the
    # earliest such previous interval contains the current one.
    intervals.sort(key=lambda x: (x[0], -x[1]))

    prefix_max_R = [0] * M
    cur = -1
    for i, (L, R, idx) in enumerate(intervals):
        if R > cur:
            cur = R
        prefix_max_R[i] = cur

    for p, (L, R, idx) in enumerate(intervals):
        if p > 0 and prefix_max_R[p - 1] >= R:
            q = bisect_left(prefix_max_R, R, 0, p)
            emit(2, [(intervals[q][2], 1), (idx, 2)])
            return

    # Cost 2, type 1+1:
    # two operation-1 intervals cover [1, N].
    if (idx_maxR1 != -1 and idx_minLN != -1 and
            idx_maxR1 != idx_minLN and maxR1 + 1 >= minLN):
        emit(2, [(idx_maxR1, 1), (idx_minLN, 1)])
        return

    # Cost 2, type 2+2:
    # two operation-2 intervals cover [1, N] iff their original intervals
    # are disjoint. This happens iff maxL > minR.
    if maxL > minR:
        emit(2, [(idx_maxL, 2), (idx_minR, 2)])
        return

    # If no cost 1 or cost 2 solution exists:
    # - M < 3: impossible.
    # - M >= 3: cost 3 is always possible.
    if M >= 3:
        a = idx_maxL
        b = idx_minR

        if a == b:
            # Pick two other distinct indices.
            b = -1
            c = -1
            for i in range(M):
                if i == a:
                    continue
                if b == -1:
                    b = i
                else:
                    c = i
                    break
        else:
            # Pick any third distinct index.
            c = -1
            for i in range(M):
                if i != a and i != b:
                    c = i
                    break

        emit(3, [(a, 2), (b, 2), (c, 1)])
        return

    sys.stdout.write('-1\n')


if __name__ == '__main__':
    solve()