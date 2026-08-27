import sys
import math
from array import array
from itertools import accumulate


def build_table(vals, blocks):
    n = len(vals)
    table = [array('q', [0]) * (n + 1)]
    if not blocks:
        return table

    f = [0] * n

    order = list(range(n))
    order.sort(key=vals.__getitem__)
    sorted_vals = [vals[i] for i in order]

    for block in blocks:
        s = len(block)
        pref = [0]
        pref.extend(accumulate(block))
        total = pref[-1]

        p = 0
        f_local = f
        block_local = block
        pref_local = pref
        total_local = total
        s_local = s
        order_local = order
        sorted_vals_local = sorted_vals

        for idx, a in zip(order_local, sorted_vals_local):
            while p < s_local and block_local[p] <= a:
                p += 1
            pp = pref_local[p]
            f_local[idx] += a * (p + p - s_local) + total_local - pp - pp

        table.append(array('q', accumulate(f_local, initial=0)))

    return table


def cross_abs(U, V):
    lu = len(U)
    lv = len(V)
    if lu == 0 or lv == 0:
        return 0

    total_u = sum(U)
    total_v = sum(V)

    U.sort()
    V.sort()

    if U[-1] <= V[0]:
        return total_v * lu - total_u * lv
    if U[0] >= V[-1]:
        return total_u * lv - total_v * lu

    i = j = 0
    su = sv = ans = 0

    while i < lu and j < lv:
        if U[i] <= V[j]:
            u = U[i]
            ans += u * j - sv
            su += u
            i += 1
        else:
            v = V[j]
            ans += v * i - su
            sv += v
            j += 1

    if i < lu:
        ans += (total_u - su) * j - sv * (lu - i)
    else:
        ans += (total_v - sv) * i - su * (lv - j)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    pos = 0
    N = data[pos]
    pos += 1

    A = data[pos:pos + N]
    pos += N

    B = data[pos:pos + N]
    pos += N

    K = data[pos]
    pos += 1

    queries = []
    for _ in range(K):
        x = data[pos]
        y = data[pos + 1]
        pos += 2
        queries.append((x, y))

    del data

    M = min(N, max(1, math.isqrt(K // 2) + 1))
    S = (N + M - 1) // M
    F = N // S

    B_blocks = [sorted(B[i * S:(i + 1) * S]) for i in range(F)]
    A_blocks = [sorted(A[i * S:(i + 1) * S]) for i in range(F)]

    PA = build_table(A, B_blocks)
    PB = build_table(B, A_blocks)

    del A_blocks, B_blocks

    G = [[0] * (F + 1) for _ in range(F + 1)]
    for x in range(F + 1):
        idx = x * S
        gx = G[x]
        for y in range(F + 1):
            gx[y] = PA[y][idx]

    ans = [0] * K
    groups = {}

    PA_l = PA
    PB_l = PB
    G_l = G
    S_l = S
    A_l = A
    B_l = B

    for qi, (X, Y) in enumerate(queries):
        xb = X // S_l
        yb = Y // S_l
        sa = xb * S_l
        sb = yb * S_l

        rA = X - sa
        rB = Y - sb

        val = G_l[xb][yb]

        if yb and rA:
            val += PA_l[yb][X] - PA_l[yb][sa]
        if xb and rB:
            val += PB_l[xb][Y] - PB_l[xb][sb]

        ans[qi] = val

        if rA and rB:
            key = (xb, yb)
            groups.setdefault(key, []).append((rA, rB, qi))

    del queries
    del PA, PB, G, PA_l, PB_l, G_l

    cross = cross_abs

    for (xb, yb), items in groups.items():
        pair_map = {}
        maxR = 0
        maxC = 0

        for rA, rB, qi in items:
            pair_map.setdefault((rA, rB), []).append(qi)
            if rA > maxR:
                maxR = rA
            if rB > maxC:
                maxC = rB

        sum_per = 0
        uniqueR = set()
        uniqueC = set()
        for (rA, rB) in pair_map:
            sum_per += rA + rB
            uniqueR.add(rA)
            uniqueC.add(rB)

        costA = (maxR + len(uniqueR)) * maxC
        costB = (maxC + len(uniqueC)) * maxR
        best = costA if costA < costB else costB

        startA = xb * S_l
        startB = yb * S_l

        if len(pair_map) >= 16 and best < sum_per:
            if costA <= costB:
                by_rA = {}
                for (rA, rB), idxs in pair_map.items():
                    by_rA.setdefault(rA, []).append((rB, idxs))

                b_block = B_l[startB:startB + maxC]
                acc = [0] * maxC
                ans_l = ans

                for i in range(maxR):
                    a = A_l[startA + i]
                    acc = [x + (a - b if a >= b else b - a) for x, b in zip(acc, b_block)]

                    lst = by_rA.get(i + 1)
                    if lst is not None:
                        pref = list(accumulate(acc, initial=0))
                        for rB, idxs in lst:
                            v = pref[rB]
                            for qi in idxs:
                                ans_l[qi] += v
            else:
                by_rB = {}
                for (rA, rB), idxs in pair_map.items():
                    by_rB.setdefault(rB, []).append((rA, idxs))

                a_block = A_l[startA:startA + maxR]
                acc = [0] * maxR
                ans_l = ans

                for j in range(maxC):
                    b = B_l[startB + j]
                    acc = [x + (b - a if b >= a else a - b) for x, a in zip(acc, a_block)]

                    lst = by_rB.get(j + 1)
                    if lst is not None:
                        pref = list(accumulate(acc, initial=0))
                        for rA, idxs in lst:
                            v = pref[rA]
                            for qi in idxs:
                                ans_l[qi] += v
        else:
            ans_l = ans
            for (rA, rB), idxs in pair_map.items():
                if rA == 1 and rB == 1:
                    u = A_l[startA]
                    v = B_l[startB]
                    s = u - v if u >= v else v - u
                elif rA == 1:
                    u = A_l[startA]
                    s = 0
                    for v in B_l[startB:startB + rB]:
                        if u >= v:
                            s += u - v
                        else:
                            s += v - u
                elif rB == 1:
                    v = B_l[startB]
                    s = 0
                    for u in A_l[startA:startA + rA]:
                        if u >= v:
                            s += u - v
                        else:
                            s += v - u
                else:
                    U = A_l[startA:startA + rA]
                    V = B_l[startB:startB + rB]
                    s = cross(U, V)

                for qi in idxs:
                    ans_l[qi] += s

    sys.stdout.write('\n'.join(map(str, ans)))


if __name__ == "__main__":
    main()