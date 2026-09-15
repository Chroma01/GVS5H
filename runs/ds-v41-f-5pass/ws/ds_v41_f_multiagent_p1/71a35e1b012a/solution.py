import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); m = int(data[1])
    L = [0] * m
    R = [0] * m
    ptr = 2
    for i in range(m):
        L[i] = int(data[ptr]); R[i] = int(data[ptr + 1]); ptr += 2

    op = [0] * m

    # ---- cost 1: some interval equals [1, N], used as op1 ----
    for i in range(m):
        if L[i] == 1 and R[i] == n:
            op[i] = 1
            sys.stdout.write("1\n" + " ".join(map(str, op)) + "\n")
            return

    found = False

    # ---- cost 2, case A (tried FIRST): op1 interval pi contains op2 interval q ----
    # contains[i] iff exists j != i with L_j >= L_i and R_j <= R_i
    order = sorted(range(m), key=lambda i: L[i], reverse=True)
    contains = bytearray(m)
    minR = n + 1
    cnt = 0
    j = 0
    while j < m:
        k = j
        lv = L[order[j]]
        while k < m and L[order[k]] == lv:
            k += 1
        # merge the whole equal-L group before evaluating its members
        for t in range(j, k):
            ri = R[order[t]]
            if ri < minR:
                minR = ri; cnt = 1
            elif ri == minR:
                cnt += 1
        for t in range(j, k):
            i = order[t]
            if R[i] > minR or (R[i] == minR and cnt >= 2):
                contains[i] = 1
        j = k

    pi = -1
    for i in range(m):
        if contains[i]:
            pi = i
            break
    if pi != -1:
        Lp = L[pi]; Rp = R[pi]
        for i in range(m):
            if i != pi and L[i] >= Lp and R[i] <= Rp:
                op[pi] = 1; op[i] = 2
                found = True
                break

    # ---- cost 2, case B: two op1 whose union is [1, N] ----
    if not found:
        a = -1; bestR1 = -1
        for i in range(m):
            if L[i] == 1 and R[i] > bestR1:
                bestR1 = R[i]; a = i
        b = -1; bestLN = n + 1
        for i in range(m):
            if R[i] == n and L[i] < bestLN:
                bestLN = L[i]; b = i
        if a != -1 and b != -1 and a != b and bestR1 + 1 >= bestLN:
            op[a] = 1; op[b] = 1
            found = True

    # ---- cost 2, case C: two disjoint op2 intervals ----
    if not found:
        p2 = 0
        for i in range(1, m):
            if R[i] < R[p2]:
                p2 = i
        q2 = 0
        for i in range(1, m):
            if L[i] > L[q2]:
                q2 = i
        if p2 != q2 and R[p2] < L[q2]:
            op[p2] = 2; op[q2] = 2
            found = True

    if found:
        sys.stdout.write("2\n" + " ".join(map(str, op)) + "\n")
        return

    # ---- cost 3 (only reachable when M >= 3) ----
    if m >= 3:
        ista = 0
        for i in range(1, m):
            if L[i] > L[ista]:
                ista = i
        jsta = 0
        for i in range(1, m):
            if R[i] < R[jsta]:
                jsta = i
        kk = -1
        for t in range(m):
            if t != ista and t != jsta:
                kk = t
                break
        op[ista] = 2; op[jsta] = 2; op[kk] = 1
        sys.stdout.write("3\n" + " ".join(map(str, op)) + "\n")
        return

    sys.stdout.write("-1\n")

main()