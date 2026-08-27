from bisect import bisect_right, bisect_left

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into three literal parts around the two '*'
        star1 = p.index('*')
        star2 = p.index('*', star1 + 1)
        A = p[:star1]
        B = p[star1 + 1:star2]
        C = p[star2 + 1:]
        n = len(s)
        la, lb, lc = len(A), len(B), len(C)

        def kmp_occurrences(pat: str):
            """Return sorted list of start indices where pat occurs in s."""
            m = len(pat)
            if m == 0:
                return list(range(n + 1))  # empty pattern matches at every position 0..n
            # build prefix function
            pi = [0] * m
            k = 0
            for i in range(1, m):
                while k > 0 and pat[i] != pat[k]:
                    k = pi[k - 1]
                if pat[i] == pat[k]:
                    k += 1
                pi[i] = k
            res = []
            q = 0
            for i, ch in enumerate(s):
                while q > 0 and ch != pat[q]:
                    q = pi[q - 1]
                if ch == pat[q]:
                    q += 1
                if q == m:
                    res.append(i - m + 1)
                    q = pi[q - 1]
            return res

        a_pos = kmp_occurrences(A)  # start positions of A
        b_pos = kmp_occurrences(B)  # start positions of B
        c_pos = kmp_occurrences(C)  # start positions of C

        INF = float('inf')
        ans = INF

        # For each occurrence of B starting at b:
        #   need A start a with a + la <= b  -> a <= b - la
        #   need C start c with c >= b + lb
        #   length = (c + lc) - a
        # To minimize, take the largest valid a and smallest valid c.
        for b in b_pos:
            # latest A start
            ai = bisect_right(a_pos, b - la) - 1
            if ai < 0:
                continue
            a = a_pos[ai]
            # earliest C start
            ci = bisect_left(c_pos, b + lb)
            if ci >= len(c_pos):
                continue
            c = c_pos[ci]
            length = c + lc - a
            if length < ans:
                ans = length

        return -1 if ans == INF else ans