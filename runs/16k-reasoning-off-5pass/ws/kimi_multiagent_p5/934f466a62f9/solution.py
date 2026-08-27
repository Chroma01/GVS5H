import sys
from collections import defaultdict


def solve_case(cakes, K):
    n = len(cakes)
    m = 2 * K

    # label each cake by a coordinate attaining its max (ties -> first)
    maxv = [0] * n
    label_of = [0] * n
    for i in range(n):
        x, y, z = cakes[i]
        if x >= y and x >= z:
            maxv[i] = x
            label_of[i] = 0
        elif y >= z:
            maxv[i] = y
            label_of[i] = 1
        else:
            maxv[i] = z
            label_of[i] = 2

    order = sorted(range(n), key=lambda i: -maxv[i])
    selected = order[:m]
    unselected = order[m:]

    cnt = [0, 0, 0]
    base = 0
    for i in selected:
        cnt[label_of[i]] += 1
        base += maxv[i]

    odd = [c for c in range(3) if cnt[c] & 1]
    if not odd:
        return base
    a, b = odd
    c = 3 - a - b

    # For each label l, keep the top few unselected cakes by cakes[·][l].
    # Any optimal fix uses <= 3 ops, each needing a distinct unselected cake,
    # so the top 8 per label are more than sufficient.
    POOL = 8
    top_unsel = []
    for l in range(3):
        pool = sorted(unselected, key=lambda j: -cakes[j][l])[:POOL]
        top_unsel.append(pool)

    # Candidate ops. Each op toggles the parity of exactly two labels.
    #  flip: relabel selected cake i to label l; cost = maxv[i] - cakes[i][l]
    #  swap: replace selected i by unselected j labeled l; cost = maxv[i] - cakes[j][l]
    # (Costs are always >= 0: for flips maxv[i] >= cakes[i][l]; for swaps
    #  maxv[i] >= maxv[j] >= cakes[j][l] since i is in the top-m by maxv.)
    ops_by_pair = defaultdict(list)

    def add_op(p, q, cost, items):
        key = (p, q) if p < q else (q, p)
        ops_by_pair[key].append((cost, items))

    for i in selected:
        li = label_of[i]
        mi = maxv[i]
        ci = cakes[i]
        for l in range(3):
            if l != li:
                add_op(li, l, mi - ci[l], (('s', i),))
        for l in range(3):
            if l == li:
                continue
            for j in top_unsel[l]:
                add_op(li, l, mi - cakes[j][l], (('s', i), ('u', j)))

    # keep top 8 cheapest per toggle-pair (enough for disjoint combos of <=3 ops)
    for key in ops_by_pair:
        ops_by_pair[key] = sorted(ops_by_pair[key], key=lambda t: t[0])[:8]

    def key2(p, q):
        return (p, q) if p < q else (q, p)

    INF = 1 << 62
    best_fix = INF

    # Pattern 1: a single op toggling (a, b)
    for cost, _ in ops_by_pair.get(key2(a, b), ()):
        if cost < best_fix:
            best_fix = cost

    # Pattern 2: two ops toggling (a,c) and (b,c), using distinct items
    for cost1, items1 in ops_by_pair.get(key2(a, c), ()):
        if cost1 >= best_fix:
            break
        s1 = set(items1)
        for cost2, items2 in ops_by_pair.get(key2(b, c), ()):
            t = cost1 + cost2
            if t >= best_fix:
                break
            if s1.isdisjoint(items2):
                best_fix = t
                break

    # Pattern 3: three ops each toggling (a,b), pairwise distinct items
    lst = ops_by_pair.get(key2(a, b), [])
    L = len(lst)
    for x in range(L):
        cx, ix = lst[x]
        if cx >= best_fix:
            break
        sx = set(ix)
        for y in range(x + 1, L):
            cy, iy = lst[y]
            if cx + cy >= best_fix:
                break
            if not sx.isdisjoint(iy):
                continue
            sxy = sx | set(iy)
            for z in range(y + 1, L):
                cz, iz = lst[z]
                t = cx + cy + cz
                if t >= best_fix:
                    break
                if sxy.isdisjoint(iz):
                    best_fix = t
                    break

    return base - best_fix


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(data[idx]); K = int(data[idx + 1]); idx += 2
        cakes = []
        for _ in range(N):
            x = int(data[idx]); y = int(data[idx + 1]); z = int(data[idx + 2]); idx += 3
            cakes.append((x, y, z))
        out.append(str(solve_case(cakes, K)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()