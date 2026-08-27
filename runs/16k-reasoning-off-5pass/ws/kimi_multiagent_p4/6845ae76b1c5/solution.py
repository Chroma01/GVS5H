import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    A = data[p:p+N]; p += N
    B = data[p:p+N]; p += N
    K = data[p]; p += 1
    Xs = [0]*K
    Ys = [0]*K
    for q in range(K):
        Xs[q] = data[p]; Ys[q] = data[p+1]; p += 2

    SA = [0]*(N+1)
    SB = [0]*(N+1)
    for i in range(N):
        SA[i+1] = SA[i] + A[i]
        SB[i+1] = SB[i] + B[i]

    # answer(X,Y) = Y*SA[X] - X*SB[Y] + 2*T(X,Y)
    # T(X,Y) = sum_{i<=X} sum_{j<=Y, A_i <= B_j} (B_j - A_i)
    T = [0]*K

    # CDQ on A-index. Queries positioned at X. At node [l,r], mid=(l+r)/2:
    # queries with X<=mid go left, X>mid go right. Cross contribution for
    # right queries: sum_{j<=Y} sum_{left i, A_i<=B_j} (B_j - A_i).
    # Per node: sort left A values + prefix sums; sort right queries by Y;
    # sweep j upward maintaining G; adding B_j=b updates G += b*cntLE(b)-sumLE(b).

    # Iterative CDQ: process nodes level by level to limit memory.
    # Each item: (l, r, qids list). We split qids down the recursion.
    # To bound total work, skip nodes with no right queries.

    sys.setrecursionlimit(1 << 20)

    A_l = A
    B_l = B
    T_l = T
    X_l = Xs
    Y_l = Ys
    bl = bisect_left

    def cdq(l, r, qids):
        if l >= r or not qids:
            return
        mid = (l + r) >> 1
        lq = []
        rq = []
        for q in qids:
            if X_l[q] <= mid:
                lq.append(q)
            else:
                rq.append(q)
        cdq(l, mid, lq)
        cdq(mid + 1, r, rq)
        if not rq:
            return
        vals = sorted(A_l[i] for i in range(l - 1, mid))
        pref = [0]*(len(vals) + 1)
        s = 0
        for i, v in enumerate(vals):
            s += v
            pref[i+1] = s
        rq.sort(key=lambda q: Y_l[q])
        G = 0
        j = 0
        for q in rq:
            Y = Y_l[q]
            while j < Y:
                b = B_l[j]; j += 1
                t = bl(vals, b + 1)   # count of left A <= b
                G += b * t - pref[t]
            T_l[q] += G

    cdq(1, N, list(range(K)))

    out = []
    for q in range(K):
        X = Xs[q]; Y = Ys[q]
        out.append(str(Y*SA[X] - X*SB[Y] + 2*T[q]))
    sys.stdout.write("\n".join(out) + "\n")

main()