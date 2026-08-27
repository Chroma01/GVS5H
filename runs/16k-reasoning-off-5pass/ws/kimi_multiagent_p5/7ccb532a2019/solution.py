class Solution:
    def makeStringGood(self, s: str) -> int:
        c = [0] * 26
        for ch in s:
            c[ord(ch) - 97] += 1

        ans = len(s)  # delete everything (empty string is vacuously good)

        # For a fixed target uniform count k, the optimal final string keeps a
        # subset S of letters at exactly k occurrences. Moving a character is
        # only strictly beneficial to an adjacent letter (distance 1 costs 1
        # and saves a delete+insert pair costing 2; distance >= 2 never helps).
        # So for fixed k:
        #   cost(S) = sum_i g_i(t_i) - sum_{i=0..24} min(surplus_i, deficit_{i+1})
        # which is a chain energy solvable by a 2-state DP over the 26 letters.
        # Optimal k never exceeds max(c) (beyond it every included letter only
        # needs more insertions and no surplus exists), so scan k = 1..max(c).

        for k in range(1, max(c) + 1):
            c0 = c[0]
            dp0 = c0                           # letter 0 excluded: delete all its chars
            dp1 = c0 - k if c0 >= k else k - c0  # letter 0 included: |c0 - k|
            sp0 = c0                           # surplus when excluded
            sp1 = c0 - k if c0 > k else 0      # surplus when included
            for i in range(1, 26):
                ci = c[i]
                g0 = ci                                  # exclude: delete ci chars
                g1 = ci - k if ci >= k else k - ci       # include: |ci - k|
                d1 = k - ci if k > ci else 0             # deficit when included
                # Exclude letter i: deficit is 0, so no edge saving possible.
                nd0 = g0 + (dp0 if dp0 < dp1 else dp1)
                # Include letter i: previous surplus can fill its deficit,
                # saving min(prev_surplus, d1) operations.
                a = dp0 - (sp0 if sp0 < d1 else d1)
                b = dp1 - (sp1 if sp1 < d1 else d1)
                nd1 = g1 + (a if a < b else b)
                dp0, dp1 = nd0, nd1
                sp0 = ci
                sp1 = ci - k if ci > k else 0
            m = dp0 if dp0 < dp1 else dp1
            if m < ans:
                ans = m

        return ans