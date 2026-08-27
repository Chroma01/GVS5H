from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)

        # Split pattern into three literal parts at the two '*'
        star1 = p.index('*')
        star2 = p.index('*', star1 + 1)
        pre = p[:star1]
        mid = p[star1 + 1:star2]
        suf = p[star2 + 1:]

        # KMP: return all start indices where pat occurs in s (incl. overlaps)
        def occurrences(pat: str):
            m = len(pat)
            if m == 0:
                return list(range(n + 1))  # empty pattern "occurs" everywhere
            # build failure function
            fail = [0] * m
            k = 0
            for i in range(1, m):
                while k > 0 and pat[i] != pat[k]:
                    k = fail[k - 1]
                if pat[i] == pat[k]:
                    k += 1
                fail[i] = k
            # scan s
            res = []
            k = 0
            for i, ch in enumerate(s):
                while k > 0 and ch != pat[k]:
                    k = fail[k - 1]
                if ch == pat[k]:
                    k += 1
                if k == m:
                    res.append(i - m + 1)
                    k = fail[k - 1]
            return res

        pre_pos = occurrences(pre)   # start positions of prefix
        mid_pos = occurrences(mid)   # start positions of middle
        suf_pos = occurrences(suf)   # start positions of suffix

        lp, lm, ls = len(pre), len(mid), len(suf)
        ans = float('inf')

        # For each prefix occurrence i (window start), greedily chain:
        # earliest mid start >= i + lp, then earliest suf start >= mid_start + lm.
        # Empty parts naturally impose no constraint via their full position lists.
        for i in pre_pos:
            mid_need = i + lp
            j = bisect_left(mid_pos, mid_need)
            if j == len(mid_pos):
                continue
            m_start = mid_pos[j]
            suf_need = m_start + lm
            k = bisect_left(suf_pos, suf_need)
            if k == len(suf_pos):
                continue
            end = suf_pos[k] + ls
            length = end - i
            if length < ans:
                ans = length

        return -1 if ans == float('inf') else ans