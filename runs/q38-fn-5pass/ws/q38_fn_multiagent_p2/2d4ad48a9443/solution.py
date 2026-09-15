from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        # Prefix sums for fast range-sum queries.
        pref = [0] * (n + 1)
        for i, v in enumerate(nums):
            pref[i + 1] = pref[i] + v

        # nxt[i] = first index j > i with nums[j] > nums[i], or n if none.
        # Strictly greater is required because equal values do not raise the prefix maximum.
        nxt = [n] * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            v = nums[i]
            while stack and nums[stack[-1]] <= v:
                stack.pop()
            if stack:
                nxt[i] = stack[-1]
            stack.append(i)
        del stack

        # cost0[i] is the full cost of the record segment [i, nxt[i] - 1],
        # where the prefix maximum is nums[i].
        cost0 = array('q', [0]) * (n + 1)
        for i in range(n):
            j = nxt[i]
            cost0[i] = nums[i] * (j - i) - (pref[j] - pref[i])

        # Binary lifting over the next-greater chain.
        # up[j][i] = node reached after 2^j next-greater jumps from i.
        # jumpcost[j][i] = sum of full segment costs for those 2^j jumps.
        LOG = (n + 1).bit_length()
        size = n + 1
        up = [nxt]
        jumpcost = [cost0]

        for _ in range(1, LOG):
            prev_up = up[-1]
            prev_cost = jumpcost[-1]

            up.append([prev_up[prev_up[i]] for i in range(size)])

            cur_cost = array('q', [0]) * size
            pc = prev_cost
            cc = cur_cost
            pu = prev_up
            for i, mid in enumerate(pu):
                cc[i] = pc[i] + pc[mid]

            jumpcost.append(cur_cost)

        # Store levels from high to low for query speed.
        levels = [(up[j], jumpcost[j]) for j in range(LOG - 1, -1, -1)]
        del up, jumpcost

        def valid(l: int, r: int, levels=levels, nums=nums, pref=pref, k=k) -> bool:
            """Return True iff minimum operations for nums[l..r] <= k."""
            cur = l
            total = 0

            # Jump over complete record segments whose next record is still <= r.
            for upj, costj in levels:
                nxt_node = upj[cur]
                if nxt_node <= r:
                    total += costj[cur]
                    if total > k:
                        return False
                    cur = nxt_node

            # Add the final partial record segment [cur, r].
            total += nums[cur] * (r - cur + 1) - (pref[r + 1] - pref[cur])
            return total <= k

        ans = 0
        left = 0

        # For fixed right, cost(l, right) is non-increasing as l increases.
        # For fixed left, cost(left, right) is non-decreasing as right increases.
        for right in range(n):
            while left <= right and not valid(left, right):
                left += 1
            ans += right - left + 1

        return ans