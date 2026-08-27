import sys
from bisect import bisect_right
from array import array


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    left = [0] * m
    right = [0] * m

    p = 2
    for i in range(m):
        left[i] = data[p]
        right[i] = data[p + 1]
        p += 2

    order = sorted(range(m), key=lambda i: (left[i], i))
    sorted_left = [left[i] for i in order]

    top1 = [-1] * m
    top2 = [-1] * m
    top3 = [-1] * m

    a = b = c = -1
    for pos, idx in enumerate(order):
        ri = right[idx]
        if a == -1 or ri > right[a]:
            c, b, a = b, a, idx
        elif b == -1 or ri > right[b]:
            c, b = b, idx
        elif c == -1 or ri > right[c]:
            c = idx

        top1[pos] = a
        top2[pos] = b
        top3[pos] = c

    coords = {1, n + 1}
    coords.update(left)
    coords.update(r + 1 for r in right)
    coords = sorted(coords)
    state_id = {x: i for i, x in enumerate(coords)}
    s = len(coords)

    state_top = array("i", [-1]) * s
    state_second = array("i", [-1]) * s

    for si, pos in enumerate(coords):
        q = bisect_right(sorted_left, pos) - 1
        if q >= 0:
            state_top[si] = top1[q]
            state_second[si] = top2[q]

    ordinary = array("i", [-1]) * s
    second = array("i", [-1]) * s

    for si, pos in enumerate(coords):
        t = state_top[si]
        if t != -1 and right[t] >= pos:
            ordinary[si] = state_id[right[t] + 1]

        t = state_second[si]
        if t != -1 and right[t] >= pos:
            second[si] = state_id[right[t] + 1]

    log = max(1, s.bit_length())

    ordinary_jump = [ordinary]
    for _ in range(1, log):
        prev = ordinary_jump[-1]
        cur = array("i", [-1]) * s
        for v in range(s):
            mid = prev[v]
            if mid != -1:
                cur[v] = prev[mid]
        ordinary_jump.append(cur)

    second_jump = [second]
    uniform_top = [array("i", [-1]) * s]

    for v in range(s):
        if second[v] != -1 and state_top[v] != -1:
            uniform_top[0][v] = state_top[v]

    for _ in range(1, log):
        prev_jump = second_jump[-1]
        prev_uniform = uniform_top[-1]
        cur_jump = array("i", [-1]) * s
        cur_uniform = array("i", [-1]) * s

        for v in range(s):
            mid = prev_jump[v]
            if mid != -1:
                cur_jump[v] = prev_jump[mid]
                x = prev_uniform[v]
                y = prev_uniform[mid]
                if x != -1 and x == y:
                    cur_uniform[v] = x

        second_jump.append(cur_jump)
        uniform_top.append(cur_uniform)

    def count_global(start, end):
        if start > end:
            return 0

        v = state_id[start]
        result = 0

        for k in range(log - 1, -1, -1):
            nv = ordinary_jump[k][v]
            if nv != -1 and coords[nv] <= end:
                v = nv
                result += 1 << k

        if coords[v] <= end:
            nv = ordinary_jump[0][v]
            if nv == -1:
                return None
            result += 1

        return result

    def count_without(forbidden, start, end):
        if start > end:
            return 0

        v = state_id[start]
        result = 0

        while coords[v] <= end:
            if state_top[v] != forbidden:
                tail = count_global(coords[v], end)
                if tail is None:
                    return None
                return result + tail

            for k in range(log - 1, -1, -1):
                nv = second_jump[k][v]
                if (
                    nv != -1
                    and uniform_top[k][v] == forbidden
                    and coords[nv] <= end
                ):
                    v = nv
                    result += 1 << k

            if coords[v] > end:
                return result

            nv = second[v]
            if nv == -1:
                return None
            v = nv
            result += 1

        return result

    def best_interval(pos, forbidden1=-1, forbidden2=-1):
        q = bisect_right(sorted_left, pos) - 1
        if q < 0:
            return -1

        for idx in (top1[q], top2[q], top3[q]):
            if idx != -1 and idx != forbidden1 and idx != forbidden2:
                return idx
        return -1

    def cover(start, end, forbidden1=-1, forbidden2=-1):
        if start > end:
            return []

        pos = start
        result = []

        while pos <= end:
            idx = best_interval(pos, forbidden1, forbidden2)
            if idx == -1 or right[idx] < pos:
                return None
            result.append(idx)
            pos = right[idx] + 1

        return result

    best_cost = None
    best_twos = []
    best_ones = []

    def consider(cost, twos, ones):
        nonlocal best_cost, best_twos, best_ones
        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_twos = twos
            best_ones = ones

    only_ones = count_global(1, n)
    if only_ones is not None:
        consider(only_ones, [], [])

    for i in range(m):
        covered = count_without(i, left[i], right[i])
        if covered is not None:
            consider(1 + covered, [i], [])

    max_left_idx = max(range(m), key=lambda i: left[i])
    min_right_idx = min(range(m), key=lambda i: right[i])

    if max_left_idx != min_right_idx:
        residual_left = max(left[max_left_idx], left[min_right_idx])
        residual_right = min(right[max_left_idx], right[min_right_idx])

        if residual_left > residual_right:
            consider(2, [max_left_idx, min_right_idx], [])
        else:
            ones = cover(
                residual_left,
                residual_right,
                max_left_idx,
                min_right_idx,
            )
            if ones is not None:
                consider(
                    2 + len(ones),
                    [max_left_idx, min_right_idx],
                    ones,
                )

    if best_cost is None:
        print(-1)
        return

    if len(best_twos) == 1 and not best_ones:
        idx = best_twos[0]
        best_ones = cover(left[idx], right[idx], idx)
        if best_ones is None:
            print(-1)
            return
    elif len(best_twos) == 0 and not best_ones:
        best_ones = cover(1, n)
        if best_ones is None:
            print(-1)
            return

    operations = [0] * m
    for idx in best_twos:
        operations[idx] = 2
    for idx in best_ones:
        if operations[idx] == 0:
            operations[idx] = 1

    print(best_cost)
    print(*operations)


if __name__ == "__main__":
    main()