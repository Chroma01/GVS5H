from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums for fast segment sums.
        ps = [0] * (n + 1)
        for i, x in enumerate(nums):
            ps[i + 1] = ps[i] + x

        # nxt[i] = nearest index to the right with nums[nxt[i]] > nums[i],
        # or n if none exists. Sentinel n points to itself.
        nxt = [n] * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] <= x:
                stack.pop()
            if stack:
                nxt[i] = stack[-1]
            stack.append(i)
        nxt[n] = n
        del stack

        # pref[i] = total full-segment cost from i to the sentinel n
        # along the next-greater chain.
        pref = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            j = nxt[i]
            pref[i] = nums[i] * (j - i) - (ps[j] - ps[i]) + pref[j]

        # The whole array has cost at least as large as any subarray.
        if pref[0] <= k:
            return n * (n + 1) // 2

        # Binary lifting over the next-greater chain.
        LOG = (n + 1).bit_length()
        up = [nxt]
        rng = range(n + 1)
        for _ in range(1, LOG):
            prev = up[-1]
            up.append([prev[prev[i]] for i in rng])

        up_rev = up[::-1]

        # Cost of half-open interval [l, R), compared with limit k.
        def cost_leq(l, R, limit=k, up_rev=up_rev, pref=pref, ps=ps, nums=nums):
            cur = l
            pref_l = pref[l]

            # Farthest chain ancestor with index <= R.
            for level in up_rev:
                anc = level[cur]
                if anc <= R:
                    cur = anc

            # Full chain segments from l up to cur.
            total = pref_l - pref[cur]
            if total > limit:
                return False

            # Partial segment from cur to R, where nums[cur] is the running max.
            if cur < R:
                total += nums[cur] * (R - cur) - (ps[R] - ps[cur])

            return total <= limit

        ans = 0
        e = 0  # exclusive end of the current valid window
        cost = cost_leq

        for l in range(n):
            if e < l:
                e = l

            while e < n and cost(l, e + 1):
                e += 1

            ans += e - l

        return ans