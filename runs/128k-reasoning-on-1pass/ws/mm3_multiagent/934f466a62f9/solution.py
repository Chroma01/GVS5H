import sys

INF = 10 ** 30
X_BIT = 1          # 001
Y_BIT = 2          # 010
Z_BIT = 4          # 100


def update_best(cat, D, idx):
    """store the two largest D of a category"""
    if D > cat['best1_D']:
        cat['best2_D'] = cat['best1_D']
        cat['best2_idx'] = cat['best1_idx']
        cat['best1_D'] = D
        cat['best1_idx'] = idx
    elif D > cat['best2_D']:
        cat['best2_D'] = D
        cat['best2_idx'] = idx


def feasible(cnt1, cnt2, cnt4, cnt3, cnt5, cnt6, cnt7):
    """
    Check whether we can assign colors to the cakes so that the numbers of
    X, Y, Z coloured cakes are all even.
    cnt1 – forced X (mask 1)
    cnt2 – forced Y (mask 2)
    cnt4 – forced Z (mask 4)
    cnt3 – mask 3 (X,Y)
    cnt5 – mask 5 (X,Z)
    cnt6 – mask 6 (Y,Z)
    cnt7 – mask 7 (X,Y,Z)
    """
    for p3 in (0, 1):
        if p3 and cnt3 == 0:
            continue
        for p5 in (0, 1):
            if p5 and cnt5 == 0:
                continue
            for p6 in (0, 1):
                if p6 and cnt6 == 0:
                    continue
                for p7 in (0, 1):
                    if p7 and cnt7 == 0:
                        continue
                    for q7 in (0, 1):
                        # q7: number of mask7 items assigned to Y (mod 2)
                        if q7 and (cnt7 - p7) <= 0:
                            continue
                        if p7 + q7 > cnt7:
                            continue
                        # parity constraints
                        if ((cnt1 + p3 + p5 + p7) & 1):
                            continue
                        if ((cnt2 + cnt3 + p3 + p6 + q7) & 1):
                            continue
                        if ((cnt4 + cnt5 + cnt6 + cnt7 + p5 + p6 + p7 + q7) & 1):
                            continue
                        return True
    return False


