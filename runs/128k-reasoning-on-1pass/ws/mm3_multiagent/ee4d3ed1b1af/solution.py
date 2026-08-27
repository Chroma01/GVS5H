class Solution:
    def _kmp_occurrences(self, text: str, pat: str):
        if not pat:
            return []
        m = len(pat)
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j
        res = []
        j = 0
        for i, ch in enumerate(text):
            while j > 0 and ch != pat[j]:
                j = pi[j - 1]
            if ch == pat[j]:
                j += 1
            if j == m:
                res.append(i - m + 1)
                j = pi[j - 1]
        return res

    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        first = p.find('*')
        second = p.find('*', first + 1)
        L = p[:first]
        M = p[first + 1:second]
        R = p[second + 1:]

        if not L and not R:
            return 0

        left = self._kmp_occurrences(s, L) if L else []
        mid = self._kmp_occurrences(s, M) if M else []
        right = self._kmp_occurrences(s, R) if R else []

        INF = n + 1
        ans = INF

        if not M:
            if L and R:
                i = j = 0
                while i < len(left) and j < len(right):
                    l_start = left[i]
                    while j < len(right) and right[j] < l_start + len(L):
                        j += 1
                    if j == len(right):
                        break
                    r_start = right[j]
                    ans = min(ans, (r_start + len(R)) - l_start)
                    i += 1
            elif L:
                if left:
                    ans = min(ans, len(L))
            elif R:
                if right:
                    ans = min(ans, len(R))
            return ans if ans <= n else -1

        if L and R:
            i = j = k = 0
            while i < len(left):
                l_start = left[i]
                while j < len(mid) and mid[j] < l_start + len(L):
                    j += 1
                if j == len(mid):
                    break
                m_start = mid[j]
                while k < len(right) and right[k] < m_start + len(M):
                    k += 1
                if k == len(right):
                    break
                r_start = right[k]
                ans = min(ans, (r_start + len(R)) - l_start)
                i += 1
        elif L:
            i = j = 0
            while i < len(left) and j < len(mid):
                l_start = left[i]
                while j < len(mid) and mid[j] < l_start + len(L):
                    j += 1
                if j == len(mid):
                    break
                m_start = mid[j]
                ans = min(ans, (m_start + len(M)) - l_start)
                i += 1
        elif R:
            i = j = 0
            while i < len(mid) and j < len(right):
                m_start = mid[i]
                while j < len(right) and right[j] < m_start + len(M):
                    j += 1
                if j == len(right):
                    break
                r_start = right[j]
                ans = min(ans, (r_start + len(R)) - m_start)
                i += 1
        else:
            if mid:
                ans = min(ans, len(M))

        return ans if ans <= n else -1