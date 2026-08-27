import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    A = [int(x) for x in data[idx:idx+N]]; idx += N
    B = [int(x) for x in data[idx:idx+N]]; idx += N
    P = [int(x) for x in data[idx:idx+N]]; idx += N
    Q = [int(x) for x in data[idx:idx+N]]; idx += N

    # Build cycle walk containing X for a permutation perm.
    # Returns (walk, dist) where walk[0]=X, walk[j+1]=perm[walk[j]],
    # dist[v] = number of applications of perm to reach X (only for v on this cycle; else -1).
    def cycle_info(perm):
        walk = []
        dist = [-1] * (N + 1)
        cur = X
        while dist[cur] == -1:
            dist[cur] = 0  # temporary mark "on cycle"
            walk.append(cur)
            cur = perm[cur - 1]
        L = len(walk)
        for j, v in enumerate(walk):
            dist[v] = (L - j) % L  # dist(X)=0, dist(perm^{-1}(X))=1, ...
        return walk, dist

    walkP, distP = cycle_info(P)
    walkQ, distQ = cycle_info(Q)

    # Feasibility: every red ball on X's P-cycle, every blue ball on X's Q-cycle.
    R = 0
    for i in range(1, N + 1):
        if A[i - 1]:
            if distP[i] == -1:
                print(-1)
                return
            if distP[i] > R:
                R = distP[i]
    Bm = 0
    for i in range(1, N + 1):
        if B[i - 1]:
            if distQ[i] == -1:
                print(-1)
                return
            if distQ[i] > Bm:
                Bm = distQ[i]

    # seqP: boxes visited by red batch, from farthest red ball (dist R) down to dist 1.
    # Node with dist d is walkP[(L - d) % L]; so seqP = walkP[L-R .. L-1].
    LP = len(walkP)
    seqP = walkP[LP - R:] if R > 0 else []
    LQ = len(walkQ)
    seqQ = walkQ[LQ - Bm:] if Bm > 0 else []

    # LCS of two sequences with all-distinct elements via LIS reduction.
    posQ = {v: i for i, v in enumerate(seqQ)}
    mapped = [posQ[v] for v in seqP if v in posQ]
    # LIS (strictly increasing) via patience sorting.
    tails = []
    for x in mapped:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    lcs = len(tails)

    print(R + Bm - lcs)

main()