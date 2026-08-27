import sys
from bisect import bisect_left


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1] - 1

    idx = 2
    A = data[idx:idx + N]
    idx += N
    B = data[idx:idx + N]
    idx += N

    P = [data[idx + i] - 1 for i in range(N)]
    idx += N
    Q = [data[idx + i] - 1 for i in range(N)]
    idx += N

    del data

    invP = [0] * N
    for i, p in enumerate(P):
        invP[p] = i

    invQ = [0] * N
    for i, q in enumerate(Q):
        invQ[q] = i

    def build_order(inv):
        dist = [-1] * N
        order = []
        cur = X
        d = 0
        while True:
            dist[cur] = d
            order.append(cur)
            cur = inv[cur]
            d += 1
            if cur == X:
                break
        return dist, order

    distP, orderP = build_order(invP)
    distQ, orderQ = build_order(invQ)

    D_R = 0
    for i, a in enumerate(A):
        if a:
            d = distP[i]
            if d == -1:
                print(-1)
                return
            if d > D_R:
                D_R = d

    D_B = 0
    for i, b in enumerate(B):
        if b:
            d = distQ[i]
            if d == -1:
                print(-1)
                return
            if d > D_B:
                D_B = d

    if D_R == 0:
        print(D_B)
        return
    if D_B == 0:
        print(D_R)
        return

    del A, B, P, Q, invP, invQ, distP, distQ

    R = orderP[D_R:0:-1]
    Bchain = orderQ[D_B:0:-1]

    pos = [-1] * N
    for i, v in enumerate(Bchain):
        pos[v] = i

    tails = []
    for v in R:
        p = pos[v]
        if p != -1:
            j = bisect_left(tails, p)
            if j == len(tails):
                tails.append(p)
            else:
                tails[j] = p

    ans = len(R) + len(Bchain) - len(tails)
    print(ans)


if __name__ == "__main__":
    main()