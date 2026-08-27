class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1
        n = len(s)
        ans = n  # delete everything (also covered by all f_i = 0 in any k's DP)

        # For a fixed target frequency k, each letter is either unused (f=0,
        # final count 0) or used (f=1, final count k).
        #   cost_i(0) = cnt[i]            (delete all)
        #   cost_i(1) = |cnt[i] - k|      (delete surplus / insert deficit)
        # Shifting is only ever useful one step (i -> i+1): a j-step shift costs
        # j >= delete+insert (=2), so multi-step shifts never strictly help.
        # A one-step shift of x chars from i to i+1 saves x deletions at i and
        # x insertions at i+1 while costing x shifts => net saving x, where
        #   x <= min(surplus_i, deficit_{i+1}),
        #   surplus_i = cnt[i] if f_i=0 else max(0, cnt[i]-k),
        #   deficit_i = 0      if f_i=0 else max(0, k-cnt[i]).
        # Shifting into an unused letter or beyond a deficit is never better
        # than deleting at the source, so edges are independent given the
        # f-pattern, and the best x is exactly min(surplus_i, deficit_{i+1}).
        # This gives a chain DP with binary state per letter: O(26) per k.

        for k in range(1, n + 1):
            # dp0/dp1: min cost for processed prefix, previous letter unused/used.
            # Letter 0 ('a') has no incoming edge.
            dp0 = cnt[0]               # f=0: delete all of letter 0
            dp1 = abs(cnt[0] - k)      # f=1: adjust to exactly k
            prev_c = cnt[0]
            for i in range(1, 26):
                c = cnt[i]
                a0 = c                 # cost if letter i unused
                a1 = c - k if c >= k else k - c  # cost if letter i used
                d1 = k - c if k > c else 0       # deficit if used (d0 = 0)
                # surplus of previous letter under each of its states
                s0 = prev_c
                s1 = prev_c - k if prev_c > k else 0
                # edge saving = min(prev surplus, current deficit); deficit of
                # an unused letter is 0, so min(s, 0) = 0.
                ndp0 = a0 + (dp0 if dp0 < dp1 else dp1)
                # used current letter: saving min(s0, d1) or min(s1, d1)
                save0 = s0 if s0 < d1 else d1
                save1 = s1 if s1 < d1 else d1
                cand0 = dp0 - save0
                cand1 = dp1 - save1
                ndp1 = a1 + (cand0 if cand0 < cand1 else cand1)
                dp0, dp1 = ndp0, ndp1
                prev_c = c
            best = dp0 if dp0 < dp1 else dp1
            if best < ans:
                ans = best
        return ans