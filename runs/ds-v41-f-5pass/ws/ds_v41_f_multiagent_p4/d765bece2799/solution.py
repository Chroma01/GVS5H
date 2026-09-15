from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def tri(s: int) -> int:
            # number of nonnegative integer pairs (x, y) with x + y <= s
            if s < 0:
                return 0
            return (s + 1) * (s + 2) // 2

        def min_sum(arr: List[int]) -> int:
            n = len(arr)

            # left[i] = nearest index < i with arr[index] < arr[i]
            left = [-1] * n
            st = []
            for i, v in enumerate(arr):
                while st and arr[st[-1]] >= v:
                    st.pop()
                if st:
                    left[i] = st[-1]
                st.append(i)

            m = k - 1
            tm = tri(m)
            total = 0
            st = []

            # right = nearest index > i with arr[index] <= arr[i]
            for i in range(n - 1, -1, -1):
                v = arr[i]
                while st and arr[st[-1]] > v:
                    st.pop()
                right = st[-1] if st else n

                a = i - left[i] - 1
                b = right - i - 1

                cnt = (
                    tm
                    - tri(m - a - 1)
                    - tri(m - b - 1)
                    + tri(m - a - b - 2)
                )
                total += v * cnt
                st.append(i)

            return total

        # sum of subarray maxima = -sum of subarray minima of the negated array
        return min_sum(nums) - min_sum([-x for x in nums])