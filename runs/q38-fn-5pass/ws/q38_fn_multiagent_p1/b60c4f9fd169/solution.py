import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    K = int(data[0])
    S = data[1]
    T = data[2]

    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    if K == 0:
        sys.stdout.write("Yes\n" if S == T else "No\n")
        return

    # Edit distance is always at most max(len(S), len(T)).
    if K >= max(n, m):
        sys.stdout.write("Yes\n")
        return

    # Edit distance is symmetric.  Keep the shorter string as S.
    if n > m:
        S, T = T, S
        n, m = m, n

    end_d = n - m

    # 64-bit rolling hash (mod 2^64).
    MASK = (1 << 64) - 1
    BASE = 911382323
    max_len = m

    powB = [1] * (max_len + 1)
    base = BASE
    mask = MASK
    for i in range(max_len):
        powB[i + 1] = (powB[i] * base) & mask

    Hs = [0] * (n + 1)
    h = 0
    for i, c in enumerate(S):
        h = (h * base + c) & mask
        Hs[i + 1] = h

    Ht = [0] * (m + 1)
    h = 0
    for i, c in enumerate(T):
        h = (h * base + c) & mask
        Ht[i + 1] = h

    mvS = memoryview(S)
    mvT = memoryview(T)
    lcp_cache = {}

    def lcp(i, j):
        """Exact LCP length of S[i:] and T[j:]."""
        key = (i, j)
        cached = lcp_cache.get(key, -1)
        if cached >= 0:
            return cached

        maxl = n - i
        if m - j < maxl:
            maxl = m - j

        if maxl <= 0:
            lcp_cache[key] = 0
            return 0

        if S[i] != T[j]:
            lcp_cache[key] = 0
            return 0

        if maxl == 1:
            lcp_cache[key] = 1
            return 1

        low = 1
        high = maxl
        hs_i = Hs[i]
        ht_j = Ht[j]

        while low < high:
            mid = (low + high + 1) >> 1
            hs = (Hs[i + mid] - ((hs_i * powB[mid]) & mask)) & mask
            ht = (Ht[j + mid] - ((ht_j * powB[mid]) & mask)) & mask
            if hs == ht:
                low = mid
            else:
                high = mid - 1

        # Exact verification.  A 64-bit hash collision can only make `low`
        # too large; if verification fails, fall back to a linear scan.
        if low > 1 and mvS[i:i + low] != mvT[j:j + low]:
            ii = i
            jj = j
            while ii < n and jj < m and S[ii] == T[jj]:
                ii += 1
                jj += 1
            res = ii - i
        else:
            res = low

        lcp_cache[key] = res
        return res

    # Landau-Vishkin furthest-reaching DP.
    # prev[d + off] = furthest index in S on diagonal d after exactly e-1 edits
    # and then a maximal snake of matches.
    size = 2 * K + 3
    off = K + 1

    prev = [-1] * size
    prev[off] = lcp(0, 0)

    if end_d == 0 and prev[off] >= n:
        sys.stdout.write("Yes\n")
        return

    for e in range(1, K + 1):
        curr = [-1] * size

        for d in range(-e, e + 1):
            best = -1

            # Delete one character from S: diagonal d-1 -> d.
            dp = d - 1
            if -K <= dp <= K:
                ip = prev[dp + off]
                if ip >= 0 and ip < n:
                    cand = ip + 1
                    if cand > best:
                        best = cand

            # Insert one character into S (consume T): diagonal d+1 -> d.
            dp = d + 1
            if -K <= dp <= K:
                ip = prev[dp + off]
                if ip >= 0:
                    jp = ip - dp
                    if 0 <= jp < m:
                        cand = ip
                        if cand > best:
                            best = cand

            # Substitute one character: diagonal d -> d.
            dp = d
            if -K <= dp <= K:
                ip = prev[dp + off]
                if ip >= 0:
                    jp = ip - dp
                    if ip < n and 0 <= jp < m:
                        cand = ip + 1
                        if cand > best:
                            best = cand

            if best >= 0:
                j = best - d
                if 0 <= best <= n and 0 <= j <= m:
                    ii = best + lcp(best, j)
                    curr[d + off] = ii
                    if d == end_d and ii >= n:
                        sys.stdout.write("Yes\n")
                        return

        prev = curr

    sys.stdout.write("No\n")


if __name__ == "__main__":
    solve()