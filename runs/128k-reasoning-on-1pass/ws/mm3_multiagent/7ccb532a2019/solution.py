class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - 97] += 1
        max_f = max(freq)
        ans = n  # delete everything

        # Try every possible target frequency k (1 … max_f)
        for k in range(1, max_f + 1):
            # cost[l][r] = minimal ops to make interval [l,r] good with target k
            cost = [[0] * 26 for _ in range(26)]
            for l in range(26):
                carry = 0          # excess that can be moved right
                baseline = 0       # sum of |freq[i] - k|
                flow = 0           # amount of excess used to cover deficits
                for r in range(l, 26):
                    diff = freq[r] - k
                    baseline += abs(diff)
                    if diff >= 0:
                        carry += diff
                    else:
                        need = -diff
                        used = carry if carry < need else need
                        flow += used
                        carry -= used
                    cost[l][r] = baseline - flow

            # DP over letters: dp[i] = minimal cost for letters 0..i
            dp = [0] * 26
            prev_dp = 0  # represents dp[-1] = 0
            for i in range(26):
                # Option 1: delete letter i (cost = freq[i])
                best = prev_dp + freq[i]
                # Option 2: make some interval [j..i] good with target k
                for j in range(i + 1):
                    interval_cost = cost[j][i]
                    prev = 0 if j == 0 else dp[j - 1]
                    total = prev + interval_cost
                    if total < best:
                        best = total
                dp[i] = best
                prev_dp = best
            ans = min(ans, dp[25])
            if ans == 0:          # cannot improve further
                break
        return ans