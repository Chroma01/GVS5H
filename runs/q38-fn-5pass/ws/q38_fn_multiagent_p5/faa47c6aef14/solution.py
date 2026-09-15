import sys
from bisect import bisect_left

def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    try:
        N = next(it)
    except StopIteration:
        return

    X = next(it) - 1

    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]

    P = [next(it) - 1 for _ in range(N)]
    invP = [0] * N
    for i, p in enumerate(P):
        invP[p] = i
    del P

    Q = [next(it) - 1 for _ in range(N)]
    invQ = [0] * N
    for i, q in enumerate(Q):
        invQ[q] = i
    del Q

    # distP[v] = number of forward P-steps from v to X, if v is in X's P-cycle.
    distP = [-1] * N
    cur = X
    d = 0
    while distP[cur] == -1:
        distP[cur] = d
        d += 1
        cur = invP[cur]

    # distQ[v] = number of forward Q-steps from v to X, if v is in X's Q-cycle.
    distQ = [-1] * N
    cur = X
    d = 0
    while distQ[cur] == -1:
        distQ[cur] = d
        d += 1
        cur = invQ[cur]

    DR = 0
    for i, a in enumerate(A):
        if a:
            di = distP[i]
            if di == -1:
                print(-1)
                return
            if di > DR:
                DR = di

    DB = 0
    for i, b in enumerate(B):
        if b:
            di = distQ[i]
            if di == -1:
                print(-1)
                return
            if di > DB:
                DB = di

    # Required red chain: farthest occupied red vertex, then next, ..., predecessor of X.
    chainR = []
    cur = X
    for _ in range(DR):
        cur = invP[cur]
        chainR.append(cur)
    chainR.reverse()

    # Required blue chain.
    chainB = []
    cur = X
    for _ in range(DB):
        cur = invQ[cur]
        chainB.append(cur)
    chainB.reverse()

    del A, B, distP, distQ, invP, invQ

    # LCS of two sequences with distinct elements, via LIS.
    if chainR and chainB:
        pos = [-1] * N
        for idx, v in enumerate(chainB):
            pos[v] = idx

        tails = []
        for v in chainR:
            p = pos[v]
            if p != -1:
                j = bisect_left(tails, p)
                if j == len(tails):
                    tails.append(p)
                else:
                    tails[j] = p

        lcs = len(tails)
    else:
        lcs = 0

    print(len(chainR) + len(chainB) - lcs)

if __name__ == "__main__":
    solve()