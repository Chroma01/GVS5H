class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        if n == 0:
            return 0

        # Keeping only the most frequent letter at its current frequency costs
        # at most n - 1, so the all-deleted cost n is only a safe upper bound.
        ans = n

        for f in range(1, n + 1):
            # dp0: minimum cost up to previous letter if previous letter is absent
            # dp1: minimum cost up to previous letter if previous letter is present
            dp0 = cnt[0]
            dp1 = abs(cnt[0] - f)

            for i in range(1, 26):
                c = cnt[i]
                pc = cnt[i - 1]

                # Node costs for current letter.
                cost0 = c              # absent: delete all original occurrences
                cost1 = abs(c - f)     # present: adjust to exactly f

                # If current letter is absent, it has no deficit, so no incoming
                # change can save an operation.
                new0 = min(dp0, dp1) + cost0

                # If current letter is present, it may have a deficit that can be
                # filled by changing surplus characters from the previous letter.
                deficit = f - c
                if deficit < 0:
                    deficit = 0

                # Previous letter absent: all pc characters are surplus.
                save0 = pc if pc < deficit else deficit

                # Previous letter present: only characters above f are surplus.
                prev_surplus = pc - f
                if prev_surplus < 0:
                    prev_surplus = 0
                save1 = prev_surplus if prev_surplus < deficit else deficit

                new1 = min(dp0 - save0, dp1 - save1) + cost1

                dp0, dp1 = new0, new1

            ans = min(ans, dp0, dp1)

        return ans