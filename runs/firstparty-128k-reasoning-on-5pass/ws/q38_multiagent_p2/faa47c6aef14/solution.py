import sys
from bisect import bisect_left


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    try:
        n = next(it)
    except StopIteration:
        return
    x = next(it) - 1

    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    inv_p = [0] * n
    for i, v in enumerate(p):
        inv_p[v] = i

    inv_q = [0] * n
    for i, v in enumerate(q):
        inv_q[v] = i

    def required(inv, balls):
        dist = [-1] * n
        dist[x] = 0
        cur = inv[x]
        d = 1
        while cur != x:
            dist[cur] = d
            cur = inv[cur]
            d += 1

        m = 0
        for i, v in enumerate(balls):
            if v:
                di = dist[i]
                if di == -1:
                    return None
                if di > m:
                    m = di

        seq = []
        cur = x
        for _ in range(m):
            cur = inv[cur]
            seq.append(cur)
        seq.reverse()
        return m, seq

    red = required(inv_p, a)
    if red is None:
        print(-1)
        return
    mr, rseq = red

    blue = required(inv_q, b)
    if blue is None:
        print(-1)
        return
    mb, bseq = blue

    if rseq and bseq:
        pos = [-1] * n
        for i, v in enumerate(bseq):
            pos[v] = i

        tails = []
        for v in rseq:
            ppos = pos[v]
            if ppos != -1:
                j = bisect_left(tails, ppos)
                if j == len(tails):
                    tails.append(ppos)
                else:
                    tails[j] = ppos
        lcs = len(tails)
    else:
        lcs = 0

    print(mr + mb - lcs)


if __name__ == "__main__":
    solve()