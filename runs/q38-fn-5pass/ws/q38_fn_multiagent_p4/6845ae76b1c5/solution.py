import sys
import math
from bisect import bisect_right
from itertools import accumulate

DIRECT = 2000


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)

    N = next(it)
    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]
    K = next(it)

    X = [0] * K
    Y = [0] * K
    maxX = 0
    maxY = 0
    for i in range(K):
        x = next(it)
        y = next(it)
        X[i] = x
        Y[i] = y
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y

    def partial_sum(sa, x, sb, y, A=A, B=B, br=bisect_right, acc=accumulate):
        la = x - sa
        lb = y - sb
        if la <= 0 or lb <= 0:
            return 0

        if la == 1:
            ai = A[sa]
            s = 0
            for j in range(sb, y):
                d = ai - B[j]
                if d < 0:
                    d = -d
                s += d
            return s

        if lb == 1:
            bj = B[sb]
            s = 0
            for i in range(sa, x):
                d = A[i] - bj
                if d < 0:
                    d = -d
                s += d
            return s

        if la * lb <= DIRECT:
            s = 0
            A_loc = A
            B_loc = B
            for i in range(sa, x):
                ai = A_loc[i]
                for j in range(sb, y):
                    d = ai - B_loc[j]
                    if d < 0:
                        d = -d
                    s += d
            return s

        if la <= lb:
            vb = B[sb:y]
            vb.sort()
            m = lb
            pref = [0]
            pref.extend(acc(vb))
            total = pref[m]
            ans = 0
            for i in range(sa, x):
                v = A[i]
                p = br(vb, v)
                ss = pref[p]
                ans += v * (p + p - m) + total - (ss << 1)
            return ans
        else:
            va = A[sa:x]
            va.sort()
            m = la
            pref = [0]
            pref.extend(acc(va))
            total = pref[m]
            ans = 0
            for j in range(sb, y):
                v = B[j]
                p = br(va, v)
                ss = pref[p]
                ans += v * (p + p - m) + total - (ss << 1)
            return ans

    # For very small total work, answer each query directly.
    if K * max(maxX, maxY) <= 3_000_000:
        out_lines = []
        cache = {}
        for i in range(K):
            key = (0, X[i], 0, Y[i])
            res = cache.get(key)
            if res is None:
                res = partial_sum(0, X[i], 0, Y[i])
                cache[key] = res
            out_lines.append(str(res))
        sys.stdout.write("\n".join(out_lines))
        return

    area = maxX * maxY
    S = int(math.sqrt(area / K) * 1.2) + 1
    if K > 5000:
        maxS = 1200
    elif K > 1000:
        maxS = 1800
    else:
        maxS = 2500
    if S > maxS:
        S = maxS
    if S > max(maxX, maxY):
        S = max(maxX, maxY)
    if S < 1:
        S = 1

    bx = [0] * K
    by = [0] * K
    startA = [0] * K
    startB = [0] * K

    for i in range(K):
        b = X[i] // S
        c = Y[i] // S
        bx[i] = b
        by[i] = c
        startA[i] = b * S
        startB[i] = c * S

    ans = [0] * K

    # Full A blocks vs all B prefixes.
    need_A = [i for i in range(K) if bx[i] > 0]
    if need_A:
        ys = sorted({Y[i] for i in need_A})
        y_idx = {y: i for i, y in enumerate(ys)}
        q_yidx = [-1] * K
        max_bx_A = 0
        for i in need_A:
            q_yidx[i] = y_idx[Y[i]]
            if bx[i] > max_bx_A:
                max_bx_A = bx[i]

        q_by_a = [[] for _ in range(max_bx_A + 1)]
        for i in need_A:
            q_by_a[bx[i]].append(i)

        cum = [0] * len(ys)
        max_y_A = ys[-1]
        orderB_eff = list(range(max_y_A))
        orderB_eff.sort(key=B.__getitem__)
        out = [0] * max_y_A
        D = len(ys)

        A_loc = A
        B_loc = B

        for b in range(max_bx_A + 1):
            for qi in q_by_a[b]:
                ans[qi] += cum[q_yidx[qi]]

            if b == max_bx_A:
                break

            sa = b * S
            ea = sa + S
            if ea > N:
                ea = N

            vals = A_loc[sa:ea]
            vals.sort()
            L = ea - sa
            total = sum(vals)

            p = 0
            t2 = total
            vals_loc = vals
            out_loc = out
            B_loc2 = B_loc

            for idx in orderB_eff:
                v = B_loc2[idx]
                while p < L:
                    vv = vals_loc[p]
                    if vv > v:
                        break
                    t2 -= vv + vv
                    p += 1
                out_loc[idx] = v * (p + p - L) + t2

            cum_loc = cum
            out_loc = out
            if D * 8 < max_y_A:
                run = 0
                pos = 0
                for idx, y in enumerate(ys):
                    for j in range(pos, y):
                        run += out_loc[j]
                    cum_loc[idx] += run
                    pos = y
            else:
                run = 0
                yi = 0
                next_y = ys[0]
                for j, val in enumerate(out_loc, 1):
                    run += val
                    if j == next_y:
                        cum_loc[yi] += run
                        yi += 1
                        if yi == D:
                            break
                        next_y = ys[yi]

    # Partial A vs full B blocks.
    need_B = [i for i in range(K) if by[i] > 0 and X[i] > startA[i]]
    if need_B:
        pos_set = set()
        max_by_B = 0
        for i in need_B:
            pos_set.add(X[i])
            pos_set.add(startA[i])
            if by[i] > max_by_B:
                max_by_B = by[i]

        pos_list = sorted(p for p in pos_set if p > 0)
        pos_idx = {p: i for i, p in enumerate(pos_list)}

        q_posX = [-1] * K
        q_posS = [-1] * K
        for i in need_B:
            q_posX[i] = pos_idx[X[i]]
            s = startA[i]
            if s > 0:
                q_posS[i] = pos_idx[s]

        q_by_b = [[] for _ in range(max_by_B + 1)]
        for i in need_B:
            q_by_b[by[i]].append(i)

        cum = [0] * len(pos_list)
        max_x_B = pos_list[-1]
        orderA_eff = list(range(max_x_B))
        orderA_eff.sort(key=A.__getitem__)
        out = [0] * max_x_B
        D = len(pos_list)

        A_loc = A
        B_loc = B

        for b in range(max_by_B + 1):
            for qi in q_by_b[b]:
                val = cum[q_posX[qi]]
                ps = q_posS[qi]
                if ps != -1:
                    val -= cum[ps]
                ans[qi] += val

            if b == max_by_B:
                break

            sa = b * S
            ea = sa + S
            if ea > N:
                ea = N

            vals = B_loc[sa:ea]
            vals.sort()
            L = ea - sa
            total = sum(vals)

            p = 0
            t2 = total
            vals_loc = vals
            out_loc = out
            A_loc2 = A_loc

            for idx in orderA_eff:
                v = A_loc2[idx]
                while p < L:
                    vv = vals_loc[p]
                    if vv > v:
                        break
                    t2 -= vv + vv
                    p += 1
                out_loc[idx] = v * (p + p - L) + t2

            cum_loc = cum
            out_loc = out
            if D * 8 < max_x_B:
                run = 0
                pos = 0
                for idx, p in enumerate(pos_list):
                    for j in range(pos, p):
                        run += out_loc[j]
                    cum_loc[idx] += run
                    pos = p
            else:
                run = 0
                pi = 0
                next_pos = pos_list[0]
                for j, val in enumerate(out_loc, 1):
                    run += val
                    if j == next_pos:
                        cum_loc[pi] += run
                        pi += 1
                        if pi == D:
                            break
                        next_pos = pos_list[pi]

    # Partial A vs partial B.
    cache = {}
    for qi in range(K):
        sa = startA[qi]
        x = X[qi]
        sb = startB[qi]
        y = Y[qi]
        if x > sa and y > sb:
            key = (sa, x, sb, y)
            res = cache.get(key)
            if res is None:
                res = partial_sum(sa, x, sb, y)
                cache[key] = res
            ans[qi] += res

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()