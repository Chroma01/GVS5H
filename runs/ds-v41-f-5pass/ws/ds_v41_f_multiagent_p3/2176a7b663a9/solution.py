import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1
    W = [0] * (N + 1)
    for i in range(1, N + 1):
        W[i] = int(data[ptr]); ptr += 1
    L = [0] * (N + 1)
    R = [0] * (N + 1)
    for i in range(1, N + 1):
        L[i] = int(data[ptr]); ptr += 1
        R[i] = int(data[ptr]); ptr += 1

    INF = float('inf')

    # prefix minimum of W over intervals sorted by R
    orderR = sorted(range(1, N + 1), key=R.__getitem__)
    Rs = [R[i] for i in orderR]
    prefMin = [0] * N
    cur = INF
    for pos in range(N):
        w = W[orderR[pos]]
        if w < cur:
            cur = w
        prefMin[pos] = cur

    # suffix minimum of W over intervals sorted by L
    orderL = sorted(range(1, N + 1), key=L.__getitem__)
    Ls = [L[i] for i in orderL]
    suffMin = [0] * N
    cur = INF
    for pos in range(N - 1, -1, -1):
        w = W[orderL[pos]]
        if w < cur:
            cur = w
        suffMin[pos] = cur

    Q = int(data[ptr]); ptr += 1
    out = []
    for _ in range(Q):
        s = int(data[ptr]); ptr += 1
        t = int(data[ptr]); ptr += 1

        # direct edge: intervals disjoint
        if R[s] < L[t] or R[t] < L[s]:
            out.append(str(W[s] + W[t]))
            continue

        base = W[s] + W[t]
        best = INF

        # common neighbour left of both s and t : R_k < min(L_s, L_t)
        x = L[s] if L[s] < L[t] else L[t]
        c = bisect_left(Rs, x)
        if c > 0 and prefMin[c - 1] < best:
            best = prefMin[c - 1]

        # common neighbour right of both s and t : L_k > max(R_s, R_t)
        x = R[s] if R[s] > R[t] else R[t]
        c = bisect_right(Ls, x)
        if c < N and suffMin[c] < best:
            best = suffMin[c]

        # cross: a left of s (R_a < L_s), b right of t (L_b > R_t)
        c1 = bisect_left(Rs, L[s])
        c2 = bisect_right(Ls, R[t])
        if c1 > 0 and c2 < N:
            val = prefMin[c1 - 1] + suffMin[c2]
            if val < best:
                best = val

        # cross: a right of s (L_a > R_s), b left of t (R_b < L_t)
        c1 = bisect_right(Ls, R[s])
        c2 = bisect_left(Rs, L[t])
        if c1 < N and c2 > 0:
            val = suffMin[c1] + prefMin[c2 - 1]
            if val < best:
                best = val

        if best < INF:
            out.append(str(base + best))
        else:
            out.append("-1")

    sys.stdout.write("\n".join(out) + "\n")

main()