from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k - 1                     # maximal allowed a+b (length = a+b+1)

        # ---------- previous strictly smaller (for minimum) ----------
        prev_less = [-1] * n
        st = []
        for i in range(n):
            # pop while top value >= current to keep a strictly increasing stack
            while st and nums[st[-1]] >= nums[i]:
                st.pop()
            prev_less[i] = st[-1] if st else -1
            st.append(i)

        # ---------- next smaller-or-equal (for minimum) ----------
        next_le = [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            # pop while top value > current to find first <=
            while st and nums[st[-1]] > nums[i]:
                st.pop()
            next_le[i] = st[-1] if st else n
            st.append(i)

        # ---------- previous strictly greater (for maximum) ----------
        prev_greater = [-1] * n
        st = []
        for i in range(n):
            # pop while top value <= current to keep a strictly decreasing stack
            while st and nums[st[-1]] <= nums[i]:
                st.pop()
            prev_greater[i] = st[-1] if st else -1
            st.append(i)

        # ---------- next greater-or-equal (for maximum) ----------
        next_ge = [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            # pop while top value < current to find first >=
            while st and nums[st[-1]] < nums[i]:
                st.pop()
            next_ge[i] = st[-1] if st else n
            st.append(i)

        # ----- helper: count (a,b) with a in [0,A-1], b in [0,B-1], a+b <= limit -----
        def count_pairs(A: int, B: int) -> int:
            # only the first limit+1 values of a can ever be used
            A_prime = A if A <= limit + 1 else limit + 1
            if B >= limit + 1:
                # min(B, limit-a+1) = limit-a+1 for all a
                return A_prime * (limit + 1) - (A_prime * (A_prime - 1)) // 2
            else:
                t = limit - (B - 1)          # largest a with cnt(a) = B
                region1_len = t + 1          # number of a with cnt(a) = B
                if region1_len >= A_prime:
                    return A_prime * B
                else:
                    total = region1_len * B
                    rem = A_prime - region1_len   # remaining a values
                    # sum of a from region1_len to A_prime-1
                    sum_a = (region1_len + (A_prime - 1)) * rem // 2
                    total += rem * (limit + 1) - sum_a
                    return total

        ans = 0
        for i in range(n):
            left_min = i - prev_less[i]
            right_min = next_le[i] - i
            left_max = i - prev_greater[i]
            right_max = next_ge[i] - i

            cnt_min = count_pairs(left_min, right_min)
            cnt_max = count_pairs(left_max, right_max)

            ans += nums[i] * (cnt_min + cnt_max)

        return ans


# Simple test harness
if __name__ == "__main__":
    sol = Solution()
    # Example 1
    print(sol.minMaxSubarraySum([1, 2, 3], 2))      # expected 20
    # Example 2
    print(sol.minMaxSubarraySum([1, -3, 1], 2))   # expected -6