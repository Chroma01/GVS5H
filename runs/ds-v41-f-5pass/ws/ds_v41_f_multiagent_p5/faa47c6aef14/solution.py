import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    x = int(data[idx]) - 1; idx += 1
    A = [int(v) for v in data[idx:idx + n]]; idx += n
    B = [int(v) for v in data[idx:idx + n]]; idx += n
    P = [int(v) - 1 for v in data[idx:idx + n]]; idx += n
    Q = [int(v) - 1 for v in data[idx:idx + n]]; idx += n

    def cycle_dist(perm):
        # nodes on X's cycle, in order following perm starting from X
        cyc = []
        cur = x
        while True:
            cyc.append(cur)
            cur = perm[cur]
            if cur == x:
                break
        L = len(cyc)
        dist = [-1] * n
        for k, v in enumerate(cyc):
            dist[v] = (L - k) % L   # steps from v to X along perm
        return dist

    distR = cycle_dist(P)
    distB = cycle_dist(Q)

    # every red ball must lie on X's red-cycle; likewise for blue
    DR = 0
    for i in range(n):
        if A[i]:
            d = distR[i]
            if d == -1:
                print(-1)
                return
            if d > DR:
                DR = d
    DB = 0
    for i in range(n):
        if B[i]:
            d = distB[i]
            if d == -1:
                print(-1)
                return
            if d > DB:
                DB = d

    # required boxes: red 1..DR, blue 1..DB.
    # Box can be served by one operation iff red & blue orders agree (chain).
    pairs = []
    for i in range(n):
        dr = distR[i]
        db = distB[i]
        if 1 <= dr <= DR and 1 <= db <= DB:
            pairs.append((dr, db))
    pairs.sort()

    # longest strictly increasing subsequence of db (patience sorting)
    lis = []
    for _, db in pairs:
        pos = bisect_left(lis, db)
        if pos == len(lis):
            lis.append(db)
        else:
            lis[pos] = db

    print(DR + DB - len(lis))


main()