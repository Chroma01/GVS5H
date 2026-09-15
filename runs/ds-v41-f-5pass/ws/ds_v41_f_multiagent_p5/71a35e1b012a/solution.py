import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = int(data[pos]); pos += 1
        R[i] = int(data[pos]); pos += 1

    ops = [0] * M
    out = sys.stdout

    def output(k, pairs):
        for idx, o in pairs:
            ops[idx] = o
        out.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # ---- cost 1: an interval exactly [1, N] taken as type-1 (first check) ----
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            output(1, [(i, 1)])
            return

    # ---- cost 2 (c): containment, input-order scan with two prefix-max Fenwick trees ----
    # tree1: index R -> max L among seen indices
    # tree2: index L -> max R among seen indices
    tree1 = [-1] * (N + 1)
    tree2 = [-1] * (N + 1)

    found_i = -1
    found_type = 0
    for i in range(M):
        # condition1: exists prev j with R_j <= R_i and L_j >= L_i  => interval_j subset interval_i
        p = R[i]
        m = -1
        while p > 0:
            v = tree1[p]
            if v > m:
                m = v
            p -= p & (-p)
        if m >= L[i]:
            found_i = i; found_type = 1; break
        # condition2: exists prev j with L_j <= L_i and R_j >= R_i  => interval_i subset interval_j
        p = L[i]
        m = -1
        while p > 0:
            v = tree2[p]
            if v > m:
                m = v
            p -= p & (-p)
        if m >= R[i]:
            found_i = i; found_type = 2; break
        # insert i into both trees
        p = R[i]
        lv = L[i]
        while p <= N:
            if tree1[p] < lv:
                tree1[p] = lv
            p += p & (-p)
        p = L[i]
        rv = R[i]
        while p <= N:
            if tree2[p] < rv:
                tree2[p] = rv
            p += p & (-p)

    if found_i != -1:
        Li = L[found_i]; Ri = R[found_i]
        j = -1
        if found_type == 1:
            for t in range(found_i):
                if R[t] <= Ri and L[t] >= Li:
                    j = t; break
            output(2, [(found_i, 1), (j, 2)])
            return
        else:
            for t in range(found_i):
                if L[t] <= Li and R[t] >= Ri:
                    j = t; break
            output(2, [(found_i, 2), (j, 1)])
            return

    # ---- cost 2 (a): two type-1 intervals whose union is [1, N] ----
    maxR = -1; argMaxR = -1
    minL = N + 1; argMinL = -1
    for i in range(M):
        if L[i] == 1 and R[i] > maxR:
            maxR = R[i]; argMaxR = i
        if R[i] == N and L[i] < minL:
            minL = L[i]; argMinL = i
    if argMaxR != -1 and argMinL != -1 and argMaxR != argMinL and maxR + 1 >= minL:
        output(2, [(argMaxR, 1), (argMinL, 1)])
        return

    # ---- cost 2 (b): two disjoint type-2 intervals ----
    minR = N + 1; argMinR = -1
    maxL = -1; argMaxL = -1
    for i in range(M):
        if R[i] < minR:
            minR = R[i]; argMinR = i
        if L[i] > maxL:
            maxL = L[i]; argMaxL = i
    if minR < maxL:  # forces argMinR != argMaxL
        output(2, [(argMinR, 2), (argMaxL, 2)])
        return

    # ---- cost 3: always achievable when M >= 3 ----
    if M >= 3:
        A = argMaxL
        B = argMinR
        if A != B:
            for c in range(M):
                if c != A and c != B:
                    output(3, [(A, 2), (B, 2), (c, 1)])
                    return
        else:
            D = -1
            for d in range(M):
                if d != A:
                    D = d
                    break
            for c in range(M):
                if c != A and c != D:
                    output(3, [(A, 2), (D, 2), (c, 1)])
                    return

    out.write("-1\n")

main()