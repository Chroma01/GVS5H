from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def count_pairs(A: int, B: int, m: int) -> int:
            # Count pairs (p, q) with 0 <= p <= A, 0 <= q <= B, p + q <= m.
            if m >= A + B:
                return (A + 1) * (B + 1)
            hi = A if A < m else m
            if m >= B:
                p1 = hi if hi < (m - B) else (m - B)
                c1 = (p1 + 1) * (B + 1)
                lo = p1 + 1
                if lo <= hi:
                    cnt = hi - lo + 1
                    first = m - lo + 1
                    last = m - hi + 1
                    c2 = cnt * (first + last) // 2
                else:
                    c2 = 0
                return c1 + c2
            else:
                cnt = hi + 1
                first = m + 1
                last = m - hi + 1
                return cnt * (first + last) // 2

        def min_sum(arr: List[int]) -> int:
            n = len(arr)

            # L[i] = previous index with arr[j] < arr[i]
            L = [-1] * n
            st = []
            for i in range(n):
                x = arr[i]
                while st and arr[st[-1]] >= x:
                    st.pop()
                if st:
                    L[i] = st[-1]
                st.append(i)

            # R[i] = next index with arr[j] <= arr[i]
            R = [n] * n
            st = []
            for i in range(n - 1, -1, -1):
                x = arr[i]
                while st and arr[st[-1]] > x:
                    st.pop()
                if st:
                    R[i] = st[-1]
                st.append(i)

            m = k - 1
            total = 0
            for i in range(n):
                A = i - L[i] - 1
                B = R[i] - i - 1
                total += arr[i] * count_pairs(A, B, m)
            return total

        min_part = min_sum(nums)
        max_part = -min_sum([-x for x in nums])
        return min_part + max_part