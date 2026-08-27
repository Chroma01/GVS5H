class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        c = [0] * 26
        for ch in s:
            c[ord(ch) - 97] += 1

        # Baseline: delete everything (k = 0), cost = n.
        ans = n

        # For target frequency k, each letter's final count f[i] is 0 or k.
        # Base cost = sum |c[i] - f[i]|; a change i -> i+1 (cost 1) beats
        # delete+insert (cost 2), saving 1 per matched adjacent
        # (surplus at i, deficit at i+1) pair. Longer chains cost >= 2 and
        # are never better than delete+insert, so only adjacent savings matter.
        # DP over 26 letters x 2 states per k.
        for k in range(1, 2 * n + 1):
            NEG = float('inf')
            # dp[q] = min cost for processed letters, last letter has f = q*k
            dp = [NEG, NEG]
            prev_sur = [0, 0]
            for i in range(26):
                ci = c[i]
                # stats for choice q: f = q*k
                base0 = ci            # f = 0: delete all ci
                sur0 = ci
                base1 = abs(ci - k)   # f = k
                sur1 = ci - k if ci > k else 0
                def1 = k - ci if ci < k else 0

                if dp[0] == NEG:
                    # first letter (i == 0)
                    dp = [base0, base1]
                    prev_sur = [sur0, sur1]
                    continue

                # choose f[i] = 0 (deficit 0)
                best0 = dp[0] - min(prev_sur[0], 0)
                if dp[1] - min(prev_sur[1], 0) < best0:
                    best0 = dp[1] - min(prev_sur[1], 0)
                # min(x, 0) is always 0, so simplify:
                best0 = dp[0] if dp[0] < dp[1] else dp[1]

                # choose f[i] = k (deficit def1)
                b0 = dp[0] - (prev_sur[0] if prev_sur[0] < def1 else def1)
                b1 = dp[1] - (prev_sur[1] if prev_sur[1] < def1 else def1)
                best1 = b0 if b0 < b1 else b1

                dp = [best0 + base0, best1 + base1]
                prev_sur = [sur0, sur1]

            cand = dp[0] if dp[0] < dp[1] else dp[1]
            if cand < ans:
                ans = cand

        return ans