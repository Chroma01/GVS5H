import sys
from operator import itemgetter

INF = 10**30

BITS = (1, 2, 4)  # X, Y, Z
TOG_IDX = [-1] * 8
TOG_IDX[3] = 0  # X <-> Y
TOG_IDX[5] = 1  # X <-> Z
TOG_IDX[6] = 2  # Y <-> Z

# For toggle 0,1,2 = (3,5,6), valid (base_color, target_color) pairs.
SWAP_BASES = ((0, 1), (0, 2), (1, 2))
SWAP_TARGETS = ((1, 0), (2, 0), (2, 1))

# Top 2 is provably enough; 5 is a small safety margin.
L = 5


def finish_recolor_only(rec_lists, P, S):
    """Used when all cakes are selected (no outside items)."""
    if P == 0:
        return S
    p = TOG_IDX[P]
    if p < 0:
        return S

    tops = []
    for lst in rec_lists:
        lst.sort()
        tops.append(lst[:3])

    best = INF
    for cost, _ in tops[p]:
        if cost < best:
            best = cost

    others = [i for i in range(3) if i != p]
    o1, o2 = others[0], others[1]
    for c1, id1 in tops[o1]:
        for c2, id2 in tops[o2]:
            if id1 != id2:
                v = c1 + c2
                if v < best:
                    best = v

    return S - best


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    ptr = 0
    T = data[ptr]
    ptr += 1
    out = []

    for _ in range(T):
        N = data[ptr]
        K = data[ptr + 1]
        ptr += 2
        C = 2 * K

        # One pair: max over attributes of the sum of the top two values.
        if K == 1:
            x1 = x2 = y1 = y2 = z1 = z2 = 0
            for _ in range(N):
                x = data[ptr]
                y = data[ptr + 1]
                z = data[ptr + 2]
                ptr += 3

                if x >= x1:
                    x2 = x1
                    x1 = x
                elif x > x2:
                    x2 = x

                if y >= y1:
                    y2 = y1
                    y1 = y
                elif y > y2:
                    y2 = y

                if z >= z1:
                    z2 = z1
                    z1 = z
                elif z > z2:
                    z2 = z

            ans = x1 + x2
            if y1 + y2 > ans:
                ans = y1 + y2
            if z1 + z2 > ans:
                ans = z1 + z2
            out.append(str(ans))
            continue

        # If all cakes must be used, only recolors are possible.
        if C == N:
            S = 0
            P = 0
            rec_lists = [[], [], []]

            for sid in range(N):
                x = data[ptr]
                y = data[ptr + 1]
                z = data[ptr + 2]
                ptr += 3

                if x >= y and x >= z:
                    M = x
                    b = 0
                elif y >= z:
                    M = y
                    b = 1
                else:
                    M = z
                    b = 2

                S += M
                P ^= BITS[b]

                if b == 0:
                    rec_lists[0].append((M - y, sid))
                    rec_lists[1].append((M - z, sid))
                elif b == 1:
                    rec_lists[0].append((M - x, sid))
                    rec_lists[2].append((M - z, sid))
                else:
                    rec_lists[1].append((M - x, sid))
                    rec_lists[2].append((M - y, sid))

            out.append(str(finish_recolor_only(rec_lists, P, S)))
            continue

        items = []
        append = items.append

        for sid in range(N):
            x = data[ptr]
            y = data[ptr + 1]
            z = data[ptr + 2]
            ptr += 3

            if x >= y and x >= z:
                M = x
                b = 0
            elif y >= z:
                M = y
                b = 1
            else:
                M = z
                b = 2

            append((M, x, y, z, b, sid))

        items.sort(key=itemgetter(0), reverse=True)

        S = 0
        P = 0
        for pos in range(C):
            M, x, y, z, b, sid = items[pos]
            S += M
            P ^= BITS[b]

        if P == 0:
            out.append(str(S))
            continue

        sel_base = [[], [], []]
        rec_lists = [[], [], []]

        for pos in range(C):
            M, x, y, z, b, sid = items[pos]
            sel_base[b].append((M, sid))

            if b == 0:
                rec_lists[0].append((M - y, sid))
                rec_lists[1].append((M - z, sid))
            elif b == 1:
                rec_lists[0].append((M - x, sid))
                rec_lists[2].append((M - z, sid))
            else:
                rec_lists[1].append((M - x, sid))
                rec_lists[2].append((M - y, sid))

        outside_vals = [[], [], []]
        for pos in range(C, N):
            M, x, y, z, b, sid = items[pos]
            outside_vals[0].append((x, sid))
            outside_vals[1].append((y, sid))
            outside_vals[2].append((z, sid))

        for c in range(3):
            outside_vals[c].sort(reverse=True)

        ops = [[], [], []]

        # Recolor candidates: three cheapest per toggle.
        for ti in range(3):
            rec_lists[ti].sort()
            for cost, sid in rec_lists[ti][:3]:
                ops[ti].append((cost, sid, -1))

        # Swap candidates: only a few smallest-M selected items per base color
        # and a few largest-value outside items per target color are needed.
        sel_top = [lst[-L:] for lst in sel_base]
        out_top = [lst[:L] for lst in outside_vals]

        for ti in range(3):
            bases = SWAP_BASES[ti]
            targets = SWAP_TARGETS[ti]
            for k in range(2):
                b = bases[k]
                c = targets[k]
                sel_list = sel_top[b]
                out_list = out_top[c]
                if not sel_list or not out_list:
                    continue
                for M, i in sel_list:
                    for val, j in out_list:
                        cost = M - val
                        if cost < 0:
                            cost = 0
                        ops[ti].append((cost, i, j))

        for ti in range(3):
            ops[ti].sort()

        p = TOG_IDX[P]
        if p < 0:
            out.append(str(S))
            continue

        best = INF
        if ops[p]:
            best = ops[p][0][0]

        others = [i for i in range(3) if i != p]
        o1, o2 = others[0], others[1]

        for c1, i1, j1 in ops[o1]:
            if c1 >= best:
                break
            for c2, i2, j2 in ops[o2]:
                s = c1 + c2
                if s >= best:
                    break
                if i1 == i2:
                    continue
                if j1 != -1 and j2 != -1 and j1 == j2:
                    continue
                best = s

        if best >= INF:
            best = 0

        out.append(str(S - best))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()