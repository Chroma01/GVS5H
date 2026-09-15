import sys
import random


def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 3:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)
    out = sys.stdout.write

    if abs(n - m) > K:
        out("No\n")
        return

    MASK = (1 << 64) - 1
    base = random.randrange(1 << 30, 1 << 62) | 1

    maxlen = n if n > m else m
    pw = [1] * (maxlen + 1)
    p = 1
    for i in range(1, maxlen + 1):
        p = (p * base) & MASK
        pw[i] = p

    hS = [0] * (n + 1)
    a = 0
    for i in range(n):
        a = (a * base + S[i]) & MASK
        hS[i + 1] = a

    hT = [0] * (m + 1)
    a = 0
    for i in range(m):
        a = (a * base + T[i]) & MASK
        hT[i + 1] = a

    def lcp(i, j):
        # length of common prefix of S[i:] and T[j:], via binary search on hashes
        hi = n - i
        t2 = m - j
        if t2 < hi:
            hi = t2
        lo = 0
        bi = hS[i]
        bj = hT[j]
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            hs = (hS[i + mid] - bi * pw[mid]) & MASK
            ht = (hT[j + mid] - bj * pw[mid]) & MASK
            if hs == ht:
                lo = mid
            else:
                hi = mid - 1
        return lo

    OFF = K
    size = 2 * K + 1
    NEG = -1

    Vprev = [NEG] * size
    Vprev[OFF] = lcp(0, 0) if (n and m) else 0

    goal = n - m + OFF
    if Vprev[goal] >= n:
        out("Yes\n")
        return

    for d in range(1, K + 1):
        Vcur = [NEG] * size
        for k in range(-d, d + 1):
            idx = k + OFF
            best = Vprev[idx]  # at most d-1 edits (no extra edit)

            # substitution: same diagonal, from furthest cell
            if best >= 0:
                ni = best + 1
                nj = ni - k
                if ni <= n and nj <= m and nj >= 0 and ni > best:
                    best = ni

            # deletion (consume S): predecessor on diagonal k-1
            if idx - 1 >= 0:
                i0 = Vprev[idx - 1]
                if i0 >= 0:
                    ni = i0 + 1
                    nj = ni - k
                    if ni <= n and nj <= m and nj >= 0 and ni > best:
                        best = ni

            # insertion (consume T): predecessor on diagonal k+1
            if idx + 1 < size:
                i0 = Vprev[idx + 1]
                if i0 >= 0:
                    nj = i0 - k
                    if i0 <= n and nj <= m and nj >= 0 and i0 > best:
                        best = i0

            if best >= 0:
                j = best - k
                if best < n and j < m:
                    Vcur[idx] = best + lcp(best, j)
                else:
                    Vcur[idx] = best

        Vprev = Vcur
        if Vprev[goal] >= n:
            out("Yes\n")
            return

    out("No\n")


main()