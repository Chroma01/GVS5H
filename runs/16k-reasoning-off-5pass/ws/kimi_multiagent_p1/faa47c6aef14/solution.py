import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]) - 1; idx += 1
    A = [int(x) for x in data[idx:idx + N]]; idx += N
    B = [int(x) for x in data[idx:idx + N]]; idx += N
    P = [int(x) - 1 for x in data[idx:idx + N]]; idx += N
    Q = [int(x) - 1 for x in data[idx:idx + N]]; idx += N

    def compute(perm, balls):
        # Walk X's cycle in the permutation, assign distances to X.
        dist = [-1] * N
        cyc = []
        v = X
        while True:
            cyc.append(v)
            v = perm[v]
            if v == X:
                break
        L = len(cyc)
        for j, node in enumerate(cyc):
            dist[node] = (L - j) % L
        # Feasibility + furthest ball distance.
        D = 0
        for i in range(N):
            if balls[i]:
                if dist[i] == -1:
                    return None  # ball can never reach X
                if dist[i] > D:
                    D = dist[i]
        # Required chain: boxes at distances D, D-1, ..., 1 (in this order).
        chain = [cyc[(L - d) % L] for d in range(D, 0, -1)]
        return D, chain

    red = compute(P, A)
    if red is None:
        print(-1)
        return
    blue = compute(Q, B)
    if blue is None:
        print(-1)
        return
    D_r, R = red
    D_b, Bc = blue

    # LCS of the two chains (both have distinct elements) via LIS.
    pos_in_B = {}
    for j, u in enumerate(Bc):
        pos_in_B[u] = j
    seq = [pos_in_B[u] for u in R if u in pos_in_B]
    tails = []
    for x in seq:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    lcs = len(tails)

    print(D_r + D_b - lcs)

main()