def solve() -> None:
    it = iter(sys.stdin.buffer.read().split())
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        N = int(next(it))
        K = int(next(it))
        items = []
        for i in range(N):
            X = int(next(it))
            Y = int(next(it))
            Z = int(next(it))
            M = X if X >= Y else Y
            if Z > M:
                M = Z
            mask = 0
            if X == M:
                mask |= X_BIT
            if Y == M:
                mask |= Y_BIT
            if Z == M:
                mask |= Z_BIT
            slackX = M - X
            slackY = M - Y
            slackZ = M - Z
            items.append((M, mask, slackX, slackY, slackZ))

        items.sort(key=lambda x: x[0], reverse=True)          # descending by M
        twoK = 2 * K
        sumTop = sum(it[0] for it in items[:twoK])

        # ---------- data of the selected set S ----------
        cnt = [0] * 8
        min_M = [INF] * 8
        min_idx = [-1] * 8
        for idx in range(twoK):
            M, mask, _, _, _ = items[idx]
            cnt[mask] += 1
            if M < min_M[mask]:
                min_M[mask] = M
                min_idx[mask] = idx

        cnt1 = cnt[1]   # forced X
        cnt2 = cnt[2]   # forced Y
        cnt4 = cnt[4]   # forced Z
        cnt3 = cnt[3]   # X,Y
        cnt5 = cnt[5]   # X,Z
        cnt6 = cnt[6]   # Y,Z
        cnt7 = cnt[7]   # X,Y,Z

        if feasible(cnt1, cnt2, cnt4, cnt3, cnt5, cnt6, cnt7):
            out_lines.append(str(sumTop))
            continue

        # ---------- minimum penalty inside S ----------
        pMin = INF
        groups = [{'cnt': 0,
                   'zeroX': False, 'posX': INF,
                   'zeroY': False, 'posY': INF,
                   'zeroZ': False, 'posZ': INF}
                  for _ in range(8)]
        for idx in range(twoK):
            M, mask, sx, sy, sz = items[idx]
            g = groups[mask]
            g['cnt'] += 1
            if sx == 0:
                g['zeroX'] = True
            elif sx < g['posX']:
                g['posX'] = sx
            if sy == 0:
                g['zeroY'] = True
            elif sy < g['posY']:
                g['posY'] = sy
            if sz == 0:
                g['zeroZ'] = True
            elif sz < g['posZ']:
                g['posZ'] = sz

        cross_pairs = [(X_BIT, Y_BIT),
                       (X_BIT, Z_BIT),
                       (Y_BIT, Z_BIT),
                       (X_BIT, Y_BIT | Z_BIT),
                       (Y_BIT, X_BIT | Z_BIT),
                       (Z_BIT, X_BIT | Y_BIT)]
        for ma, mb in cross_pairs:
            ga = groups[ma]
            gb = groups[mb]
            if ga['cnt'] == 0 or gb['cnt'] == 0:
                continue
            best = INF
            # coordinate X
            za, pa = ga['zeroX'], ga['posX']
            zb, pb = gb['zeroX'], gb['posX']
            if za and zb:
                pass
            elif za:
                if pb < best:
                    best = pb
            elif zb:
                if pa < best:
                    best = pa
            else:
                if pa + pb < best:
                    best = pa + pb
            # coordinate Y
            za, pa = ga['zeroY'], ga['posY']
            zb, pb = gb['zeroY'], gb['posY']
            if za and zb:
                pass
            elif za:
                if pb < best:
                    best = pb
            elif zb:
                if pa < best:
                    best = pa
            else:
                if pa + pb < best:
                    best = pa + pb
            # coordinate Z
            za, pa = ga['zeroZ'], ga['posZ']
            zb, pb = gb['zeroZ'], gb['posZ']
            if za and zb:
                pass
            elif za:
                if pb < best:
                    best = pb
            elif zb:
                if pa < best:
                    best = pa
            else:
                if pa + pb < best:
                    best = pa + pb
            if best < pMin:
                pMin = best

        # ---------- improvement by at most two swaps ----------
        # removal candidates (from S)
        removal_set = set()
        removal = []                     # each element = (M, mask, idx)
        if twoK >= 1:
            removal.append((items[twoK - 1][0], items[twoK - 1][1], twoK - 1))
            removal_set.add(twoK - 1)
        if twoK >= 2:
            removal.append((items[twoK - 2][0], items[twoK - 2][1], twoK - 2))
            removal_set.add(twoK - 2)
        for m in (1, 2, 3, 4, 5, 6, 7):
            if min_M[m] != INF and min_idx[m] not in removal_set:
                removal.append((min_M[m], m, min_idx[m]))
                removal_set.add(min_idx[m])

        # addition candidates (outside S) – the best two in each of seven categories
        cats = [{'best1_D': -1, 'best1_idx': -1,
                 'best2_D': -1, 'best2_idx': -1}
                for _ in range(7)]

        if twoK < N:
            for idx in range(twoK, N):
                M, mask, _, _, _ = items[idx]
                if mask & X_BIT:
                    update_best(cats[0], M, idx)
                if mask & Y_BIT:
                    update_best(cats[1], M, idx)
                if mask & Z_BIT:
                    update_best(cats[2], M, idx)
                if not (mask & X_BIT):
                    update_best(cats[3], M, idx)
                if not (mask & Y_BIT):
                    update_best(cats[4], M, idx)
                if not (mask & Z_BIT):
                    update_best(cats[5], M, idx)
                if (mask & X_BIT) and (mask & Y_BIT):
                    update_best(cats[6], M, idx)

        add = []
        for ci in range(7):
            if cats[ci]['best1_D'] != -1:
                idx = cats[ci]['best1_idx']
                add.append((cats[ci]['best1_D'], items[idx][1], idx))
            if cats[ci]['best2_D'] != -1:
                idx = cats[ci]['best2_idx']
                add.append((cats[ci]['best2_D'], items[idx][1], idx))

        minLoss = INF
        if twoK < N and add:
            init_cnt = cnt[:]   # list of length 8

            # ---------- one swap ----------
            for rem_M, rem_mask, rem_idx in removal:
                for add_M, add_mask, add_idx in add:
                    if rem_idx == add_idx:
                        continue
                    cur = init_cnt[:]
                    cur[rem_mask] -= 1
                    cur[add_mask] += 1
                    if feasible(cur[1], cur[2], cur[4], cur[3], cur[5], cur[6], cur[7]):
                        loss = rem_M - add_M
                        if loss < minLoss:
                            minLoss = loss

            # ---------- two swaps ----------
            rcnt = len(removal)
            acnt = len(add)
            for i in range(rcnt):
                for j in range(i + 1, rcnt):
                    r1_M, r1_mask, r1_idx = removal[i]
                    r2_M, r2_mask, r2_idx = removal[j]
                    if r1_idx == r2_idx:
                        continue
                    for p in range(acnt):
                        for q in range(p + 1, acnt):
                            a1_M, a1_mask, a1_idx = add[p]
                            a2_M, a2_mask, a2_idx = add[q]
                            if a1_idx == a2_idx or a1_idx == r1_idx or a1_idx == r2_idx or a2_idx == r1_idx or a2_idx == r2_idx:
                                continue
                            cur = init_cnt[:]
                            cur[r1_mask] -= 1
                            cur[r2_mask] -= 1
                            cur[a1_mask] += 1
                            cur[a2_mask] += 1
                            if feasible(cur[1], cur[2], cur[4], cur[3], cur[5], cur[6], cur[7]):
                                loss = (r1_M + r2_M) - (a1_M + a2_M)
                                if loss < minLoss:
                                    minLoss = loss

        # ---------- final answer ----------
        ans_no_penalty = (sumTop - minLoss) if minLoss != INF else -INF
        ans_with_penalty = sumTop - pMin
        answer = max(ans_no_penalty, ans_with_penalty)
        out_lines.append(str(answer))

    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()