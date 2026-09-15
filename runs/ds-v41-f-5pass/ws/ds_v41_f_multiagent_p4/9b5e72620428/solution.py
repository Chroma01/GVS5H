import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    Araw = data[1:1 + n]
    Braw = data[1 + n:1 + 2 * n]

    cntA = {}
    cntB = {}
    u = 0          # number of A_i == -1
    p = 0          # number of known B values
    maxA = -1
    maxB = -1

    for tok in Araw:
        x = int(tok)
        if x == -1:
            u += 1
        else:
            cntA[x] = cntA.get(x, 0) + 1
            if x > maxA:
                maxA = x

    for tok in Braw:
        x = int(tok)
        if x == -1:
            continue
        cntB[x] = cntB.get(x, 0) + 1
        p += 1
        if x > maxB:
            maxB = x

    # If we have at least as many A-wildcards as known B entries,
    # choose S = L, put wildcards on every known-B position.
    if u >= p:
        sys.stdout.write("Yes\n")
        return

    need = p - u                      # known-A values that must hit known-B
    L = maxA if maxA > maxB else maxB  # S must be >= this

    Alist = list(cntA.items())
    Bs = sorted(cntB.items())          # distinct known B values, ascending
    m = len(Bs)
    bvals = [t[0] for t in Bs]
    cbvals = [t[1] for t in Bs]

    # suffix maximum of counts, for the cheap "single pair is enough" test
    sufmax = [0] * (m + 1)
    for i in range(m - 1, -1, -1):
        v = cbvals[i]
        sufmax[i] = v if v > sufmax[i + 1] else sufmax[i + 1]

    # accumulate coverage(S) = sum_a min(cntA[a], cntB[S-a])
    d = {}
    dget = d.get
    for a, ca in Alist:
        start = bisect_left(bvals, L - a)   # only S = a + b with S >= L
        # one distinct pair already supplies >= need matches
        if start < m and ca >= need and sufmax[start] >= need:
            sys.stdout.write("Yes\n")
            return
        for idx in range(start, m):
            cb = cbvals[idx]
            v = ca if ca < cb else cb
            S = a + bvals[idx]
            cur = dget(S, 0) + v
            if cur >= need:
                sys.stdout.write("Yes\n")
                return
            d[S] = cur

    sys.stdout.write("No\n")


main()