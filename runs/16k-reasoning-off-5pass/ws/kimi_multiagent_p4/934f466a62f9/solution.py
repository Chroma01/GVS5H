import sys

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out_lines = []
    NEG = -10**30
    INF = float('inf')
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos+1]); pos += 2
        X = [0]*N; Y = [0]*N; Z = [0]*N
        for i in range(N):
            X[i] = int(data[pos]); Y[i] = int(data[pos+1]); Z[i] = int(data[pos+2]); pos += 3
        M = 2*K
        m = [0]*N
        c = [0]*N
        for i in range(N):
            xi, yi, zi = X[i], Y[i], Z[i]
            if xi >= yi and xi >= zi:
                m[i] = xi; c[i] = 0
            elif yi >= zi:
                m[i] = yi; c[i] = 1
            else:
                m[i] = zi; c[i] = 2
        order = sorted(range(N), key=lambda i: -m[i])
        S0 = order[:M]
        inS = [False]*N
        for i in S0:
            inS[i] = True
        base = 0
        cnt = [0, 0, 0]
        for i in S0:
            base += m[i]
            cnt[c[i]] += 1
        odd = [col for col in range(3) if cnt[col] % 2 == 1]
        if not odd:
            out_lines.append(str(base))
            continue
        A, B = odd[0], odd[1]
        C = 3 - A - B
        vals = [X, Y, Z]
        vA, vB, vC = vals[A], vals[B], vals[C]

        groupA = [i for i in S0 if c[i] == A]
        groupB = [i for i in S0 if c[i] == B]
        groupC = [i for i in S0 if c[i] == C]

        minA = min(vA[i] for i in groupA)
        minB = min(vB[i] for i in groupB)
        minA_B = min(vA[i]-vB[i] for i in groupA)
        minB_A = min(vB[i]-vA[i] for i in groupB)
        minA_C = min(vA[i]-vC[i] for i in groupA)
        minB_C = min(vB[i]-vC[i] for i in groupB)

        candC_A = sorted(((vC[i]-vA[i], i) for i in groupC))[:2]
        candC_B = sorted(((vC[i]-vB[i], i) for i in groupC))[:2]
        candC_v = sorted(((vC[i], i) for i in groupC))[:2]
        minC_A = candC_A[0][0]
        minC_B = candC_B[0][0]
        minC1 = candC_v[0][0]
        minC2 = candC_v[1][0] if len(candC_v) > 1 else INF

        outsiders = [i for i in range(N) if not inS[i]]
        outA = sorted(((vA[i], i) for i in outsiders), reverse=True)[:2]
        outB = sorted(((vB[i], i) for i in outsiders), reverse=True)[:2]
        outC = sorted(((vC[i], i) for i in outsiders), reverse=True)[:2]
        maxOutA = outA[0][0] if outA else NEG
        maxOutB = outB[0][0] if outB else NEG
        maxOutC = outC[0][0] if outC else NEG

        def best_pair_sum_diff(L1, L2):
            best = NEG
            for v1, j1 in L1:
                for v2, j2 in L2:
                    if j1 != j2 and v1+v2 > best:
                        best = v1+v2
            return best

        loss = INF
        loss = min(loss, minA_B)
        loss = min(loss, minB_A)
        if outB:
            loss = min(loss, minA - maxOutB)
        if outA:
            loss = min(loss, minB - maxOutA)

        # Pattern 5: net (-1,+1,0) via C: (e_C - e_A) + (e_B - e_C)
        p5 = minA_C + minC_B
        if outC:
            p5 = min(p5, minA - maxOutC + minC_B)
        if outB:
            p5 = min(p5, minA_C + minC1 - maxOutB)
        add = best_pair_sum_diff(outC, outB)
        if add != NEG:
            p5 = min(p5, minA + minC1 - add)
        loss = min(loss, p5)

        # Pattern 6: net (+1,-1,0) via C: (e_C - e_B) + (e_A - e_C)
        p6 = minB_C + minC_A
        if outC:
            p6 = min(p6, minB - maxOutC + minC_A)
        if outA:
            p6 = min(p6, minB_C + minC1 - maxOutA)
        add = best_pair_sum_diff(outC, outA)
        if add != NEG:
            p6 = min(p6, minB + minC1 - add)
        loss = min(loss, p6)

        # Pattern 7: net (-1,-1,+2): (e_C - e_A) + (e_C - e_B)
        p7 = minA_C + minB_C
        if outC:
            p7 = min(p7, minA - maxOutC + minB_C)
            p7 = min(p7, minA_C + minB - maxOutC)
        if len(outC) >= 2:
            p7 = min(p7, minA + minB - (outC[0][0]+outC[1][0]))
        loss = min(loss, p7)

        # Pattern 8: net (+1,+1,-2): (e_A - e_C) + (e_B - e_C)
        p8 = INF
        best = INF
        for d1, i1 in candC_A:
            for d2, i2 in candC_B:
                if i1 != i2 and d1+d2 < best:
                    best = d1+d2
        p8 = min(p8, best)
        if outB:
            best = INF
            for d1, i1 in candC_A:
                for vv, i2 in candC_v:
                    if i1 != i2 and d1+vv-maxOutB < best:
                        best = d1+vv-maxOutB
            p8 = min(p8, best)
        if outA:
            best = INF
            for d1, i1 in candC_B:
                for vv, i2 in candC_v:
                    if i1 != i2 and d1+vv-maxOutA < best:
                        best = d1+vv-maxOutA
            p8 = min(p8, best)
        if minC2 != INF:
            add = best_pair_sum_diff(outA, outB)
            if add != NEG:
                p8 = min(p8, minC1+minC2-add)
        loss = min(loss, p8)

        out_lines.append(str(base - loss))
    sys.stdout.write("\n".join(out_lines) + "\n")

solve()