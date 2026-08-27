import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = data[2 + 2 * i]
        R[i] = data[3 + 2 * i]

    def output(chosen):
        ops = [0] * M
        for idx, typ in chosen:
            ops[idx] = typ
        print(len(chosen))
        print(*ops)
        sys.exit()

    # Cost 1: operation 1 on [1, N].
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            output([(i, 1)])

    # Extremal intervals, also used for disjoint-pair and cost-3 checks.
    min_r_idx = 0
    max_l_idx = 0
    for i in range(1, M):
        if R[i] < R[min_r_idx]:
            min_r_idx = i
        if L[i] > L[max_l_idx]:
            max_l_idx = i

    # Cost 2, pattern 1:
    # Operation 2 on I and operation 1 on a distinct J containing I.
    # Strictly smaller left endpoints are preferred over equal-left choices.
    order = list(range(M))
    order.sort(key=lambda i: L[i])

    previous_best_idx = -1
    previous_best_r = -1
    p = 0

    while p < M:
        q = p
        left_value = L[order[p]]
        while q < M and L[order[q]] == left_value:
            q += 1

        first_idx = -1
        first_r = -1
        second_idx = -1
        second_r = -1

        for pos in range(p, q):
            idx = order[pos]
            value = R[idx]
            if value > first_r:
                second_idx, second_r = first_idx, first_r
                first_idx, first_r = idx, value
            elif value > second_r:
                second_idx, second_r = idx, value

        for pos in range(p, q):
            i = order[pos]

            # Prefer a candidate with strictly smaller left endpoint.
            if previous_best_idx != -1 and previous_best_r >= R[i]:
                output([(i, 2), (previous_best_idx, 1)])

            # Fall back to another interval in the equal-left group.
            group_idx = first_idx
            group_r = first_r
            if group_idx == i:
                group_idx = second_idx
                group_r = second_r

            if group_idx != -1 and group_r >= R[i]:
                output([(i, 2), (group_idx, 1)])

        if first_r > previous_best_r:
            previous_best_idx = first_idx
            previous_best_r = first_r

        p = q

    # Cost 2, pattern 2:
    # Two operation-1 intervals cover [1, N].
    best_left_idx = -1
    best_left_r = -1
    best_right_idx = -1
    best_right_l = N + 1

    for i in range(M):
        if L[i] == 1 and R[i] > best_left_r:
            best_left_r = R[i]
            best_left_idx = i
        if R[i] == N and L[i] < best_right_l:
            best_right_l = L[i]
            best_right_idx = i

    if (best_left_idx != -1 and best_right_idx != -1
            and best_left_idx != best_right_idx
            and best_right_l <= best_left_r + 1):
        output([(best_left_idx, 1), (best_right_idx, 1)])

    # Cost 2, pattern 3:
    # Two operation-2 intervals cover everything iff original intervals are disjoint.
    if R[min_r_idx] < L[max_l_idx]:
        output([(min_r_idx, 2), (max_l_idx, 2)])

    # If no cost at most 2 solution exists, every M >= 3 instance has cost 3.
    if M >= 3:
        a = max_l_idx
        b = min_r_idx

        if a != b:
            c = 0
            while c == a or c == b:
                c += 1
            output([(a, 2), (b, 2), (c, 1)])

        # This is unreachable because a common extremal interval is contained
        # in every other interval, yielding a mixed cost-2 solution.
        c = 1 if a == 0 else 0
        output([(a, 2), (c, 1)])

    print(-1)


if __name__ == "__main__":
    main()