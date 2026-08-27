import sys
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1
    L = [0]*(M+1); R = [0]*(M+1)
    for i in range(1, M+1):
        L[i] = int(data[pos]); R[i] = int(data[pos+1]); pos += 2

    INF = float('inf')

    # ---------- coordinate compression ----------
    xs = set()
    xs.add(1); xs.add(N+1)
    for i in range(1, M+1):
        xs.add(L[i])
        xs.add(R[i]+1)
    xs = sorted(xs)
    K = len(xs)
    idx_of = {v:k for k,v in enumerate(xs)}

    # ---------- sweep: top-3 (R, idx) among intervals with L <= coord ----------
    order = sorted(range(1, M+1), key=lambda i: L[i])
    topR = [[-1]*3 for _ in range(K)]
    topI = [[-1]*3 for _ in range(K)]
    p = 0
    cur_top = []  # up to 3 best (R, idx), sorted desc by R
    for k in range(K):
        x = xs[k]
        while p < M and L[order[p]] <= x:
            i = order[p]; p += 1
            r = R[i]
            inserted = False
            for t in range(len(cur_top)):
                if r > cur_top[t][0]:
                    cur_top.insert(t, (r, i))
                    inserted = True
                    break
            if not inserted:
                cur_top.append((r, i))
            if len(cur_top) > 3:
                cur_top.pop()
        for t in range(len(cur_top)):
            topR[k][t] = cur_top[t][0]
            topI[k][t] = cur_top[t][1]

    # ---------- exact greedy cover (forbid-aware) with step cap ----------
    # Minimum list of interval indices (none in `forbid`) covering [p_val,q_val],
    # or None if infeasible or if the cover would reach `cap` steps.
    def recover_cover(p_val, q_val, forbid, cap):
        if p_val > q_val:
            return []
        cur = idx_of[p_val]
        res = []
        while xs[cur] <= q_val:
            if len(res) >= cap:
                return None
            x = xs[cur]
            chosen = -1; chosenR = -1
            tr = topR[cur]; ti = topI[cur]
            for t in range(3):
                ii = ti[t]
                if ii == -1:
                    break
                if ii not in forbid:
                    chosen = ii; chosenR = tr[t]
                    break
            if chosen == -1 or chosenR < x:
                return None
            res.append(chosen)
            cur = idx_of[chosenR+1]
        return res

    best_cost = INF
    best_plan = None

    def consider(cost, B, A):
        nonlocal best_cost, best_plan
        if cost < best_cost:
            best_cost = cost
            best_plan = (list(B), list(A))

    # (c) disjoint pair -> cost 2
    minR = INF; minRi = -1
    maxL = -1; maxLi = -1
    for i in range(1, M+1):
        if R[i] < minR:
            minR = R[i]; minRi = i
        if L[i] > maxL:
            maxL = L[i]; maxLi = i
    if minRi != -1 and maxLi != -1 and minR < maxL:
        consider(2, [minRi, maxLi], [])

    # (a) B = empty: cover [1, N]
    cap = best_cost if best_cost != INF else M + 1
    planA = recover_cover(1, N, frozenset(), cap)
    if planA is not None:
        consider(len(planA), [], planA)

    # (b) B = {b}: 1 + cover [L_b, R_b] avoiding b
    if best_cost > 2:
        # cost-2 candidate exists iff some a != b contains [L_b, R_b]
        ordL = sorted(range(1, M+1), key=lambda i: (L[i], R[i]))
        groups = []
        gi = 0
        while gi < M:
            gj = gi
            while gj < M and L[ordL[gj]] == L[ordL[gi]]:
                gj += 1
            groups.append(ordL[gi:gj])
            gi = gj
        found2 = False
        best1 = (-1, -1)  # (R, idx) among L_a <= L_b
        best2 = (-1, -1)
        witness = None
        for members in groups:
            for a in members:
                ra = R[a]
                if ra >= best1[0]:
                    best2 = best1; best1 = (ra, a)
                elif ra > best2[0]:
                    best2 = (ra, a)
            for b in members:
                if best1[1] != b:
                    if best1[0] >= R[b]:
                        found2 = True; witness = (b, best1[1]); break
                else:
                    if best2[0] >= R[b]:
                        found2 = True; witness = (b, best2[1]); break
            if found2:
                break
        if found2:
            b, a = witness
            consider(2, [b], [a])
        else:
            for b in range(1, M+1):
                if 2 >= best_cost:
                    break
                cap = best_cost - 1
                planA = recover_cover(L[b], R[b], frozenset([b]), cap)
                if planA is not None:
                    consider(1 + len(planA), [b], planA)

    # (d) B = {i,j} overlapping: 2 + cover [max L, min R] avoiding {i,j}
    if best_cost > 3:
        Ri_sorted = sorted((R[i], i) for i in range(1, M+1))
        Rs = [r for r, _ in Ri_sorted]
        Li_sorted = sorted((L[i], i) for i in range(1, M+1))
        Ls = [l for l, _ in Li_sorted]
        for i in range(1, M+1):
            if 3 >= best_cost:
                break
            cand_js = []
            # j != i with smallest R_j >= L_i
            posj = bisect.bisect_left(Rs, L[i])
            for t in range(posj, min(M, posj+2)):
                if Ri_sorted[t][1] != i:
                    cand_js.append(Ri_sorted[t][1])
                    break
            # partner != i with largest L <= R_i (symmetric direction)
            posi = bisect.bisect_right(Ls, R[i]) - 1
            for t in range(posi, max(-1, posi-2), -1):
                if Li_sorted[t][1] != i:
                    cand_js.append(Li_sorted[t][1])
                    break
            for j in cand_js:
                p_val = max(L[i], L[j]); q_val = min(R[i], R[j])
                if p_val > q_val:
                    continue
                cap = best_cost - 2
                planA = recover_cover(p_val, q_val, frozenset([i, j]), cap)
                if planA is not None:
                    consider(2 + len(planA), [i, j], planA)

    if best_cost == INF:
        sys.stdout.write("-1\n")
        return

    B, A = best_plan
    ops = [0]*(M+1)
    for i in A:
        ops[i] = 1
    for i in B:
        ops[i] = 2
    out = [str(best_cost)]
    out.append(' '.join(str(ops[i]) for i in range(1, M+1)))
    sys.stdout.write('\n'.join(out) + '\n')

main()