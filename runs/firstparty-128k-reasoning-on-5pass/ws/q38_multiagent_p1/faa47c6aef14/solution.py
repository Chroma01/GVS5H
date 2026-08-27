import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x = data[1] - 1
    off = 2

    A = data[off:off + n]
    off += n
    B = data[off:off + n]
    off += n
    P = [v - 1 for v in data[off:off + n]]
    off += n
    Q = [v - 1 for v in data[off:off + n]]
    off += n

    del data

    invP = [0] * n
    for i, v in enumerate(P):
        invP[v] = i

    invQ = [0] * n
    for i, v in enumerate(Q):
        invQ[v] = i

    def build(inv):
        dist = [-1] * n
        order = [x]
        dist[x] = 0
        cur = x
        while True:
            cur = inv[cur]
            if cur == x:
                break
            dist[cur] = len(order)
            order.append(cur)
        return dist, order

    distP, orderP = build(invP)
    distQ, orderQ = build(invQ)

    max_r = 0
    for i, a in enumerate(A):
        if a:
            d = distP[i]
            if d == -1:
                print(-1)
                return
            if d > max_r:
                max_r = d

    max_b = 0
    for i, b in enumerate(B):
        if b:
            d = distQ[i]
            if d == -1:
                print(-1)
                return
            if d > max_b:
                max_b = d

    red_chain = orderP[max_r:0:-1]
    blue_chain = orderQ[max_b:0:-1]

    pos = [-1] * n
    for i, v in enumerate(red_chain):
        pos[v] = i

    tails = []
    for v in blue_chain:
        p = pos[v]
        if p != -1:
            j = bisect_left(tails, p)
            if j == len(tails):
                tails.append(p)
            else:
                tails[j] = p

    print(len(red_chain) + len(blue_chain) - len(tails))

if __name__ == "__main__":
    main()