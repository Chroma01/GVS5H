import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    toks = data[1:1 + 2 * n]

    fixedA = []
    wA = 0
    fixedB = []
    wB = 0

    for i in range(n):
        x = int(toks[i])
        if x == -1:
            wA += 1
        else:
            fixedA.append(x)
    for i in range(n, 2 * n):
        x = int(toks[i])
        if x == -1:
            wB += 1
        else:
            fixedB.append(x)

    mB = len(fixedB)  # number of fixed B entries

    # If wildcards in A can cover every fixed B position, always possible with T = L.
    if wA >= mB:
        print("Yes")
        return

    R = mB - wA  # > 0 : fixed B demands that must be met by fixed A matches

    L = 0
    if fixedA:
        L = max(L, max(fixedA))
    if fixedB:
        L = max(L, max(fixedB))

    # With R == 1 the pair (max fixed A, max fixed B) already has sum >= L
    # and each count >= 1, so S(T) >= 1.
    if R == 1:
        print("Yes")
        return

    from collections import Counter
    cA = Counter(fixedA)
    cB = Counter(fixedB)
    listA = sorted(cA.items())  # (value, count) ascending
    listB = sorted(cB.items())

    # Fast vectorized path if numpy is available.
    try:
        import numpy as np
        av = np.array([a for a, _ in listA], dtype=np.int64)
        cav = np.array([c for _, c in listA], dtype=np.int64)
        bv = np.array([b for b, _ in listB], dtype=np.int64)
        cbv = np.array([c for _, c in listB], dtype=np.int64)

        sums = av[:, None] + bv[None, :]
        mins = np.minimum(cav[:, None], cbv[None, :])
        fs = sums.ravel()
        fm = mins.ravel()
        sel = fs >= L
        fs = fs[sel]
        fm = fm[sel]
        if fs.size == 0:
            print("No")
            return
        _, inv = np.unique(fs, return_inverse=True)
        tot = np.bincount(inv, weights=fm)
        print("Yes" if tot.max() >= R else "No")
        return
    except ImportError:
        pass

    # Pure python fallback.
    from bisect import bisect_left
    bvals = [b for b, _ in listB]
    q = len(listB)
    acc = {}
    get = acc.get
    for a, ca in listA:
        j = bisect_left(bvals, L - a)  # need a + b >= L
        for b, cb in listB[j:]:
            s = a + b
            m = ca if ca < cb else cb
            cur = get(s)
            if cur is None:
                if m >= R:
                    print("Yes")
                    return
                acc[s] = m
            else:
                v = cur + m
                if v >= R:
                    print("Yes")
                    return
                acc[s] = v
    print("No")


main()