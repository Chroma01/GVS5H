import sys
from array import array

MASK = (1 << 64) - 1
B1 = 0x9e3779b97f4a7c15
B2 = 0xbf58476d1ce4e5b9


def solve():
    data = sys.stdin.buffer.read().split()
    if len(data) < 3:
        return

    K = int(data[0])
    S = data[1]
    T = data[2]
    del data

    out = sys.stdout.write
    YES = "Yes\n"
    NO = "No\n"

    n = len(S)
    m = len(T)

    # Length difference is a lower bound.
    if abs(n - m) > K:
        out(NO)
        return

    # Trim common prefix.
    p = 0
    while p < n and p < m and S[p] == T[p]:
        p += 1
    if p:
        S = S[p:]
        T = T[p:]
        n -= p
        m -= p

    # Trim common suffix.
    q = 0
    while q < n and q < m and S[n - 1 - q] == T[m - 1 - q]:
        q += 1
    if q:
        S = S[:n - q]
        T = T[:m - q]
        n -= q
        m -= q

    if abs(n - m) > K:
        out(NO)
        return

    # Any two strings of lengths n, m have edit distance at most max(n, m).
    if K >= max(n, m):
        out(YES)
        return

    if K == 0:
        out(NO)
        return

    maxlen = max(n, m)
    mask = MASK
    b1 = B1
    b2 = B2

    # Powers for double 64-bit rolling hashes.
    pow1 = array('Q', [0]) * (maxlen + 1)
    pow2 = array('Q', [0]) * (maxlen + 1)
    pow1[0] = 1
    pow2[0] = 1

    p1 = 1
    p2 = 1
    for i in range(1, maxlen + 1):
        p1 = (p1 * b1) & mask
        p2 = (p2 * b2) & mask
        pow1[i] = p1
        pow2[i] = p2

    def build_hash(s, b1=b1, b2=b2, mask=mask):
        ln = len(s)
        h1 = array('Q', [0]) * (ln + 1)
        h2 = array('Q', [0]) * (ln + 1)
        a1 = 0
        a2 = 0
        for i, c in enumerate(s, 1):
            v = c - 96
            a1 = (a1 * b1 + v) & mask
            a2 = (a2 * b2 + v) & mask
            h1[i] = a1
            h2[i] = a2
        return h1, h2

    hS1, hS2 = build_hash(S)
    hT1, hT2 = build_hash(T)

    cache = {}
    stride = m + 1

    def lcp(i, j, S=S, T=T, n=n, m=m,
            hS1=hS1, hS2=hS2, hT1=hT1, hT2=hT2,
            pow1=pow1, pow2=pow2, mask=mask,
            stride=stride, cache=cache):
        if i < 0 or j < 0 or i >= n or j >= m:
            return 0

        key = i * stride + j
        res = cache.get(key, -1)
        if res >= 0:
            return res

        max_len = n - i
        if m - j < max_len:
            max_len = m - j

        if max_len <= 0:
            cache[key] = 0
            return 0

        if S[i] != T[j]:
            cache[key] = 0
            return 0

        if max_len == 1:
            cache[key] = 1
            return 1

        hs1_i = hS1[i]
        hs2_i = hS2[i]
        ht1_j = hT1[j]
        ht2_j = hT2[j]

        lo = 1
        hi = max_len

        while lo < hi:
            mid = (lo + hi + 1) >> 1
            im = i + mid
            jm = j + mid

            p1 = pow1[mid]
            hs1 = (hS1[im] - ((hs1_i * p1) & mask)) & mask
            ht1 = (hT1[jm] - ((ht1_j * p1) & mask)) & mask
            if hs1 != ht1:
                hi = mid - 1
                continue

            p2 = pow2[mid]
            hs2 = (hS2[im] - ((hs2_i * p2) & mask)) & mask
            ht2 = (hT2[jm] - ((ht2_j * p2) & mask)) & mask
            if hs2 != ht2:
                hi = mid - 1
            else:
                lo = mid

        cache[key] = lo
        return lo

    # Landau-Vishkin furthest-reaching edit distance.
    # Diagonal d = i - j. V[d] = furthest i reachable on diagonal d.
    size = 2 * K + 5
    offset = K + 2
    off = offset

    prev = [-1] * size
    x = lcp(0, 0)
    prev[off] = x

    if x >= n and x >= m:
        out(YES)
        return

    for e in range(1, K + 1):
        curr = [-1] * size

        for d in range(-e, e + 1):
            idx = off + d
            x = -1

            # Deletion from S: from diagonal d-1, i increases by 1.
            p = prev[idx - 1]
            if p >= 0:
                cand = p + 1
                if cand > x:
                    x = cand

            # Insertion into S: from diagonal d+1, i stays the same.
            p = prev[idx + 1]
            if p >= 0 and p > x:
                x = p

            # Substitution: from diagonal d, i increases by 1.
            p = prev[idx]
            if p >= 0:
                cand = p + 1
                if cand > x:
                    x = cand

            if x < 0:
                continue

            y = x - d

            if 0 <= x < n and 0 <= y < m:
                x += lcp(x, y)

            if x >= n and x - d >= m:
                out(YES)
                return

            curr[idx] = x

        prev = curr

    out(NO)


if __name__ == "__main__":
    solve()