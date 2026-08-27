class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        ans = n  # fallback: delete everything

        # For a target uniform frequency k, each letter is either:
        #   used   -> final count k: deletions = max(0, c-k), insertions = max(0, k-c)
        #   unused -> final count 0: deletions = c, insertions = 0
        # Base cost = total deletions + total insertions.
        # Changing letter i -> i+1 (cost 1) replaces delete@i + insert@i+1 (cost 2),
        # saving 1. Changes over distance >= 2 cost >= delete+insert, so only
        # adjacent changes matter. Total saving = sum_i min(del[i], ins[i+1]).
        # DP over 26 letters; state = choice (unused/used) of previous letter,
        # which determines its deletion count for the matching term.

        for k in range(1, max(cnt) + 1):
            # options[j][choice] = (deletions, insertions)
            options = [
                ((c, 0), (c - k if c > k else 0, k - c if k > c else 0))
                for c in cnt
            ]

            INF = float('inf')
            d, ins = options[0][0]
            dp0 = d + ins
            d, ins = options[0][1]
            dp1 = d + ins

            for j in range(1, 26):
                ndp0 = ndp1 = INF
                pd0 = options[j - 1][0][0]  # deletions of prev letter if unused
                pd1 = options[j - 1][1][0]  # deletions of prev letter if used
                for choice in (0, 1):
                    d, ins = options[j][choice]
                    base = d + ins
                    v0 = dp0 + base - min(pd0, ins)
                    v1 = dp1 + base - min(pd1, ins)
                    best = v0 if v0 < v1 else v1
                    if choice == 0:
                        ndp0 = best
                    else:
                        ndp1 = best
                dp0, dp1 = ndp0, ndp1

            cur = dp0 if dp0 < dp1 else dp1
            if cur < ans:
                ans = cur

        return ans