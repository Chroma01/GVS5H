import sys
from bisect import bisect_left, bisect_right

INF = 10**9


def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())

    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i], R[i] = map(int, input().split())

    order_l = sorted(range(M), key=lambda i: (L[i], -R[i]))
    starts = [L[i] for i in order_l]

    def add_max2(pair, idx):
        a, b = pair
        if idx == a or idx == b:
            return pair
        if a == -1 or R[idx] > R[a]:
            return idx, a
        if b == -1 or R[idx] > R[b]:
            return a, idx
        return pair

    pref_best = [(-1, -1)] * M
    cur = (-1, -1)
    for k, idx in enumerate(order_l):
        cur = add_max2(cur, idx)
        pref_best[k] = cur

    order_r = sorted(range(M), key=lambda i: (-R[i], L[i]))
    neg_rights = [-R[i] for i in order_r]

    def add_min2(pair, idx):
        a, b = pair
        if idx == a or idx == b:
            return pair
        if a == -1 or L[idx] < L[a]:
            return idx, a
        if b == -1 or L[idx] < L[b]:
            return a, idx
        return pair

    pref_right_best = [(-1, -1)] * M
    cur = (-1, -1)
    for k, idx in enumerate(order_r):
        cur = add_min2(cur, idx)
        pref_right_best[k] = cur

    def greedy_cover(a, b):
        if a > b:
            return []

        current = a
        p = 0
        result = []

        while current <= b:
            farthest = current - 1
            chosen = -1

            while p < M and L[order_l[p]] <= current:
                idx = order_l[p]
                if R[idx] > farthest:
                    farthest = R[idx]
                    chosen = idx
                p += 1

            if farthest < current:
                return None

            result.append(chosen)
            current = farthest + 1

        return result

    best_cost = INF
    best_op1 = ()
    best_op2 = ()

    def register(op2, op1):
        nonlocal best_cost, best_op1, best_op2

        if len(op1) != len(set(op1)):
            return
        if len(op2) != len(set(op2)):
            return
        if set(op1) & set(op2):
            return

        cost = len(op1) + len(op2)
        if cost < best_cost:
            best_cost = cost
            best_op1 = tuple(op1)
            best_op2 = tuple(op2)

    # No operation 2.
    whole = greedy_cover(1, N)
    if whole is not None:
        register((), whole)

    # One operation 2 and one operation 1.
    for i in range(M):
        k = bisect_right(starts, L[i]) - 1
        if k < 0:
            continue

        a, b = pref_best[k]
        for j in (a, b):
            if j == -1 or j == i:
                continue
            if L[j] <= L[i] and R[j] >= R[i]:
                register((i,), (j,))

    # Two disjoint operation-2 intervals.
    farthest_r = -1
    farthest_id = -1
    for i in order_l:
        if farthest_id != -1 and farthest_r < L[i]:
            register((farthest_id, i), ())
            break
        if R[i] > farthest_r:
            farthest_r = R[i]
            farthest_id = i

    # One operation 2 and two operation 1 intervals.
    for i in range(M):
        left_candidates = []
        k1 = bisect_right(starts, L[i]) - 1
        if k1 >= 0:
            a, b = pref_best[k1]
            if a != -1 and a != i:
                left_candidates.append(a)
            if b != -1 and b != i:
                left_candidates.append(b)

        right_candidates = []
        k2 = bisect_right(neg_rights, -R[i]) - 1
        if k2 >= 0:
            a, b = pref_right_best[k2]
            if a != -1 and a != i:
                right_candidates.append(a)
            if b != -1 and b != i:
                right_candidates.append(b)

        for left_id in left_candidates:
            if R[left_id] < L[i]:
                continue

            for right_id in right_candidates:
                if right_id == left_id:
                    continue
                if L[right_id] > R[i]:
                    continue
                if R[left_id] < L[right_id] - 1:
                    continue

                register((i,), (left_id, right_id))

    # Two operation 2 intervals and one operation 1 interval.
    order_r_asc = sorted(range(M), key=lambda i: (R[i], L[i]))
    rights = [R[i] for i in order_r_asc]

    for c in range(M):
        # Choose one operation-2 interval whose left endpoint lies in c.
        lo_l = bisect_left(starts, L[c])
        hi_l = bisect_right(starts, R[c])
        left_candidates = order_l[max(lo_l, hi_l - 4):hi_l]

        # Choose one operation-2 interval whose right endpoint lies in c.
        lo_r = bisect_left(rights, L[c])
        hi_r = bisect_right(rights, R[c])
        right_candidates = order_r_asc[lo_r:min(hi_r, lo_r + 4)]

        for a in left_candidates:
            if a == c:
                continue
            for b in right_candidates:
                if b == c or b == a:
                    continue
                register((a, b), (c,))

    if best_cost == INF:
        print(-1)
        return

    answer = [0] * M
    for i in best_op1:
        answer[i] = 1
    for i in best_op2:
        answer[i] = 2

    print(best_cost)
    print(*answer)


if __name__ == "__main__":
    solve()