from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        LOG = max(1, n.bit_length())

        # up[p][i] = index reached after 2^p "next strictly greater" jumps from i
        # path_sum[p][i] = total full contribution of those 2^p record segments
        up = [[n] * (n + 1) for _ in range(LOG)]
        path_sum = [array('q', [0]) * (n + 1) for _ in range(LOG)]

        # Base level: next strictly greater element to the right.
        # Equal values are popped, so the jump is strictly greater.
        up0 = up[0]
        path0 = path_sum[0]
        stack = []
        for i in range(n - 1, -1, -1):
            ai = nums[i]
            while stack and nums[stack[-1]] <= ai:
                stack.pop()
            j = stack[-1] if stack else n
            up0[i] = j
            path0[i] = ai * (j - i)
            stack.append(i)

        # Binary lifting table.
        for p in range(1, LOG):
            prev_up = up[p - 1]
            prev_path = path_sum[p - 1]
            cur_up = up[p]
            cur_path = path_sum[p]
            for i in range(n):
                mid = prev_up[i]
                cur_up[i] = prev_up[mid]
                cur_path[i] = prev_path[i] + prev_path[mid]
            # Sentinel n remains up=n and path_sum=0.

        # Prefix sums of original elements.
        pref = [0] * (n + 1)
        s = 0
        for i, x in enumerate(nums):
            s += x
            pref[i + 1] = s

        levels = list(zip(up[::-1], path_sum[::-1]))
        nums_local = nums
        pref_local = pref

        def cost(l: int, r: int) -> int:
            """Minimum operations to make nums[l..r] non-decreasing."""
            i = l
            total_max_sum = 0

            # Jump over complete record segments whose next record is <= r.
            for up_p, path_p in levels:
                ni = up_p[i]
                if ni <= r:
                    total_max_sum += path_p[i]
                    i = ni

            # Last record is truncated at r.
            total_max_sum += nums_local[i] * (r + 1 - i)

            element_sum = pref_local[r + 1] - pref_local[l]
            return total_max_sum - element_sum

        ans = 0
        r = -1

        # For each left endpoint, valid right endpoints form a prefix.
        # The maximal valid r is non-decreasing as l increases.
        for l in range(n):
            if r < l:
                r = l - 1
            while r + 1 < n and cost(l, r + 1) <= k:
                r += 1
            ans += r - l + 1

        return ans


def _brute(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0
    for l in range(n):
        mx = 0
        sum_max = 0
        sum_elem = 0
        for r in range(l, n):
            x = nums[r]
            if x > mx:
                mx = x
            sum_max += mx
            sum_elem += x
            if sum_max - sum_elem <= k:
                ans += 1
    return ans


if __name__ == "__main__":
    import random

    sol = Solution()

    # Given examples.
    assert sol.countNonDecreasingSubarrays([6, 3, 1, 2, 4, 4], 7) == 17
    assert sol.countNonDecreasingSubarrays([6, 3, 1, 3, 6], 4) == 12

    # Deterministic edge cases.
    assert sol.countNonDecreasingSubarrays([1, 1, 1], 0) == 6
    assert sol.countNonDecreasingSubarrays([1, 2, 3], 0) == 6
    assert sol.countNonDecreasingSubarrays([3, 2, 1], 1) == 5

    # Random small verification against brute force.
    random.seed(12345)
    for _ in range(300):
        n = random.randint(1, 8)
        nums = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(0, 20)
        expected = _brute(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != expected:
            raise AssertionError((nums, k, got, expected))

    for _ in range(20):
        n = random.randint(1, 60)
        nums = [random.randint(1, 100) for _ in range(n)]
        k = random.randint(0, 1000)
        expected = _brute(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != expected:
            raise AssertionError((nums, k, got, expected))