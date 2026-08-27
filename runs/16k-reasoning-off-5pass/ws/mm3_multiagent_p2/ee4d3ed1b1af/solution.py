class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Special case: pattern is exactly "**"
        if p == "**":
            return 0

        # Split pattern at the two '*' characters
        parts = p.split('*')
        L, M, R = parts[0], parts[1], parts[2]

        n = len(s)

        # ---------- KMP helper ----------
        def kmp_occurrences(text, pat):
            if not pat:
                return None
            m = len(pat)
            lps = [0] * m
            j = 0
            for i in range(1, m):
                while j > 0 and pat[i] != pat[j]:
                    j = lps[j - 1]
                if pat[i] == pat[j]:
                    j += 1
                    lps[i] = j
            res = []
            j = 0
            for i, ch in enumerate(text):
                while j > 0 and ch != pat[j]:
                    j = lps[j - 1]
                if ch == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = lps[j - 1]
            return res

        left_starts = kmp_occurrences(s, L) if L else None
        right_starts = kmp_occurrences(s, R) if R else None
        mid_starts = kmp_occurrences(s, M) if M else None

        # ---------- left_prefix[i] = start of latest L match with end == i, or -1 ----------
        left_prefix = [-1] * n
        if L:
            idx = 0
            last_start = -1
            for i in range(n):
                while idx < len(left_starts) and left_starts[idx] + len(L) - 1 == i:
                    last_start = left_starts[idx]
                    idx += 1
                left_prefix[i] = last_start
        else:
            # L empty: zero-length match at every position, start = i
            for i in range(n):
                left_prefix[i] = i

        # ---------- left_prefix_best[i] = best (largest start) L with end <= i ----------
        left_prefix_best = [-1] * n
        best = -1
        for i in range(n):
            v = left_prefix[i]
            if v != -1:
                best = v
            left_prefix_best[i] = best

        # ---------- right_suffix[i] = end of earliest R match with start == i, or n ----------
        right_suffix = [n] * n
        if R:
            r_ends = [start + len(R) - 1 for start in right_starts]
            ptr = len(right_starts) - 1
            min_end = n
            for i in range(n - 1, -1, -1):
                while ptr >= 0 and right_starts[ptr] == i:
                    if r_ends[ptr] < min_end:
                        min_end = r_ends[ptr]
                    ptr -= 1
                right_suffix[i] = min_end
        else:
            # R empty: zero-length match at every position, end = i - 1
            for i in range(n):
                right_suffix[i] = i - 1

        # ---------- right_suffix_best[i] = best (smallest end) R with start >= i ----------
        right_suffix_best = [n] * n
        best = n
        for i in range(n - 1, -1, -1):
            v = right_suffix[i]
            if v != n:
                best = v
            right_suffix_best[i] = best

        INF = n + 1
        ans = INF

        # ---------- Handle M empty ----------
        if not M:
            if not L and not R:
                return 0
            # Try every split point: L ends at or before i, R starts at or after i+1
            for i in range(n):
                # L_end = i if L else i-1 (zero-length ending at i-1)
                # Find best L with end <= i
                if L:
                    ls = left_prefix_best[i]
                    le = i
                else:
                    if i == 0:
                        continue
                    ls = i - 1
                    le = i - 1
                if ls == -1:
                    continue
                # R_start = i+1 if R else i+1 (zero-length starting at i+1)
                if i + 1 < n:
                    re = right_suffix_best[i + 1]
                else:
                    re = n
                if R:
                    if re == n:
                        continue
                    rs = re - len(R) + 1
                else:
                    re = i
                    rs = i + 1
                if le >= rs:
                    continue
                cand = re - ls + 1
                if cand < ans:
                    ans = cand
            return ans if ans <= n else -1

        # ---------- General case ----------
        for ms in mid_starts:
            me = ms + len(M) - 1
            # Find best L with end < ms
            if L:
                if ms == 0:
                    ls = -1
                else:
                    ls = left_prefix_best[ms - 1]
                if ls == -1:
                    continue
                le = ls + len(L) - 1
                if le >= ms:
                    continue
            else:
                # L empty, zero-length match ending at ms-1, starting at ms
                if ms == 0:
                    ls = 0
                    le = -1
                else:
                    ls = ms
                    le = ms - 1
            # Find best R with start > me
            if R:
                if me + 1 < n:
                    re = right_suffix_best[me + 1]
                else:
                    re = n
                if re == n:
                    continue
                rs = re - len(R) + 1
                if rs <= me:
                    continue
            else:
                # R empty, zero-length match starting at me+1
                if me + 1 >= n:
                    continue
                re = me
                rs = me + 1
            cand = re - ls + 1
            if cand < ans:
                ans = cand

        return ans if ans <= n else -1