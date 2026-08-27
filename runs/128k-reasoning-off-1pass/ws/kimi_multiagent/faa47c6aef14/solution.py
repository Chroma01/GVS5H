import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    A = [int(data[idx + i]) for i in range(N)]; idx += N
    B = [int(data[idx + i]) for i in range(N)]; idx += N
    P = [int(data[idx + i]) - 1 for i in range(N)]; idx += N
    Q = [int(data[idx + i]) - 1 for i in range(N)]; idx += N
    X -= 1

    # Build X's cycle in perm, with dist[v] = number of perm-steps to reach X.
    # Returns (cycle list in walk order cyc[k] = perm^k(X), dist array).
    def cycle_info(perm):
        dist = [-1] * N
        cyc = []
        v = X
        while dist[v] == -1:
            dist[v] = 0  # temporary "visited" mark
            cyc.append(v)
            v = perm[v]
        L = len(cyc)
        for k in range(L):
            dist[cyc[k]] = (L - k) % L
        return cyc, dist

    cycP, distP = cycle_info(P)
    Mr = -1
    for i in range(N):
        if A[i]:
            if distP[i] < 0:      # red ball not on X's P-cycle -> can never reach X
                print(-1)
                return
            if distP[i] > Mr:
                Mr = distP[i]
    # Boxes the red balls must pass through, in required firing order (decreasing dist).
    R = [cycP[k] for k in range(len(cycP)) if 1 <= distP[cycP[k]] <= Mr]

    cycQ, distQ = cycle_info(Q)
    Mb = -1
    for i in range(N):
        if B[i]:
            if distQ[i] < 0:      # blue ball not on X's Q-cycle
                print(-1)
                return
            if distQ[i] > Mb:
                Mb = distQ[i]
    Bseq = [cycQ[k] for k in range(len(cycQ)) if 1 <= distQ[cycQ[k]] <= Mb]

    # Answer = |R| + |B| - LCS(R, B). Elements distinct -> LCS = LIS of R-positions in B order.
    rpos = [0] * N
    inR = [False] * N
    for i, b in enumerate(R):
        rpos[b] = i
        inR[b] = True
    tails = []
    for b in Bseq:
        if not inR[b]:
            continue
        p = rpos[b]
        i = bisect_left(tails, p)
        if i == len(tails):
            tails.append(p)
        else:
            tails[i] = p
    print(len(R) + len(Bseq) - len(tails))

main()