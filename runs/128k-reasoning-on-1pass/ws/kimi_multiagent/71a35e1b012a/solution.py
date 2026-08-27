import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    if m == 0:
        sys.stdout.write("-1\n")
        return

    L = [0] * m
    R = [0] * m

    p = 2
    full_idx = -1

    min_r_idx = 0
    max_l_idx = 0

    left_idx = -1      # among L == 1, maximum R
    left_best_r = -1
    right_idx = -1     # among R == N, minimum L
    right_best_l = n + 1

    for i in range(m):
        l, r = data[p], data[p + 1]
        p += 2
        L[i] = l
        R[i] = r

        if l == 1 and r == n and full_idx == -1:
            full_idx = i

        if r < R[min_r_idx]:
            min_r_idx = i
        if l > L[max_l_idx]:
            max_l_idx = i

        if l == 1 and r > left_best_r:
            left_idx = i
            left_best_r = r

        if r == n and l < right_best_l:
            right_idx = i
            right_best_l = l

    def emit(k, ops):
        sys.stdout.write(str(k) + "\n")
        sys.stdout.write(" ".join(map(str, ops)) + "\n")

    ops = [0] * m

    # Cost 1: only Operation 1 on [1, N] can cover everything.
    if full_idx != -1:
        ops[full_idx] = 1
        emit(1, ops)
        return

    # Cost 2, Operation 1 + Operation 1: chain from 1 to N.
    if (
        left_idx != -1
        and right_idx != -1
        and left_idx != right_idx
        and left_best_r >= right_best_l - 1
    ):
        ops[left_idx] = 1
        ops[right_idx] = 1
        emit(2, ops)
        return

    # Cost 2, Operation 2 + Operation 2: holes must be disjoint.
    if R[min_r_idx] < L[max_l_idx]:
        ops[min_r_idx] = 2
        ops[max_l_idx] = 2
        emit(2, ops)
        return

    # Cost 2, Operation 1 + Operation 2:
    # the Operation-2 hole must be contained in the Operation-1 interval.
    order = sorted(range(m), key=lambda i: (L[i], -R[i]))
    best_r = -1
    best_idx = -1
    for i in order:
        if R[i] <= best_r:
            ops[best_idx] = 1
            ops[i] = 2
            emit(2, ops)
            return
        if R[i] > best_r:
            best_r = R[i]
            best_idx = i

    # With fewer than three operations, all possibilities have been checked.
    if m < 3:
        sys.stdout.write("-1\n")
        return

    # Cost 3.
    # No cost-2 solution implies:
    #   * no two intervals are disjoint, so all intervals pairwise intersect;
    #   * hence I = [max L_i, min R_i] is nonempty and lies in every interval;
    #   * no interval contains another.
    # Operation 2 on the max-L and min-R intervals leaves exactly I uncovered,
    # and Operation 1 on any third interval covers I.
    a = max_l_idx
    b = min_r_idx
    if a == b:  # unreachable after the containment check when m >= 3
        b = 0 if a != 0 else 1

    c = 0
    while c == a or c == b:
        c += 1

    ops[a] = 2
    ops[b] = 2
    ops[c] = 1
    emit(3, ops)


if __name__ == "__main__":
    main()