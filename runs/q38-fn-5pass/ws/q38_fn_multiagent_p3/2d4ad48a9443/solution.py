from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k + 1

        # Prefix sums of original elements.
        pref = [0] * (n + 1)
        for i, x in enumerate(nums):
            pref[i + 1] = pref[i] + x

        # nxt[i] = first index to the right with nums[nxt[i]] > nums[i],
        # or n if none exists.
        nxt = array('i', [n]) * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] <= x:
                stack.pop()
            if stack:
                nxt[i] = stack[-1]
            stack.append(i)
        stack = None

        # Binary lifting tables.
        # up[t][i] = 2^t-th next-greater record from i.
        # sum_cost[t][i] = sum of full-block costs for those 2^t jumps,
        # capped at k + 1.
        LOG = (n + 1).bit_length()
        up = [nxt]

        sum0 = array('q', [0]) * (n + 1)
        for i in range(n):
            q = nxt[i]
            if q < n:
                # Full block [i, q) has running maximum nums[i].
                val = nums[i] * (q - i) - (pref[q] - pref[i])
                if val > limit:
                    val = limit
                sum0[i] = val
        sum_cost = [sum0]

        for _ in range(1, LOG):
            prev_up = up[-1]
            prev_sum = sum_cost[-1]

            curr_up = [n] * (n + 1)
            curr_sum = array('q', [0]) * (n + 1)

            for i in range(n):
                mid = prev_up[i]
                curr_up[i] = prev_up[mid]

                s = prev_sum[i] + prev_sum[mid]
                if s > limit:
                    s = limit
                curr_sum[i] = s

            up.append(curr_up)
            sum_cost.append(curr_sum)

        # Iterate levels from high to low during queries.
        levels = list(zip(up, sum_cost))
        levels.reverse()

        ans = 0
        left = 0

        for r in range(n):
            pref_r1 = pref[r + 1]

            # Single-element subarrays are always feasible, so only query
            # while left < r.
            while left < r:
                cur = left
                total = 0

                # Sum full record blocks that are completely inside [left, r].
                for up_t, sum_t in levels:
                    nxt_cur = up_t[cur]
                    if nxt_cur <= r:
                        total += sum_t[cur]
                        if total > k:
                            break
                        cur = nxt_cur

                if total > k:
                    left += 1
                    continue

                # Last record contributes a partial block [cur, r].
                cost = total + nums[cur] * (r - cur + 1) - (pref_r1 - pref[cur])

                if cost <= k:
                    break

                left += 1

            ans += r - left + 1

        return ans