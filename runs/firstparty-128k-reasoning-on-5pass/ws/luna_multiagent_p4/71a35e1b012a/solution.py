import sys
from bisect import bisect_left, bisect_right
from array import array
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    seg = [(data[2 + 2 * i], data[3 + 2 * i]) for i in range(m)]

    type1 = []
    type2 = []
    for i, (l, r) in enumerate(seg):
        type1.append((l, r, i))
        type2.append((l, r, i))

    # Greedy interval-cover preprocessing.
    by_l = sorted(range(m), key=lambda i: seg[i][0])
    best_r = array('i', [0]) * (n + 2)
    best_i = array('i', [-1]) * (n + 2)

    ptr = 0
    cur_r = 0
    cur_i = -1
    for x in range(1, n + 1):
        while ptr < m and seg[by_l[ptr]][0] <= x:
            i = by_l[ptr]
            if seg[i][1] > cur_r:
                cur_r = seg[i][1]
                cur_i = i
            ptr += 1
        best_r[x] = cur_r
        best_i[x] = cur_i

    nxt = array('i', [n + 1]) * (n + 2)
    for x in range(1, n + 1):
        if best_r[x] >= x:
            nxt[x] = best_r[x] + 1

    logs = (n + 1).bit_length()
    jump = [nxt]
    for _ in range(1, logs):
        prev = jump[-1]
        cur = array('i', [n + 1]) * (n + 2)
        for x in range(1, n + 1):
            y = prev[x]
            cur[x] = prev[y] if y <= n else n + 1
        jump.append(cur)

    def cover(l, r):
        if l > r:
            return 0, []
        if l < 1 or r > n or best_r[l] < l:
            return None

        pos = l
        count = 0
        for p in range(logs - 1, -1, -1):
            y = jump[p][pos]
            if y <= r:
                pos = y
                count += 1 << p

        if pos <= r:
            if best_r[pos] < r:
                return None
            count += 1

        chosen = []
        pos = l
        while pos <= r:
            i = best_i[pos]
            if i < 0:
                return None
            chosen.append(i)
            pos = nxt[pos]
        return count, chosen

    answer = None

    # No type-2 operation: cover the whole range by type-1 intervals.
    q = cover(1, n)
    if q is not None:
        answer = (q[0], [(i, 1) for i in q[1]])

    # One type-2 operation plus a minimum cover of its excluded interval.
    for l, r, j in type2:
        q = cover(l, r)
        if q is not None:
            cand = (1 + q[0], [(j, 2)] + [(i, 1) for i in q[1]])
            if answer is None or cand[0] < answer[0]:
                answer = cand

    # Two disjoint type-2 intervals immediately cover everything.
    by_r = sorted(type2, key=lambda z: z[1])
    min_r_seen = None
    min_r_idx = -1
    for l, r, i in by_r:
        if min_r_seen is not None and min_r_seen < l:
            cand = (2, [(min_r_idx, 2), (i, 2)])
            if answer is None or cand[0] < answer[0]:
                answer = cand
                break
        if min_r_seen is None or r < min_r_seen:
            min_r_seen = r
            min_r_idx = i

    # For two type-2 operations, process pairs through their intersection.
    # Case A: L_b <= L_a.  Choose the smallest R_b >= L_a.
    by_l_type2 = sorted(type2, key=lambda z: z[0])
    queries = sorted(type2, key=lambda z: z[0])
    heap = []
    p = 0

    for la, ra, a in queries:
        while p < m and by_l_type2[p][0] <= la:
            lb, rb, b = by_l_type2[p]
            heapq.heappush(heap, (rb, b))
            p += 1

        removed = []
        while heap and heap[0][0] < la:
            heapq.heappop(heap)

        candidate = None
        while heap:
            rb, b = heap[0]
            if b == a:
                removed.append(heapq.heappop(heap))
            else:
                candidate = (rb, b)
                break
        for item in removed:
            heapq.heappush(heap, item)

        if candidate is not None:
            rb, b = candidate
            right = min(ra, rb)
            q = cover(la, right)
            if q is not None:
                cand = (2 + q[0], [(a, 2), (b, 2)] +
                        [(i, 1) for i in q[1]])
                if answer is None or cand[0] < answer[0]:
                    answer = cand

    # Case B: L_b > L_a.  Sweep by decreasing L_a, activating R_b >= L_a.
    coords = sorted(set(l for l, _, _ in type2))
    cnum = len(coords)
    pos_of = {x: k for k, x in enumerate(coords)}

    size = 1
    while size < cnum:
        size <<= 1
    tree = [0] * (2 * size)
    active_idx = [-1] * cnum

    def activate(k, idx):
        active_idx[k] = idx
        v = k + size
        tree[v] = 1
        v >>= 1
        while v:
            nv = tree[v << 1] | tree[v << 1 | 1]
            if tree[v] == nv:
                break
            tree[v] = nv
            v >>= 1

    def find_rightmost(node, left, right, ql, qr):
        if right < ql or qr < left or tree[node] == 0:
            return -1
        if left == right:
            return left
        mid = (left + right) >> 1
        res = find_rightmost(node << 1 | 1, mid + 1, right, ql, qr)
        if res != -1:
            return res
        return find_rightmost(node << 1, left, mid, ql, qr)

    by_r_desc = sorted(type2, key=lambda z: z[1], reverse=True)
    queries_desc = sorted(type2, key=lambda z: z[0], reverse=True)
    p = 0

    for la, ra, a in queries_desc:
        while p < m and by_r_desc[p][1] >= la:
            lb, rb, b = by_r_desc[p]
            activate(pos_of[lb], b)
            p += 1

        lo = bisect_right(coords, la)
        hi = bisect_right(coords, ra) - 1
        if lo <= hi:
            k = find_rightmost(1, 0, size - 1, lo, hi)
            if k != -1:
                b = active_idx[k]
                lb, rb = seg[b]
                q = cover(lb, ra)
                if q is not None:
                    cand = (2 + q[0], [(a, 2), (b, 2)] +
                            [(i, 1) for i in q[1]])
                    if answer is None or cand[0] < answer[0]:
                        answer = cand

    if answer is None:
        print(-1)
        return

    cost, chosen = answer
    ops = [0] * m
    for i, t in chosen:
        ops[i] = t

    print(cost)
    print(*ops)


if __name__ == "__main__":
    main()