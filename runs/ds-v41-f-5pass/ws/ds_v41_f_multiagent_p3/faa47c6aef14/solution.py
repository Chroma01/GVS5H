import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    x = int(next(it)) - 1
    A = [int(next(it)) for _ in range(n)]
    B = [int(next(it)) for _ in range(n)]
    P = [int(next(it)) - 1 for _ in range(n)]
    Q = [int(next(it)) - 1 for _ in range(n)]

    def cycle_info(perm, target):
        # returns (dist array, traversal list starting at target, cycle length)
        dist = [-1] * n
        trav = []
        v = target
        while dist[v] == -1:
            dist[v] = len(trav)   # temporarily store position
            trav.append(v)
            v = perm[v]
        L = len(trav)
        d = [-1] * n
        for i, node in enumerate(trav):
            d[node] = (L - i) % L  # steps to reach target following perm
        return d, trav, L

    dP, travP, LP = cycle_info(P, x)
    dQ, travQ, LQ = cycle_info(Q, x)

    # farthest red ball
    dred = 0
    for i in range(n):
        if A[i]:
            di = dP[i]
            if di == -1:
                print(-1); return
            if di > dred:
                dred = di

    # farthest blue ball
    dblue = 0
    for i in range(n):
        if B[i]:
            di = dQ[i]
            if di == -1:
                print(-1); return
            if di > dblue:
                dblue = di

    # required red chain: nodes at P-distance dred, dred-1, ..., 1
    R = travP[LP - dred:] if dred > 0 else []
    # required blue chain: nodes at Q-distance dblue, ..., 1
    Bl = travQ[LQ - dblue:] if dblue > 0 else []

    # LCS(R, Bl) via LIS after mapping Bl nodes to their index in R
    pos_of = {node: j for j, node in enumerate(R)}
    tails = []
    for node in Bl:
        j = pos_of.get(node)
        if j is None:
            continue
        p = bisect_left(tails, j)
        if p == len(tails):
            tails.append(j)
        else:
            tails[p] = j
    lcs = len(tails)

    print(dred + dblue - lcs)

main()