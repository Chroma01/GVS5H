from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)

        # Split p into pre, mid, post at the two '*'
        first = p.index('*')
        second = p.index('*', first + 1)
        pre = p[:first]
        mid = p[first + 1:second]
        post = p[second + 1:]

        lp, lm, lq = len(pre), len(mid), len(post)

        def occurrences(pat: str):
            """Sorted list of start indices where pat occurs in s.
               Empty pattern matches at every position 0..n."""
            m = len(pat)
            if m == 0:
                return list(range(n + 1))
            if m > n:
                return []
            # KMP prefix function
            pi = [0] * m
            k = 0
            for i in range(1, m):
                while k > 0 and pat[i] != pat[k]:
                    k = pi[k - 1]
                if pat[i] == pat[k]:
                    k += 1
                pi[i] = k
            res = []
            k = 0
            for i, ch in enumerate(s):
                while k > 0 and ch != pat[k]:
                    k = pi[k - 1]
                if ch == pat[k]:
                    k += 1
                if k == m:
                    res.append(i - m + 1)
                    k = pi[k - 1]
            return res

        pre_occ = occurrences(pre)
        mid_occ = occurrences(mid)
        post_occ = occurrences(post)

        if not pre_occ or not mid_occ or not post_occ:
            return -1

        ans = None
        M = len(mid_occ)
        Q = len(post_occ)
        for a in pre_occ:
            # earliest mid occurrence starting at >= a + len(pre)
            mi = bisect_left(mid_occ, a + lp)
            if mi == M:
                break  # mid_occ sorted; larger a won't help
            mstart = mid_occ[mi]
            # earliest post occurrence starting at >= mstart + len(mid)
            qi = bisect_left(post_occ, mstart + lm)
            if qi == Q:
                break  # no post occurrence can fit for this or later a
            qstart = post_occ[qi]
            cand = qstart + lq - a
            if ans is None or cand < ans:
                ans = cand
            if ans == lp + lm + lq:
                break  # cannot do better than the literal total length

        return ans if ans is not None else -1