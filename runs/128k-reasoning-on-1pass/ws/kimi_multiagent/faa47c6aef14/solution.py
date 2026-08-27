import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]) - 1; idx += 1
    A = [int(x) for x in data[idx:idx+N]]; idx += N
    B = [int(x) for x in data[idx:idx+N]]; idx += N
    P = [int(x) - 1 for x in data[idx:idx+N]]; idx += N
    Q = [int(x) - 1 for x in data[idx:idx+N]]; idx += N

    # dist[v] = number of F-applications to reach X, -1 if X not in v's cycle
    def compute_dist(F):
        dist = [-1] * N
        cyc = [X]
        v = F[X]
        while v != X:
            cyc.append(v)
            v = F[v]
        k = len(cyc)
        for j, node in enumerate(cyc):
            dist[node] = (k - j) % k
        return dist

    distP = compute_dist(P)
    distQ = compute_dist(Q)

    # Build chain of boxes that must be operated (farthest ball -> X, excluding X)
    # Returns None if some ball can never reach X.
    def build_chain(balls, dist, F):
        start = -1
        best = -1
        for i in range(N):
            if balls[i]:
                if dist[i] < 0:
                    return None
                if dist[i] > best:
                    best = dist[i]
                    start = i
        chain = []
        if start != -1:
            v = start
            while v != X:
                chain.append(v)
                v = F[v]
        return chain

    R = build_chain(A, distP, P)
    if R is None:
        print(-1)
        return
    Bc = build_chain(B, distQ, Q)
    if Bc is None:
        print(-1)
        return

    # LCS of the two chains via LIS on mapped positions (vertices are distinct)
    pos = {v: i for i, v in enumerate(Bc)}
    seq = [pos[v] for v in R if v in pos]
    tails = []
    for x in seq:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    lcs = len(tails)

    print(len(R) + len(Bc) - lcs)

main()