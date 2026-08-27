import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    L = [0] * (M + 1)
    R = [0] * (M + 1)
    for i in range(1, M + 1):
        L[i] = int(next(it))
        R[i] = int(next(it))

    INF = M + 1

    # ---------- 1 paid operation ----------
    # op1 with [L,R] = [1,N] covers everything.
    for i in range(1, M + 1):
        if L[i] == 1 and R[i] == N:
            ops = ['0'] * (M + 1)
            ops[i] = '1'
            out = ['1', ' '.join(ops[1:])]
            sys.stdout.write('\n'.join(out) + '\n')
            return

    # ---------- 2 paid operations ----------
    # Case A: op1(i) + op1(k): union = [1,N]
    #   need L_i = 1, R_k = N, R_i >= L_k - 1 (i may equal k only if [1,N], already handled)
    bestR_L1 = -1          # max R among ops with L == 1
    idxR_L1 = -1
    minL_RN = INF          # min L among ops with R == N
    idxL_RN = -1
    for i in range(1, M + 1):
        if L[i] == 1 and R[i] > bestR_L1:
            bestR_L1 = R[i]; idxR_L1 = i
        if R[i] == N and L[i] < minL_RN:
            minL_RN = L[i]; idxL_RN = i
    if idxR_L1 != -1 and idxL_RN != -1 and idxR_L1 != idxL_RN and bestR_L1 >= minL_RN - 1:
        ops = ['0'] * (M + 1)
        ops[idxR_L1] = '1'
        ops[idxL_RN] = '1'
        sys.stdout.write('2\n' + ' '.join(ops[1:]) + '\n')
        return

    # Case B: op2(i) + op2(k): complements union to [1,N] iff intervals disjoint
    #   exists i,k with R_i < L_k  <=>  min R < max L (indices automatically distinct)
    minR = INF; idxMinR = -1
    maxL = -1; idxMaxL = -1
    for i in range(1, M + 1):
        if R[i] < minR:
            minR = R[i]; idxMinR = i
        if L[i] > maxL:
            maxL = L[i]; idxMaxL = i
    if idxMinR != -1 and idxMaxL != -1 and minR < maxL:
        ops = ['0'] * (M + 1)
        ops[idxMinR] = '2'
        ops[idxMaxL] = '2'
        sys.stdout.write('2\n' + ' '.join(ops[1:]) + '\n')
        return

    # Case C: op1(i) + op2(k), i != k, with L_i <= L_k and R_i >= R_k
    #   (interval i contains interval k)
    # Sweep over L ascending; maintain top-two (R, idx) among processed ops.
    order = sorted(range(1, M + 1), key=lambda i: (L[i], R[i]))
    # process groups by L; query against structure built from ops with L < current L,
    # then also need L_i == L_k with i != k: handle by querying within group using
    # a structure that includes same-L ops but excludes k itself via top-two.
    # Simpler: process all ops sorted by L; for each k in group, query top-two of
    # (previous groups + current group). Build current group's top-two first.
    ans_pair = None
    p = 0
    # global top-two among ops with L strictly less than current group
    g1 = (-1, -1)  # (R, idx) best
    g2 = (-1, -1)  # second best
    def upd(top, cand):
        (b1, b2) = top
        if cand[0] > b1[0]:
            return (cand, b1)
        elif cand[0] > b2[0]:
            return (b1, cand)
        return top
    while p < M:
        q = p
        while q < M and L[order[q]] == L[order[p]]:
            q += 1
        # group = order[p:q], all with same L value
        # top-two within group
        h1 = (-1, -1); h2 = (-1, -1)
        for t in range(p, q):
            i = order[t]
            h1, h2 = upd((h1, h2), (R[i], i))
        for t in range(p, q):
            k = order[t]
            # candidate i from previous groups (L_i < L_k) or same group (L_i == L_k, i != k)
            for (b1, b2) in ((g1, g2), (h1, h2)):
                for (rv, ri) in (b1, b2):
                    if ri == -1 or ri == k:
                        continue
                    if rv >= R[k]:
                        ans_pair = (ri, k)
                        break
                if ans_pair:
                    break
            if ans_pair:
                break
        if ans_pair:
            break
        # merge group into global
        for (rv, ri) in (h1, h2):
            if ri != -1:
                g1, g2 = upd((g1, g2), (rv, ri))
        p = q
    if ans_pair:
        (i, k) = ans_pair
        ops = ['0'] * (M + 1)
        ops[i] = '1'
        ops[k] = '2'
        sys.stdout.write('2\n' + ' '.join(ops[1:]) + '\n')
        return

    sys.stdout.write('-1\n')

solve()