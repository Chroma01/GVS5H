class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        ans = n

        for f in range(1, n + 1):
            # dp0: minimum cost for processed prefix if current letter is removed.
            # dp1: minimum cost for processed prefix if current letter is kept.
            dp0 = cnt[0]
            dp1 = abs(cnt[0] - f)

            for i in range(1, 26):
                c = cnt[i]
                prev = cnt[i - 1]

                # Current letter is absent in the final string.
                ndp0 = (dp0 if dp0 < dp1 else dp1) + c

                # Current letter is present with frequency f.
                cost1 = abs(c - f)
                deficit = f - c
                if deficit < 0:
                    deficit = 0

                # Previous letter absent: all its original characters are surplus.
                save0 = prev if prev < deficit else deficit

                # Previous letter present: only characters beyond f are surplus.
                surplus = prev - f
                if surplus < 0:
                    surplus = 0
                save1 = surplus if surplus < deficit else deficit

                v0 = dp0 + cost1 - save0
                v1 = dp1 + cost1 - save1
                ndp1 = v0 if v0 < v1 else v1

                dp0, dp1 = ndp0, ndp1

            if dp0 < ans:
                ans = dp0
            if dp1 < ans:
                ans = dp1

            if ans == 0:
                return 0

        return ans