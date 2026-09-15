import sys
import bisect

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    X = next(it) - 1
    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]
    P = [next(it) - 1 for _ in range(N)]
    Q = [next(it) - 1 for _ in range(N)]

    invP = [0] * N
    for i, p in enumerate(P):
        invP[p] = i
    invQ = [0] * N
    for i, q in enumerate(Q):
        invQ[q] = i

    # distances along P from each box to X
    distP = [-1] * N
    atDistP = []
    cur = X
    d = 0
    while distP[cur] == -1:
        distP[cur] = d
        atDistP.append(cur)
        cur = invP[cur]
        d += 1

    # distances along Q from each box to X
    distQ = [-1] * N
    atDistQ = []
    cur = X
    d = 0
    while distQ[cur] == -1:
        distQ[cur] = d
        atDistQ.append(cur)
        cur = invQ[cur]
        d += 1

    M_R = 0
    for i in range(N):
        if A[i] == 1:
            if distP[i] == -1:
                print(-1)
                return
            if distP[i] > M_R:
                M_R = distP[i]

    M_B = 0
    for i in range(N):
        if B[i] == 1:
            if distQ[i] == -1:
                print(-1)
                return
            if distQ[i] > M_B:
                M_B = distQ[i]

    # required operation sequences (decreasing distance to X)
    R = [atDistP[d] for d in range(M_R, 0, -1)]
    Bseq = [atDistQ[d] for d in range(M_B, 0, -1)]

    # LCS of R and Bseq via LIS on mapped positions
    posR = [-1] * N
    for idx, box in enumerate(R):
        posR[box] = idx

    L = []
    for box in Bseq:
        p = posR[box]
        if p != -1:
            L.append(p)

    tails = []
    for x in L:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    lcs = len(tails)

    ans = len(R) + len(Bseq) - lcs
    print(ans)

if __name__ == "__main__":
    solve()