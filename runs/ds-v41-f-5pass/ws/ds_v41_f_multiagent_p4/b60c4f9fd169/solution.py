import sys
from random import randrange


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    m = len(S)
    n = len(T)
    out = sys.stdout

    # Necessary condition on lengths.
    if abs(m - n) > K:
        out.write("No\n")
        return

    # Rolling hash (single 61-bit prime modulus) to answer LCP in O(log n).
    MOD = (1 << 61) - 1
    BASE = randrange(257, MOD - 1)
    L = m if m > n else n
    P = [1] * (L + 1)
    b = BASE
    for i in range(L):
        P[i + 1] = P[i] * b % MOD
    HS = [0] * (m + 1)
    for i in range(m):
        HS[i + 1] = (HS[i] * b + S[i]) % MOD
    HT = [0] * (n + 1)
    for i in range(n):
        HT[i + 1] = (HT[i] * b + T[i]) % MOD

    def lcp(i, j):
        # longest common prefix of S[i:] and T[j:]
        hi = m - i
        t = n - j
        if t < hi:
            hi = t
        if hi <= 0:
            return 0
        lo = 0
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if (HS[i + mid] - HS[i] * P[mid]) % MOD == (HT[j + mid] - HT[j] * P[mid]) % MOD:
                lo = mid
            else:
                hi = mid - 1
        return lo

    OFF = K
    size = 2 * K + 1
    prev = [-1] * size
    prev[OFF] = lcp(0, 0)  # diagonal k = 0 with 0 edits
    target = m - n
    tidx = target + OFF
    if prev[tidx] == m:
        out.write("Yes\n")
        return

    for d in range(1, K + 1):
        cur = prev[:]  # "at most d-1" (no extra op)
        for k in range(-d, d + 1):
            idx = k + OFF
            best = cur[idx]
            start_k = k if k > 0 else 0

            # Substitution: source on same diagonal k.
            r = prev[idx]
            if r >= 0:
                src = r
                t1 = m - 1
                if t1 < src:
                    src = t1
                t2 = n + k - 1
                if t2 < src:
                    src = t2
                if src >= start_k:
                    i2 = src + 1
                    j2 = i2 - k
                    if i2 < m and j2 < n:
                        i2 += lcp(i2, j2)
                    if i2 > best:
                        best = i2

            # Deletion: source on diagonal k-1 (i increases).
            if k - 1 >= -K:
                r = prev[k - 1 + OFF]
                if r >= 0:
                    src = r
                    t1 = m - 1
                    if t1 < src:
                        src = t1
                    skm = k - 1 if k - 1 > 0 else 0
                    if src >= skm:
                        i2 = src + 1
                        j2 = i2 - k
                        if i2 < m and j2 < n:
                            i2 += lcp(i2, j2)
                        if i2 > best:
                            best = i2

            # Insertion: source on diagonal k+1 (j increases, i same).
            if k + 1 <= K:
                r = prev[k + 1 + OFF]
                if r >= 0:
                    src = r
                    t1 = n + k
                    if t1 < src:
                        src = t1
                    skp = k + 1 if k + 1 > 0 else 0
                    if src >= skp:
                        i2 = src
                        j2 = i2 - k
                        if i2 < m and j2 < n:
                            i2 += lcp(i2, j2)
                        if i2 > best:
                            best = i2

            cur[idx] = best

        prev = cur
        if prev[tidx] == m:
            out.write("Yes\n")
            return

    out.write("No\n")


main()