import sys
import random


def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 3:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]

    n0 = len(S)
    m0 = len(T)

    # Trim common prefix (edit distance is invariant under a shared prefix)
    p = 0
    lim = n0 if n0 < m0 else m0
    while p < lim and S[p] == T[p]:
        p += 1
    if p:
        S = S[p:]
        T = T[p:]

    n2 = len(S)
    m2 = len(T)

    # Trim common suffix of the remainders
    q = 0
    lim = n2 if n2 < m2 else m2
    while q < lim and S[n2 - 1 - q] == T[m2 - 1 - q]:
        q += 1
    if q:
        S = S[:n2 - q]
        T = T[:m2 - q]

    n = len(S)
    m = len(T)

    if n == 0 or m == 0:
        print("Yes" if (n + m) <= K else "No")
        return
    if n - m > K or m - n > K:
        print("No")
        return

    # 64-bit rolling hash for longest-common-prefix queries
    MASK = (1 << 64) - 1
    BASE = random.randrange(1 << 33, 1 << 62) | 1

    preS = [0] * (n + 1)
    h = 0
    for i in range(n):
        h = (h * BASE + S[i]) & MASK
        preS[i + 1] = h

    preT = [0] * (m + 1)
    h = 0
    for i in range(m):
        h = (h * BASE + T[i]) & MASK
        preT[i + 1] = h

    maxlen = n if n > m else m
    pw = [1] * (maxlen + 1)
    x = 1
    for i in range(1, maxlen + 1):
        x = (x * BASE) & MASK
        pw[i] = x

    pS, pT, p2 = preS, preT, pw

    def lcp(a, b):
        # longest common prefix of S[a:] and T[b:]
        hi = n - a
        t = m - b
        if t < hi:
            hi = t
        if hi <= 0:
            return 0
        lo = 0
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if ((pS[a + mid] - pS[a] * p2[mid]) & MASK) == \
               ((pT[b + mid] - pT[b] * p2[mid]) & MASK):
                lo = mid
            else:
                hi = mid - 1
        return lo

    # Banded wavefront: V[d] = furthest x on diagonal d = x - y using exactly c ops
    off = K + 1
    size = 2 * K + 3
    V = [-1] * size
    V[off] = lcp(0, 0)
    ds = n - m

    if V[off + ds] >= n:
        print("Yes")
        return

    for c in range(1, K + 1):
        nV = [-1] * size
        for d in range(-c, c + 1):
            best = -1
            x0 = V[off + d]                      # substitution: stay on diagonal d
            if x0 >= 0 and x0 < n and x0 - d < m:
                best = x0 + 1
            x0 = V[off + d - 1]                  # deletion: come from diagonal d-1
            if x0 >= 0 and x0 < n and x0 + 1 > best:
                best = x0 + 1
            x0 = V[off + d + 1]                  # insertion: come from diagonal d+1
            if x0 >= 0 and x0 - (d + 1) < m and x0 > best:
                best = x0
            if best >= 0:
                nV[off + d] = best + lcp(best, best - d)
        V = nV
        if V[off + ds] >= n:
            print("Yes")
            return

    print("No")


main()