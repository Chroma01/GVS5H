class Solution:
    def makeStringGood(self, s: str) -> int:
        c = [0] * 26
        for ch in s:
            c[ord(ch) - 97] += 1
        n = len(s)
        ans = n  # delete everything (empty string is vacuously good)
        INF = float('inf')

        # Key fact: moving a char forward d >= 2 steps via increments costs d,
        # while delete+insert achieves the same relocation in 2 ops. So WLOG the
        # only relocations used are single-step increments (cost 1) and
        # delete+insert pairs (cost 2). A moved char is used at its destination
        # (moving then deleting/re-moving is never strictly better).
        #
        # For a fixed target frequency k, choose a set S of active letters, each
        # ending with exactly k chars. Baseline cost = n (delete all) + |S|*k
        # (insert all). A char kept at its own letter saves 2; a char moved one
        # step into an active neighbor saves 1. Kept chars are prioritized
        # (save 2 > 1), so for active letter i: kept = min(c[i], k), and
        # in-move = min(avail_{i-1}, k - kept), where avail_{i-1} =
        # c[i-1] - min(c[i-1], k) if i-1 active, else c[i-1] (all its chars).
        # Contribution of active letter i: k - 2*kept - in_move.
        # This depends only on whether the previous letter is active -> 2-state DP.
        for k in range(1, n + 1):
            dp0, dp1 = 0, INF  # min extra cost so far; prev letter inactive/active
            for i in range(26):
                ci = c[i]
                kept = ci if ci < k else k
                rem = k - kept
                cost_active = k - 2 * kept
                if i == 0:
                    in0 = in1 = 0  # no previous letter
                else:
                    pc = c[i - 1]
                    in0 = pc if pc < rem else rem                       # prev inactive
                    pa = pc - k
                    if pa < 0:
                        pa = 0
                    in1 = pa if pa < rem else rem                       # prev active
                ndp0 = dp0 if dp0 < dp1 else dp1                        # i inactive
                a = dp0 + cost_active - in0
                b = dp1 + cost_active - in1
                ndp1 = a if a < b else b                                # i active
                dp0, dp1 = ndp0, ndp1
            total = n + (dp0 if dp0 < dp1 else dp1)
            if total < ans:
                ans = total
        return ans