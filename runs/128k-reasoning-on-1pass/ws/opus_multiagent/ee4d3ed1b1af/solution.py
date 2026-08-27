from bisect import bisect_left, bisect_right


def kmp_occurrences(text, pat):
    """All (possibly overlapping) start indices of pat in text, via prefix function."""
    m = len(pat)
    n = len(text)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    # prefix function of pat
    fail = [0] * m
    k = 0
    for i in range(1, m):
        c = pat[i]
        while k and pat[k] != c:
            k = fail[k - 1]
        if pat[k] == c:
            k += 1
        fail[i] = k
    res = []
    k = 0
    for i, c in enumerate(text):
        while k and pat[k] != c:
            k = fail[k - 1]
        if pat[k] == c:
            k += 1
            if k == m:
                res.append(i - m + 1)
                k = fail[k - 1]
    return res


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        parts = p.split('*')
        # p contains exactly two '*', so parts has 3 elements
        a, b, c = parts[0], parts[1], parts[2]
        la, lb, lc = len(a), len(b), len(c)

        if la == 0 and lb == 0 and lc == 0:
            return 0

        if la + lb + lc > n:
            return -1

        A = kmp_occurrences(s, a) if la else None
        B = kmp_occurrences(s, b) if lb else None
        C = kmp_occurrences(s, c) if lc else None

        if la and not A:
            return -1
        if lb and not B:
            return -1
        if lc and not C:
            return -1

        best = -1
        js = B if lb else range(n + 1)

        for j in js:
            # choose largest a-occurrence l with l + la <= j
            if la == 0:
                l = j
            else:
                idx = bisect_right(A, j - la) - 1
                if idx < 0:
                    continue
                l = A[idx]
            # choose smallest c-occurrence k with k >= j + lb
            end = j + lb
            if lc == 0:
                k = end
            else:
                idx = bisect_left(C, end)
                if idx >= len(C):
                    continue
                k = C[idx]
            cand = k + lc - l
            if best == -1 or cand < best:
                best = cand

        return best


if __name__ == "__main__":
    sol = Solution()
    print(sol.shortestMatchingSubstring("abaacbaecebce", "ba*c*ce"))  # 8
    print(sol.shortestMatchingSubstring("baccbaadbc", "cc*baa*adb"))  # -1
    print(sol.shortestMatchingSubstring("a", "**"))                   # 0
    print(sol.shortestMatchingSubstring("madlogic", "*adlogi*"))      # 6