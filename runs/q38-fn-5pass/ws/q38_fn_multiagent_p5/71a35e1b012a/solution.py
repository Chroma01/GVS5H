import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    L = [0] * M
    R = [0] * M

    full_idx = -1

    # For cost-2 union check: one interval must start at 1, another must end at N.
    max_r_start1 = -1
    idx_start1 = -1
    min_l_endN = N + 1
    idx_endN = -1

    p = 2
    for i in range(M):
        l = int(data[p])
        r = int(data[p + 1])
        p += 2

        L[i] = l
        R[i] = r

        if full_idx == -1 and l == 1 and r == N:
            full_idx = i

        if l == 1 and r > max_r_start1:
            max_r_start1 = r
            idx_start1 = i

        if r == N and l < min_l_endN:
            min_l_endN = l
            idx_endN = i

    del data

    def emit(k, ops):
        sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: one operation 1 on [1, N].
    if full_idx != -1:
        ops = [0] * M
        ops[full_idx] = 1
        emit(1, ops)
        return

    # Sort by L ascending, and for equal L by R ascending.
    order = list(range(M))
    order.sort(key=lambda i: (L[i], R[i]))

    # Cost 2, case (1, 2): one interval contains another.
    # Use operation 1 on the container and operation 2 on the contained interval.
    #
    # Cross-L containments are found by maintaining the maximum R seen in earlier
    # L-groups. Same-L containments are handled separately because ascending R
    # makes the container appear after the contained interval.
    max_r = -1
    max_r_idx = -1
    p = 0
    while p < M:
        cur_l = L[order[p]]
        q = p + 1
        while q < M and L[order[q]] == cur_l:
            q += 1

        # First try cross-L containment using only earlier L-groups.
        for t in range(p, q):
            i = order[t]
            if max_r >= R[i]:
                ops = [0] * M
                ops[max_r_idx] = 1
                ops[i] = 2
                emit(2, ops)
                return

        # If no cross-L containment exists in this group, same-L containment
        # exists whenever the group has at least two intervals.
        if q - p >= 2:
            contained = order[p]       # smallest R in this same-L group
            container = order[q - 1]   # largest R in this same-L group
            ops = [0] * M
            ops[container] = 1
            ops[contained] = 2
            emit(2, ops)
            return

        # Update maximum R for future groups.
        gi = order[q - 1]
        if R[gi] > max_r:
            max_r = R[gi]
            max_r_idx = gi

        p = q

    # Cost 2, case (1, 1): two intervals whose union is [1, N].
    if (
        idx_start1 != -1
        and idx_endN != -1
        and idx_start1 != idx_endN
        and max_r_start1 + 1 >= min_l_endN
    ):
        ops = [0] * M
        ops[idx_start1] = 1
        ops[idx_endN] = 1
        emit(2, ops)
        return

    # Cost 2, case (2, 2): two intervals with empty intersection.
    # Use operation 2 on both.
    INF = 10**18
    min_r = INF
    min_r_idx = -1
    for i in order:
        if min_r < L[i]:
            ops = [0] * M
            ops[min_r_idx] = 2
            ops[i] = 2
            emit(2, ops)
            return
        if R[i] < min_r:
            min_r = R[i]
            min_r_idx = i

    # If no cost-2 pair exists and M >= 3, cost 3 is always possible.
    # Let A be min-L interval and C be max-L interval.
    # Operation 2 on A and C leaves exactly I_A ∩ I_C uncovered.
    # Any third interval covers that intersection when no cost-2 pair exists.
    if M >= 3:
        A = order[0]
        C = order[-1]

        l = L[A] if L[A] > L[C] else L[C]
        r = R[A] if R[A] < R[C] else R[C]

        # Safety: if A and C are already disjoint, cost 2 is enough.
        if l > r:
            ops = [0] * M
            ops[A] = 2
            ops[C] = 2
            emit(2, ops)
            return

        B = -1
        for i in order:
            if i != A and i != C and L[i] <= l and r <= R[i]:
                B = i
                break

        if B != -1:
            ops = [0] * M
            ops[A] = 2
            ops[C] = 2
            ops[B] = 1
            emit(3, ops)
            return

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    solve()