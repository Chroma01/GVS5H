import sys


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    t = next(it)
    out = []

    for _ in range(t):
        n = next(it)
        k = next(it)
        cakes = []
        for idx in range(n):
            x = next(it)
            y = next(it)
            z = next(it)
            vals = (x, y, z)
            m = max(vals)
            # Any maximizing coordinate is acceptable as the baseline color.
            c = 0 if x == m else (1 if y == m else 2)
            cakes.append((m, c, vals, idx))

        l = 2 * k
        cakes.sort(reverse=True, key=lambda q: q[0])

        selected = cakes[:l]
        outside = cakes[l:]

        base_value = sum(q[0] for q in selected)
        target = 0
        for m, c, vals, idx in selected:
            target ^= c

        if target == 0:
            out.append(str(base_value))
            continue

        # An operation is (parity_delta, cost, selected_item_id, outside_item_id).
        # outside_item_id = -1 denotes a recoloring operation.
        actions = []

        # For recolorings, retain a few cheapest actions of each parity delta.
        recolor_by_delta = [[] for _ in range(4)]
        for m, p, vals, idx in selected:
            for c in range(3):
                if c != p:
                    d = p ^ c
                    recolor_by_delta[d].append((m - vals[c], idx))

        for d in range(1, 4):
            recolor_by_delta[d].sort()
            for cost, idx in recolor_by_delta[d][:3]:
                actions.append((d, cost, idx, -1))

        # For exchanges, only the three cheapest removable baseline items of each
        # baseline color and the three best outside items for each target color
        # can be relevant to a compatible pair of operations.
        source = [[] for _ in range(3)]
        for m, p, vals, idx in selected:
            source[p].append((m, idx))

        dest = [[] for _ in range(3)]
        for m, p, vals, idx in outside:
            for c in range(3):
                dest[c].append((-vals[c], idx, vals[c]))

        for p in range(3):
            source[p].sort()
            source[p] = source[p][:3]

        for c in range(3):
            dest[c].sort()
            dest[c] = dest[c][:3]

        for p in range(3):
            for c in range(3):
                d = p ^ c
                if d == 0:
                    continue
                for sm, si in source[p]:
                    for negv, di, v in dest[c]:
                        actions.append((d, sm - v, si, di))

        best = 10**30

        # One operation.
        for d, cost, si, di in actions:
            if d == target and cost < best:
                best = cost

        # Two compatible operations.
        a_len = len(actions)
        for i in range(a_len):
            d1, c1, s1, o1 = actions[i]
            for j in range(i + 1, a_len):
                d2, c2, s2, o2 = actions[j]
                if (d1 ^ d2) != target:
                    continue
                if s1 == s2:
                    continue
                if o1 != -1 and o1 == o2:
                    continue
                cost = c1 + c2
                if cost < best:
                    best = cost

        out.append(str(base_value - best))

    print("\n".join(out))


if __name__ == "__main__":
    solve()