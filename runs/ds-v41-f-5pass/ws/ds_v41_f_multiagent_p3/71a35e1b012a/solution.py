import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1
    M = int(data[ptr]); ptr += 1
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = int(data[ptr]); ptr += 1
        R[i] = int(data[ptr]); ptr += 1

    out = sys.stdout

    # -------- cost 1: an interval equal to [1, N] chosen as op1 --------
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            ops = [0] * M
            ops[i] = 1
            out.write("1\n" + " ".join(map(str, ops)) + "\n")
            return

    # -------- containment: for each i, min-index container j --------
    # j != i, L_j <= L_i, R_j >= R_i  =>  op2 on i, op1 on j covers [1,N].
    # Sort by (L asc, R asc).  Sweep equal-L groups; inside a group process
    # R-batches from largest R to smallest.  Fenwick holds prefix-min over
    # reversed R ranks, i.e. suffix-min over R' >= R.  Query before inserting.
    rvals = sorted(set(R), reverse=True)
    rev = {}
    for rank, v in enumerate(rvals, start=1):
        rev[v] = rank
    size = len(rvals)
    INF = M
    tree = [INF] * (size + 1)

    order = sorted(range(M), key=lambda t: (L[t], R[t]))
    container = [-1] * M

    i = 0
    while i < M:
        Lval = L[order[i]]
        j = i
        while j < M and L[order[j]] == Lval:
            j += 1
        group = order[i:j]              # sorted by R ascending
        idx = len(group) - 1
        while idx >= 0:                 # largest R batch first
            Rval = R[group[idx]]
            batch = []
            while idx >= 0 and R[group[idx]] == Rval:
                batch.append(group[idx])
                idx -= 1
            blen = len(batch)
            s1 = -1; s2 = -1
            if blen >= 2:               # equal (L,R) are mutually containing
                s1 = min(batch)
                s2 = min(x for x in batch if x != s1)
            for t in batch:
                p = rev[R[t]]
                res = INF
                while p > 0:
                    tv = tree[p]
                    if tv < res:
                        res = tv
                    p -= p & -p
                best = res
                if blen >= 2:
                    mb = s2 if t == s1 else s1
                    if mb < best:
                        best = mb
                if best < INF:
                    container[t] = best
            for t in batch:             # insert only after querying whole batch
                p = rev[R[t]]
                while p <= size:
                    if t < tree[p]:
                        tree[p] = t
                    p += p & -p
        i = j

    for t in range(M):
        if container[t] != -1:
            ops = [0] * M
            ops[t] = 2
            ops[container[t]] = 1
            out.write("2\n" + " ".join(map(str, ops)) + "\n")
            return

    # -------- disjoint pair -> two op2 --------
    minR = min(R)
    maxL = max(L)
    if minR < maxL:
        ii = R.index(minR)
        jj = L.index(maxL)              # ii != jj because R_ii >= L_ii
        ops = [0] * M
        ops[ii] = 2
        ops[jj] = 2
        out.write("2\n" + " ".join(map(str, ops)) + "\n")
        return

    # -------- two op1 whose union is [1, N] --------
    a_idx = -1; a_best = -1
    b_idx = -1; b_best = N + 1
    for t in range(M):
        if L[t] == 1 and R[t] > a_best:
            a_best = R[t]; a_idx = t
        if R[t] == N and L[t] < b_best:
            b_best = L[t]; b_idx = t
    if a_idx != -1 and b_idx != -1 and a_idx != b_idx and a_best >= b_best - 1:
        ops = [0] * M
        ops[a_idx] = 1
        ops[b_idx] = 1
        out.write("2\n" + " ".join(map(str, ops)) + "\n")
        return

    # -------- cost 3 (feasible whenever M >= 3) --------
    if M >= 3:
        minL = min(L); maxR2 = max(R)
        cntMinL = 0; cntMaxR = 0
        for t in range(M):
            if L[t] == minL: cntMinL += 1
            if R[t] == maxR2: cntMaxR += 1
        chosen = -1
        for t in range(M):
            if L[t] == minL and cntMinL == 1: continue
            if R[t] == maxR2 and cntMaxR == 1: continue
            chosen = t
            break
        if chosen != -1:
            ci = chosen
            if L[ci] > minL:
                jj = L.index(minL)
            else:
                jj = -1
                for t in range(M):
                    if t != ci and L[t] == minL:
                        jj = t
                        break
            if R[ci] < maxR2:
                kk = R.index(maxR2)
            else:
                kk = -1
                for t in range(M):
                    if t != ci and R[t] == maxR2:
                        kk = t
                        break
            ops = [0] * M
            ops[ci] = 2
            ops[jj] = 1
            ops[kk] = 1
            out.write("3\n" + " ".join(map(str, ops)) + "\n")
            return

    out.write("-1\n")

main()