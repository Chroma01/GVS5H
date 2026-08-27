import sys
from bisect import bisect_left, bisect_right


def solve_case(n, k, cakes):
    length = 2 * k

    vals = [0] * n
    labels = [0] * n
    for i, (x, y, z) in enumerate(cakes):
        if x >= y and x >= z:
            labels[i] = 0
            vals[i] = x
        elif y >= z:
            labels[i] = 1
            vals[i] = y
        else:
            labels[i] = 2
            vals[i] = z

    order = sorted(range(n), key=lambda i: vals[i], reverse=True)
    rank = [0] * n
    pref = [0]
    for r, i in enumerate(order):
        rank[i] = r
        pref.append(pref[-1] + vals[i])

    groups = [[] for _ in range(3)]
    for i in range(n):
        groups[labels[i]].append(i)

    group_items = []
    group_positions = []
    group_index = [-1] * n
    for g in range(3):
        arr = sorted(groups[g], key=lambda i: vals[i], reverse=True)
        group_items.append(arr)
        positions = []
        for j, i in enumerate(arr):
            positions.append(rank[i])
            group_index[i] = j
        group_positions.append(positions)

    def best_selection(target_mask, forced):
        forced = list(dict.fromkeys(forced))
        f = len(forced)
        if f > length:
            return None

        forced_ranks = [rank[i] for i in forced]
        need = length - f
        if need < 0 or need > n - f:
            return None

        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            nonforced = mid - sum(r < mid for r in forced_ranks)
            if nonforced >= need:
                hi = mid
            else:
                lo = mid + 1
        limit = lo

        forced_sum = sum(vals[i] for i in forced)
        forced_before_sum = sum(
            vals[i] for i in forced if rank[i] < limit
        )
        total = pref[limit] - forced_before_sum + forced_sum

        forced_count = [0, 0, 0]
        forced_local = [[] for _ in range(3)]
        for i in forced:
            g = labels[i]
            forced_count[g] += 1
            forced_local[g].append(group_index[i])
        for g in range(3):
            forced_local[g].sort()

        count = [0, 0, 0]
        for g in range(3):
            c = bisect_left(group_positions[g], limit)
            c -= sum(p < limit for p in (
                group_positions[g][j] for j in forced_local[g]
            ))
            count[g] = c

        actual_mask = 0
        for g in range(3):
            if (count[g] + forced_count[g]) & 1:
                actual_mask |= 1 << g

        mismatch = actual_mask ^ target_mask
        if mismatch == 0:
            return total
        if mismatch.bit_count() != 2:
            return None

        def kth_nonforced_index(g, q):
            arr_len = len(group_items[g])
            if q < 0:
                return None
            idx = q
            while idx < arr_len:
                skipped = bisect_right(forced_local[g], idx)
                new_idx = q + skipped
                if new_idx == idx:
                    return idx
                idx = new_idx
            return None

        def selected_min(g):
            q = count[g]
            if q == 0:
                return None
            idx = kth_nonforced_index(g, q - 1)
            return None if idx is None else vals[group_items[g][idx]]

        def unselected_max(g):
            idx = kth_nonforced_index(g, count[g])
            return None if idx is None else vals[group_items[g][idx]]

        bad = [g for g in range(3) if (mismatch >> g) & 1]
        u, v = bad
        ru, rv = selected_min(u), selected_min(v)
        au, av = unselected_max(u), unselected_max(v)

        answer = None

        if ru is not None and av is not None:
            answer = total - ru + av
        if rv is not None and au is not None:
            candidate = total - rv + au
            answer = candidate if answer is None else max(answer, candidate)

        w = 3 ^ u ^ v
        rw, aw = selected_min(w), unselected_max(w)

        if ru is not None and rw is not None and av is not None and aw is not None:
            candidate = total - ru - rw + av + aw
            answer = candidate if answer is None else max(answer, candidate)

        if rv is not None and rw is not None and au is not None and aw is not None:
            candidate = total - rv - rw + au + aw
            answer = candidate if answer is None else max(answer, candidate)

        return answer

    answer = best_selection(0, [])

    # For a cross-label pair witnessed by coordinate t, the endpoint
    # contribution outside the selection sum is coordinate_t - individual_max.
    # Outside the boundary region, selected/unselected status is fixed, so
    # only the endpoint with maximum such contribution is needed.
    boundary = 8
    left = max(0, length - boundary)
    right = min(n, length + boundary + 3)

    for t in range(3):
        candidates = [[] for _ in range(3)]

        for g in range(3):
            used = set()

            for r in range(left, right):
                i = order[r]
                if labels[i] == g:
                    used.add(i)

            best_deep = None
            best_delta = None
            for lo, hi in ((0, left), (right, n)):
                for r in range(lo, hi):
                    i = order[r]
                    if labels[i] != g:
                        continue
                    delta = cakes[i][t] - vals[i]
                    if best_delta is None or delta > best_delta:
                        best_delta = delta
                        best_deep = i
            if best_deep is not None:
                used.add(best_deep)

            candidates[g] = list(used)

        for a in range(3):
            for b in range(a + 1, 3):
                target = (1 << a) | (1 << b)
                for e in candidates[b]:
                    for i in candidates[a]:
                        forced_value = best_selection(target, [e, i])
                        if forced_value is None:
                            continue
                        candidate = (
                            forced_value
                            - vals[e]
                            - vals[i]
                            + cakes[e][t]
                            + cakes[i][t]
                        )
                        if answer is None or candidate > answer:
                            answer = candidate

    return answer


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    out = []

    for _ in range(t):
        n = next(it)
        k = next(it)
        cakes = [(next(it), next(it), next(it)) for _ in range(n)]
        out.append(str(solve_case(n, k, cakes)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()