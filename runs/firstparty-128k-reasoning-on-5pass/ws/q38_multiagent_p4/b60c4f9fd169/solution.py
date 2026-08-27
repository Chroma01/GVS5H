import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    K = int(data[0])
    S = data[1]
    T = data[2]
    del data

    # Make S the shorter string. The edit distance is symmetric.
    if len(S) > len(T):
        S, T = T, S

    n = len(S)
    m = len(T)

    # Length difference is a lower bound on the edit distance.
    if m - n > K:
        print("No")
        return

    # If K is at least the longer length, replace all of S and insert the rest.
    if K >= m:
        print("Yes")
        return

    MASK = (1 << 64) - 1
    BASE = 911382323

    # Powers of BASE modulo 2^64.
    powb = [1] * (m + 1)
    x = 1
    base = BASE
    mask = MASK
    for i in range(1, m + 1):
        x = (x * base) & mask
        powb[i] = x

    def build_hash(b):
        h = [0] * (len(b) + 1)
        x = 0
        base = BASE
        mask = MASK
        for i, c in enumerate(b, 1):
            x = (x * base + c) & mask
            h[i] = x
        return h

    hS = build_hash(S)
    hT = build_hash(T)

    mvS = memoryview(S)
    mvT = memoryview(T)

    def lcp(i, j):
        """Exact LCP of S[i:] and T[j:]."""
        if i < 0 or j < 0 or i > n or j > m:
            return 0

        max_l = n - i
        rem = m - j
        if rem < max_l:
            max_l = rem
        if max_l <= 0:
            return 0

        lo = 0
        hi = max_l
        hS_l = hS
        hT_l = hT
        pow_l = powb
        mask = MASK
        hS_i = hS_l[i]
        hT_j = hT_l[j]

        # Binary search the largest length whose 64-bit hashes are equal.
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            hs = (hS_l[i + mid] - hS_i * pow_l[mid]) & mask
            ht = (hT_l[j + mid] - hT_j * pow_l[mid]) & mask
            if hs == ht:
                lo = mid
            else:
                hi = mid - 1

        L = lo

        # Verify the hash result. If a collision broke the search, scan directly.
        if L:
            if mvS[i:i + L] != mvT[j:j + L]:
                L = 0
                s = S
                t = T
                si = i
                tj = j
                while L < max_l and s[si] == t[tj]:
                    L += 1
                    si += 1
                    tj += 1

        return L

    delta = m - n
    offset = K + 2
    size = 2 * K + 5
    UNREACH = -1

    # prev[d] = furthest i reachable with the current number of edits on diagonal d = j - i.
    prev = [UNREACH] * size
    i0 = lcp(0, 0)
    prev[offset] = i0

    # S is already a prefix of T.
    if i0 == n and delta <= K:
        print("Yes")
        return

    for e in range(1, K + 1):
        curr = [UNREACH] * size
        rem_budget = K - e

        d_min = -e
        d_max = e

        # Even with all remaining edits, the diagonal must be able to reach delta.
        lb = delta - rem_budget
        ub = delta + rem_budget
        if d_min < lb:
            d_min = lb
        if d_max > ub:
            d_max = ub

        for d in range(d_min, d_max + 1):
            best = UNREACH

            # Substitution: same diagonal, consume one character from both strings.
            val = prev[d + offset]
            if val != UNREACH:
                j = val + d
                if val < n and 0 <= j < m:
                    ni = val + 1
                    ni += lcp(ni, ni + d)
                    if ni > best:
                        best = ni

            # Insertion into S: diagonal increases by 1, consume one character from T.
            val = prev[d - 1 + offset]
            if val != UNREACH:
                j = val + d - 1
                if 0 <= j < m:
                    ni = val
                    ni += lcp(ni, ni + d)
                    if ni > best:
                        best = ni

            # Deletion from S: diagonal decreases by 1, consume one character from S.
            val = prev[d + 1 + offset]
            if val != UNREACH:
                j = val + d + 1
                if val < n and 0 <= j <= m:
                    ni = val + 1
                    ni += lcp(ni, ni + d)
                    if ni > best:
                        best = ni

            curr[d + offset] = best

            if best != UNREACH:
                j = best + d
                if 0 <= j <= m:
                    # S is fully consumed; only insertions are needed.
                    if best == n:
                        if d <= delta and delta - d <= rem_budget:
                            print("Yes")
                            return

                    # T is fully consumed; only deletions are needed.
                    if j == m:
                        if d >= delta and d - delta <= rem_budget:
                            print("Yes")
                            return

        prev = curr

    if prev[delta + offset] >= n:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()