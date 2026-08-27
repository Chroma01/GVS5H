from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        # Monotonic deque of blocks [value, count]:
        # the prefix-max sequence over the current window is non-decreasing,
        # so it can be represented as blocks of equal values; block values are
        # strictly increasing from front to back.
        dq = deque()
        S = 0  # sum of prefix maxima over the window
        W = 0  # sum of elements in the window
        l = 0
        for r in range(n):
            x = nums[r]
            # Push x at the right: all trailing elements whose previous prefix
            # max <= x now have prefix max x (plus the new element itself).
            cnt = 1
            removed_sum = 0
            while dq and dq[-1][0] <= x:
                v, c = dq.pop()
                cnt += c
                removed_sum += v * c
            dq.append([x, cnt])
            S += x * cnt - removed_sum
            W += x

            # Shrink from the left while cost = S - W exceeds k.
            while l <= r and S - W > k:
                y = nums[l]
                W -= y
                front = dq[0]
                S -= front[0]
                front[1] -= 1
                if front[1] == 0:
                    dq.popleft()
                l += 1

            # All subarrays ending at r starting in [l, r] are valid.
            ans += r - l + 1
        return ans


# ---------------- verification harness ----------------
def brute(nums, k):
    n = len(nums)
    ans = 0
    for l in range(n):
        run = 0
        cost = 0
        for r in range(l, n):
            if nums[r] < run:
                cost += run - nums[r]
            else:
                run = nums[r]
            if cost <= k:
                ans += 1
    return ans


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([6, 3, 1, 2, 4, 4], 7, 17),   # example 1
        ([6, 3, 1, 3, 6], 4, 12),      # example 2
        ([5], 0, 1),                   # n = 1
        ([1, 2, 3, 4, 5], 0, 15),      # strictly increasing -> all subarrays
        ([5, 4, 3, 2, 1], 0, 5),       # strictly decreasing, k=0 -> singletons
        ([10**9, 1, 10**9], 10**9, 6), # large values, k just enough
        ([10**9, 1, 10**9], 10**9 - 1, 5),  # [1e9,1,1e9] costs 1e9-1+1e9-1? no: 1e9-1 then 0 -> valid; [1e9,1] costs 1e9-1 > k -> invalid
        ([3, 3, 3], 0, 6),             # all equal
    ]
    for nums, k, expected in tests:
        got = sol.countNonDecreasingSubarrays(nums, k)
        bf = brute(nums, k)
        assert got == expected == bf, (nums, k, got, expected, bf)
        print(f"nums={nums}, k={k} -> {got} (expected {expected}) OK")

    # randomized cross-check against brute force
    import random
    random.seed(0)
    for _ in range(2000):
        n = random.randint(1, 12)
        nums = [random.randint(1, 20) for _ in range(n)]
        k = random.randint(0, 50)
        got = sol.countNonDecreasingSubarrays(nums, k)
        bf = brute(nums, k)
        assert got == bf, (nums, k, got, bf)
    print("All randomized tests passed.")