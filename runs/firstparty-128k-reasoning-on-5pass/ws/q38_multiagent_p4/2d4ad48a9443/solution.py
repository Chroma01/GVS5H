from typing import List
from array import array
import random


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # 1-indexed prefix sums of original values.
        prefix = array('q', [0]) * (n + 1)
        s = 0
        for i, x in enumerate(nums, 1):
            s += x
            prefix[i] = s

        # ng[i] = nearest index j > i with nums[j] > nums[i], or n if none.
        ng = array('i', [n]) * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            xi = nums[i]
            while stack and nums[stack[-1]] <= xi:
                stack.pop()
            if stack:
                ng[i] = stack[-1]
            stack.append(i)

        log = (n + 1).bit_length()
        up = [None] * log
        sum_w = [None] * log

        # Level 0: one next record.
        up[0] = ng
        sum_w[0] = array('q', [0]) * (n + 1)
        sw0 = sum_w[0]
        for i in range(n):
            j = ng[i]
            if j < n:
                sw0[i] = nums[i] * (j - i)
        del ng, stack

        # Binary lifting tables.
        for t in range(1, log):
            prev_up = up[t - 1]
            prev_sum = sum_w[t - 1]
            curr_up = array('i', [0]) * (n + 1)
            curr_sum = array('q', [0]) * (n + 1)
            for i, mid in enumerate(prev_up):
                curr_up[i] = prev_up[mid]
                curr_sum[i] = prev_sum[i] + prev_sum[mid]
            up[t] = curr_up
            sum_w[t] = curr_sum

        # Prebind levels in high-to-low order for the cost oracle.
        levels = tuple(zip(reversed(up), reversed(sum_w)))

        def cost(l: int, r: int, nums_local=nums, prefix_local=prefix, levels=levels) -> int:
            cur = l
            total = 0

            # Jump through complete record blocks that end at or before r.
            for up_t, sum_t in levels:
                nxt = up_t[cur]
                if nxt <= r:
                    total += sum_t[cur]
                    cur = nxt

            # cur is the last record <= r; clip its contribution at r.
            total += nums_local[cur] * (r + 1 - cur)
            return total - (prefix_local[r + 1] - prefix_local[l])

        ans = 0
        left = 0
        cost_fn = cost

        # For each right endpoint, valid left endpoints form a suffix.
        for right in range(n):
            while left <= right and cost_fn(left, right) > k:
                left += 1
            ans += right - left + 1

        return ans


def brute_count(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0
    for l in range(n):
        mx = 0
        ops = 0
        for r in range(l, n):
            if nums[r] > mx:
                mx = nums[r]
            ops += mx - nums[r]
            if ops <= k:
                ans += 1
            else:
                # For fixed l, cost is nondecreasing as r grows.
                break
    return ans


if __name__ == "__main__":
    sol = Solution()

    print(sol.countNonDecreasingSubarrays([6, 3, 1, 2, 4, 4], 7))
    print(sol.countNonDecreasingSubarrays([6, 3, 1, 3, 6], 4))

    edge_cases = [
        [1], [1, 1], [2, 1], [1, 2], [2, 2, 1], [1, 2, 2, 1], [3, 1, 2, 1, 3]
    ]
    for nums in edge_cases:
        for k in (0, 1, 2, 5, 100):
            if brute_count(nums, k) != sol.countNonDecreasingSubarrays(nums, k):
                print("FAIL", nums, k)
                raise SystemExit(1)
    print("edge ok")

    big_inc = list(range(1, 1001))
    if sol.countNonDecreasingSubarrays(big_inc, 1) != 1000 * 1001 // 2:
        print("FAIL big increasing")
        raise SystemExit(1)

    big_dec = list(range(1000, 0, -1))
    if sol.countNonDecreasingSubarrays(big_dec, 0) != 1000:
        print("FAIL big decreasing k=0")
        raise SystemExit(1)
    if sol.countNonDecreasingSubarrays(big_dec, 10**9) != 1000 * 1001 // 2:
        print("FAIL big decreasing large k")
        raise SystemExit(1)
    print("big sanity ok")

    random.seed(12345)

    for _ in range(300):
        n = random.randint(1, 8)
        nums = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(0, 20)
        expected = brute_count(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if expected != got:
            print("FAIL", nums, k, expected, got)
            raise SystemExit(1)
    print("small random ok")

    for _ in range(20):
        n = random.randint(1, 200)
        nums = [random.randint(1, 1000) for _ in range(n)]
        k = random.randint(0, 10000)
        expected = brute_count(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if expected != got:
            print("FAIL", n, k, expected, got)
            raise SystemExit(1)
    print("moderate random ok")