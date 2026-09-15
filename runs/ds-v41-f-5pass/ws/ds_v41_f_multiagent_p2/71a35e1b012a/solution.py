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

    ans = [0] * M
    write = sys.stdout.write

    def emit(k):
        write(str(k) + "\n")
        write(" ".join(map(str, ans)) + "\n")

    # cost 1: an operation exactly [1, N]
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            ans[i] = 1
            emit(1)
            return

    maxL = max(L)
    minR = min(R)

    # non-common intersection: the max-L and min-R ops have empty intersection,
    # their complements already cover everything.
    if maxL > minR:
        p = L.index(maxL)
        q = R.index(minR)
        ans[p] = 2
        ans[q] = 2
        emit(2)
        return

    # common intersection: containment check (s contains t: s type-1, t type-2)
    # prefix max of R over points with L <= L[t]
    maxRbyL = {}
    for i in range(M):
        l = L[i]; r = R[i]
        v = maxRbyL.get(l)
        if v is None or r > v:
            maxRbyL[l] = r
    pref = {}
    cur = 0
    for k in sorted(maxRbyL):
        v = maxRbyL[k]
        if v > cur:
            cur = v
        pref[k] = cur

    # two smallest L values per R (to detect a duplicate-rank partner)
    min1 = {}
    min2 = {}
    for i in range(M):
        r = R[i]; l = L[i]
        a = min1.get(r)
        if a is None:
            min1[r] = l
        elif l < a:
            min2[r] = a
            min1[r] = l
        else:
            b = min2.get(r)
            if b is None or l < b:
                min2[r] = l

    INF = N + M + 1
    found_t = -1
    for t in range(M):
        if pref[L[t]] > R[t] or min2.get(R[t], INF) <= L[t]:
            found_t = t
            break

    if found_t != -1:
        t = found_t
        Lt = L[t]; Rt = R[t]
        best_j = -1
        for j in range(M):
            if j != t and L[j] <= Lt and R[j] >= Rt:
                best_j = j
                break
        if best_j != -1:
            ans[best_j] = 1
            ans[t] = 2
            emit(2)
            return

    # cost 2 via two type-1 ops covering [1, N]
    bestA = -1; bestA_R = -1
    for i in range(M):
        if L[i] == 1 and R[i] > bestA_R:
            bestA_R = R[i]; bestA = i
    bestB = -1; bestB_L = N + 1
    for i in range(M):
        if R[i] == N and L[i] < bestB_L:
            bestB_L = L[i]; bestB = i
    if bestA != -1 and bestB != -1 and bestA != bestB and bestB_L <= bestA_R + 1:
        ans[bestA] = 1
        ans[bestB] = 1
        emit(2)
        return

    # cost 3: max-L and min-R as type-2, any other op as type-1
    if M >= 3:
        p = L.index(maxL)
        q = R.index(minR)
        r = -1
        for i in range(M):
            if i != p and i != q:
                r = i
                break
        ans[p] = 2
        ans[q] = 2
        ans[r] = 1
        emit(3)
        return

    write("-1\n")

main()