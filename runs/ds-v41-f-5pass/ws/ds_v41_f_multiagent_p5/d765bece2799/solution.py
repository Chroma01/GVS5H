from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def sum_of_mins(arr):
            n = len(arr)

            # left[i]: number of consecutive strictly-greater values directly
            # to the left of i (stop at first value <= arr[i]).
            left = [0] * n
            st = []
            for i in range(n):
                v = arr[i]
                while st and arr[st[-1]] > v:
                    st.pop()
                left[i] = i - st[-1] - 1 if st else i
                st.append(i)

            # right[i]: number of consecutive greater-or-equal values directly
            # to the right of i (stop at first value < arr[i]).
            right = [0] * n
            st = []
            for i in range(n - 1, -1, -1):
                v = arr[i]
                while st and arr[st[-1]] >= v:
                    st.pop()
                right[i] = st[-1] - i - 1 if st else n - 1 - i
                st.append(i)

            K = k - 1  # max allowed x + y, where length = x + y + 1

            def G(t):
                # number of non-negative integer pairs (x, y) with x + y <= t
                return (t + 1) * (t + 2) // 2 if t >= 0 else 0

            base = G(K)
            total = 0
            for i in range(n):
                L = left[i]
                R = right[i]
                # count (x, y): 0 <= x <= L, 0 <= y <= R, x + y <= K
                cnt = base - G(K - L - 1) - G(K - R - 1) + G(K - L - R - 2)
                total += arr[i] * cnt
            return total

        # sum of maxima of arr == -(sum of minima of -arr)
        return sum_of_mins(nums) - sum_of_mins([-x for x in nums])