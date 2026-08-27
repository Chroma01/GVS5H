class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)

        # Split p into the three literal parts around the two '*'
        i1 = p.index('*')
        i2 = p.index('*', i1 + 1)
        a, b, c = p[:i1], p[i1 + 1:i2], p[i2 + 1:]
        la, lb, lc = len(a), len(b), len(c)

        INF = n + 5

        def occurrence_flags(pat: str):
            """ok[i] is True iff pat occurs in s starting at index i.
            Empty pattern matches at every boundary 0..n."""
            m = len(pat)
            if m == 0:
                return [True] * (n + 1)
            ok = [False] * (n + 1)
            if m > n:
                return ok
            # KMP prefix function over pat + '#' + s (finds overlapping matches)
            combined = pat + '#' + s
            pi = [0] * len(combined)
            for i in range(1, len(combined)):
                j = pi[i - 1]
                while j > 0 and combined[i] != combined[j]:
                    j = pi[j - 1]
                if combined[i] == combined[j]:
                    j += 1
                pi[i] = j
                if j == m:
                    # match ends at combined index i; start in s is i - 2*m
                    ok[i - 2 * m] = True
            return ok

        okA = occurrence_flags(a)
        okB = occurrence_flags(b)
        okC = occurrence_flags(c)

        # nextB[t] / nextC[t]: earliest start position >= t where b / c occurs
        nextB = [INF] * (n + 2)
        for t in range(n, -1, -1):
            nextB[t] = t if okB[t] else nextB[t + 1]
        nextC = [INF] * (n + 2)
        for t in range(n, -1, -1):
            nextC[t] = t if okC[t] else nextC[t + 1]

        ans = INF
        for i in range(n + 1):
            if not okA[i]:
                continue
            j = nextB[i + la]          # earliest b at/after end of a
            if j == INF:
                continue
            k = nextC[j + lb]          # earliest c at/after end of b
            if k == INF:
                continue
            cur = k + lc - i           # length of substring s[i : k+lc]
            if cur < ans:
                ans = cur

        return -1 if ans == INF else ans