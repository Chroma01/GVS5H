import sys
import heapq
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    ls = array("i", [0]) * m
    rs = array("i", [0]) * m
    head = array("i", [-1]) * (n + 2)
    nxt = array("i", [-1]) * m

    p = 2
    for i in range(m):
        l, r = data[p], data[p + 1]
        p += 2
        ls[i] = l
        rs[i] = r
        nxt[i] = head[l]
        head[l] = i
    del data

    reach = array("i", [0]) * (n + 2)
    best_id = array("i", [-1]) * (n + 2)
    second_reach = array("i", [0]) * (n + 2)
    second_id = array("i", [-1]) * (n + 2)
    owner_end = array("i", [0]) * m

    best_r = 0
    second_r = 0
    best = -1
    second = -1
    owner = -1

    for q in range(1, n + 1):
        j = head[q]
        while j != -1:
            r = rs[j]
            if r > best_r:
                second_r, second = best_r, best
                best_r, best = r, j
            elif j != best and r > second_r:
                second_r, second = r, j
            j = nxt[j]

        if best != owner:
            if owner != -1:
                owner_end[owner] = q - 1
            owner = best

        reach[q] = best_r
        best_id[q] = best
        second_reach[q] = second_r
        second_id[q] = second

    if owner != -1:
        owner_end[owner] = n

    inf = n + 2
    levels = (inf + 1).bit_length()

    first = array("i", [inf]) * (n + 3)
    first_alt = array("i", [inf]) * (n + 3)

    for q in range(1, n + 1):
        if reach[q] >= q:
            first[q] = reach[q] + 1
        if second_reach[q] >= q:
            first_alt[q] = second_reach[q] + 1

    ordinary = [first]
    alternate = [first_alt]

    for _ in range(1, levels):
        prev = ordinary[-1]
        cur = array("i", [inf]) * (n + 3)
        for q in range(1, n + 3):
            cur[q] = prev[prev[q]]
        ordinary.append(cur)

        prev = alternate[-1]
        cur = array("i", [inf]) * (n + 3)
        for q in range(1, n + 3):
            cur[q] = prev[prev[q]]
        alternate.append(cur)

    def segment_count(start, end, table):
        if start > end:
            return 0
        if start < 1 or start > n:
            return None

        q = start
        used = 0

        for k in range(levels - 1, -1, -1):
            z = table[k][q]
            if z <= end:
                q = z
                used += 1 << k

        z = table[0][q]
        if z > end + 1:
            return None
        return used + 1

    best_cost = 10**18
    best_mode = None

    count = segment_count(1, n, ordinary)
    if count is not None:
        best_cost = count
        best_mode = ("none", -1)

    for forbidden in range(m):
        l = ls[forbidden]
        r = rs[forbidden]

        if best_id[l] != forbidden:
            count = segment_count(l, r, ordinary)
            if count is None:
                continue
            total = count + 1
        else:
            end_owner = owner_end[forbidden]

            count1 = segment_count(l, end_owner, alternate)
            if count1 is None:
                continue

            q = l
            for k in range(levels - 1, -1, -1):
                z = alternate[k][q]
                if z <= end_owner:
                    q = z

            q = alternate[0][q]
            count2 = segment_count(q, r, ordinary)
            if count2 is None:
                continue

            total = count1 + count2 + 1

        if total < best_cost:
            best_cost = total
            best_mode = ("one", forbidden)

    min_r_id = min(range(m), key=lambda i: rs[i])
    max_l_id = max(range(m), key=lambda i: ls[i])

    if ls[max_l_id] > rs[min_r_id] and best_cost > 2:
        best_cost = 2
        best_mode = ("two", (max_l_id, min_r_id))

    active = []
    triple = None

    for left in range(1, n + 1):
        j = head[left]
        while j != -1:
            heapq.heappush(active, (rs[j], j))
            j = nxt[j]

        while active and active[0][0] < left:
            heapq.heappop(active)

        if len(active) >= 3:
            triple = [active[0][1], active[1][1], active[2][1]]
            break

    if triple is not None and best_cost > 3:
        a, b, c = triple
        candidates = (
            (a, b, c), (a, c, b),
            (b, a, c), (b, c, a),
            (c, a, b), (c, b, a),
        )

        for i, j, k in candidates:
            common_left = max(ls[i], ls[j])
            common_right = min(rs[i], rs[j])
            if (
                common_left <= common_right
                and ls[k] <= common_left
                and common_right <= rs[k]
            ):
                best_cost = 3
                best_mode = ("three", (i, j, k))
                break

    if best_mode is None:
        print(-1)
        return

    type1 = []
    type2 = []
    mode, value = best_mode

    if mode == "none":
        q = 1
        while q <= n:
            type1.append(best_id[q])
            q = reach[q] + 1

    elif mode == "one":
        forbidden = value
        type2.append(forbidden)

        l = ls[forbidden]
        r = rs[forbidden]

        if best_id[l] != forbidden:
            q = l
            while q <= r:
                type1.append(best_id[q])
                q = reach[q] + 1
        else:
            end_owner = owner_end[forbidden]

            q = l
            while q <= end_owner:
                type1.append(second_id[q])
                q = second_reach[q] + 1

            q = end_owner + 1
            while q <= r:
                type1.append(best_id[q])
                q = reach[q] + 1

    elif mode == "two":
        type2.extend(value)

    else:
        i, j, k = value
        type2.extend((i, j))
        type1.append(k)

    ops = [0] * m
    for i in type1:
        ops[i] = 1
    for i in type2:
        ops[i] = 2

    print(best_cost)
    print(*ops)


if __name__ == "__main__":
    solve()