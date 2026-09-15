import sys
import random


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)

    # ---- strip longest common prefix / suffix (invariant for edit distance) ----
    p = 0
    while p < n and p < m and S[p] == T[p]:
        p += 1
    ln = n - p
    lm = m - p
    s = 0
    while s < ln and s < lm and S[n - 1 - s] == T[m - 1 - s]:
        s += 1
    if s:
        S = S[p:n - s]
        T = T[p:m - s]
    else:
        S = S[p:]
        T = T[p:]
    n = len(S)
    m = len(T)

    if n == 0 and m == 0:
        sys.stdout.write("Yes\n")
        return
    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    d_star = m - n  # final diagonal j - i

    # ---- rolling hash, modulus 2^61 - 1, random odd base ----
    MOD = (1 << 61) - 1
    BASE = random.randrange(1 << 20, 1 << 40) | 1

    mx = n if n > m else m
    pw = [1] * (mx + 1)
    acc = 1
    for i in range(1, mx + 1):
        acc = acc * BASE % MOD
        pw[i] = acc

    hs = [0] * (n + 1)
    cur = 0
    for i in range(n):
        cur = (cur * BASE + S[i]) % MOD
        hs[i + 1] = cur
    ht = [0] * (m + 1)
    cur = 0
    for i in range(m):
        cur = (cur * BASE + T[i]) % MOD
        ht[i + 1] = cur

    def lcp(i, j):
        # longest common prefix of S[i:] and T[j:]
        a = n - i
        b = m - j
        maxl = a if a < b else b
        if maxl <= 0:
            return 0
        if (hs[i + 1] - hs[i] * BASE) % MOD != (ht[j + 1] - ht[j] * BASE) % MOD:
            return 0
        lo = 1
        while lo * 2 <= maxl:
            L = lo * 2
            if (hs[i + L] - hs[i] * pw[L]) % MOD == (ht[j + L] - ht[j] * pw[L]) % MOD:
                lo = L
            else:
                break
        hi = lo * 2
        if hi > maxl:
            hi = maxl
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if (hs[i + mid] - hs[i] * pw[mid]) % MOD == (ht[j + mid] - ht[j] * pw[mid]) % MOD:
                lo = mid
            else:
                hi = mid - 1
        return lo

    size = 2 * K + 1
    # V[K+d] = furthest i reachable with <= c edits on diagonal d = j - i
    V = [-1] * size
    V[K] = lcp(0, 0)
    if V[K + d_star] >= n:
        sys.stdout.write("Yes\n")
        return

    for c in range(1, K + 1):
        NV = [-1] * size
        for d in range(-K, K + 1):
            idx = K + d
            best = V[idx]  # use fewer edits (carry)
            # insert into S: predecessor diagonal d-1, i unchanged
            if d - 1 >= -K:
                i0 = V[idx - 1]
                if i0 >= 0:
                    j = i0 + d
                    if 0 <= j <= m:
                        val = i0 + lcp(i0, j)
                        if val > best:
                            best = val
            # delete from S: predecessor diagonal d+1, i+1
            if d + 1 <= K:
                i0 = V[idx + 1]
                if i0 >= 0:
                    i1 = i0 + 1
                    if i1 <= n:
                        j = i1 + d
                        if 0 <= j <= m:
                            val = i1 + lcp(i1, j)
                            if val > best:
                                best = val
            # replace: predecessor diagonal d, i+1
            i0 = V[idx]
            if i0 >= 0:
                i1 = i0 + 1
                if i1 <= n:
                    j = i1 + d
                    if 0 <= j <= m:
                        val = i1 + lcp(i1, j)
                        if val > best:
                            best = val
            NV[idx] = best
        V = NV
        if V[K + d_star] >= n:
            sys.stdout.write("Yes\n")
            return

    sys.stdout.write("No\n")


if __name__ == "__main__":
    solve()