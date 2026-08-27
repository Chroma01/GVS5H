import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]) - 1; idx += 1
    A = [int(data[idx + i]) for i in range(N)]; idx += N
    B = [int(data[idx + i]) for i in range(N)]; idx += N
    P = [int(data[idx + i]) - 1 for i in range(N)]; idx += N
    Q = [int(data[idx + i]) - 1 for i in range(N)]; idx += N

    def dist_to_X(perm):
        # dist[v] = number of applications of perm to reach X, only on X's cycle
        inv = [0] * N
        for i in range(N):
            inv[perm[i]] = i
        dist = [-1] * N
        dist[X] = 0
        cur = inv[X]
        d = 1
        while cur != X:
            dist[cur] = d
            d += 1
            cur = inv[cur]
        return dist

    distP = dist_to_X(P)
    distQ = dist_to_X(Q)

    maxRed = 0
    for v in range(N):
        if A[v]:
            if distP[v] == -1:
                print(-1)
                return
            if distP[v] > maxRed:
                maxRed = distP[v]

    maxBlue = 0
    for v in range(N):
        if B[v]:
            if distQ[v] == -1:
                print(-1)
                return
            if distQ[v] > maxBlue:
                maxBlue = distQ[v]

    ans = 0
    for u in range(N):
        if (0 < distP[u] <= maxRed) or (0 < distQ[u] <= maxBlue):
            ans += 1
    print(ans)

solve()