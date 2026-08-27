import sys
from bisect import bisect_left, bisect_right
from array import array


def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())

    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i], R[i] = map(int, input().split())

    order_l = sorted(range(M), key=lambda i: (L[i], R[i], i))
    sorted_l = [L[i] for i in order_l]

    top0 = array('i', [-1]) * M
    top1 = array('i', [-1]) * M
    top2 = array('i', [-1]) * M

    for p, idx in enumerate(order_l):
        cand = [idx]
        if p:
            if top0[p - 1] != -1:
                cand.append(top0[p - 1])
            if top1[p - 1] != -1:
                cand.append(top1[p - 1])
            if top2[p - 1] != -1:
                cand.append(top2[p - 1])
        cand.sort(key=lambda x: (-R[x], x))
        if len(cand) > 0:
            top0[p] = cand[0]
        if len(cand) > 1:
            top1[p] = cand[1]
        if len(cand) > 2:
            top2[p] = cand[2]

    def best_starting_at(pos, ban1=-1, ban2=-1):
        p = bisect_right(sorted_l, pos) - 1
        if p < 0:
            return -1
        x = top0[p]
        if x != -1 and x != ban1 and x != ban2:
            return x
        x = top1[p]
        if x != -1 and x != ban1 and x != ban2:
            return x
        x = top2[p]
        if x != -1 and x != ban1 and x != ban2:
            return x
        return -1

    sentinel = N + 1
    nxt = array('i', [sentinel]) * (N + 2)
    chosen = array('i', [-1]) * (N + 2)

    for pos in range(1, N + 1):
        x = best_starting_at(pos)
        if x != -1 and R[x] >= pos:
            nxt[pos] = R[x] + 1
            chosen[pos] = x

    LOG = (N + 2).bit_length()
    jump = [nxt]
    for _ in range(1, LOG):
        prev = jump[-1]
        cur = array('i', [sentinel]) * (N + 2)
        for p in range(1, N + 1):
            q = prev[p]
            cur[p] = prev[q]
        jump.append(cur)

    first_choice = array('i', [sentinel]) * M
    last_choice = array('i', [0]) * M
    for p in range(1, N + 1):
        x = chosen[p]
        if x != -1:
            if p < first_choice[x]:
                first_choice[x] = p
            last_choice[x] = p

    def first_path_at_least(pos, threshold):
        if pos >= threshold:
            return pos, 0
        cur = pos
        cnt = 0
        for k in range(LOG - 1, -1, -1):
            q = jump[k][cur]
            if q < threshold:
                cur = q
                cnt += 1 << k
        q = nxt[cur]
        if q >= threshold:
            return q, cnt + 1
        return sentinel, cnt

    def baseline_until(pos, target):
        if pos > target:
            return pos, 0
        cur = pos
        cnt = 0
        limit = target + 1
        for k in range(LOG - 1, -1, -1):
            q = jump[k][cur]
            if q <= limit:
                cur = q
                cnt += 1 << k
        return cur, cnt

    def cover_count(left, right, ban1=-1, ban2=-1):
        if left > right:
            return 0

        cur = left
        answer = 0

        while cur <= right:
            event_pos = sentinel
            event_id = -1

            for b in (ban1, ban2):
                if b == -1:
                    continue
                a = first_choice[b]
                z = last_choice[b]
                if a > z or z < cur:
                    continue
                a = max(a, cur)
                p, _ = first_path_at_least(cur, a)
                if p <= z and p < event_pos:
                    event_pos = p
                    event_id = b

            if event_id == -1 or event_pos > right:
                p, c = baseline_until(cur, right)
                if c == 0:
                    return None
                answer += c
                return answer

            p, c = baseline_until(cur, event_pos - 1)
            answer += c
            cur = p
            if cur != event_pos:
                return None

            x = best_starting_at(cur, ban1, ban2)
            if x == -1 or R[x] < cur:
                return None
            answer += 1
            cur = R[x] + 1

        return answer

    def reconstruct(left, right, ban1=-1, ban2=-1):
        result = []
        cur = left
        while cur <= right:
            x = best_starting_at(cur, ban1, ban2)
            if x == -1 or R[x] < cur:
                return None
            result.append(x)
            cur = R[x] + 1
        return result

    best_cost = 10**18
    best_desc = None

    def update(left, right, bans):
        nonlocal best_cost, best_desc
        c = cover_count(
            left,
            right,
            bans[0] if len(bans) >= 1 else -1,
            bans[1] if len(bans) >= 2 else -1,
        )
        if c is None:
            return
        c += len(bans)
        if c < best_cost:
            best_cost = c
            best_desc = (left, right, bans)

    update(1, N, ())

    for i in range(M):
        update(L[i], R[i], (i,))

    by_left = sorted(range(M), key=lambda i: (L[i], R[i], i))
    min_r = sentinel
    min_idx = -1
    for i in by_left:
        if min_r < L[i]:
            update(1, 0, (min_idx, i))
            break
        if R[i] < min_r:
            min_r = R[i]
            min_idx = i

    by_right = sorted(range(M), key=lambda i: (R[i], L[i], i))
    sorted_r = [R[i] for i in by_right]

    size = 1
    while size < M:
        size <<= 1

    INF = N + 1
    seg = [INF] * (2 * size)
    for p, i in enumerate(by_right):
        seg[size + p] = L[i]
    for p in range(size - 1, 0, -1):
        seg[p] = min(seg[p << 1], seg[p << 1 | 1])

    def first_with_l_at_most(lo, hi, limit):
        if lo > hi:
            return -1

        def rec(node, nl, nr):
            if nr < lo or hi < nl or seg[node] > limit:
                return -1
            if nl == nr:
                return nl
            mid = (nl + nr) >> 1
            q = rec(node << 1, nl, mid)
            if q != -1:
                return q
            return rec(node << 1 | 1, mid + 1, nr)

        return rec(1, 0, size - 1)

    def last_with_l_at_most(lo, hi, limit):
        if lo > hi:
            return -1

        def rec(node, nl, nr):
            if nr < lo or hi < nl or seg[node] > limit:
                return -1
            if nl == nr:
                return nl
            mid = (nl + nr) >> 1
            q = rec(node << 1 | 1, mid + 1, nr)
            if q != -1:
                return q
            return rec(node << 1, nl, mid)

        return rec(1, 0, size - 1)

    candidate_pairs = set()

    for i in range(M):
        start = L[i]
        end = R[i]
        lo = bisect_left(sorted_r, start)
        hi = bisect_right(sorted_r, end) - 1
        if lo > hi:
            continue

        p = lo
        for _ in range(3):
            p = first_with_l_at_most(p, hi, start)
            if p == -1:
                break
            j = by_right[p]
            if j != i and L[j] <= start <= R[j]:
                candidate_pairs.add((i, j))
            p += 1

        p = hi
        for _ in range(3):
            p = last_with_l_at_most(lo, p, start)
            if p == -1:
                break
            j = by_right[p]
            if j != i and L[j] <= start <= R[j]:
                candidate_pairs.add((i, j))
            p -= 1

    for i, j in candidate_pairs:
        left = max(L[i], L[j])
        right = min(R[i], R[j])
        update(left, right, (i, j))

    if best_desc is None:
        print(-1)
        return

    left, right, bans = best_desc
    ordinary = reconstruct(
        left,
        right,
        bans[0] if len(bans) >= 1 else -1,
        bans[1] if len(bans) >= 2 else -1,
    )
    if ordinary is None:
        print(-1)
        return

    ops = [0] * M
    for x in bans:
        ops[x] = 2
    for x in ordinary:
        ops[x] = 1

    print(best_cost)
    print(*ops)


if __name__ == "__main__":
    solve()