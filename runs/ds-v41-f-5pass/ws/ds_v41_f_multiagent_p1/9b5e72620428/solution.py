import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]

    cntA = {}
    cntB = {}
    wA = wB = 0
    maxA = maxB = -1
    for tok in A:
        v = int(tok)
        if v == -1:
            wA += 1
        else:
            cntA[v] = cntA.get(v, 0) + 1
            if v > maxA:
                maxA = v
    for tok in B:
        v = int(tok)
        if v == -1:
            wB += 1
        else:
            cntB[v] = cntB.get(v, 0) + 1
            if v > maxB:
                maxB = v

    nA = n - wA          # number of fixed A entries
    nB = n - wB          # number of fixed B entries
    needed = nA + nB - n # minimum number of fixed A-fixed B matches required

    # If there are enough wildcards overall, we can avoid all fixed-fixed
    # matches (x = 0 >= needed), so any sufficiently large S works.
    if needed <= 0:
        print("Yes")
        return

    # needed > 0 implies both cntA and cntB are non-empty, so maxA,maxB >= 0.
    lower = maxA if maxA > maxB else maxB

    itemsA = list(cntA.items())
    itemsB = list(cntB.items())
    itemsB.sort()
    us = [u for u, _ in itemsB]

    C = {}
    get = C.get
    for v, ca in itemsA:
        th = lower - v
        idx = bisect_left(us, th)          # only u with v+u >= lower matter
        for j in range(idx, len(us)):
            u, cb = itemsB[j]
            add = ca if ca < cb else cb
            s = v + u
            c = get(s, 0) + add
            if c >= needed:
                print("Yes")
                return
            C[s] = c

    print("No")

main()