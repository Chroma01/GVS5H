import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    intervals = [None] * M
    rs = [0] * M

    full_idx = -1
    INF = 10**18

    minR = INF
    minR_idx = -1
    maxL = -1
    maxL_idx = -1

    minL = INF
    minL_idx = -1
    maxR = -1
    maxR_idx = -1

    # interval with L=1 and maximum R
    p_idx = -1
    p_R = -1

    # interval with R=N and minimum L
    q_idx = -1
    q_L = INF

    pos = 2
    for i in range(M):
        l = int(data[pos])
        r = int(data[pos + 1])
        pos += 2

        # sort key: L ascending, R descending, original index ascending
        intervals[i] = (l, -r, i)
        rs[i] = r

        if l == 1 and r == N:
            full_idx = i

        if r < minR:
            minR = r
            minR_idx = i
        if l > maxL:
            maxL = l
            maxL_idx = i

        if l < minL:
            minL = l
            minL_idx = i
        if r > maxR:
            maxR = r
            maxR_idx = i

        if l == 1 and r > p_R:
            p_R = r
            p_idx = i
        if r == N and l < q_L:
            q_L = l
            q_idx = i

    data = None

    def emit(k, ops):
        sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: one interval is the whole range.
    if full_idx != -1:
        ops = [0] * M
        ops[full_idx] = 1
        emit(1, ops)
        return

    # Cost 2, type 1 + type 2:
    # Find a containment pair I contains J.  Choose the container with the
    # smallest original index among all such pairs.
    #
    # Process intervals sorted by L ascending and R descending.  Then every
    # previously processed interval has L <= current L.  We need a previous
    # interval with R >= current R.  A Fenwick tree over reversed compressed
    # R ranks stores the minimum original index seen so far, allowing suffix
    # queries R >= current R as prefix queries.
    vals = sorted(set(rs))
    K = len(vals)
    rev_rank = {v: K - idx for idx, v in enumerate(vals)}
    rs = None
    vals = None

    intervals.sort()

    INF_IDX = M + 1
    tree = [INF_IDX] * (K + 1)

    best_container = INF_IDX
    best_contained = -1

    tr = tree
    kk = K
    inf_idx = INF_IDX
    rev = rev_rank

    for l, nr, i in intervals:
        r = -nr
        idx = rev[r]

        # Query minimum original index among previous intervals with R >= r.
        j = idx
        res = inf_idx
        while j > 0:
            v = tr[j]
            if v < res:
                res = v
            j -= j & -j

        if res != inf_idx and res < best_container:
            best_container = res
            best_contained = i
            if res == 0:
                # Cannot improve the container index further.
                break

        # Insert current interval as a possible container for later intervals.
        j = idx
        while j <= kk:
            if i < tr[j]:
                tr[j] = i
            j += j & -j

    if best_contained != -1:
        ops = [0] * M
        ops[best_container] = 1
        ops[best_contained] = 2
        emit(2, ops)
        return

    # Cost 2, type 2 + type 2:
    # two disjoint intervals. Equivalent to min R < max L.
    if minR < maxL:
        ops = [0] * M
        ops[minR_idx] = 2
        ops[maxL_idx] = 2
        emit(2, ops)
        return

    # Cost 2, type 1 + type 1:
    # one interval starts at 1, another ends at N, and they overlap/touch.
    if p_idx != -1 and q_idx != -1 and p_idx != q_idx and q_L <= p_R + 1:
        ops = [0] * M
        ops[p_idx] = 1
        ops[q_idx] = 1
        emit(2, ops)
        return

    # If no cost <= 2 solution exists, three operations are enough when M >= 3.
    if M >= 3:
        A = minL_idx
        C = maxR_idx

        # If the same interval has both minimum L and maximum R, it contains
        # all others. This is normally caught by the containment check, but
        # handle it safely.
        if A == C:
            other = 0 if A != 0 else 1
            ops = [0] * M
            ops[A] = 1
            ops[other] = 2
            emit(2, ops)
            return

        B = 0
        if B == A or B == C:
            B = 1
        if B == A or B == C:
            B = 2

        ops = [0] * M
        ops[A] = 1
        ops[C] = 1
        ops[B] = 2
        emit(3, ops)
        return

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    solve()